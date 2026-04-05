# MeetMind — AI Meeting Summarizer

AI-powered meeting recorder, transcriber, and summarizer built with Groq Whisper + Llama 3.3 + Google Docs.

## Features
- Real-time audio recording
- Automatic transcription with Groq Whisper
- Speaker detection and labeling
- AI-generated summaries with Key Points, Decisions, Action Items
- 5 meeting templates (Standup, Client Call, Brainstorm, 1:1, General)
- Export as PDF, TXT, or Google Docs
- Session history

## Tech Stack
- Streamlit — UI
- Groq Whisper — transcription
- Llama 3.3 70B — summarization & speaker detection
- Google Docs API — storage
- fpdf2 — PDF export

## Setup

1. Clone the repo
\```bash
git clone https://github.com/yourusername/meetmind.git
cd meetmind
\```

2. Install dependencies
\```bash
pip install -r requirements.txt
\```

3. Create `.env` file
\```
GROQ_API_KEY=your_groq_key_here
\```

4. Add Google credentials
- Go to Google Cloud Console
- Enable Google Docs API
- Download OAuth credentials as `credentials.json`
- Place in project root

5. Run
\```bash
streamlit run meeting_summarizer.py
\```

