#  MeetMind — AI Meeting Summarizer

> Transform conversations into structured insights — instantly.

**MeetMind** is an AI-powered meeting assistant that records, transcribes, and intelligently summarizes meetings into actionable outputs using state-of-the-art language and speech models.

---
<img width="1916" height="892" alt="1" src="https://github.com/user-attachments/assets/ff475520-7f4f-448a-9f99-6263678ff0b5" />
<img width="1912" height="921" alt="2" src="https://github.com/user-attachments/assets/ade43ce1-c368-462b-8cab-a2b76612dafd" />
<img width="1918" height="902" alt="3" src="https://github.com/user-attachments/assets/0e14770d-6de0-4a16-84b4-8c79a19df6e4" />
<img width="1917" height="862" alt="4" src="https://github.com/user-attachments/assets/515c7307-7c6a-4b08-bc37-a5b72284db5f" />
<img width="1907" height="857" alt="5" src="https://github.com/user-attachments/assets/0ee229f4-bbdf-4193-a384-35834f501f85" />
<img width="1912" height="865" alt="6" src="https://github.com/user-attachments/assets/d0d35f86-6486-44f4-850d-a50043aa62c3" />

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


