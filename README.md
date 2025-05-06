
# 🤖 MockMate AI – AI-Powered Mock Interview Preparation System

**MockMate AI** is a smart mock interview system designed to help users prepare for technical interviews using AI technologies. It generates domain-specific questions, converts verbal responses to text, evaluates the answers using NLP, and provides insightful feedback.

---

## 🚀 Features

- 💡 Intelligent question generation via Google Gemini API
- 🎙️ Speech-to-text transcription using AssemblyAI
- 🧠 NLP-based evaluation of spoken responses
- 🔐 JWT-secured login and user management
- 🖥️ Native desktop app built with Electron (MyApp)
- 🗃️ SQLite-powered persistent data storage

---


## ⚙️ Technologies Used

- **Django** & **Django REST Framework**
- **AssemblyAI API** (for speech-to-text)
- **Google Gemini API** (for question generation)
- **NLP** for answer evaluation
- **Electron** for desktop integration
- **JWT Authentication**



## 📁 Project Structure

```

MockMate-AI/
│
├── backend/           # Django backend
│   ├── manage.py
│   └── ai_interview/
│
├── MyApp/             # Electron desktop frontend
│   ├── index.js
│   └── package.json

````

## 🛠️ Backend Setup Instructions (Django + DRF)

### 1. Navigate to the backend folder
```bash
cd backend
````

### 2. Create and activate virtual environment

```
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys in `settings.py`

Edit `ai_interview/settings.py` and add the following:

```python
GOOGLE_GEMINI_API_KEY = "your_google_gemini_api_key"
ASSEMBLYAI_API_KEY = "your_assemblyai_api_key"
```

> These are used for question generation and speech-to-text functionality.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the backend server

```bash
python manage.py runserver
```

> Backend runs at: `http://127.0.0.1:8000`

---

## 🖥️ Desktop App Setup (Electron - MyApp)

### 1. Navigate to the frontend directory

```bash
cd ../MyApp
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the app in development mode

```bash
npm start
```

> The app will open as a desktop window and connect to the Django backend.

---

## 🔐 Authentication

* The system uses JWT authentication.
* By default, all API endpoints require user login.


## 🧪 How It Works

1. User logs in to the desktop app (MyApp)
2. Selects domain/skills and begins the interview
3. Questions are generated via Google Gemini
4. User speaks the answer — transcribed via AssemblyAI
5. NLP compares the response to ideal answers and scores it
6. Detailed feedback is shown at the end of the session
   

## 📦 Key Dependencies

### Python

* Django
* djangorestframework
* djangorestframework-simplejwt
* requests
* numpy
* scikit-learn
* google-generativeai

### JavaScript (Electron)

* Electron
* Axios
* Node.js



## 🏁 Running the Complete System

1. Start the Django backend:

```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

2. Launch the Electron frontend:

```bash
cd ../MyApp
npm start
```

> To bundle the app as an executable (`MyApp.exe`), use Electron Packager or Electron Builder.
