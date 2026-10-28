# 🚀 GenAI Career Navigator

### AI-Powered Career Guidance & Skill Gap Analysis

GenAI Career Navigator is a web-based application designed to help students and aspiring professionals prepare for their target careers. It helps users identify potential skill gaps, compare current skills with required skills, and plan their learning journey through personalized career guidance.

🌐 **Live Demo:** [GenAI Career Navigator](https://gen-ai-career-navigator.vercel.app)


---

## 📌 Project Overview

Choosing a career path can be challenging when learners do not know which technical skills they need or what to study next.

GenAI Career Navigator aims to simplify this process by allowing users to select a target career, compare their current skills with the skills required for that role, visualize potential gaps, and receive career guidance.

The project combines a web-based interface with a Python backend and an AI integration intended to support personalized career recommendations.

## ✨ Key Features

- 🎯 **Career Role Selection** — Select a target career for analysis.
- 📊 **Skill Gap Analysis** — Compare current skills with the skills required for a selected role.
- 🕸️ **Radar Chart Visualization** — View current and required skills graphically.
- 🗺️ **Personalized Learning Roadmap** — Generate career-learning guidance based on user preferences.
- 🤖 **AI Career Guidance** — AI integration through Groq, subject to successful API configuration and testing.
- 📱 **Interactive Web Interface** — Explore career information through a web-based dashboard.

## 🛠️ Technology Stack

### Frontend
- React
- JavaScript
- HTML5
- CSS3
- Vite

### Backend
- Python
- FastAPI

### AI Integration
- Groq API integration (verify availability and configuration before relying on AI-generated responses)

### Tools and Deployment
- Git and GitHub
- Vercel — frontend hosting
- Render — backend hosting

## 🏗️ System Architecture

The application follows a frontend–backend architecture.

1. **User Input:** The user selects a career role and provides relevant skills and learning preferences.
2. **Frontend:** The React application collects input and communicates with the backend API.
3. **Backend Processing:** The Python/FastAPI backend processes the career-analysis request.
4. **AI Integration:** If configured and available, the backend can use Groq to generate personalized guidance.
5. **Results:** The backend returns the result to the frontend for display in the dashboard.

```text
User
  |
  v
React Frontend (Vercel)
  |
  v
FastAPI Backend (Render)
  |
  +---- Career & Skill Analysis
  |
  +---- Groq AI Integration (if configured)
  |
  v
Results displayed in the dashboard
```

## 📊 Skill Gap Visualization

The application uses a radar chart to compare current skills with required skills for a target career.

- **Current Skills:** Represented in blue.
- **Required Skills:** Represented in green.
- **Potential Skill Gaps:** Skills where the current value is below the required value.

This visualization helps users identify areas to focus on when preparing for a career.

*Note: Chart values represent the application's displayed data and should not automatically be interpreted as independently verified measurements of a user's actual ability.*

## 🌐 Live Deployment

- **Frontend:** [Open the application](https://gen-ai-career-navigator.vercel.app)
- **Backend:** Hosted on Render.

The frontend and backend communicate through API requests. The backend URL and API configuration should be set appropriately for the deployment environment.

## 🚀 Getting Started

Follow these steps to run the project locally. Adjust the paths and commands if your repository structure differs.

### Prerequisites

- Node.js and npm
- Python 3.10 or a version compatible with the backend dependencies
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/sharvani801/GenAI-Career-Navigator.git
cd GenAI-Career-Navigator
```

### 2. Run the Frontend

Open a terminal in the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Vite will display the local development URL in your terminal.

### 3. Run the Backend

Open a separate terminal and navigate to the backend directory:

```bash
cd backend
```

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server using the actual backend entry-point module in your repository. For example, if the FastAPI application is defined in `app.py`:

```bash
uvicorn app:app --reload
```

If your entry-point module or FastAPI application variable has a different name, adjust the command accordingly.

The backend API documentation is usually available at `/docs` when the local server is running and FastAPI's documentation is enabled.

## 🔐 Environment Configuration

If the backend uses Groq, configure the API key as an environment variable:

```env
GROQ_API_KEY=your_groq_api_key
```

- Store real API keys in your local environment or deployment platform's environment-variable settings.
- Add `.env` to `.gitignore`.
- Never commit API keys or other secrets to GitHub.
- Confirm the backend's actual environment-variable name before configuring deployment.

## 🎯 Project Objectives

- Help users understand career-related skill requirements.
- Identify potential differences between current and required skills.
- Present skill comparisons through an interactive visualization.
- Support structured career learning and preparation.
- Explore AI-assisted personalized career guidance.

## 🔮 Future Improvements

- Improve skill-proficiency scoring and validation.
- Expand the range of supported career roles.
- Add more learning resources and course recommendations.
- Improve API error handling and automated testing.
- Validate the quality and reliability of AI-generated guidance.
- Enhance accessibility and mobile responsiveness.

## 🎓 Academic Project

**Project:** GenAI Career Navigator  
**Course:** BCA, Final Year  
**Department:** Department of Computer Applications  
**University:** Alliance University

## 👩‍💻 Author

**Sharvani**

GitHub: [@sharvani801](https://github.com/sharvani801)

---

⭐ If you find this project interesting, feel free to explore the repository and try the live demo.
