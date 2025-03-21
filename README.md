# PrepPal – Your Interview Buddy.

# AI-Powered Interview Scheduling System

## Overview

This project automates the interview scheduling and assessment process using AI. HR can schedule interviews for candidates, and the interview is conducted by an AI bot that evaluates responses and provides a report.

## Features

- HR schedules an interview with a single click.
- Automatically generates and sends interview links to candidates and HR.
- AI conducts the interview and evaluates responses.
- Stores candidate responses and generates a report.
- HR can review AI-generated interview analysis.

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, JavaScript
- **Database:** SQLite / PostgreSQL
- **AI Processing:** OpenAI GPT API, Google Speech-to-Text
- **Communication:** SMTP for emails

## Setup Instructions

### 1. Clone the repository

```sh
   git clone https://github.com/your-repo/ai-interview.git
   cd ai-interview
```

### 2. Create a Virtual Environment

```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```sh
   pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file and add:

```env
SMTP_SERVER=smtp.example.com
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-email-password
OPENAI_API_KEY=your-api-key
DATABASE_URL=sqlite:///database.db
```

### 5. Run the Backend Server

```sh
   python app.py
```

### 6. Run the Frontend

Serve the `index.html` file using any static server:

```sh
   python -m http.server 8000
```

Then open `http://localhost:8000` in a browser.

## API Endpoints

### **1. Schedule Interview**

**Endpoint:** `POST /schedule_interview`

- **Request Body:**

```json
{
    "candidate_email": "candidate@example.com",
    "hr_email": "hr@example.com",
    "job_id": "12345"
}
```

- **Response:**

```json
{
    "success": true,
    "interview_link": "https://your-ai-interview.com/interview/abcd1234"
}
```

### **2. AI Conducts Interview**

**Endpoint:** `GET /interview/{interview_id}`

### **3. Fetch Interview Results**

**Endpoint:** `GET /interview_results`

- **Response:**

```json
[
    {
        "name": "John Doe",
        "score": "85%",
        "summary": "Strong technical skills in Python and problem-solving."
    }
]
```

## Next Steps

- **Integrate AI voice/video processing.**
- **Improve AI response evaluation.**
- **Add real-time feedback to candidates.**




