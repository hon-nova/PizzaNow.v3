def get_storage_client():   
   from google.cloud import storage   
   return storage.Client()