from langgraph.checkpoint.memory import MemorySaver 
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage,AnyMessage
from typing import TypedDict, Optional,List
from langchain_google_vertexai import ChatVertexAI
from core.config import settings
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

def tracer(fn):
   def wrapped(state):
      print(f"▶ Enter {fn.__name__}")
      result = fn(state)
      print(f"◀ Exit {fn.__name__} → {result}")
      return result
   return wrapped

def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def multiply(a: int, b: int|str) -> int|str:
   """Multiplies a and b.

   Args:
      a: first int
      b: second int
   """
   if isinstance(b,(int,str)):
      return a * b
  
def divide(a: int, b: int) -> float|None:
   """Divide a and b.

   Args:
      a: first int
      b: second int
   """
   return a/b if b!=0 else None

class AppGraph(TypedDict):
   user_id: Optional[str]
   messages: List[BaseMessage]

memory = MemorySaver()
def build_graph():    
   
   tools = [add, multiply, divide]   
   llm = ChatVertexAI(
      model="gemini-2.5-flash",
      project=settings.PROJECT_ID,
      location=settings.VERTEX_REGION
   )
   llm_with_tools = llm.bind_tools(tools)
   
   sys_msg = SystemMessage(
    content=(
        "You are a helpful assistant. You can perform arithmetic operations, "
        "and multiplying a string repeats it, like Python. "
        "Always give clear explanations for arithmetic questions. "
        "Remember their introduced name and explicitly tell them if ask or request. "
        "Keep track of the conversation with the user and summarize it at the end of the session."    ))

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
         messages = [placeholder]  # start with dummy if empty
      else:
         messages = messages  # keep all history

      llm_response = llm_with_tools.invoke([sys_identity, sys_msg] + messages)
      
      state["messages"].append(AIMessage(
         content=llm_response.content,
         additional_kwargs=getattr(llm_response, "additional_kwargs", {}),
         response_metadata=getattr(llm_response, "response_metadata", {}),
         tool_calls=getattr(llm_response, "tool_calls", None)
      ))
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