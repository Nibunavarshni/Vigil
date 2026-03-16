import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import os
from exif import Image as ExifImage 
import time
import pickle
import base64
import io
import re
import hashlib
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import pandas as pd
from fpdf import FPDF
import sqlite3
import uuid
import json
import random
import math
from datetime import datetime, timedelta
from google.cloud import speech_v1 as speech
from google.cloud import texttospeech_v1 as texttospeech
from google.oauth2 import service_account 

# ==========================================
# 0. AUTHENTICATION (FIXED)
# ==========================================

tts_client = None
stt_client = None

json_path = "credentials.json" 

EMBEDDED_CREDS = {
  "type": "service_account",
  "project_id": "project-707e889e-2bc0-4df3-867",
  "private_key_id": "e0f4e108584e7da7e560b5848bd37febd7bfaa41",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDPeXJDN5QF926h\nOWOXc1Z9m355ctVM6D4DFS+aT9WbYWmdCnMhhPODp2UfGR0BQ+sbMYwkBhDGy/5e\nnkEYNkpQ++F0tpzO6Dmp8oUzkiCIWp+RlKAdJmH86nBRK/zXJW39SGDmqguh8kCi\nx7H4QVJunKasKY+dEzp48G6FlnOcKPkjkbL7BbHHLjk1lDDLhNw4Bbdsuqob64UP\n7ggp6zZKCzsadl+nXaHW5sAH75X2okW6Yg9HeeU6TZrIRv79Ei7/6NPgoBUD2g5S\nHE4qHTGLXbKVXUqT8JmtLdEpkcUz/Lg/aqrZih1fGRcKf+tCGML9LKKYzhq4fQhx\n60OkhQN3AgMBAAECggEAQhfYsBQM+iecHQ0ork8GTwZRcIQF8jWLx7SgkQJ8tD6A\nhBAXpCZz4s1ZN+JqrIQD6gpLMBCkmIfUtTSp3Poyi4DqDiG8a2dsMzj4ePjEl1tz\nOM/Ff/PBxG20sQ8XwTwBwW2kvOaPxRvkvlZqWgEJLwaFTBQDVZESEAPb2X+Xvbd2\n6uDiV9q5rbtBePZUplq3DNTJizFqcdhxwnBJGTt1fMGXcrK2VbWGdDkzZsgfXje8\n8xXBv5whAUq/Bv73DCaC2iwFR9mUZQVpwbI13xdBGPmGswsSuzGbdaczN8h7HtSb\nFHf3osmcbcrPcXGhTk6tLxZqwatybFKo97vKkIvw2QKBgQDos2fVwCx+jkDVaBg4\nZdU/kVSEugOCPH5VeI4sRNsBxjoRp8E/p+fL345xRg2uHdLptdWZyKdwydhRI6z5\nrjSoNnNfWcqYI87fGGArfaOjay2E9bXxZfc0Gj4S2hKgEm4eNynvWNGKcV/qH9sY\nMt3HETCgDKZd8vd/4xhADNwdOQKBgQDkP2/PYIQ3xai9D67f6GBHJcozqTHK4XHp\nX9ba6eGuLphbDOss7dwivd78YBMDXWRBQhOuJcIuh0fiOOX+3n1OeLDHgur+CrlV\nCksqLjYfxWFiLYDcVjt7IJwX9VA1D84VS41jFzQS/oHQ1PnaLaimQAVUu4VWmFjt\nRF2/sx7WLwKBgQC6WanmuH4pXzw2aqUyzQIoZPb9T4Wtz0oQonmgpAeK9Tbdmq0c\nkBcF4mLM/Z/I9yNHfBGxlMnafhoYaGyGiuaqauibzGl8yvhJGtkxGu1n2lXaq3bn\n+ZMtC3L4X+EYhYinf8qdHgKZVqxN3h8lKKLoISBDbqyW0CPYBWVi7OlEvqQKBgFOy\nb228Fr/c22N4vMeejq+IS/1lrbyXrw3E9ySPXxJgQ74fnp17G54hwgMJt+8j7/9+\nG3lgnzQwp0ttUemD7K850plWiJVfmVZ1z9pH19EOsAcwaHBjrqwX6SVf72mFwixM\n6CvN9mqAqVnKv1QiKhXMpCfOG7cFZpaa20XQiR5BAoGAfnuPcvXI5Z9VKhqVfgtD\nYHJMvBG3Mfm0D2LV8NhFY95eR5cluwVw3MmXpyrSWgNBOcfO/SK1p2YrPHXq4jEr\nZHLRmw+nJ5oWvE4hPAHBcRFeS8jFl/uA6CPBEDzg/FF/iMC/M+ZPHQ1vlBkkEXuL\nE/q76NXzc5tbr+ONv+jqO10=\n-----END PRIVATE KEY-----\n",
  "client_email": "vigil-873@project-707e889e-2bc0-4df3-867.iam.gserviceaccount.com",
  "client_id": "100380016829311007769",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vigil-873%40project-707e889e-2bc0-4df3-867.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

try:
    creds = None
    if os.path.exists(json_path):
        with open(json_path) as f:
            creds_data = json.load(f)
        if 'client_email' in creds_data and 'private_key' in creds_data:
            creds = service_account.Credentials.from_service_account_info(creds_data)
            st.success("✅ VIGIL Systems Online (Local File)")
        else:
            creds = None
    if not creds:
        creds = service_account.Credentials.from_service_account_info(EMBEDDED_CREDS)
        st.success("✅ VIGIL Systems Online (Secure Embedded Auth)")
    tts_client = texttospeech.TextToSpeechClient(credentials=creds)
    stt_client = speech.SpeechClient(credentials=creds)
except Exception as e:
    pass

# ==========================================
# 1. DATABASE & CORE SETUP
# ==========================================

def init_db():
    conn = sqlite3.connect('vigil_core.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   user_name TEXT, 
                   location TEXT, 
                   dept TEXT, 
                   risk_score INTEGER, 
                   petition TEXT, 
                   status TEXT DEFAULT 'Pending',
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   evidence_hash TEXT,
                   sentiment TEXT,
                   success_score INTEGER)''')
    try:
        c.execute("SELECT evidence_hash FROM reports LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("ALTER TABLE reports ADD COLUMN evidence_hash TEXT")
    try:
        c.execute("SELECT sentiment FROM reports LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("ALTER TABLE reports ADD COLUMN sentiment TEXT")
    try:
        c.execute("SELECT success_score FROM reports LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("ALTER TABLE reports ADD COLUMN success_score INTEGER")
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

STATE_LANG_MAP = {
    "Andhra Pradesh": "Telugu", "Tamil Nadu": "Tamil", "Karnataka": "Kannada",
    "Maharashtra": "Marathi", "Delhi": "Hindi", "Gujarat": "Gujarati",
    "West Bengal": "Bengali", "Kerala": "Malayalam"
}

def get_petition_language_logic(dept, state):
    state_lang = STATE_LANG_MAP.get(state, "English")
    technical_depts = ["PWD/Roads", "Electricity", "Water/Sewerage"]
    if state_lang != "English":
        if dept in technical_depts:
            return f"Generate the petition primarily in English for technical specifications, but include a summary in {state_lang}."
        else:
            return f"Generate the petition in BOTH English AND {state_lang}. It is mandatory to include the regional language translation."
    return "Generate the petition in English."

def calculate_deadline(time_str):
    try:
        if "hour" in time_str.lower():
            hours = int(re.search(r'\d+', time_str).group())
            return datetime.now() + timedelta(hours=hours)
        elif "day" in time_str.lower():
            days = int(re.search(r'\d+', time_str).group())
            return datetime.now() + timedelta(days=days)
        elif "week" in time_str.lower():
            weeks = int(re.search(r'\d+', time_str).group())
            return datetime.now() + timedelta(weeks=weeks)
        else:
            return datetime.now() + timedelta(days=2)
    except:
        return datetime.now() + timedelta(days=2)

# ==========================================
# 3. GOOGLE CLOUD AUTHENTICATION SETUP
# ==========================================

def get_google_credentials():
    try:
        if "google_credentials" in st.secrets:
            cred_dict = dict(st.secrets["google_credentials"])
            if "private_key" in cred_dict:
                cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
            return service_account.Credentials.from_service_account_info(cred_dict)
        else:
            return None
    except Exception as e:
        return None

g_creds = get_google_credentials()

if g_creds:
    tts_client = texttospeech.TextToSpeechClient(credentials=g_creds)
    stt_client = speech.SpeechClient(credentials=g_creds)

# ==========================================
# 4. REALTIME AGENT FUNCTIONS (STT & TTS)
# ==========================================

def speak_now_google(text, speech_id=None):
    if not text: return
    if speech_id and st.session_state.get('last_speech_id') == speech_id: return
    st.session_state.last_spoken_time = time.time()
    st.session_state.agent_state = 'speaking'
    
    target_lang = st.session_state.u_data.get('lang', 'English')
    
    # FIX: Optimized for Natural Female Voices (Neural2 > Wavenet > Standard)
    # Neural2 voices are the most realistic.
    lang_voice_map = {
        "English": {"code": "en-US", "name": "en-US-Neural2-F"}, # Top tier Natural Female
        "Hindi": {"code": "hi-IN", "name": "hi-IN-Neural2-C"},   # Natural Female
        "Tamil": {"code": "ta-IN", "name": "ta-IN-Wavenet-D"},    # High Quality Female
        "Telugu": {"code": "te-IN", "name": "te-IN-Wavenet-A"},   # Upgraded to Wavenet Female
        "Kannada": {"code": "kn-IN", "name": "kn-IN-Wavenet-A"},  # Upgraded to Wavenet Female
        "Malayalam": {"code": "ml-IN", "name": "ml-IN-Standard-A"},
        "Marathi": {"code": "mr-IN", "name": "mr-IN-Standard-A"},
        "Bengali": {"code": "bn-IN", "name": "bn-IN-Standard-A"},
        "Gujarati": {"code": "gu-IN", "name": "gu-IN-Standard-A"}
    }
    
    voice_params = lang_voice_map.get(target_lang, {"code": "en-US", "name": "en-US-Neural2-F"})
    lang_code = voice_params["code"]
    voice_name = voice_params["name"]

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE # Explicitly set Female
    )
    # Optimized audio config for natural speech
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0, # Normal rate
        pitch=0.0 # Normal pitch, relying on the model's natural voice
    )
    
    try:
        response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        audio_bytes = response.audio_content
        b64 = base64.b64encode(audio_bytes).decode()
        components.html(f"""
            <audio autoplay src="data:audio/mp3;base64,{b64}"></audio>
            <script>
            document.querySelector('audio').onended = function() {{
                window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'speaking_end'}}, '*');
            }};
            </script>
        """, height=0)
        if speech_id: st.session_state.last_speech_id = speech_id
    except Exception as e:
        pass

def listen_google(audio_bytes):
    if not stt_client: return ""
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000, 
        language_code="en-IN",
        enable_automatic_punctuation=True,
        alternative_language_codes=["hi-IN", "ta-IN", "te-IN", "kn-IN"] 
    )
    transcript = ""
    try:
        response = stt_client.recognize(config=config, audio=audio)
        for result in response.results:
            transcript = result.alternatives[0].transcript
    except Exception:
        try:
            config.encoding = speech.RecognitionConfig.AudioEncoding.WEBM_OPUS
            response = stt_client.recognize(config=config, audio=audio)
            for result in response.results:
                transcript = result.alternatives[0].transcript
        except Exception:
            try:
                config.encoding = speech.RecognitionConfig.AudioEncoding.OGG_OPUS
                response = stt_client.recognize(config=config, audio=audio)
                for result in response.results:
                    transcript = result.alternatives[0].transcript
            except:
                pass
    return transcript

def speak_now_fallback(text, speech_id=None):
    if not text: return
    if speech_id and st.session_state.get('last_speech_id') == speech_id: return
    clean_text = text.replace("*", "").replace("`", "").replace("'", "").replace("\n", " ").strip()
    target_lang = st.session_state.u_data.get('lang', 'English')
    lang_map = {"English": "en-GB", "Hindi": "hi-IN", "Tamil": "ta-IN", "Telugu": "te-IN", "Kannada": "kn-IN"}
    lang_code = lang_map.get(target_lang, "en-IN")
    st.session_state.last_spoken_time = time.time()
    st.session_state.agent_state = 'speaking'
    # FIX: Fallback voice logic for Browser TTS
    components.html(f"""
        <script>
        if (window.vigilRecognition) {{ try {{ window.vigilRecognition.stop(); }} catch(e){{}} }}
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = '{lang_code}';
        // Force Female Voice with Natural Settings
        var voices = window.speechSynthesis.getVoices();
        var femaleKeywords = ["female", "zira", "samantha", "google uk english female", "victoria", "karen"];
        var v = voices.find(v => v.lang.startsWith('{lang_code}') && femaleKeywords.some(k => v.name.toLowerCase().includes(k))) || voices.find(v => v.lang.startsWith('{lang_code}')) || voices[0];
        if(v) msg.voice = v;
        msg.rate = 0.95; // Slightly slower for clarity
        msg.pitch = 1.1; // Slightly higher pitch for feminine tone
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)
    if speech_id: st.session_state.last_speech_id = speech_id

def speak_now(text, speech_id=None):
    active_tts = tts_client if tts_client else (tts_client if 'tts_client' in globals() else None)
    if active_tts:
        speak_now_google(text, speech_id)
    else:
        speak_now_fallback(text, speech_id)

# ==========================================
# 5. CORE LOGIC (PRESERVED)
# ==========================================

def generate_blockchain_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()

def create_pdf_report(petition_text, user_data, urgency, dept, time_frame, hash_code):
    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 16)
    except Exception as e:
        pdf.set_font("Arial", 'B', 16)
        petition_text = "".join([i if ord(i) < 128 else " " for i in petition_text])
    pdf.cell(200, 10, txt="VIGIL: OFFICIAL CIVIC REPORT", ln=True, align='C')
    pdf.ln(5)
    pdf.set_font('DejaVu' if 'DejaVu' in pdf.fonts else 'Arial', size=10)
    pdf.cell(200, 8, txt=f"Reporter: {user_data['name']}", ln=True)
    pdf.cell(200, 8, txt=f"Location: {user_data['loc']} | Ward: {user_data.get('ward', 'N/A')}", ln=True)
    pdf.cell(200, 8, txt=f"Assigned Dept: {dept} | Urgency: {urgency}/10", ln=True)
    pdf.cell(200, 8, txt=f"Estimated Resolution Time: {time_frame}", ln=True)
    pdf.cell(200, 8, txt=f"Evidence Hash (SHA-256): {hash_code[:20]}...", ln=True)
    pdf.ln(5)
    pdf.set_font('DejaVu' if 'DejaVu' in pdf.fonts else 'Arial', size=12)
    pdf.multi_cell(0, 8, txt=petition_text)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def get_google_service(api_name='gmail', api_version='v1'):
    """Generic function to get Google API service (Gmail or Calendar)"""
    scopes_map = {
        'gmail': ['https://www.googleapis.com/auth/gmail.compose'],
        'calendar': ['https://www.googleapis.com/auth/calendar.events']
    }
    SCOPES = scopes_map.get(api_name, [])
    
    creds = None
    token_file = f'token_{api_name}.pickle'
    
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token: creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as token: pickle.dump(creds, token)
    return build(api_name, api_version, credentials=creds)

def create_gmail_draft(body_text, subject, recipient):
    try:
        service = get_google_service('gmail', 'v1')
        message = EmailMessage()
        message.set_content(body_text)
        message['To'], message['From'], message['Subject'] = recipient, "me", subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft = service.users().drafts().create(userId="me", body={'message': {'raw': encoded_message}}).execute()
        return draft
    except Exception as e: return str(e)

def add_to_google_calendar(summary, description, deadline_dt):
    """Creates an event in the user's Google Calendar"""
    try:
        service = get_google_service('calendar', 'v3')
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': deadline_dt.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': (deadline_dt + timedelta(hours=1)).isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60}, 
                    {'method': 'popup', 'minutes': 60},      
                ],
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event.get('htmlLink')
    except HttpError as e:
        # FIX: Robust error handling for disabled API
        if e.resp.status == 403:
            st.error("🚫 **Google Calendar API Access Denied**")
            st.warning("The Google Calendar API is not enabled for your project credentials.")
            with st.expander("🔧 How to Fix This (Click to Expand)"):
                st.markdown("""
                **Step 1:** Click the link below to go to the Google Cloud Console.
                **Step 2:** Click the **"Enable"** button.
                **Step 3:** Wait 2-3 minutes for the changes to propagate.
                **Step 4:** Try adding to the calendar again.
                """)
                st.link_button("Enable Google Calendar API", "https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview?project=336991820781")
        else:
            st.error(f"An unexpected error occurred: {e}")
        return None
    except Exception as e:
        st.error(f"Auth Configuration Error: {e}")
        return None

def get_image_coordinates(img_file):
    try:
        img_bytes = img_file.getvalue()
        readable_img = ExifImage(img_bytes)
        if readable_img.has_exif:
            lat = readable_img.get("gps_latitude")
            lon = readable_img.get("gps_longitude")
            lat_ref = readable_img.get("gps_latitude_ref")
            lon_ref = readable_img.get("gps_longitude_ref")
            if lat and lon:
                def dms_to_dd(d, m, s, ref):
                    dd = d + m/60.0 + s/3600.0
                    if ref in ['S', 'W']: dd = -dd
                    return dd
                decimal_lat = dms_to_dd(lat[0], lat[1], lat[2], lat_ref)
                decimal_lon = dms_to_dd(lon[0], lon[1], lon[2], lon_ref)
                return pd.DataFrame({'lat': [decimal_lat], 'lon': [decimal_lon]})
        return None
    except: return None

def save_report(user, loc, dept, risk, petition, hash_code, sentiment="Neutral", success_score=50):
    try:
        conn = sqlite3.connect('vigil_core.db', check_same_thread=False)
        c = conn.cursor()
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO reports (user_name, location, dept, risk_score, petition, timestamp, evidence_hash, sentiment, success_score) VALUES (?,?,?,?,?,?,?,?,?)",
                  (user, loc, dept, risk, petition, ts, hash_code, sentiment, success_score))
        conn.commit()
        st.toast(f"✅ Report Synced to Database", icon='💾')
    except Exception as e:
        st.error(f"Database Write Failure: {e}")
    finally:
        conn.close()

def get_past_reports():
    conn = sqlite3.connect('vigil_core.db')
    df = pd.read_sql_query("SELECT timestamp, location, dept, risk_score, status FROM reports ORDER BY id DESC", conn)
    conn.close()
    return df

# ==========================================
# 6. BRAIN CONFIGURATION
# ==========================================

API_KEY = "AIzaSyDpznMWbVTFkj-zagQGwjthvNIzMFgA-Vk" 
os.environ["GOOGLE_GENAI_USE_V1"] = "1"
genai.configure(api_key=API_KEY)
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if "flash" in m), "gemini-1.5-flash")
    model = genai.GenerativeModel(target_model)
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 7. DATA & UI INITIALIZATION
# ==========================================

LOC_DATA = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Tirupati", "Anantapur"],
    "Tamil Nadu": ["Salem", "Chennai", "Coimbatore", "Madurai", "Trichy", "Erode", "Vellore"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi-Dharwad", "Mangaluru", "Belagavi"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad"],
    "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi"]
}

DEPT_EMAILS = {
    "PWD/Roads": "pwd.executive.{dist}@gov.in",
    "Electricity": "superintending.engineer.{dist}@electricity.gov.in",
    "Sanitation/Health": "health.officer.{dist}@gov.in",
    "Water/Sewerage": "water.board.{dist}@gov.in",
    "General/Municipal": "commissioner.{dist}@gov.in",
    "Emergency": "emergency.control@nic.in",
    "Escalation": "district.collector.{dist}@nic.in",
    "RTI": "pio.{dist}@nic.in",
    "Lokayukta": "lokayukta.{state}@nic.in"
}

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'policy_accepted' not in st.session_state: st.session_state.policy_accepted = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'urgency_score' not in st.session_state: st.session_state.urgency_score = 0
if 'hero_points' not in st.session_state: st.session_state.hero_points = 0
if 'u_data' not in st.session_state: st.session_state.u_data = {}
if 'map_coords' not in st.session_state: st.session_state.map_coords = None
if 'stage' not in st.session_state: st.session_state.stage = 'greeting'
if 'xp_trigger' not in st.session_state: st.session_state.xp_trigger = False
if 'last_speech_id' not in st.session_state: st.session_state.last_speech_id = ""
if 'last_spoken_text' not in st.session_state: st.session_state.last_spoken_text = ""
if 'impact_score' not in st.session_state: st.session_state.impact_score = 0
if 'voice_mode_active' not in st.session_state: st.session_state.voice_mode_active = False
if 'last_spoken_time' not in st.session_state: st.session_state.last_spoken_time = 0
if 'transcription' not in st.session_state: st.session_state.transcription = ""
if 'speech_processed' not in st.session_state: st.session_state.speech_processed = False
if 'agent_state' not in st.session_state: st.session_state.agent_state = 'idle'
if 'escalation_level' not in st.session_state: st.session_state.escalation_level = 0
if 'live_text' not in st.session_state: st.session_state.live_text = ""
if 'success_prediction' not in st.session_state: st.session_state.success_prediction = 0
if 'user_sentiment' not in st.session_state: st.session_state.user_sentiment = "Neutral"
if 'voice_intent' not in st.session_state: st.session_state.voice_intent = ""

st.set_page_config(page_title="Vigil Neural Command", layout="wide")

# ==========================================
# 8. NEON CSS & ANIMATIONS (ENHANCED)
# ==========================================

st.markdown("""<style>
    .stApp { background-color: #050505 !important; }
    
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 400%; height: 400%;
        background-image: linear-gradient(rgba(0, 255, 170, 0.18) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 255, 170, 0.18) 1px, transparent 1px);
        background-size: 50px 50px; animation: gridMove 20s linear infinite; z-index: 0;
        pointer-events: none;
    }
    @keyframes gridMove { from { transform: translate(0, 0); } to { transform: translate(-100px, -100px); } }
    
    .glow-title { color: #00FFAA !important; font-family: 'Orbitron', sans-serif; font-size: 40px; text-shadow: 0 0 10px #00FFAA; font-weight: bold; text-align: center; margin: 0; }
    
    .glass-panel { 
        background: linear-gradient(145deg, rgba(10, 20, 15, 0.85), rgba(5, 10, 7, 0.95)); 
        backdrop-filter: blur(20px); border: 1px solid rgba(0, 255, 170, 0.3); 
        border-radius: 20px; padding: 25px; margin-bottom: 20px; color: white; 
        box-shadow: 0 0 30px rgba(0, 255, 170, 0.1), inset 0 0 20px rgba(0,0,0,0.5);
        position: relative; z-index: 1; overflow: hidden;
        display: flex; flex-direction: column; height: 100%;
    }
    
    .glass-panel::after {
        content: ""; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 170, 0.05), transparent);
        animation: scan 4s linear infinite;
    }
    @keyframes scan { 0% { left: -100%; } 100% { left: 200%; } }
    
    .chat-container { 
        display: flex; flex-direction: column; gap: 15px; 
        padding: 20px; overflow-y: auto; flex-grow: 1;
        scrollbar-width: thin; scrollbar-color: #00FFAA #050505;
        border: 1px solid rgba(0,255,170,0.1); border-radius: 10px;
        background: rgba(0,0,0,0.2);
        max-height: 400px;
    }
    .chat-bubble-ai { 
        background: linear-gradient(90deg, rgba(0, 255, 170, 0.15), rgba(0, 100, 80, 0.05)); 
        border-left: 4px solid #00FFAA; padding: 18px; border-radius: 4px 20px 20px 4px; 
        color: #f0f0f0; box-shadow: 0 4px 15px rgba(0,0,0,0.2); animation: slideIn 0.4s ease-out;
        font-family: 'Segoe UI', sans-serif; font-size: 16px; max-width: 85%;
        align-self: flex-start;
    }
    .chat-bubble-user { 
        background: rgba(0, 170, 255, 0.15); border-right: 4px solid #00AAFF;
        padding: 18px; border-radius: 20px 4px 4px 20px; text-align: right; 
        color: #ddd; animation: slideIn 0.4s ease-out;
        align-self: flex-end; max-width: 85%;
    }
    
    .live-transcript {
        font-style: italic; color: #aaa; 
        border-left: 2px solid #555; padding-left: 10px;
        animation: fadeIn 0.5s;
        opacity: 0.7;
    }
    
    @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    
    .urgency-bar { height: 8px; background: #111; border-radius: 4px; overflow: hidden; margin: 10px 0; border: 1px solid #333; }
    .urgency-fill { height: 100%; transition: width 1s ease; }
    
    @keyframes fly-to-sidebar { 
        0% { transform: scale(1) translate(0, 0) rotate(0deg); opacity: 1; } 
        50% { transform: scale(1.5) translate(-20vw, -20vh) rotate(360deg); opacity: 1; text-shadow: 0 0 40px gold; }
        100% { transform: scale(0) translate(-80vw, -60vh) rotate(720deg); opacity: 0; } 
    }
    .xp-medal { 
        position: fixed; top: 50%; left: 50%; font-size: 100px; z-index: 9999; 
        animation: fly-to-sidebar 1.8s ease-in-out forwards; pointer-events: none; 
        text-shadow: 0 0 30px gold;
    }
    
    .stButton>button { border: 1px solid #00FFAA; background: rgba(0,40,30,0.6); color: #00FFAA; transition: all 0.3s; font-weight: bold; }
    .stButton>button:hover { background: #00FFAA; color: black; box-shadow: 0 0 25px #00FFAA; transform: translateY(-2px); }
    
    .stProgress > div > div > div { background-color: #00FFAA; }
    
    .vigil-logo { 
        width: 80px; height: 80px; border-radius: 50%; border: 2px solid #00FFAA;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.5); background: black;
        display: flex; align-items: center; justify-content: center; font-size: 40px;
        margin-bottom: 10px;
    }
    
    .voice-container { 
        position: sticky; bottom: 0; background: rgba(5, 10, 7, 0.95); padding: 20px; 
        border-top: 1px solid #00FFAA; border-radius: 20px 20px 0 0; z-index: 100;
        backdrop-filter: blur(10px); margin-top: 20px;
    }
    
    .waveform-container {
        display: flex; justify-content: center; align-items: center; gap: 4px; height: 40px;
        margin-bottom: 10px;
    }
    .wave-bar {
        width: 4px; height: 10px; background-color: #00FFAA; border-radius: 2px;
        transition: height 0.1s ease;
    }
    .wave-bar.active {
        animation: wave-anim 0.5s ease-in-out infinite;
    }
    
    @keyframes wave-anim {
        0%, 100% { height: 10px; }
        50% { height: 30px; }
    }
    
    @keyframes pulse { 
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 170, 0.7); transform: scale(1); } 
        70% { box-shadow: 0 0 0 20px rgba(0, 255, 170, 0); transform: scale(1.1); } 
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 170, 0); transform: scale(1); } 
    }
    .listening-indicator { 
        width: 20px; height: 20px; background: #00FFAA; border-radius: 50%; 
        display: inline-block; animation: pulse 1.5s infinite;
    }
    
    .stat-card {
        background: rgba(0,0,0,0.3); border: 1px solid rgba(0,255,170,0.2);
        border-radius: 10px; padding: 10px; text-align: center;
    }
    .stat-value { font-size: 20px; font-weight: bold; color: #00FFAA; }
    .stat-label { font-size: 12px; color: #888; }
    
    section[data-testid="stAudioInput"] { border: 2px solid #00FFAA; border-radius: 20px; padding: 10px; background: rgba(0,40,30,0.6); }
    
    /* Timeline Calendar Styles */
    .timeline-card {
        background: linear-gradient(135deg, rgba(0,0,0,0.6), rgba(0,40,30,0.4));
        border: 1px solid #00FFAA;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0,255,170,0.2);
    }
    .timeline-date {
        font-size: 28px;
        font-weight: bold;
        color: #00FFAA;
        text-shadow: 0 0 10px rgba(0,255,170,0.5);
    }
    .timeline-month {
        font-size: 14px;
        color: #FFF;
        letter-spacing: 2px;
    }
    .calendar-btn {
        background: linear-gradient(90deg, #00FFAA, #00AAFF) !important;
        color: #000 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        margin-top: 10px !important;
        width: 100% !important;
    }
    
    </style>""", unsafe_allow_html=True)

components.html("""
    <canvas id="n" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;background:transparent;"></canvas>
    <script>
    const c=document.getElementById("n"),x=c.getContext("2d");
    c.width=window.innerWidth;c.height=window.innerHeight;
    let p=[];for(let i=0;i<60;i++)p.push({x:Math.random()*c.width,y:Math.random()*c.height,vx:(Math.random()-0.5)*0.5,vy:(Math.random()-0.5)*0.5});
    function d(){x.clearRect(0,0,c.width,c.height);p.forEach(n=>{n.x+=n.vx;n.y+=n.vy;if(n.x<0||n.x>c.width)n.vx*=-1;if(n.y<0||n.y>c.height)n.vy*=-1;
    x.fillStyle="rgba(0,255,170,0.5)";x.beginPath();x.arc(n.x,n.y,1,0,Math.PI*2);x.fill();
    p.forEach(n2=>{let d=Math.hypot(n.x-n2.x,n.y-n2.y);if(d<120){x.strokeStyle=`rgba(0,255,170,${0.8-d/120})`;x.lineWidth=0.3;x.beginPath();x.moveTo(n.x,n.y);x.lineTo(n2.x,n2.y);x.stroke();}})});
    requestAnimationFrame(d);}d();
    </script>
""", height=0)

# ==========================================
# 9. SIDEBAR (VP & LOGOUT)
# ==========================================

with st.sidebar:
    st.markdown("### ⚡ VIGIL STATUS")
    
    if st.session_state.logged_in:
        if st.button("🚪 System Logout"):
            st.session_state.logged_in = False
            st.session_state.chat_history = []
            st.session_state.stage = 'greeting'
            st.session_state.hero_points = 0
            st.session_state.urgency_score = 0
            st.session_state.last_speech_id = ""
            st.session_state.transcription = ""
            st.session_state.escalation_level = 0
            st.session_state.xp_trigger = False
            st.rerun()
        st.divider()

    pts = st.session_state.hero_points
    rank = "NOVICE" if pts < 100 else "GUARDIAN" if pts < 300 else "LEGEND"
    color = "#888" if pts < 100 else "#00FFAA" if pts < 300 else "#0088ff"
    
    st.markdown(f"""
    <div style='background:{color}; color:#000; padding:8px; 
    border-radius:20px; font-weight:bold; text-align:center; font-size:14px;'>
       🎖️ {rank} AGENT
    </div>
    """, unsafe_allow_html=True)
    
    st.metric("Vigil Points (VP)", f"{pts} XP")
    st.progress(min(100, pts % 100) / 100, text="Level Progress")
    
    st.divider()
    st.markdown("### 🕒 Incident History")
    history_df = get_past_reports()
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True, hide_index=True, height=200)
    else:
        st.info("No past reports.")

# ==========================================
# 10. LOGIN PAGE
# ==========================================

@st.dialog("🛡️ Vigil: Data Privacy & Legal Consent")
def show_policy():
    st.write("Vigil uses vision-AI to analyze civic infrastructure. Your identity is shared only with designated authorities. Evidence is hashed for integrity.")
    if st.button("I Accept Policy"):
        st.session_state.policy_accepted = True
        st.rerun()

VIGIL_LOGO_SVG = """
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M50 10 L90 30 L90 60 C90 80 50 95 50 95 C50 95 10 80 10 60 L10 30 Z" fill="none" stroke="#00FFAA" stroke-width="3"/>
  <circle cx="50" cy="45" r="15" fill="none" stroke="#00FFAA" stroke-width="2"/>
  <circle cx="50" cy="45" r="5" fill="#00FFAA"/>
  <path d="M30 55 Q50 70 70 55" fill="none" stroke="#00FFAA" stroke-width="2"/>
</svg>
"""
VIGIL_LOGO_HTML = f"<div style='width:80px; height:80px; margin: 0 auto;'>{VIGIL_LOGO_SVG}</div>"

if not st.session_state.logged_in:
    st.markdown(VIGIL_LOGO_HTML, unsafe_allow_html=True)
    st.markdown("<h1 class='glow-title'>RESIDENT LOGIN</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        sel_state = st.selectbox("Select State", list(LOC_DATA.keys()))
        sel_dist = st.selectbox("Select District", LOC_DATA.get(sel_state, ["Select"]))
        default_lang_index = ["English", "Hindi", "Tamil", "Kannada", "Telugu"].index(STATE_LANG_MAP.get(sel_state, "English"))
        u_lang = st.selectbox("System Voice Language", ["English", "Hindi", "Tamil", "Kannada", "Telugu"], index=default_lang_index)
        u_ward = st.text_input("Ward Number / Area", placeholder="e.g. Ward 12")
        st.divider()
        u_name = st.text_input("Full Name")
        u_phone = st.text_input("Mobile Number (+91)")
        u_mail = st.text_input("Official Email ID")
        if st.button("📜 Read Privacy Policy"): show_policy()
        policy_check = st.checkbox("I accept Privacy Policy", value=st.session_state.policy_accepted)
        if st.button("Initialize System"):
            if u_name and u_mail and u_phone and policy_check:
                st.session_state.logged_in = True
                st.session_state.u_data = {
                    "name": u_name, "mail": u_mail, "phone": u_phone, 
                    "loc": f"{sel_dist}, {u_ward}", "state": sel_state, 
                    "dist": sel_dist, "ward": u_ward, "lang": u_lang
                }
                st.session_state.chat_history.append({"role": "ai", "content": f"Hello {u_name}, I am Vigil. How can I help you today?"})
                st.session_state.speech_text = f"Hello {u_name}, I am Vigil. How can I help you today?"
                st.session_state.speech_id = str(uuid.uuid4())
                st.rerun()
            else: st.warning("Please complete all fields.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 11. AGENT WORKSPACE
# ==========================================

else:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 20px;">
        <div style="font-size: 40px; text-shadow: 0 0 15px #00FFAA;">🛡️</div>
        <div>
            <h1 class='glow-title' style="margin: 0;">VIGIL</h1>
            <p style='text-align:center; color:#00FFAA; font-family:Orbitron; margin:0; font-size: 12px;'>THE INTELLIGENCE BEHIND A BETTER INDIA</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4, m5 = st.columns(5)
    urg_lbl = ["LOW", "MODERATE", "HIGH", "CRITICAL"]
    risk_idx = min(3, int(st.session_state.urgency_score / 2.6)) if st.session_state.urgency_score > 0 else 0
    m1.metric("STATUS", "ACTIVE"); 
    m2.metric("REGION", st.session_state.u_data['dist'].upper()); 
    m3.metric("DEPT", st.session_state.get('assigned_dept', 'General')); 
    m4.metric("URGENCY", urg_lbl[risk_idx])
    m5.metric("IMPACT SCORE", st.session_state.get('impact_score', 0))

    col_work, col_logic = st.columns([1, 1.3], gap="large")

    # --- LEFT COLUMN: INPUTS ---
    with col_work:
        st.markdown("<div class='glass-panel'><h3>🛰️ Workspace</h3>", unsafe_allow_html=True)
        
        mode = st.radio("Input Mode", ["Upload Evidence", "Camera 📷"], horizontal=True)
        evidence_photo = None
        audio_value = None
        
        if mode == "Upload Evidence":
            uploaded_file = st.file_uploader("Upload Evidence Photo", type=['jpg', 'png', 'jpeg'])
            if uploaded_file:
                evidence_photo = uploaded_file
                st.image(uploaded_file, use_container_width=True)
                coords = get_image_coordinates(uploaded_file)
                if coords is not None: st.session_state.map_coords = coords
            
            st.divider()
            st.markdown("#### 🎙️ Audio Evidence")
            st.caption("Click below to record audio directly from your microphone.")
            audio_val = st.audio_input("Record Audio Evidence")
            if audio_val:
                st.audio(audio_val)
                st.success("✅ Audio evidence recorded and attached.")

        elif mode == "Camera 📷":
            st.markdown("##### 📷 Live Geotagged Camera")
            cam_html = f"""
                <div style="background:#080808; padding:15px; border-radius:15px; border:1px solid #00FFAA;">
                    <video id="v" width="100%" autoplay style="border-radius:10px;"></video>
                    <canvas id="canvas" style="display:none;"></canvas>
                    <div id="loc_info" style="color:#00FFAA; font-family:monospace; font-size:13px; margin-top:10px;">Acquiring Satellite Lock...</div>
                    <button id="snap" style="width:100%; margin-top:10px; padding:12px; background:#00FFAA; border:none; border-radius:8px; color:#000; font-weight:bold; cursor:pointer;">CAPTURE</button>
                </div>
                <script>
                const v=document.getElementById('v'), btn=document.getElementById('snap'), info=document.getElementById('loc_info'), canvas=document.getElementById('canvas');
                let lat="", lon="", addr="{st.session_state.u_data['loc']}";
                navigator.mediaDevices.getUserMedia({{video: true}}).then(s=>v.srcObject=s);
                navigator.geolocation.watchPosition(p=>{{
                    lat=p.coords.latitude.toFixed(6); lon=p.coords.longitude.toFixed(6);
                    info.innerHTML = "📍 GPS: " + lat + ", " + lon;
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: {{'lat':lat, 'lon':lon}} }}, '*');
                }}, e=>console.log(e), {{enableHighAccuracy: true}});
                btn.onclick=()=>{{
                    canvas.width=v.videoWidth; canvas.height=v.videoHeight;
                    const ctx=canvas.getContext('2d'); ctx.drawImage(v,0,0);
                    ctx.fillStyle="rgba(0,0,0,0.7)"; ctx.fillRect(0, canvas.height-60, canvas.width, 60);
                    ctx.fillStyle="#00FFAA"; ctx.font="bold 18px Arial";
                    ctx.fillText("VIGIL | " + addr, 10, canvas.height-35);
                    ctx.fillText("GPS: " + lat + ", " + lon, 10, canvas.height-15);
                    const data = canvas.toDataURL('image/jpeg', 0.9);
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: {{'img':data, 'lat':lat, 'lon':lon}} }}, '*');
                }};
                </script>
            """
            components.html(cam_html, height=450)

        if st.session_state.map_coords is not None:
            st.map(st.session_state.map_coords, zoom=14)
        else:
            default_data = pd.DataFrame({'lat': [11.6643], 'lon': [78.1460]})
            st.map(default_data, zoom=6)

        st.markdown("</div>", unsafe_allow_html=True)

    # --- RIGHT COLUMN: AI LOGIC ---
    with col_logic:
        st.markdown("<div class='glass-panel'><h3>🧠 Agent Interface</h3>", unsafe_allow_html=True)
        
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            st.markdown(f"<div class='stat-card'><div class='stat-value'>{st.session_state.get('success_prediction', 0)}%</div><div class='stat-label'>Success Rate</div></div>", unsafe_allow_html=True)
        with s_col2:
            st.markdown(f"<div class='stat-card'><div class='stat-value'>{st.session_state.escalation_level}</div><div class='stat-label'>Escalation Level</div></div>", unsafe_allow_html=True)
        with s_col3:
            st.markdown(f"<div class='stat-card'><div class='stat-value'>{st.session_state.get('user_sentiment', 'Neutral')}</div><div class='stat-label'>User Sentiment</div></div>", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:rgba(0,255,170,0.2);'>", unsafe_allow_html=True)

        # CHAT UI
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            if chat['role'] == 'ai':
                st.markdown(f"<div class='chat-bubble-ai'>{chat['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble-user'>{chat['content']}</div>", unsafe_allow_html=True)
        
        if st.session_state.get('live_text'):
            st.markdown(f"<div class='live-transcript'>🎙️ {st.session_state.live_text}...</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

        current_stage = st.session_state.stage

        # ==========================================
        # PROCESS VOICE INTENT (State Machine)
        # ==========================================
        
        if 'voice_intent' in st.session_state and st.session_state.voice_intent:
            intent = st.session_state.voice_intent
            st.session_state.voice_intent = "" 
            
            if intent == "ANALYZE" and current_stage == 'greeting' and evidence_photo:
                st.session_state.trigger_analysis = True
            elif intent == "CONFIRM_DRAFT" and current_stage == 'analysis_done':
                st.session_state.trigger_draft = True
            elif intent == "RESOLVED" and current_stage == 'awaiting_resolution':
                st.session_state.trigger_resolved = True
            elif intent == "PENDING" and current_stage == 'awaiting_resolution':
                st.session_state.trigger_pending = True

        # STAGE 1: ANALYSIS
        if current_stage == 'greeting':
            should_analyze = st.session_state.pop('trigger_analysis', False)
            
            if evidence_photo and (should_analyze or st.button("Analyze Situation", type="primary")):
                st.session_state.chat_history.append({"role": "user", "content": "📷 Image Uploaded"})
                
                with st.status("🧠 Neural Processing...", expanded=True) as status:
                    st.write("🔄 Initializing Vision Core...")
                    time.sleep(0.5)
                    st.write("🔍 Scanning for anomalies...")
                    
                    if hasattr(evidence_photo, 'getvalue'): img_bytes = evidence_photo.getvalue()
                    else: img_bytes = evidence_photo.read()
                    
                    img_hash = generate_blockchain_hash(img_bytes)
                    st.session_state.current_hash = img_hash
                    img_to_process = Image.open(io.BytesIO(img_bytes)).convert('RGB')
                    img_to_process.thumbnail((800, 800))
                    
                    st.write("⚖️ Cross-referencing Laws...")
                    user_lang = st.session_state.u_data.get('lang', 'English')
                    user_name = st.session_state.u_data.get('name', 'Citizen')
                    user_state = st.session_state.u_data.get('state', '')
                    
                    petition_instruction = get_petition_language_logic(st.session_state.get('assigned_dept', 'General'), user_state)

                    prompt = f"""
                    SYSTEM: You are Vigil, a proactive civic agent.
                    Analyze image.
                    1. SPEECH: Natural response in {user_lang} to {user_name}. 
                       - Tell what you found.
                       - IMPORTANT: If EMERGENCY is TRUE, tell user to press 'ESCALATE NOW'. 
                       - If EMERGENCY is FALSE, tell user to press 'Create Draft'.
                    2. DEPT: [PWD/Roads, Electricity, Sanitation/Health, Water/Sewerage, General/Municipal].
                    3. URGENCY: 1-10.
                    4. TIME: Resolution time (e.g., "24 hours", "3 days").
                    5. EMERGENCY: TRUE/ FALSE.
                    6. IMPACT: Estimated number of affected citizens (integer).
                    7. PREDICTION: Success probability score (0-100).
                    8. PETITION: {petition_instruction} Cite Indian Laws.
                    
                    FORMAT EXACTLY:
                    SPEECH: [text]
                    DEPT: [text]
                    URGENCY: [number]
                    TIME: [text]
                    EMERGENCY: [bool]
                    IMPACT: [number]
                    PREDICTION: [number]
                    PETITION: [text]
                    """
                    
                    try:
                        response = model.generate_content([prompt, img_to_process])
                        raw_text = response.text
                        
                        speech = re.search(r"SPEECH:(.*?)(?=DEPT:)", raw_text, re.DOTALL).group(1).strip() if re.search(r"SPEECH:(.*?)(?=DEPT:)", raw_text, re.DOTALL) else "Done."
                        dept = re.search(r"DEPT:(.*?)(?=URGENCY:)", raw_text, re.DOTALL).group(1).strip() if re.search(r"DEPT:(.*?)(?=URGENCY:)", raw_text, re.DOTALL) else "General"
                        urgency = int(re.search(r'\d+', re.search(r"URGENCY:(.*?)(?=TIME:)", raw_text, re.DOTALL).group(1)).group()) if re.search(r"URGENCY:(.*?)(?=TIME:)", raw_text, re.DOTALL) else 5
                        time_r = re.search(r"TIME:(.*?)(?=EMERGENCY:)", raw_text, re.DOTALL).group(1).strip() if re.search(r"TIME:(.*?)(?=EMERGENCY:)", raw_text, re.DOTALL) else "48 hours"
                        emergency = "TRUE" in (re.search(r"EMERGENCY:(.*?)(?=IMPACT:)", raw_text, re.DOTALL).group(1).strip() if re.search(r"EMERGENCY:(.*?)(?=IMPACT:)", raw_text, re.DOTALL) else "False").upper()
                        impact = int(re.search(r'\d+', re.search(r"IMPACT:(.*?)(?=PREDICTION:)", raw_text, re.DOTALL).group(1)).group()) if re.search(r"IMPACT:(.*?)(?=PREDICTION:)", raw_text, re.DOTALL) else 50
                        prediction = int(re.search(r'\d+', re.search(r"PREDICTION:(.*?)(=PETITION:)", raw_text, re.DOTALL).group(1)).group()) if re.search(r"PREDICTION:(.*?)(=PETITION:)", raw_text, re.DOTALL) else 80
                        petition = re.search(r"PETITION:(.*)", raw_text, re.DOTALL).group(1).strip() if re.search(r"PETITION:(.*)", raw_text, re.DOTALL) else "Error."
                        
                        st.session_state.assigned_dept = dept
                        st.session_state.urgency_score = urgency
                        st.session_state.cached_petition = petition
                        st.session_state.stipulated_time = time_r
                        st.session_state.is_emergency = emergency
                        st.session_state.impact_score = impact
                        st.session_state.success_prediction = prediction
                        st.session_state.hero_points += 50
                        st.session_state.xp_trigger = True
                        
                        st.write("📝 Drafting Legal Document...")
                        time.sleep(0.5)
                        status.update(label="✅ Analysis Complete", state="complete")
                        
                        st.session_state.chat_history.append({"role": "ai", "content": speech})
                        st.session_state.speech_text = speech
                        st.session_state.speech_id = str(uuid.uuid4())
                        
                        if emergency: st.session_state.stage = 'emergency_alert'
                        else: st.session_state.stage = 'analysis_done'
                        st.rerun()
                        
                    except Exception as e:
                        status.update(label=f"❌ Error: {e}", state="error")

        # STAGE 2: ANALYSIS DONE
        elif current_stage == 'analysis_done':
            st.markdown("#### 📜 Legal Petition")
            st.text_area("Draft", value=st.session_state.get('cached_petition', ''), height=300, key='petition_view')
            
            st.markdown(f"**Evidence Hash:** `{st.session_state.get('current_hash', 'N/A')[:30]}...`")
            st.markdown("---")

            deadline = calculate_deadline(st.session_state.get('stipulated_time', '2 days'))
            
            t_col1, t_col2, t_col3 = st.columns([1, 2, 1])
            with t_col2:
                st.markdown(f"""
                <div class="timeline-card">
                    <div style="color:#aaa; font-size:12px;">PREDICTED RESOLUTION</div>
                    <div class="timeline-month">{deadline.strftime("%B %Y").upper()}</div>
                    <div class="timeline-date">{deadline.day}</div>
                    <div style="color:#00FFAA; font-size:11px;">By {deadline.strftime("%I:%M %p")}</div>
                </div>
                """, unsafe_allow_html=True)

            if st.button("📅 Add to My Google Calendar", key="add_cal"):
                with st.spinner("Connecting to Google Calendar..."):
                    summary = f"Vigil: {st.session_state.assigned_dept} Issue Resolution"
                    description = f"Issue reported at {st.session_state.u_data['loc']}.\n\nPetition Details:\n{st.session_state.cached_petition[:200]}..."
                    event_link = add_to_google_calendar(summary, description, deadline)
                    
                    if event_link:
                        st.success("✅ Event added to your Google Calendar!")
                        st.markdown(f"[View Event in Calendar]({event_link})")
                        st.session_state.chat_history.append({"role": "ai", "content": f"I have marked the deadline on your Google Calendar."})
                        st.session_state.speech_text = "I have marked the deadline on your calendar."
                        st.session_state.speech_id = str(uuid.uuid4())
                        st.rerun()

            st.markdown("---")
            
            should_draft = st.session_state.pop('trigger_draft', False)
            
            c1, c2 = st.columns(2)
            with c1:
                if should_draft or st.button("📝 Create Gmail Draft", type="primary"):
                    email_template = DEPT_EMAILS.get(st.session_state.assigned_dept, DEPT_EMAILS["General/Municipal"])
                    target = email_template.format(dist=st.session_state.u_data['dist'].lower())
                    create_gmail_draft(st.session_state.cached_petition, f"Civic Report: {st.session_state.u_data['loc']}", target)
                    
                    save_report(st.session_state.u_data['name'], st.session_state.u_data['loc'], 
                               st.session_state.assigned_dept, st.session_state.urgency_score, 
                               st.session_state.cached_petition, st.session_state.current_hash,
                               st.session_state.user_sentiment, st.session_state.success_prediction)
                    
                    resp = f"Draft prepared for {target}. Please verify and send."
                    st.session_state.chat_history.append({"role": "ai", "content": resp})
                    st.session_state.speech_text = "Draft prepared. Please verify."
                    st.session_state.speech_id = str(uuid.uuid4())
                    st.session_state.stage = 'awaiting_resolution'
                    st.rerun()
            
            with c2:
                pdf_data = create_pdf_report(st.session_state.cached_petition, st.session_state.u_data, 
                                            st.session_state.urgency_score, st.session_state.assigned_dept, 
                                            st.session_state.stipulated_time, st.session_state.current_hash)
                st.download_button("📥 Download PDF", data=pdf_data, file_name="Vigil_Report.pdf")

        # STAGE 3: EMERGENCY
        elif current_stage == 'emergency_alert':
            st.error("⚠️ **EMERGENCY DETECTED** ⚠️")
            st.warning("Immediate danger identified. Auto-escalating...")
            
            deadline = calculate_deadline("1 hour")
            st.markdown(f"""
            <div class="timeline-card" style="border-color: #FF0000;">
                <div class="timeline-month" style="color: #FFaaAA;">IMMEDIATE ACTION</div>
                <div class="timeline-date" style="color: #FF6666;">NOW</div>
                <div style="color:#aaa; font-size:12px; margin-top:10px;">
                    🚨 Authorities Notified<br>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📜 Emergency Petition")
            st.text_area("Draft", value=st.session_state.get('cached_petition', ''), height=300, key='emer_view')
            
            if st.button("🚨 ESCALATE NOW"):
                target = DEPT_EMAILS["Emergency"]
                create_gmail_draft(st.session_state.cached_petition, "URGENT: HAZARD", target)
                save_report(st.session_state.u_data['name'], st.session_state.u_data['loc'], 
                           "Emergency", 10, st.session_state.cached_petition, st.session_state.current_hash)
                
                st.session_state.chat_history.append({"role": "ai", "content": "Emergency services notified. Stay safe."})
                st.session_state.speech_text = "Emergency services notified."
                st.session_state.speech_id = str(uuid.uuid4())
                st.session_state.stage = 'awaiting_escalation_result'
                st.rerun()

        # STAGE 4: RESOLUTION
        elif current_stage == 'awaiting_resolution':
            st.success("Report Submitted.")
            st.markdown("#### Is the issue resolved?")
            
            is_resolved = st.session_state.pop('trigger_resolved', False)
            is_pending = st.session_state.pop('trigger_pending', False)
            
            c1, c2 = st.columns(2)
            with c1:
                if is_resolved or st.button("✅ Yes, Resolved"):
                    st.session_state.chat_history.append({"role": "user", "content": "Yes, resolved."})
                    st.session_state.chat_history.append({"role": "ai", "content": "Excellent work! +100 VP. Would you like to rate the municipality's response?"})
                    st.session_state.hero_points += 100
                    st.session_state.speech_text = "Excellent work! Would you like to rate the response?"
                    st.session_state.speech_id = str(uuid.uuid4())
                    st.session_state.xp_trigger = True 
                    st.session_state.stage = 'post_resolution_feedback'
                    st.rerun()
            
            with c2:
                if is_pending or st.button("❌ No, Still Pending"):
                    st.session_state.chat_history.append({"role": "user", "content": "No, still pending."})
                    st.session_state.chat_history.append({"role": "ai", "content": "I understand. I am escalating this to higher authorities."})
                    st.session_state.speech_text = "I understand. I am escalating this."
                    st.session_state.speech_id = str(uuid.uuid4())
                    st.session_state.stage = 'escalation'
                    st.session_state.escalation_level = 1
                    st.rerun()

        elif current_stage == 'post_resolution_feedback':
            st.markdown("#### 📝 Rate Your Experience")
            st.markdown("Help us improve the system by rating the response quality.")
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                if st.button("⭐ Excellent Response"):
                    st.session_state.chat_history.append({"role": "user", "content": "Rated Excellent."})
                    st.session_state.chat_history.append({"role": "ai", "content": "Thank you for your feedback! Ready for the next mission?"})
                    st.session_state.speech_text = "Thank you for your feedback."
                    st.session_state.speech_id = str(uuid.uuid4())
                    st.session_state.stage = 'greeting'
                    st.session_state.urgency_score = 0
                    st.session_state.escalation_level = 0
                    st.rerun()
            
            with col_f2:
                if st.button("😞 Slow Response"):
                    st.session_state.chat_history.append({"role": "user", "content": "Rated Slow."})
                    st.session_state.chat_history.append({"role": "ai", "content": "I have noted the delay. Do you have another issue?"})
                    st.session_state.speech_text = "I have noted the delay."
                    st.session_state.speech_id = str(uuid.uuid4())
                    st.session_state.stage = 'greeting'
                    st.session_state.urgency_score = 0
                    st.session_state.escalation_level = 0
                    st.rerun()

        elif current_stage == 'escalation':
            st.warning("⚙️ Escalating to District Collector...")
            escalated_text = st.session_state.cached_petition + "\n\n**[SYSTEM NOTE: AUTO-ESCALATED DUE TO NON-RESOLUTION]**"
            
            st.markdown("#### 📜 Escalated Draft")
            st.text_area("Escalated Content", value=escalated_text, height=300, key='esc_view')
            
            if st.button("📩 Confirm Escalation", type="primary"):
                target = DEPT_EMAILS["Escalation"].format(dist=st.session_state.u_data['dist'].lower())
                create_gmail_draft(escalated_text, "ESCALATED: Issue", target)
                st.session_state.chat_history.append({"role": "ai", "content": f"Escalated to District Collector. Reference ID #{int(time.time())}."})
                st.session_state.speech_text = "The issue has been escalated."
                st.session_state.speech_id = str(uuid.uuid4())
                st.session_state.stage = 'awaiting_escalation_result'
                st.rerun()

        elif current_stage == 'awaiting_escalation_result':
            st.info("Issue Escalated. Waiting for action...")
            st.markdown("#### Resolved after escalation?")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Yes, Resolved Now"):
                    st.session_state.chat_history.append({"role": "user", "content": "Resolved now."})
                    st.session_state.chat_history.append({"role": "ai", "content": "Justice served! +200 VP. Would you like to provide feedback?"})
                    st.session_state.hero_points += 200
                    st.session_state.speech_text = "Justice served."
                    st.session_state.speech_id = str(uuid.uuid4())
                    st.session_state.xp_trigger = True
                    st.session_state.stage = 'post_resolution_feedback'
                    st.session_state.urgency_score = 0
                    st.rerun()
            
            with c2:
                if st.button("❌ No, Still Ignored"):
                    st.session_state.chat_history.append({"role": "user", "content": "Still ignored."})
                    st.session_state.chat_history.append({"role": "ai", "content": "I am drafting the RTI application now."})
                    st.session_state.speech_text = "I am drafting the RTI application now."
                    st.session_state.speech_id = str(uuid.uuid4())
                    st.session_state.stage = 'rti_draft'
                    st.rerun()

        elif current_stage == 'rti_draft':
            st.warning("📝 Drafting Right to Information Application")
            st.markdown("#### 📜 RTI Application Draft")
            
            rti_text = f"""
            **RTI Application under Section 6(1) of the RTI Act, 2005**
            
            To: The Public Information Officer (PIO)
            Department: {st.session_state.assigned_dept}
            District: {st.session_state.u_data['dist']}
            
            Subject: Information regarding unresolved civic issue at {st.session_state.u_data['loc']}.
            
            Sir/Madam,
            
            I, {st.session_state.u_data['name']}, resident of {st.session_state.u_data['loc']}, seek the following information:
            
            1. What is the current status of the complaint regarding the issue reported on {time.strftime('%Y-%m-%d')}?
            2. What are the reasons for the delay in resolving the aforementioned issue?
            3. What action has been taken against the officials responsible for the negligence?
            
            I am depositing the prescribed fee of Rs. 10/- via IPO/DD/Cash.
            
            Yours faithfully,
            {st.session_state.u_data['name']}
            Mob: {st.session_state.u_data['phone']}
            """
            
            st.text_area("RTI Draft Content", value=rti_text, height=300, key='rti_view')
            
            if st.button("📩 Create RTI Draft", type="primary"):
                st.session_state.chat_history.append({"role": "ai", "content": "RTI Draft prepared. Do you need help finding the PIO address?"})
                st.session_state.speech_text = "RTI Draft prepared. What is your next step?"
                st.session_state.speech_id = str(uuid.uuid4())
                st.session_state.stage = 'rti_followup'
                st.rerun()

        elif current_stage == 'rti_followup':
            st.info("RTI Application Ready.")
            st.markdown("#### Next Steps")
            st.write("You can now submit this application to the Public Information Officer.")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("📍 Find PIO Address"):
                    st.session_state.chat_history.append({"role": "user", "content": "Find PIO Address."})
                    st.session_state.chat_history.append({"role": "ai", "content": f"The PIO for {st.session_state.assigned_dept} in {st.session_state.u_data['dist']} is usually located at the District Collector Office."})
                    st.session_state.speech_text = "I recommend visiting the district website."
                    st.session_state.speech_id = str(uuid.uuid4())
                    st.rerun()
            with c2:
                if st.button("✅ Issue Resolved (End Process)"):
                    st.session_state.chat_history.append({"role": "user", "content": "Issue Resolved."})
                    st.session_state.chat_history.append({"role": "ai", "content": "Glad we could resolve this together! +300 VP. Ready for the next mission?"})
                    st.session_state.hero_points += 300
                    st.session_state.speech_text = "Glad we could resolve this together!"
                    st.session_state.speech_id = str(uuid.uuid4())
                    st.session_state.xp_trigger = True
                    st.session_state.stage = 'greeting'
                    st.session_state.urgency_score = 0
                    st.session_state.escalation_level = 0
                    st.rerun()
            
            st.divider()
            st.warning("⚠️ Is the issue still unresolved after RTI?")
            if st.button("⚖️ Take Legal Action / Lokayukta"):
                st.session_state.escalation_level += 1
                st.session_state.chat_history.append({"role": "user", "content": "Issue still not resolved."})
                st.session_state.chat_history.append({"role": "ai", "content": "Understood. Initiating Protocol Omega: Contacting Lokayukta and preparing legal documents."})
                st.session_state.speech_text = "Understood. Initiating Protocol Omega: Contacting Lokayukta."
                st.session_state.speech_id = str(uuid.uuid4())
                st.session_state.cached_petition += "\n\n**LEGAL NOTICE: Initiation of Lokayukta Inquiry**"
                st.session_state.stage = 'escalation'
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.xp_trigger:
        sound_html = "<audio autoplay src='data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2teleVmYyNrLhEE8i9bKm4NVO4fSxpuDVTuH0sabg1U7h9LGm4NVO4fSxpuDVTuH0sabg1U='></audio>"
        components.html(sound_html, height=0)
        st.markdown("<div class='xp-medal'>🎖️</div>", unsafe_allow_html=True)
        time.sleep(1.5)
        st.session_state.xp_trigger = False
        st.rerun()

    if st.session_state.get('speech_text') and st.session_state.get('speech_id') != st.session_state.get('last_speech_id'):
        speak_now(st.session_state.speech_text, speech_id=st.session_state.get('speech_id'))