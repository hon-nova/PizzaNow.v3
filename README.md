# PizzaNow – Full-Stack Microservices Application

## 0. Introduction
PizzaNow is a full-stack, cloud-native pizza ordering platform demonstrating **microservices architecture**, **containerization**, and **Kubernetes orchestration**. The backend is modular, with **4 separate services**, allowing independent scaling, deployment, and maintenance. This project represents a major milestone in my IT journey, highlighting modern DevOps practices and cloud deployment patterns.  

---

## 1. Key Features

- **Microservices architecture**: Each backend service runs independently, communicating over a private network.  
- **Containerized backend**: All services run in Docker containers, ensuring environment parity and easy deployment.  
- **Kubernetes practice**: The backend can be deployed to a **K8s cluster** for auto-scaling, self-healing, and production-grade orchestration.  
- **RESTful API for frontend consumption**: FE hosted on Vercel interacts with the backend via API endpoints.  
- **Persistence & caching**: Postgres for structured data, Redis for caching and task queues.  
- **Real-time order management**: Orders are captured, processed, and updated across microservices.  

---

## 2. Tech Stack  

| Category       | Technology                                |
|--------------- |-------------------------------------------|
| Frontend       | React + Vite + Tailwind                   |
| Backend        | FastAPI, Python, Microservices, LangGraph |
| Database       | PostgreSQL                                |
| AI             | Google Vertex AI (Gemini 2.5 Flash)       |
| Containerization | Docker                                  |
| Orchestration  | Kubernetes                                |
| Deployment     | Vercel (FE), DO Docker/Droplets (BE)      |

---

## 3. Architecture Overview

- **4 Backend Services**:  
  1. `auth-service` – Manages user authentication, including custom login as well as Google and LinkedIn sign-ins  
  2. `profile-service` – Handles user profile data, including purchase history and account settings  
  3. `bot-service` – Powers **BenBot**, a chatbot that greets users and answers questions about the PizzaNow store  
  4. `paypal-service` – Executes background tasks such as PayPal payment processing, order capture, and notifications


- **Kubernetes practice (YAML)**:  
  - Each service defined as a `Deployment` with a `Service`  
  - Supports **horizontal pod scaling**, rolling updates, and auto-recovery  
  - Secrets and configuration managed via `ConfigMap` and `Secret`  

---

## 4. Demo

- [PizzaNow Demo Video](https://youtu.be/__unavail__)

---

## 5. Getting Started

**Frontend**
   ```js
      $ cd frontend
      frontend $ npm install
      frontend $ npm run dev
   ```
**Backend**
   ```js 
   backend/ 
      ├── core/
      ├── auth/app/requirements.txt 
      ├── profile_user/app/requirements.txt 
      ├── bot/app/requirements.txt 
      ├── paypal/app/requirements.txt   
      └── .gitignore 
   ```
   ```js
      For each microservice app, for instance `auth`
      1. create a virtual environment (VE) called `v_auth` and activate it 
         $ python3 -m venv v_auth
         $ source v_auth/bin/activate
      2. install all packages from `requirements.txt` into your VE
         $ cd backend/auth
         $ auth$ pip install -r requirements.txt
      3. run `auth` app
         backend$ uvicorn auth.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

