from fastapi import APIRouter, Depends, HTTPException

from app.services.custom import get_current_user
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessagesState
# from langgraph.prebuilt import ToolMessage,ToolMessage
# from langgraph.prebuilt.tools import _ToolMessage
# from langgraph.prebuilt import ToolMessage

from pydantic import BaseModel
from app.graph.graph_builder import AppGraph, build_graph
from app.core import get_storage_client
from app.models.model import User
import uuid
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import traceback  


class Query(BaseModel):
   text: str

graph = build_graph()  
graph_router = APIRouter()

thread_id =  uuid.uuid4()
config = {"thread_id": thread_id}
@graph_router.post("/query")
def query_route(query: Query, user: User = Depends(get_current_user)):
   try:
      client=get_storage_client()      
      user_id = str(user.id) if user else None   
    
      state: AppGraph = {
         "user_id": user_id,
         "messages":[HumanMessage(content=query.text)]
      }
      result_state = graph.invoke(state,config={"configurable": config})
      messages = result_state.get("messages",[])
            
      ai_messages = [m for m in messages if m.__class__.__name__ == "AIMessage" and str(m.content).strip()]
      tool_messages = [m for m in messages if m.__class__.__name__ == "ToolMessage" and str(m.content).strip()]

      # Choose one: prefer ToolMessage if it exists, else AIMessage
      if tool_messages:
         output_text = [str(m.content) for m in tool_messages]
      else:
         output_text = [str(m.content) for m in ai_messages]      

      logger.info(f"IMPORTANT output_text::{output_text}")
          
      return {"response": output_text}  
      
   except Exception as e:
      logger.error("🔥 Exception in /query")
      logger.error(traceback.format_exc()) 
      raise HTTPException(status_code=500,detail=f"EXCEPTION /query: {str(e)}")
