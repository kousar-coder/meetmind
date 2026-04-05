import streamlit as st
import pyaudio
import wave
import os
import threading
import time
import io
from groq import Groq
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
from datetime import datetime
from fpdf import FPDF

load_dotenv()

st.set_page_config(
    page_title="MeetMind",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: #0f0f0f;
    color: #e2e8f0;
}

[data-testid="stSidebar"] {
    background: #141414 !important;
    border-right: 1px solid #1e1e1e !important;
}

[data-testid="stSidebar"] * { color: #94a3b8 !important; }

.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 0 1.5rem;
    border-bottom: 1px solid #1e1e1e;
    margin-bottom: 1.5rem;
}

.top-bar h1 {
    font-size: 1.2rem;
    font-weight: 600;
    color: #f1f5f9;
    margin: 0;
}

.top-bar span {
    font-size: 0.75rem;
    color: #475569;
    background: #1a1a1a;
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid #262626;
}

.template-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}

.template-pill {
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    border: 1px solid #262626;
    background: #1a1a1a;
    color: #64748b;
    transition: all 0.15s;
}

.template-pill.active {
    background: #1e293b;
    border-color: #3b82f6;
    color: #93c5fd;
}

.record-zone {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}

.record-zone.active {
    border-color: #dc2626;
    background: #1a0f0f;
}

.rec-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #dc2626;
    display: inline-block;
    margin-right: 8px;
    animation: blink 1s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}

.timer {
    font-size: 2.5rem;
    font-weight: 300;
    color: #f1f5f9;
    letter-spacing: 0.05em;
    margin: 0.5rem 0;
    font-variant-numeric: tabular-nums;
}

.timer-label {
    font-size: 0.75rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.metrics-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 1.5rem;
}

.metric {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}

.metric-label {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 1.4rem;
    font-weight: 500;
    color: #f1f5f9;
}

.metric-sub {
    font-size: 11px;
    color: #475569;
    margin-top: 2px;
}

.section-card {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 10px;
}

.section-tag {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 3px 8px;
    border-radius: 4px;
    margin-bottom: 10px;
    display: inline-block;
}

.tag-keypoints { background: #1e3a5f; color: #93c5fd; }
.tag-decisions { background: #1a2e1a; color: #86efac; }
.tag-actions { background: #3b1f1f; color: #fca5a5; }
.tag-speakers { background: #2d1f3d; color: #c4b5fd; }
.tag-general { background: #1e1e2e; color: #a5b4fc; }

.section-content {
    font-size: 0.875rem;
    color: #94a3b8;
    line-height: 1.7;
}

.speaker-block {
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
}

.speaker-label {
    font-size: 11px;
    font-weight: 600;
    color: #3b82f6;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}

.speaker-2 { color: #8b5cf6 !important; }
.speaker-3 { color: #10b981 !important; }

.speaker-text {
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.6;
}

.action-bar {
    display: flex;
    gap: 8px;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}

.saved-banner {
    background: #0f2a1a;
    border: 1px solid #166534;
    border-radius: 10px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 1rem;
    font-size: 0.875rem;
    color: #86efac;
}

.history-item {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 6px;
    cursor: pointer;
}

.history-title {
    font-size: 12px;
    font-weight: 500;
    color: #e2e8f0;
    margin-bottom: 3px;
}

.history-meta {
    font-size: 11px;
    color: #475569;
}

.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #334155;
}

.empty-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
}

.empty-title {
    font-size: 1rem;
    font-weight: 500;
    color: #475569;
    margin-bottom: 0.5rem;
}

.empty-sub {
    font-size: 0.8rem;
    color: #334155;
}

.stButton > button {
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.15s !important;
}

div[data-testid="stSelectbox"] label { color: #64748b !important; font-size: 12px !important; }
div[data-testid="stTextInput"] label { color: #64748b !important; font-size: 12px !important; }
div[data-testid="stTextInput"] input {
    background: #1a1a1a !important;
    border: 1px solid #262626 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

.stSpinner > div { border-top-color: #3b82f6 !important; }
</style>
""", unsafe_allow_html=True)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT = "meeting.wav"
SCOPES = ["https://www.googleapis.com/auth/documents"]

TEMPLATES = {
    "General Meeting": {
        "icon": "💬",
        "prompt": "Extract: 1) Key discussion points 2) Decisions made 3) Action items with owners. Be structured and concise."
    },
    "Daily Standup": {
        "icon": "⚡",
        "prompt": "Extract for each speaker if possible: 1) What they did yesterday 2) What they're doing today 3) Any blockers. Keep it very brief."
    },
    "Client Call": {
        "icon": "🤝",
        "prompt": "Extract: 1) Client requirements mentioned 2) Commitments made by our team 3) Next steps and deadlines 4) Any concerns raised. Professional tone."
    },
    "Brainstorm": {
        "icon": "🧠",
        "prompt": "Extract: 1) Ideas generated (list all) 2) Ideas selected for action 3) Ideas parked for later 4) Next steps. Capture every idea mentioned."
    },
    "1:1 Meeting": {
        "icon": "👥",
        "prompt": "Extract: 1) Topics discussed 2) Feedback given or received 3) Goals set or reviewed 4) Action items. Keep sensitive context professional."
    }
}

SPEAKER_COLORS = ["speaker-1", "speaker-2", "speaker-3"]

for key, default in {
    "recording": False, "transcript": "", "summary": "",
    "doc_url": "", "duration": 0, "word_count": 0,
    "start_time": None, "frames": [], "stop_event": None,
    "history": [], "template": "General Meeting",
    "speaker_segments": [], "email_sent": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def record_thread(stop_event, frames_list):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)
    while not stop_event.is_set():
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames_list.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    p2 = pyaudio.PyAudio()
    with wave.open(WAVE_OUTPUT, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p2.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames_list))
    p2.terminate()

def transcribe_audio():
    client = get_client()
    with open(WAVE_OUTPUT, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f
        )
    return result.text

def detect_speakers(transcript):
    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Analyze this transcript and identify different speakers based on context, topic shifts, and speaking patterns.
                Return ONLY a JSON array like this:
                [
                  {"speaker": "Speaker 1", "text": "their words here"},
                  {"speaker": "Speaker 2", "text": "their words here"}
                ]
                If only one speaker, use Speaker 1 for everything.
                Split the transcript into logical speaker segments. Return valid JSON only, no other text."""
            },
            {"role": "user", "content": transcript}
        ]
    )
    import json
    try:
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except:
        return [{"speaker": "Speaker 1", "text": transcript}]

def summarize_transcript(transcript, template):
    client = get_client()
    prompt = TEMPLATES[template]["prompt"]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are an expert meeting summarizer for a {template}.
                {prompt}
                
                Format your response with these exact section headers on their own lines:
                KEY POINTS:
                DECISIONS MADE:
                ACTION ITEMS:
                
                Use bullet points starting with - for each item.
                Be specific and actionable. No filler phrases."""
            },
            {"role": "user", "content": f"Summarize this meeting transcript:\n\n{transcript}"}
        ]
    )
    return response.choices[0].message.content

def save_to_docs(summary, transcript, template):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    service = build("docs", "v1", credentials=creds)
    title = f"{template} — {datetime.now().strftime('%b %d, %Y %H:%M')}"
    doc = service.documents().create(body={"title": title}).execute()
    doc_id = doc["documentId"]
    content = f"{title}\n{'='*50}\n\nTEMPLATE: {template}\n\n{summary}\n\n{'='*50}\nFULL TRANSCRIPT\n{'='*50}\n\n{transcript}"
    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}
    ).execute()
    return f"https://docs.google.com/document/d/{doc_id}"

def generate_pdf(summary, transcript, template, duration, word_count):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 15, 15)
    pdf.cell(0, 12, f"MeetMind — {template}", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}  |  Duration: {duration//60:02d}:{duration%60:02d}  |  Words: {word_count}", ln=True)
    pdf.ln(6)
    pdf.set_draw_color(230, 230, 230)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 15, 15)
    pdf.cell(0, 8, "AI SUMMARY", ln=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for line in summary.split("\n"):
        if line.strip():
            if line.strip().endswith(":") and len(line.strip()) < 30:
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(30, 30, 30)
                pdf.cell(0, 6, line.strip(), ln=True)
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(60, 60, 60)
            else:
                pdf.multi_cell(0, 6, line.strip())
    pdf.ln(8)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 15, 15)
    pdf.cell(0, 8, "FULL TRANSCRIPT", ln=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 6, transcript)
    return bytes(pdf.output())

def parse_summary_sections(summary):
    sections = []
    current_tag = None
    current_lines = []
    tag_map = {
        "KEY POINTS": ("tag-keypoints", "Key Points"),
        "DECISIONS MADE": ("tag-decisions", "Decisions Made"),
        "ACTION ITEMS": ("tag-actions", "Action Items"),
    }
    for line in summary.split("\n"):
        stripped = line.strip()
        matched = False
        for key, (cls, label) in tag_map.items():
            if key in stripped.upper():
                if current_tag and current_lines:
                    sections.append((current_tag[0], current_tag[1], "\n".join(current_lines).strip()))
                current_tag = (cls, label)
                current_lines = []
                matched = True
                break
        if not matched and stripped:
            current_lines.append(stripped)
    if current_tag and current_lines:
        sections.append((current_tag[0], current_tag[1], "\n".join(current_lines).strip()))
    if not sections and summary.strip():
        sections.append(("tag-general", "Summary", summary.strip()))
    return sections

with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem;">
        <div style="font-size: 1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px;">MeetMind</div>
        <div style="font-size: 11px; color: #334155;">AI Meeting Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:11px; color:#334155; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">Meeting Type</div>', unsafe_allow_html=True)
    template = st.selectbox(
        "",
        list(TEMPLATES.keys()),
        format_func=lambda x: f"{TEMPLATES[x]['icon']} {x}",
        key="template_select",
        label_visibility="collapsed"
    )
    st.session_state.template = template

    st.markdown('<div style="height:1px; background:#1e1e1e; margin:1.2rem 0;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px; color:#334155; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">Recent Meetings</div>', unsafe_allow_html=True)

    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-8:])):
            mins, secs = divmod(item['duration'], 60)
            st.markdown(f"""
            <div class="history-item">
                <div class="history-title">{item['template']} · {item['time']}</div>
                <div class="history-meta">{mins:02d}:{secs:02d} · {item['words']} words</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:12px; color:#334155; padding:0.5rem 0;">No meetings yet</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1px; background:#1e1e1e; margin:1.2rem 0;"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11px; color:#334155; line-height:2;">
        <div>🎙️ Groq Whisper</div>
        <div>🧠 Llama 3.3 70B</div>
        <div>📄 Google Docs</div>
        <div>⚡ Free API</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="top-bar">
    <h1>{TEMPLATES[st.session_state.template]['icon']} {st.session_state.template}</h1>
    <span>{datetime.now().strftime('%A, %B %d')}</span>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])

with col_left:
    is_recording = st.session_state.recording
    zone_class = "record-zone active" if is_recording else "record-zone"

    if is_recording:
        elapsed = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0
        mins, secs = divmod(elapsed, 60)
        st.markdown(f"""
        <div class="{zone_class}">
            <div class="timer-label"><span class="rec-indicator"></span>Recording</div>
            <div class="timer">{mins:02d}:{secs:02d}</div>
            <div class="timer-label">Speak naturally — click Stop when done</div>
        </div>""", unsafe_allow_html=True)
    elif st.session_state.transcript:
        mins, secs = divmod(st.session_state.duration, 60)
        st.markdown(f"""
        <div class="record-zone">
            <div class="timer-label">Last recording</div>
            <div class="timer">{mins:02d}:{secs:02d}</div>
            <div class="timer-label">{st.session_state.word_count} words transcribed</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="{zone_class}">
            <div class="timer-label">Ready</div>
            <div class="timer">00:00</div>
            <div class="timer-label">Select a meeting type and click Start</div>
        </div>""", unsafe_allow_html=True)

    btn1, btn2, btn3 = st.columns(3)
    with btn1:
        if not is_recording:
            if st.button("▶ Start Recording", type="primary", use_container_width=True):
                st.session_state.frames = []
                st.session_state.stop_event = threading.Event()
                st.session_state.start_time = time.time()
                st.session_state.recording = True
                st.session_state.transcript = ""
                st.session_state.summary = ""
                st.session_state.doc_url = ""
                st.session_state.speaker_segments = []
                st.session_state.email_sent = False
                threading.Thread(
                    target=record_thread,
                    args=(st.session_state.stop_event, st.session_state.frames),
                    daemon=True
                ).start()
                st.rerun()

    with btn2:
        if is_recording:
            if st.button("⏹ Stop", type="secondary", use_container_width=True):
                st.session_state.stop_event.set()
                st.session_state.duration = int(time.time() - st.session_state.start_time)
                st.session_state.recording = False
                time.sleep(1.2)

                with st.spinner("Transcribing..."):
                    st.session_state.transcript = transcribe_audio()
                    st.session_state.word_count = len(st.session_state.transcript.split())

                with st.spinner("Detecting speakers..."):
                    st.session_state.speaker_segments = detect_speakers(st.session_state.transcript)

                with st.spinner("Generating summary..."):
                    st.session_state.summary = summarize_transcript(
                        st.session_state.transcript,
                        st.session_state.template
                    )

                with st.spinner("Saving to Google Docs..."):
                    try:
                        st.session_state.doc_url = save_to_docs(
                            st.session_state.summary,
                            st.session_state.transcript,
                            st.session_state.template
                        )
                        st.session_state.history.append({
                            "time": datetime.now().strftime("%H:%M"),
                            "words": st.session_state.word_count,
                            "duration": st.session_state.duration,
                            "url": st.session_state.doc_url,
                            "template": st.session_state.template
                        })
                    except Exception as e:
                        st.warning(f"Docs save failed: {e}")
                st.rerun()

    with btn3:
        if st.session_state.transcript:
            if st.button("＋ New Meeting", use_container_width=True):
                for k in ["transcript", "summary", "doc_url", "speaker_segments", "duration", "word_count"]:
                    st.session_state[k] = "" if isinstance(st.session_state[k], str) else 0 if isinstance(st.session_state[k], int) else []
                st.rerun()

    if st.session_state.transcript:
        st.markdown("<br>", unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1:
            mins, secs = divmod(st.session_state.duration, 60)
            speaker_count = len(set(s["speaker"] for s in st.session_state.speaker_segments)) if st.session_state.speaker_segments else 1
            st.markdown(f'<div class="metric"><div class="metric-label">Duration</div><div class="metric-value">{mins:02d}:{secs:02d}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric"><div class="metric-label">Words spoken</div><div class="metric-value">{st.session_state.word_count}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric"><div class="metric-label">Speakers detected</div><div class="metric-value">{speaker_count}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">AI Summary</div>', unsafe_allow_html=True)

        sections = parse_summary_sections(st.session_state.summary)
        for tag_cls, label, content in sections:
            st.markdown(f"""
            <div class="section-card">
                <span class="section-tag {tag_cls}">{label}</span>
                <div class="section-content">{content.replace(chr(10), '<br>')}</div>
            </div>""", unsafe_allow_html=True)

        if st.session_state.doc_url:
            st.markdown(f"""
            <div class="saved-banner">
                ✓ Saved to Google Docs
                <a href="{st.session_state.doc_url}" target="_blank" style="color:#4ade80; margin-left:auto; font-size:12px;">Open Document →</a>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">Export</div>', unsafe_allow_html=True)

        e1, e2, e3 = st.columns(3)
        with e1:
            st.download_button(
                "↓ Download TXT",
                f"MEETING SUMMARY\n{'='*40}\n\n{st.session_state.summary}\n\n{'='*40}\nTRANSCRIPT\n{'='*40}\n\n{st.session_state.transcript}",
                file_name=f"meetmind_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with e2:
            try:
                pdf_bytes = generate_pdf(
                    st.session_state.summary,
                    st.session_state.transcript,
                    st.session_state.template,
                    st.session_state.duration,
                    st.session_state.word_count
                )
                st.download_button(
                    "↓ Download PDF",
                    pdf_bytes,
                    file_name=f"meetmind_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.button("↓ PDF (install fpdf2)", disabled=True, use_container_width=True)
        with e3:
            copy_text = f"{st.session_state.summary}\n\nTranscript:\n{st.session_state.transcript}"
            st.download_button(
                "↓ Copy All",
                copy_text,
                file_name="meetmind_copy.txt",
                mime="text/plain",
                use_container_width=True
            )

with col_right:
    if st.session_state.speaker_segments:
        st.markdown('<div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">Transcript</div>', unsafe_allow_html=True)

        for i, seg in enumerate(st.session_state.speaker_segments):
            speaker_class = SPEAKER_COLORS[i % len(SPEAKER_COLORS)]
            st.markdown(f"""
            <div class="speaker-block">
                <div class="speaker-label {speaker_class}">{seg['speaker']}</div>
                <div class="speaker-text">{seg['text']}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎙️</div>
            <div class="empty-title">No transcript yet</div>
            <div class="empty-sub">Start a recording to see the transcript with speaker labels appear here</div>
        </div>""", unsafe_allow_html=True)