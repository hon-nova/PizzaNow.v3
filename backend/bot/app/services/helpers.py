from pathlib import Path
import vertexai
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.chains import RetrievalQA
from google.cloud import aiplatform
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI

from sqlalchemy.orm import Session
from core.model import Order 

vertexai.init(project="pizzanowai", location="us-central1")
aiplatform.init(
   project="pizzanowai",
   location="us-central1"
)

MD_PATH= Path(__file__).resolve().parents[3] / "core/db/business_blueprint.md"

# Guide: BLUEPRINT_PATH = Path(__file__).resolve().parents[2] / "core" / "db" / "business_blueprint.md"
def load_blueprint_chunks():   
   text = MD_PATH.read_text(encoding="utf-8")
   splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)   
   chunks = splitter.split_text(text)
   return chunks

chunks = load_blueprint_chunks()

embedding_model = VertexAIEmbeddings(model_name="text-embedding-005")

vectorstore = InMemoryVectorStore(embedding_model)
vectorstore.add_texts(chunks) 

retriever = vectorstore.as_retriever(search_kwargs={"k":1})

def load_blueprint(input: str):   
   """_summary_

   Returns:
       _type_: _description_
   """   
   qa_chain = RetrievalQA.from_chain_type(
      llm=ChatVertexAI(model_name="gemini-2.5-flash"),
      retriever=retriever,
      return_source_documents=False ) 
   
   query = input.strip()
   if not query:
      return "Please provide a question to lookup in the blueprint."
   
   result = qa_chain.run(query)
   return sanitize_for_tts(result)

# tools/blueprint_tool.py
# def load_blueprint(input: str) -> str:
#    """_summary_

#    Args:
#        input (str): _description_

#    Returns:
#        str: _description_
#    """
#    if not input.strip():
#       return "Please provide a question to lookup in the blueprint."

#    # Direct retriever use (no LLM here!)
#    results = retriever.get_relevant_documents(input)
#    if not results:
#       return "No relevant content found."

#    # return sanitize_for_tts(results[0].page_content)
#    return f"Context: {sanitize_for_tts(results[0].page_content)}\n\nQuestion: {input}"

from core.session import SessionLocal

def respond_shipment_status(input: str) -> str:
   with SessionLocal() as session:
      input = input.strip()
      order = session.get(Order, input)
      print(f"IMPORTANT order with order_id: {input}: {order.id}")
      if not order:
         return f"No order found with ID {input}."
      
      status = order.shipment_status.lower()
      
      base_msg = f"Order {input} has shipment status: {status}."
      if status == "succeeded":
         return f"{base_msg} Congrats!"
      if status in ("pending", "failed"):
         return f"{base_msg}  I will notify the admin perosn right now. They will contact you shortly regarding your order. Thank you for contacting us!"
      return base_msg
   
import re

def sanitize_for_tts(raw_text: str) -> str:
    text = raw_text

    # Remove Markdown headings (#, ##, ### ...)
    text = re.sub(r'^\s*#{1,6}\s*', '', text, flags=re.MULTILINE)

    # Remove bold/italic/underline (**text**, *text*, __text__)
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
    text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)

    # Remove blockquotes >
    text = re.sub(r'^\s*>+\s*', '', text, flags=re.MULTILINE)

    # Remove list markers (-, *, •)
    text = re.sub(r'^\s*[-*•]\s+', '', text, flags=re.MULTILINE)

    # Remove horizontal rules (--- or ___)
    text = re.sub(r'^[-_]{3,}$', '', text, flags=re.MULTILINE)

    # Remove emojis
    text = re.sub(r'[📧📞🔁❌😠🔄⚠️🍕🥤🌶️🍖]', '', text)

    # Replace @ in emails with ' at '
    text = text.replace('@', ' at ')

    # Replace '.' in emails/domains with ' dot '
    text = re.sub(r'(?<=\b\w)\.(?=\w+\b)', ' dot ', text)

    # Force digit-by-digit reading for phone numbers
    def digits_spaced(m):
        return ' '.join(re.sub(r'[^\d]', '', m.group(0)))

    text = re.sub(r'\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}', digits_spaced, text)

    # Replace dash between days (e.g., "Monday – Sunday") with "to"
    days_pattern = r'\b(Mon(?:day)?|Tue(?:sday)?|Wed(?:nesday)?|Thu(?:rsday)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?)'
    text = re.sub(fr'{days_pattern}\s*[-–]\s*{days_pattern}', r'\1 to \2', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

