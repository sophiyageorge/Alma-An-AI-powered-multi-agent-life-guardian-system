🌿 Alma – Wellness Guidance & Lifestyle Assistance System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.76.2-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-blue?style=for-the-badge&logo=react)](https://reactjs.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0.26-orange?style=for-the-badge&logo=langchain)](https://langchain-ai.github.io/langgraph/)
[![Docker](https://img.shields.io/badge/Docker-24.0.5-blue?style=for-the-badge&logo=docker)](https://www.docker.com)
[![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/ec2/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA-purple?style=for-the-badge&logo=groq)](https://groq.com)

## 🚀 Overview

Alma is an AI-powered multi-agent wellness platform that delivers personalized guidance across nutrition, fitness, mental health, and lifestyle management. It combines LLMs, speech-to-text, and agent orchestration to create an intelligent, scalable health assistant.

## 🎯 Features

- 🍽️ **Personalized Meal Planning**
- 🏋️ **Exercise Recommendations**
- 📊 **Health Monitoring & Insights**
- 🛒 **Automated Grocery List Generation**
- 🧠 **Mental Health Journaling & Mood Analysis**
- 🚨 **Emergency Alerts via WhatsApp**
- 🎙️ **Voice-based Journaling (Speech-to-Text)**

## 🧠 Architecture

### 🤖 Agents

| Agent | Responsibility |
|-------|----------------|
| 🥗 Nutrition Agent | Meal planning & nutrient analysis |
| 📊 Health Data Agent | Tracks health metrics & detects anomalies |
| 🏋️ Exercise Agent | Workout recommendations |
| 🛒 Grocery Agent | Generates shopping lists |
| 🧠 Mental Health Agent | Journaling & mood analysis |
| ✅ Compliance Agent | Safety validation & filtering |
| 🔁 Orchestrator Agent | Coordinates all agents |

### 🔄 Data Flow

```
User → React → FastAPI → LangGraph → Agents → DB / APIs → Response → UI
```

### 🔌 API Endpoints

#### 🔐 Authentication
- `POST /register`
- `POST /login`

#### 📊 Health Data
- `GET /health-data`
- `POST /health-data`
- `GET /health-data/weekly`
- `GET /health-data/monthly`

#### 🍽️ Meal Plan
- `GET /meal-plan`
- `POST /meal-plan/approve`
- `PUT /meal-plan/update`

#### 🏋️ Exercise
- `GET /exercise/recommendations`

#### 🧠 Journaling
- `POST /journal` → Returns mood-analyzed response

## 🛠️ Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/alma-wellness.git
cd alma-wellness
```

### 2️⃣ Backend Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3️⃣ Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🐳 Docker Setup
```bash
docker build -t alma-app .
docker run -d -p 8000:8000 alma-app
```

## ☁️ Deployment
- **Frontend**: Vercel
- **Backend**: AWS EC2 (Dockerized)

## 🖼️ Screenshots

### 🏠 Dashboard
![Dashboard](screenshots/dashboard.png)

### 🏠 Health Data
![Health Data](screenshots/health_post.png)

### 🍽️ Meal Plan
![Meal Plan](screenshots/meal-plan.png)

### 🛒 Grocery List
![Grocery List](screenshots/grocery-list.png)

### 🧠 Journaling & Mood Analysis
![Journaling](screenshots/journaling.png)

### 🧠 Exercise
![Exercise](screenshots/exercise.png)

> **Note**: Place your screenshots in the `/screenshots` folder with the exact filenames shown above.

## 🔐 Security
- JWT Authentication
- Secure API endpoints
- Data privacy best practices

## 🧪 Testing
- ✅ Unit Testing (pytest)
- ✅ API Testing (Postman)
- ✅ Edge Case Handling

## ⚠️ Challenges
- Multi-agent coordination
- LLM response formatting (JSON parsing)
- AWS EC2 + Docker deployment

## 📈 Future Enhancements
- Wearable device integration
- Real-time health monitoring
- Mobile app
- Advanced ML models

## 📌 Conclusion

Alma is a real-world AI system demonstrating:
- Multi-agent orchestration
- LLM integration
- Cloud deployment

It showcases how modern technologies can be combined to build an intelligent wellness assistant.

## 📚 References
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Groq LLaMA](https://groq.com/)
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper)
- [Twilio API](https://www.twilio.com/docs)

## ⭐ Show Your Support

If you like this project, give it a ⭐ on GitHub!

## 👩‍💻 Author

**Mary Sophiya**