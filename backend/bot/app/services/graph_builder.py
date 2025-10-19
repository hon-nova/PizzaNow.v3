from langgraph.checkpoint.memory import MemorySaver 
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage,AnyMessage
from typing import TypedDict, Optional,List
from langchain_google_vertexai import ChatVertexAI
from core.config import settings
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from bot.app.services import load_blueprint,respond_shipment_status
from langchain.tools import Tool

def tracer(fn):
   def wrapped(state):
      print(f"▶ Enter {fn.__name__}")
      result = fn(state)
      print(f"◀ Exit {fn.__name__} → {result}")
      return result
   return wrapped  

shipment_status_tool = Tool(
   name="respond_shipment_status",
   func=respond_shipment_status,
   description="Check the shipment status of a given order_id. If status is pending or failed, notify an admin."
)

load_blueprint_tool = Tool(
    name="load_blueprint",
    func=load_blueprint,
    description="Answer PizzaNow business questions. Summarize only relevant info, do not dump entire blueprint."
)

class AppGraph(TypedDict):
   user_id: Optional[str]
   messages: List[BaseMessage]

memory = MemorySaver()
def build_graph():    
   
   tools = [load_blueprint_tool,shipment_status_tool]   
   llm = ChatVertexAI(
      model="gemini-2.5-flash",
      project=settings.PROJECT_ID,
      location=settings.VERTEX_REGION
   )
   llm_with_tools = llm.bind_tools(tools)
   llm_with_tools._tools = tools 
   
   sys_msg = SystemMessage(  
      content=(
               "You are benBot, PizzaNow assistant. "
               "Use load_blueprint_tool to answer questions. "
               "Use shipment_status_tool tool for order updates. "
               "Do not dump raw blueprint; only return relevant info. "
               "If an order is pending or failed, remind the user that admin has been notified. "
               "Remember the user's introduced name when used. "
               "Summarize the conversation at the end of the session if explicitly asked."
         )
   )

   @tracer
   def login_node(state:AppGraph): 
      if not state.get("user_id"):  
         state["messages"].append(AIMessage(content=f"@login_node You're not logged in. "))
         return state
      
      return state         

   @tracer
   def query_node(state:AppGraph):     
      user_id = state.get("user_id")
      if not user_id:
         state["messages"].append(AIMessage(content="You're not logged in."))
         return state         
      
      sys_identity = SystemMessage(
         content=f"User ID is {user_id}. Do NOT greet. Answer based only on the retrieved context."
      )       
     
      messages = state.get("messages", [])
      if not messages or not any(isinstance(m, HumanMessage) for m in messages):
         placeholder = HumanMessage(content="(no user input)")
         messages = [placeholder] 
      else:
         messages = messages  

      llm_response = llm_with_tools.invoke([sys_identity, sys_msg] + messages)
      
      state["messages"].append(AIMessage(
         content=llm_response.content,
         additional_kwargs=getattr(llm_response, "additional_kwargs", {}),
         response_metadata=getattr(llm_response, "response_metadata", {}),
         tool_calls=getattr(llm_response, "tool_calls", None)
      ))
      if getattr(llm_response, "tool_calls", None):
         for call in llm_response.tool_calls:
            tool_name = call["name"]
            tool_args = call.get("args", {})
            
            if "__arg1" in tool_args:
                  tool_args["input"] = tool_args.pop("__arg1")

            tool = next((t for t in getattr(llm_with_tools, "_tools", []) if t.name == tool_name), None)

            if tool:              
               input_value = list(tool_args.values())[0] if tool_args else ""
               result = tool.func(input_value)
               state["messages"].append(AIMessage(content=result))
      return state  
   
   builder = StateGraph(AppGraph)   
   builder.add_node("login_node",login_node)
   builder.add_node("query_node",query_node)      
   builder.add_node("tools", ToolNode(tools))
   
   builder.add_edge(START,"login_node")
   
   def auth_condition(state: AppGraph):
      return "query_node" if state.get("user_id") else "login_node"
   
   builder.add_conditional_edges("login_node",auth_condition)
   builder.add_conditional_edges("query_node",tools_condition)
   
   builder.add_edge("tools","query_node")
   graph = builder.compile(checkpointer=memory)
 
   return graph   