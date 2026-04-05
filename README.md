---

#  MeetMind — AI Meeting Summarizer

> Transform conversations into structured insights — instantly.

**MeetMind** is an AI-powered meeting assistant that records, transcribes, and intelligently summarizes meetings into actionable outputs using state-of-the-art language and speech models.

---

##  Features

*  **Real-time Audio Recording**
  Capture meetings directly within the app

*  **Accurate Transcription**
  Powered by Groq Whisper for fast and reliable speech-to-text

*  **Speaker Detection & Labeling**
  Automatically identifies and separates speakers

*  **AI-Powered Summarization**
  Generates structured outputs including:

  * Key Points
  * Decisions
  * Action Items

* 🗂️ **Predefined Meeting Templates**
  Supports multiple formats:

  * Standup
  * Client Call
  * Brainstorm
  * 1:1
  * General

*  **Export Options**
  Download summaries as:

  * PDF
  * TXT
  * Google Docs

*  **Session History**
  Access and review past meetings anytime

---

##  Tech Stack

| Layer         | Technology      |
| ------------- | --------------- |
| UI            | Streamlit       |
| Transcription | Groq Whisper    |
| AI Processing | Llama 3.3 70B   |
| Storage       | Google Docs API |
| Export        | fpdf2           |

---

##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/meetmind.git
cd meetmind
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

### 4. Google Docs API Setup

1. Go to Google Cloud Console
2. Create a new project
3. Enable **Google Docs API**
4. Create OAuth credentials
5. Download the credentials file
6. Rename it to:

```
credentials.json
```

5. Place it in the project root directory

---

### 6. Run the Application

```bash
streamlit run meeting_summarizer.py
```
---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---


