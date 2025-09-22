from sqlalchemy.orm import declarative_base,sessionmaker
from core import settings
from sqlalchemy import create_engine, text, inspect

Base = declarative_base()

engine= create_engine(settings.DATABASE_URL,echo=True)
# inspector = inspect(engine)
# print(f"@core/session")
# print(inspector.get_table_names())

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

def get_db():
   db= SessionLocal()
   try:
      yield db
   finally:
      db.close() 