0. Introduction
   -  MiniMath – a chatbot leveraging LangGraph for graph-based AI orchestration and Google Vertex AI for language model inference, allowing natural language queries and dynamic computation in real time.

1. Key Features:

- Real-time math computations in natural language: "multiply 2 to 5 then add 90" → 100.
- Maintains session state via in-memory memory for multi-turn conversations.
- Modular LangGraph flow: assistant node + tool node, easily extendable.
- Fully deployable on cloud platforms (GCP Cloud Run, Vercel for frontend).

2. Tech Stack  

   | Category   | Technology                               |
   |----------- |------------------------------------------|
   | Frontend   | React + Vite + Tailwind                  |
   | Backend    | FastAPI, LangGraph, Python               |
   | AI         | Google Vertex AI (Gemini 2.5 Flash)      |
   | Deployment | Vercel, GCP Cloud Run (Docker)           |

3. Demo: [minimathdemo](https://youtu.be/ztxgofuGzjk)

4. Getting Started:
   
   **Frontend**
   ```js
      $ cd frontend
      $ npm install
      $ npm run dev
   ```
   **Backend**
   ```text 
   backend/ 
   ├── app/ 
   ├── ...
   ├── requirements.txt 
   └── .gitignore 
   ```
   ```js
      1. create a virtual environment (VE) called `v_minimath` and activate it 
         $ python3 -m venv v_minimath
         $ source v_minimath/bin/activate
      2. install all packages from `requirements.txt` into your VE
         $ cd backend
         $ backend$ pip install -r requirements.txt
      3. run the backend
         $ uvicorn app.main:app --reload
   ```

5. To use Google Vertex AI with model `Gemini-2.5-flash` or similar legacy versions from Google, you need:
   - A Google Cloud Project with Vertex AI API enabled
   - A Service Account JSON key file with access to Vertex AI
   - Install the dependency: $ pip install langchain-google-vertexai

6. Other technical notes:    
   - When creating a service account, at least give it permissions:
     - roles/run.admin
     - roles/iam.serviceAccountUser
     - roles/artifactregistry.writer  
  
   - Forget terminal deploys: To avoid the disturbance of configuring Vertex AI and other GCP services, it’s best to push your Docker image to Google Container Registry and deploy from the Cloud Console UI. This will eliminate most of the complexity of getting your app running in the cloud.
