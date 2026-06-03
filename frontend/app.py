import os
import streamlit as st
import requests
import time
import urllib.parse
import base64
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Import the cloud-friendly browser microphone
try:
    from streamlit_mic_recorder import speech_to_text
except ImportError:
    speech_to_text = None

# Import the cookie controller for persistent logins
try:
    from streamlit_cookies_controller import CookieController
    cookie_controller = CookieController()
except ImportError:
    cookie_controller = None
    st.warning("Please run: pip install streamlit-cookies-controller")

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="IT Helpdesk Portal",
    page_icon="💼",    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# MASTER CSS 
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family:'Inter',system-ui,sans-serif !important; }
.stApp { background:#F0F4F8; }

/* ── Sidebar Styling ── */
section[data-testid="stSidebar"] { 
    background: #1B3358 !important; 
    min-width: 250px !important; 
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}
div[data-testid="collapsedControl"] button, div[data-testid="collapsedControl"] svg {
    color: #1B3358 !important; fill: #1B3358 !important;
}
button[data-testid="stSidebarCollapseButton"], button[data-testid="stSidebarCollapseButton"] svg {
    color: #ffffff !important; fill: #ffffff !important;
}
button[data-testid="stSidebarCollapseButton"]:hover { background: rgba(255, 255, 255, 0.1) !important; }

/* ── File Uploader ── */
div[data-testid="stFileUploadDropzone"] {
    background-color: #1B3358 !important; border: 2px dashed #94A3B8 !important; border-radius: 8px !important;
}
div[data-testid="stFileUploadDropzone"] * { color: #ffffff !important; fill: #ffffff !important; }
div[data-testid="stFileUploader"] ul, div[data-testid="stFileUploader"] li, div[data-testid="stFileUploader"] li * { color: #1A202C !important; }
div[data-testid="stSpinner"] * { color: #1B3358 !important; font-weight: 600 !important; }

/* ── Sidebar Typography ── */
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] label { color:#E2E8F0 !important; }
section[data-testid="stSidebar"] .stButton>button {
    background:transparent !important; color:#CBD5E1 !important; border:none !important; border-radius:7px !important;
    font-size:.875rem !important; font-weight:500 !important; text-align:left !important; padding:9px 12px !important;
    width:100% !important; box-shadow:none !important; transition:background .15s !important;
}
section[data-testid="stSidebar"] .stButton>button:hover { background:rgba(255,255,255,.13) !important; color:#fff !important; }

/* ── Main Buttons ── */
div[data-testid="stButton"] button, div[data-testid="stFormSubmitButton"] button, div[data-testid="stDownloadButton"] button {
    background-color: #1B3358 !important; border: none !important; border-radius: 7px !important; 
    padding: 10px 18px !important; box-shadow: 0 1px 3px rgba(0,0,0,.15) !important; transition: background 0.2s !important;
}
div[data-testid="stButton"] button *, div[data-testid="stFormSubmitButton"] button *, div[data-testid="stDownloadButton"] button * {
    color: #ffffff !important; font-weight: 600 !important; font-size: 0.875rem !important;
}
div[data-testid="stButton"] button:hover, div[data-testid="stFormSubmitButton"] button:hover, div[data-testid="stDownloadButton"] button:hover { background-color: #274472 !important; }

/* ── Inputs & Selectboxes ── */
.stTextInput>div>input, .stTextArea>div>textarea {
    background:#fff !important; border:1.5px solid #CBD5E1 !important; color:#1A202C !important; border-radius:7px !important;
    font-size:.9rem !important; padding:9px 12px !important; -webkit-text-fill-color: #1A202C !important;
}
.stTextInput>div>input::placeholder,.stTextArea>div>textarea::placeholder { color:#94A3B8 !important; -webkit-text-fill-color: #94A3B8 !important; }
.stTextInput>div>input:focus,.stTextArea>div>textarea:focus { border-color:#1B3358 !important; box-shadow:0 0 0 3px rgba(27,51,88,.1) !important; }

.stSelectbox>div>div { background:#fff !important; border:1.5px solid #CBD5E1 !important; border-radius:7px !important; }
.stSelectbox>div>div *, div[data-baseweb="select"] * { color:#1A202C !important; }
div[data-baseweb="popover"] li,div[data-baseweb="menu"] li { color:#1A202C !important; background:#fff !important; }
div[data-baseweb="popover"] li:hover { background:#EFF6FF !important; }

/* ── Labels & Checkboxes ── */
label, label p { color: #1A202C !important; font-size: 0.875rem !important; font-weight: 600 !important; }
div[data-testid="stCheckbox"] label p, div[data-testid="stCheckbox"] label span { color: #1A202C !important; }

/* ── Tabs & Expanders ── */
.stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:2px solid #E2E8F0; }
.stTabs [data-baseweb="tab"] { color:#64748B !important; font-weight:500 !important; font-size:.9rem !important; padding:8px 16px !important; }
.stTabs [aria-selected="true"] { color:#1B3358 !important; font-weight:600 !important; border-bottom:2px solid #1B3358 !important; background:#EFF6FF !important; }

.streamlit-expanderHeader, .streamlit-expanderHeader p, div[data-testid="stExpander"] summary, div[data-testid="stExpander"] summary span, div[data-testid="stExpander"] summary p {
    color: #1B3358 !important; font-weight: 700 !important; font-size: 0.98rem !important; opacity: 1 !important;
}
.streamlit-expanderHeader:hover, div[data-testid="stExpander"] summary:hover { background: rgba(27, 51, 88, 0.05) !important; border-radius: 6px !important; }
.streamlit-expanderContent { background: transparent !important; border: none !important; color: #1A202C !important; }
div[data-testid="stExpander"] { background: transparent !important; border: none !important; box-shadow: none !important; margin-top: 2px !important; }

/* ── Utilities ── */
div[data-testid="stForm"] { background:transparent !important; border:none !important; }
div[data-testid="stAlert"] p, div[data-testid="metric-container"] label, div[data-testid="metric-container"] div { color:#1A202C !important; }
.stDataFrame { background:#fff !important; color:#1A202C !important; }
.stDataFrame td,.stDataFrame th { color:#1A202C !important; }

.page-title { font-size:1.55rem; font-weight:700; color:#1B3358; margin:0 0 4px; }
.page-sub   { font-size:.875rem; color:#64748B; margin:0 0 20px; }
.sec-hdr    { font-size:.95rem; font-weight:600; color:#1B3358; border-bottom:2px solid #DBEAFE; padding-bottom:7px; margin-bottom:14px; }
.kpi { background:#fff; border:1px solid #E2E8F0; border-radius:10px; padding:18px 20px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,.05); }
.kpi-n { font-size:2rem; font-weight:700; line-height:1.2; }
.kpi-l { font-size:.72rem; font-weight:600; color:#64748B; text-transform:uppercase; letter-spacing:.07em; margin-top:4px; }

.bubble-user { background:#1B3358; color:#fff; border-radius:16px 16px 4px 16px; padding:11px 16px; margin:8px 0; max-width:78%; margin-left:auto; font-size:.9rem; line-height:1.55; word-wrap:break-word; }
.bubble-ai { background:#fff; border:1px solid #DBEAFE; color:#1A202C; border-radius:16px 16px 16px 4px; padding:12px 16px; margin:8px 0; max-width:84%; font-size:.9rem; line-height:1.6; box-shadow:0 1px 4px rgba(0,0,0,.06); word-wrap:break-word; }

.ticket-container-box { border-radius: 12px !important; padding: 16px 20px !important; margin-bottom: 16px !important; box-shadow: 0 4px 12px rgba(0,0,0,.06) !important; border-left: 6px solid #1B3358 !important; }
.ticket-container-box.cr { border-left-color:#DC2626 !important; background:linear-gradient(to right,#FFF5F5 0%, #ffffff 100%) !important; }
.ticket-container-box.hi { border-left-color:#EA580C !important; background:linear-gradient(to right,#FFF8F5 0%, #ffffff 100%) !important; }
.ticket-container-box.me { border-left-color:#D97706 !important; background:linear-gradient(to right,#FFFDF0 0%, #ffffff 100%) !important; }
.ticket-container-box.lo { border-left-color:#16A34A !important; background:linear-gradient(to right,#F0FDF4 0%, #ffffff 100%) !important; }
.ticket-container-box.cl { border-left-color:#94A3B8 !important; background:linear-gradient(to right,#F8FAFC 0%, #ffffff 100%) !important; opacity:.8 !important; }

.asset-card { background:#fff; border-radius:10px; padding:14px 18px; margin-bottom:8px; box-shadow:0 2px 8px rgba(0,0,0,.06); border-left:5px solid #1B3358; }
.asset-available { border-left-color:#16A34A; background:linear-gradient(to right,#F0FDF4,#fff); }
.asset-assigned  { border-left-color:#1D4ED8; background:linear-gradient(to right,#EFF6FF,#fff); }
.asset-repair    { border-left-color:#D97706; background:linear-gradient(to right,#FFFDF0,#fff); }
.asset-retired   { border-left-color:#94A3B8; background:linear-gradient(to right,#F8FAFC,#fff); opacity:.8; }

.bd { padding:3px 10px; border-radius:5px; font-size:.72rem; font-weight:700; display:inline-block; letter-spacing:.02em; }
.bd-cr{background:#FEE2E2;color:#B91C1C;} .bd-hi{background:#FFEDD5;color:#C2410C;} .bd-me{background:#FEF3C7;color:#92400E;} .bd-lo{background:#DCFCE7;color:#15803D;}
.bd-op{background:#DBEAFE;color:#1D4ED8;} .bd-pr{background:#EDE9FE;color:#6D28D9;} .bd-rs{background:#DCFCE7;color:#15803D;} .bd-cl{background:#F1F5F9;color:#475569;}

.vbox { background:#fff; border:2px dashed #CBD5E1; border-radius:14px; padding:32px 20px; text-align:center; }
.pcard { background:#FFFBEB; border:1px solid #FCD34D; border-radius:8px; padding:14px 16px; margin-bottom:10px; }
.ucard { background:#fff; border:1px solid #E2E8F0; border-radius:8px; padding:12px 16px; margin-bottom:7px; }
.fix-box { background:#F0F9FF; border:1px solid #BAE6FD; border-radius:8px; padding:13px 16px; margin-top:10px; color:#1A202C; }
.doc-row { background:#fff; border:1px solid #E2E8F0; border-radius:8px; padding:10px 16px; margin-bottom:6px; display:flex; align-items:center; gap:12px; color:#1A202C; }

@keyframes fadeInUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn   { from{opacity:0} to{opacity:1} }
@keyframes slideLeft{ from{opacity:0;transform:translateX(40px)} to{opacity:1;transform:translateX(0)} }
.anim-fadeinup { animation:fadeInUp .6s ease forwards; }

@keyframes imgCycle { 0%, 28% { opacity:1; visibility: visible; } 33%, 95% { opacity:0; visibility: hidden; } 100% { opacity:1; visibility: visible; } }
.hero-container { position:relative; width:100%; height:82vh; border-radius:20px; overflow:hidden; box-shadow:0 20px 60px rgba(27,51,88,.25); }
.hero-img-slide { position:absolute; top:0; left:0; width:100%; height:100%; border-radius:20px; overflow:hidden; }
.hero-bg-img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 1; }
.hero-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; }
.hero-content { position: relative; z-index: 3; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; height: 100%; padding: 40px; }
.hero-img-slide:nth-child(1){ animation:imgCycle 9s infinite 0s; }
.hero-img-slide:nth-child(2){ animation:imgCycle 9s infinite 3s; }
.hero-img-slide:nth-child(3){ animation:imgCycle 9s infinite 6s; }
</style>
""", unsafe_allow_html=True)

# ── Session state & Cookie Hydration ──────────────────────────────────────────
for k,v in {
    "authenticated":False,"token":"","user_name":"",
    "user_role":"","user_email":"","user_id":0,
    "chat_history":[],"page":"Dashboard",
    "chat_key":0,"voice_key":0,"welcomed":False,
    "speaker_enabled": True, 
    "voice_chat": [],
    "speak_now": "" 
}.items():
    if k not in st.session_state:
        st.session_state[k]=v

# Check for persistent cookies to keep user logged in on reload
if cookie_controller and not st.session_state.authenticated:
    saved_auth = cookie_controller.get('hd_auth')
    if saved_auth:
        st.session_state.authenticated = True
        st.session_state.token = cookie_controller.get('hd_token')
        st.session_state.user_name = cookie_controller.get('hd_name')
        st.session_state.user_role = cookie_controller.get('hd_role')
        st.session_state.user_email = cookie_controller.get('hd_email')
        st.session_state.user_id = cookie_controller.get('hd_id')

# ── API Helpers ────────────────────────────────────────────────────────────────
def _h(j=True):
    h={"Authorization":f"Bearer {st.session_state.token}"}
    if j: h["Content-Type"]="application/json"
    return h

def api_get(ep):
    try:
        r=requests.get(f"{API_URL}{ep}",headers=_h(False),timeout=30)
        return r.json() if r.status_code==200 else {}
    except: return {}

def api_post(ep,data=None,files=None):
    try:
        if files: r=requests.post(f"{API_URL}{ep}",files=files,headers=_h(False),timeout=90)
        else: r=requests.post(f"{API_URL}{ep}",json=data,headers=_h(),timeout=90)
        return r.json(),r.status_code
    except Exception as e: return {"error":str(e)},500

def api_put(ep,data=None):
    try:
        r=requests.put(f"{API_URL}{ep}",json=data,headers=_h(),timeout=30)
        return r.json(),r.status_code
    except Exception as e: return {"error":str(e)},500

def api_delete(ep):
    try:
        r=requests.delete(f"{API_URL}{ep}",headers=_h(False),timeout=30)
        return r.json(),r.status_code
    except Exception as e: return {"error":str(e)},500

# ══════════════════════════════════════════════════════════════════════════════
# WELCOME ANIMATION
# ══════════════════════════════════════════════════════════════════════════════
def show_welcome():
    if st.session_state.welcomed: return
    placeholder = st.empty()
    placeholder.markdown("""
    <div style='position:fixed;top:0;left:0;width:100%;height:100%;background:#1B3358;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;animation:fadeIn .3s ease'>
        <div style='text-align:center;animation:fadeInUp .8s ease .2s both'>
            <div style='font-size:4rem;margin-bottom:16px'>💼</div>
            <h1 style='color:#fff;font-size:2.4rem;font-weight:800;margin:0;letter-spacing:-.02em'>IT Helpdesk Portal</h1>
            <p style='color:#93C5FD;font-size:1.1rem;margin:12px 0 0'>Enterprise AI Support Platform</p>
            <div style='margin-top:32px;display:flex;gap:8px;justify-content:center'>
                <div style='width:8px;height:8px;background:#60A5FA;border-radius:50%; animation:pulse 1s infinite 0s'></div>
                <div style='width:8px;height:8px;background:#60A5FA;border-radius:50%; animation:pulse 1s infinite .3s'></div>
                <div style='width:8px;height:8px;background:#60A5FA;border-radius:50%; animation:pulse 1s infinite .6s'></div>
            </div>
        </div>
    </div>
    <style>@keyframes pulse{0%,100%{opacity:.3;transform:scale(.8)}50%{opacity:1;transform:scale(1.2)}}</style>
    """, unsafe_allow_html=True)
    time.sleep(2.5)
    placeholder.empty()
    st.session_state.welcomed = True

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def show_login():
    show_welcome()
    left, right = st.columns([1, 1], gap="medium")

    with left:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='max-width:420px;margin:0 auto;padding:0 24px;animation:fadeInUp .6s ease'>
            <div style='margin-bottom:28px'>
                <div style='width:52px;height:52px;background:#1B3358;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.6rem;margin-bottom:16px;box-shadow:0 4px 14px rgba(27,51,88,.35)'>💼</div>
                <h2 style='color:#1B3358;font-size:1.75rem;font-weight:800;margin:0;letter-spacing:-.02em'>Welcome back</h2>
                <p style='color:#64748B;font-size:.9rem;margin-top:6px'>Sign in to your IT Helpdesk account</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In", "Register"])
        with tab1:
            with st.form("lf", clear_on_submit=False):
                email = st.text_input("Email address", placeholder="you@company.com")
                password = st.text_input("Password", placeholder="Your password", type="password")
                sub = st.form_submit_button("Sign In", use_container_width=True)

            if sub:
                if not email.strip() or not password.strip(): st.error("Please enter your email and password.")
                else:
                    with st.spinner("Signing in..."):
                        try:
                            r = requests.post(f"{API_URL}/auth/login", json={"username": email.strip(), "password": password}, timeout=15)
                            if r.status_code == 200:
                                d = r.json()
                                st.session_state.update({"authenticated": True, "token": d["access_token"], "user_name": d["user_name"], "user_role": d["user_role"], "user_email": d["user_email"], "user_id": d["user_id"]})
                                
                                # Set cookies so session survives a page reload
                                if cookie_controller:
                                    cookie_controller.set('hd_auth', 'true')
                                    cookie_controller.set('hd_token', d["access_token"])
                                    cookie_controller.set('hd_name', d["user_name"])
                                    cookie_controller.set('hd_role', d["user_role"])
                                    cookie_controller.set('hd_email', d["user_email"])
                                    cookie_controller.set('hd_id', d["user_id"])
                                    
                                st.rerun()
                            elif r.status_code == 403:
                                st.warning("Your account is awaiting administrator approval." if "pending" in r.json().get("detail","").lower() else f"Access denied: {r.json().get('detail','')}")
                            else:
                                st.error("Incorrect email or password.")
                        except requests.exceptions.ConnectionError: st.error("Cannot reach the server. Ensure the backend is running.")

        with tab2:
            with st.form("rf", clear_on_submit=True):
                rn = st.text_input("Full Name", placeholder="e.g. Sai Desai")
                re = st.text_input("Email", placeholder="sai@company.com")
                rd = st.text_input("Department", value="General")
                rp = st.text_input("Password", type="password")
                rr = st.selectbox("Role", ["employee","it_engineer"])
                rs = st.form_submit_button("Submit Registration", use_container_width=True)
            if rs:
                if not rn or not re or not rp: st.error("Please fill in all fields.")
                else:
                    d,c = api_post("/auth/register",{"name":rn,"email":re,"password":rp,"department":rd,"role":rr})
                    if c==200: st.success("Registration submitted. An admin will approve your account.")
                    else: st.error(d.get("detail","Registration failed."))

        st.markdown("<div style='max-width:420px;margin:24px auto 0;padding:0 24px;text-align:center;color:#94A3B8;font-size:.78rem'>Powered by Groq AI &bull; Enterprise IT Support</div>", unsafe_allow_html=True)

    with right:
        st.markdown("""
<div style="height:100vh; position:sticky; top:0; padding:24px; display:flex; align-items:center; justify-content:center; animation:slideLeft .7s ease">
    <div class="hero-container">
        <div class="hero-img-slide">
            <img class="hero-bg-img" src="https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=800&q=80" />
            <div class="hero-overlay" style="background: linear-gradient(135deg, rgba(27,51,88,0.9) 0%, rgba(37,99,235,0.85) 100%);"></div>
            <div class="hero-content">
                <div style="font-size:4.5rem;margin-bottom:15px">🖥️</div>
                <h2 style="color:#fff;font-size:1.8rem;font-weight:700;margin:0">AI-Powered IT Support</h2>
                <p style="color:#BAE6FD;font-size:1rem;margin-top:10px;max-width:320px">Get instant help for any IT issue — VPN, software, hardware and more</p>
            </div>
        </div>
        <div class="hero-img-slide">
            <img class="hero-bg-img" src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80" />
            <div class="hero-overlay" style="background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,58,95,0.85) 100%);"></div>
            <div class="hero-content">
                <div style="font-size:4.5rem;margin-bottom:15px">📊</div>
                <h2 style="color:#fff;font-size:1.8rem;font-weight:700;margin:0">Real-Time Analytics</h2>
                <p style="color:#A7F3D0;font-size:1rem;margin-top:10px;max-width:320px">Track ticket trends, monitor SLAs and make data-driven IT decisions</p>
            </div>
        </div>
        <div class="hero-img-slide">
            <img class="hero-bg-img" src="https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80" />
            <div class="hero-overlay" style="background: linear-gradient(135deg, rgba(30,27,75,0.9) 0%, rgba(67,56,202,0.85) 100%);"></div>
            <div class="hero-content">
                <div style="font-size:4.5rem;margin-bottom:15px">🔒</div>
                <h2 style="color:#fff;font-size:1.8rem;font-weight:700;margin:0">Secure &amp; Role-Based</h2>
                <p style="color:#DDD6FE;font-size:1rem;margin-top:10px;max-width:320px">3-tier access control — Admin, IT Engineer and Employee workflows</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def show_sidebar():
    role = st.session_state.user_role
    rl   = {"admin":"Administrator","it_engineer":"IT Engineer","employee":"Employee"}.get(role,role)
    rc   = {"admin":"#EF4444","it_engineer":"#F59E0B","employee":"#22C55E"}.get(role,"#94A3B8")

    with st.sidebar:
        st.markdown(f"""
        <div style='padding:18px 14px 12px'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:16px'>
                <div style='width:34px;height:34px;background:rgba(255,255,255,.18);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.1rem'>💼</div>
                <div><p style='color:#fff;font-weight:700;font-size:.9rem;margin:0'>IT Helpdesk</p><p style='color:#94A3B8;font-size:.68rem;margin:0'>Support Portal</p></div>
            </div>
            <div style='background:rgba(255,255,255,.09);border-radius:8px;padding:10px 12px'>
                <p style='color:#94A3B8;font-size:.67rem;margin:0;text-transform:uppercase;letter-spacing:.06em'>Signed in as</p>
                <p style='color:#fff;font-weight:600;font-size:.875rem;margin:3px 0;word-break:break-word'>{st.session_state.user_name}</p>
                <span style='background:{rc}30;color:{rc};padding:2px 8px;border-radius:4px;font-size:.68rem;font-weight:600'>{rl}</span>
            </div>
        </div>
        <div style='border-top:1px solid rgba(255,255,255,.1);margin:0 0 8px'></div>
        """, unsafe_allow_html=True)

        nav = [("Dashboard","Dashboard"),("AI Chat","AI Chat"),("Voice Assistant","Voice Assistant"),
               ("Tickets","Tickets"),("Screenshot Analyzer","Screenshot Analyzer"),
               ("Knowledge Base","Knowledge Base"), ("Change Password", "Change Password")]

        if role in ["admin","it_engineer"]: nav += [("Asset Manager","Assets"),("Analytics","Analytics")]
        if role=="admin": nav += [("User Management","User Management")]

        st.markdown("<p style='color:#64748B;font-size:.67rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;padding:2px 12px;margin:0'>Menu</p>", unsafe_allow_html=True)

        for label,key in nav:
            if st.session_state.page==key:
                st.markdown(f"<div style='background:rgba(255,255,255,.18);border-radius:7px;padding:9px 12px;margin:2px 0'><span style='color:#fff;font-weight:600;font-size:.875rem'>{label}</span></div>", unsafe_allow_html=True)
            else:
                if st.button(label,key=f"nav_{key}",use_container_width=True): st.session_state.page=key; st.rerun()

        st.markdown("<div style='border-top:1px solid rgba(255,255,255,.1);margin:8px 0'></div>", unsafe_allow_html=True)
        if st.button("Sign Out",key="signout",use_container_width=True):
            if cookie_controller:
                cookie_controller.remove('hd_auth')
                cookie_controller.remove('hd_token')
                cookie_controller.remove('hd_name')
                cookie_controller.remove('hd_role')
                cookie_controller.remove('hd_email')
                cookie_controller.remove('hd_id')
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def show_dashboard():
    role=st.session_state.user_role
    st.markdown(f"<p class='page-title'>Dashboard</p><p class='page-sub'>Good day, {st.session_state.user_name}. Here is your overview.</p>", unsafe_allow_html=True)

    stats=api_get("/tickets/stats/summary")
    c1,c2,c3,c4=st.columns(4)
    for col,val,lbl,cl in [(c1,stats.get("total",0),"Total Tickets","#1B3358"), (c2,stats.get("open",0),"Open","#D97706"), (c3,stats.get("resolved",0),"Resolved","#16A34A"), (c4,stats.get("critical",0),"Critical","#DC2626")]:
        with col: st.markdown(f"<div class='kpi'><div class='kpi-n' style='color:{cl}'>{val}</div><div class='kpi-l'>{lbl}</div></div>",unsafe_allow_html=True)

    if role=="admin":
        p=api_get("/auth/pending")
        if p: st.markdown("<br>",unsafe_allow_html=True); st.warning(f"{len(p)} new registration(s) awaiting approval — go to User Management.")

    st.markdown("<br>",unsafe_allow_html=True)
    ca,cb=st.columns(2)
    with ca:
        st.markdown("<p class='sec-hdr'>Priority Breakdown</p>",unsafe_allow_html=True)
        prios=stats.get("priorities",{})
        if prios:
            import plotly.graph_objects as go
            clr={"Critical":"#DC2626","High":"#EA580C","Medium":"#D97706","Low":"#16A34A"}
            fig=go.Figure(data=[go.Pie(labels=list(prios.keys()),values=list(prios.values()), marker=dict(colors=[clr.get(k,"#1B3358") for k in prios]), hole=0.52,textfont_size=12,textinfo="label+percent")])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#1A202C",family="Inter"), height=260,margin=dict(t=10,b=10),legend=dict(font=dict(color="#1A202C")))
            st.plotly_chart(fig,use_container_width=True)
        else: st.info("No ticket data yet.")
    with cb:
        st.markdown("<p class='sec-hdr'>Recent Tickets</p>",unsafe_allow_html=True)
        tickets=api_get("/tickets/all") or []
        cc_={"Critical":"cr","High":"hi","Medium":"me","Low":"lo"}
        for t in tickets[:6]:
            p = t.get("priority","Medium")
            t_id = t.get("id", "")
            t_title = t.get("title", "")[:46]
            t_status = t.get("status", "Open")
            c_class = cc_.get(p, "")
            
            st.markdown(f"<div class='ticket-container-box {c_class}'><span style='font-weight:700;color:#1B3358'>#{t_id}</span><span style='color:#374151;margin-left:8px;font-size:.9rem'>{t_title}</span><span style='float:right;background:#F1F5F9;color:#475569;padding:3px 9px;border-radius:5px;font-size:.75rem;font-weight:600'>{t_status}</span></div>",unsafe_allow_html=True)
        if not tickets: st.info("No tickets yet.")

# ══════════════════════════════════════════════════════════════════════════════
# AI CHAT
# ══════════════════════════════════════════════════════════════════════════════
def show_chat():
    st.markdown("<p class='page-title'>AI Chat Assistant</p><p class='page-sub'>Describe your IT problem and get instant step-by-step help.</p>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"]=="user": st.markdown(f'<div class="bubble-user">{msg["content"]}</div>',unsafe_allow_html=True)
        else: st.markdown(f'<div class="bubble-ai"><strong>AI Assistant</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    user_input=st.text_input("Type your IT problem", placeholder="e.g. VPN is not connecting, Outlook keeps crashing...", label_visibility="collapsed",key=f"ci_{st.session_state.chat_key}")

    ca,cb,cc=st.columns([3,1,1])
    with ca: use_kb=st.checkbox("Search company knowledge base",value=True)
    with cb: send=st.button("Send",use_container_width=True)
    with cc:
        if st.button("Clear",use_container_width=True): st.session_state.chat_history=[];st.session_state.chat_key+=1;st.rerun()

    if send and user_input.strip():
        q=user_input.strip()
        st.session_state.chat_history.append({"role":"user","content":q})
        st.session_state.chat_key+=1
        with st.spinner("AI is analysing your issue..."):
            data,code=api_post("/chat/ask",{"message":q,"use_knowledge_base":use_kb})
        ans=data.get("answer","Could not generate a response.") if code==200 else "AI unavailable."
        st.session_state.chat_history.append({"role":"ai","content":ans})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Create Ticket from This Conversation"):
            last=next((m["content"] for m in reversed(st.session_state.chat_history) if m["role"]=="user"),"")
            if last:
                d,c=api_post("/tickets/create",{"title":last[:80],"description":last,"category":"General","department":"General"})
                if c==200: st.success(f"Ticket #{d['ticket_id']} created — Priority: {d['priority']}")

# ══════════════════════════════════════════════════════════════════════════════
# VOICE ASSISTANT
# ══════════════════════════════════════════════════════════════════════════════
def show_voice():
    st.markdown("<p class='page-title'>Voice Assistant</p><p class='page-sub'>Speak your IT problem — AI listens, answers, and reads the fix aloud using your browser.</p>", unsafe_allow_html=True)

    if speech_to_text is None:
        st.error("Missing frontend audio library. Please install: pip install streamlit-mic-recorder")
        return

    st.session_state.speaker_enabled = st.toggle("🔊 Enable AI Voice Readout", value=st.session_state.speaker_enabled)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='vbox'><div style='font-size:3rem;margin-bottom:10px'>🎙️</div><h3 style='color:#1B3358;margin:0;font-size:1.15rem;font-weight:700'>Browser Microphone</h3><p style='color:#64748B;margin:8px 0 0;font-size:.875rem'>Click to start speaking your IT problem</p></div>", unsafe_allow_html=True)
        spoken_text = speech_to_text(language='en', use_container_width=True, just_once=True, key='browser_mic')
        
    with c2:
        st.markdown("<div class='vbox'><div style='font-size:3rem;margin-bottom:10px'>🔊</div><h3 style='color:#1B3358;margin:0;font-size:1.15rem;font-weight:700'>Browser Speaker</h3><p style='color:#64748B;margin:8px 0 0;font-size:.875rem'>AI uses your browser to read answers aloud</p></div>", unsafe_allow_html=True)
        if st.button("Test Speaker", use_container_width=True, disabled=not st.session_state.speaker_enabled):
            st.session_state.speak_now = "Hello. I am your IT helpdesk assistant. I am ready to help you with any IT problem you have."
            st.success("Speaker test complete. You should hear the message through your speakers.")
        elif not st.session_state.speaker_enabled:
            st.info("Speaker is currently disabled via the toggle above.")

    if spoken_text:
        with st.spinner("AI is thinking..."):
            ai, _ = api_post("/voice/ask-voice", {"text": spoken_text})
        ans = ai.get("answer", "I could not generate an answer.")
        
        st.session_state.voice_chat.append({"user": spoken_text, "ai": ans})
        
        if st.session_state.speaker_enabled:
            st.session_state.speak_now = ans.replace('"', "'").replace('\n', ' ')

    st.markdown("---")
    st.markdown("<p class='sec-hdr'>Type Your Question (works without microphone)</p>", unsafe_allow_html=True)
    typed = st.text_area("Describe your IT problem:", placeholder="e.g. My Outlook is not opening.", height=90, key=f"vt_{st.session_state.voice_key}")

    if st.button("Get AI Answer", use_container_width=True):
        if typed.strip():
            st.session_state.voice_key += 1
            with st.spinner("AI is analysing your issue..."):
                res, _ = api_post("/voice/ask-voice", {"text": typed.strip()})
            ans = res.get("answer", "")
            
            st.session_state.voice_chat.append({"user": typed.strip(), "ai": ans})
            
            if st.session_state.speaker_enabled:
                st.session_state.speak_now = ans.replace('"', "'").replace('\n', ' ')
        else:
            st.warning("Please describe your IT problem first.")

    if st.session_state.voice_chat:
        st.markdown("<br><p class='sec-hdr'>Conversation History</p>", unsafe_allow_html=True)
        for msg in st.session_state.voice_chat:
            st.markdown(f"<div style='background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:12px 16px;margin-bottom:8px'><span style='color:#64748B;font-size:.75rem;font-weight:600'>YOU SAID</span><br><span style='color:#1B3358;font-weight:600;font-size:1rem'>{msg['user']}</span></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="bubble-ai"><strong>AI Assistant</strong><br>{msg["ai"]}</div>', unsafe_allow_html=True)

    if st.session_state.speak_now:
        components.html(f"""<script>var msg = new SpeechSynthesisUtterance("{st.session_state.speak_now}"); window.speechSynthesis.speak(msg);</script>""", height=0, width=0)
        st.session_state.speak_now = "" 

# # ══════════════════════════════════════════════════════════════════════════════
# TICKETS
# ══════════════════════════════════════════════════════════════════════════════
def show_tickets():
    role = st.session_state.user_role
    st.markdown("<p class='page-title'>Ticket Management</p><p class='page-sub'>Submit and track your IT support requests.</p>", unsafe_allow_html=True)
    if role == "employee": 
        st.info("You can create unlimited tickets. You can only view your own tickets. IT Engineers manage resolution and status updates.")

    tab1, tab2 = st.tabs(["Create New Ticket", "View Tickets"])
    with tab1:
        st.markdown("<p class='sec-hdr'>Submit a New IT Support Ticket</p>", unsafe_allow_html=True)
        with st.form("ct", clear_on_submit=True):
            title = st.text_input("Issue Title *", placeholder="Brief summary of your problem")
            desc = st.text_area("Detailed Description *", height=110, placeholder="Describe the issue...")
            c1, c2 = st.columns(2)
            with c1: cat = st.selectbox("Category", ["Network", "Software", "Hardware", "Email", "VPN", "Printer", "Security", "Account", "Other"])
            with c2: dept = st.text_input("Your Department", value="General")
            auto_p = st.checkbox("Auto-detect priority using AI (recommended)", value=True)
            man_p = "Medium"
            if not auto_p: man_p = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"])
            sub = st.form_submit_button("Submit Ticket", use_container_width=True)

        if sub:
            if not title or not desc: 
                st.error("Please fill in both Title and Description.")
            else:
                with st.spinner("Submitting ticket and running AI analysis..."):
                    data, code = api_post("/tickets/create", {
                        "title": title, 
                        "description": desc, 
                        "category": cat, 
                        "department": dept, 
                        "priority": None if auto_p else man_p
                    })
                    
                if code == 200:
                    p = data.get("priority", "Medium")
                    t_id = str(data.get("ticket_id", "")) # Ensure it's a string
                    pc_ = {"Critical":"#DC2626", "High":"#EA580C", "Medium":"#D97706", "Low":"#16A34A"}
                    p_color = pc_.get(p, "#374151")
                    
                    st.markdown(f"<div style='background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:14px 16px'><strong style='color:#15803D'>Ticket #{t_id[:8]} submitted successfully</strong><br><span style='color:#374151'>AI assigned priority: </span><strong style='color:{p_color}'>{p}</strong></div>", unsafe_allow_html=True)
                    
                    if data.get("ai_suggested_fix"):
                        with st.expander("View AI Suggested Fix"): st.write(data["ai_suggested_fix"])
                else: 
                    st.error(f"Failed to submit ticket. Server returned error code {code}. Please try again.")

    with tab2:
        cf1, cf2 = st.columns(2)
        with cf1: sf = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
        with cf2: pf = st.selectbox("Filter by Priority", ["All", "Critical", "High", "Medium", "Low"])

        ep = "/tickets/all"
        params = []
        if sf != "All": params.append(f"status={sf}")
        if pf != "All": params.append(f"priority={pf}")
        if params: ep += "?" + "&".join(params)

        tickets = api_get(ep) or []
        pb_ = {"Critical":"bd-cr", "High":"bd-hi", "Medium":"bd-me", "Low":"bd-lo"}
        sb_ = {"Open":"bd-op", "In Progress":"bd-pr", "Resolved":"bd-rs", "Closed":"bd-cl"}
        cc_ = {"Critical":"cr", "High":"hi", "Medium":"me", "Low":"lo", "Closed":"cl"}

        if not tickets: 
            st.info("No tickets found." if role != "employee" else "You have not submitted any tickets yet.")

        for t in tickets:
            p = t.get("priority", "Medium")
            s = t.get("status", "Open")
            is_closed = (s == "Closed")
            card_class = cc_.get("Closed", "cl") if is_closed else cc_.get(p, "")
            
            pb_class = pb_.get(p, "")
            sb_class = sb_.get(s, "")
            t_id = str(t.get("id", "")) # Explicitly cast to string
            t_title = t.get("title", "")

            st.markdown(f"""
            <div class='ticket-container-box {card_class}'>
                <div style='display:flex;gap:12px;align-items:center;width:100%;padding-bottom:10px;margin-bottom:8px;border-bottom:1px dashed rgba(0,0,0,0.08);'>
                    <span style='font-weight:800;color:#1B3358;font-size:1.05rem;'>#{t_id[:8]}</span>
                    <span style='font-weight:700;color:#1A202C;font-size:1rem;'>{t_title}</span>
                    <div style='margin-left:auto; display:flex; gap:6px; align-items:center;'>
                        <span class='bd {pb_class}'>{p}</span>
                        <span class='bd {sb_class}'>{s}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            with st.container():
                with st.expander("📄 View Ticket Thread Details & Actions", expanded=False):
                    created_at = str(t.get('created_at', ''))[:16]
                    cat = t.get('category', 'N/A')
                    dept = t.get('department', 'N/A')
                    desc = t.get('description', '')
                    
                    st.markdown(f"<div style='padding:4px 10px; background: rgba(255,255,255,0.5); border-radius:6px; margin-bottom:10px;'><span style='color:#1B3358; font-size:0.85rem; font-weight:600;'>Created Timestamp: {created_at}</span></div>", unsafe_allow_html=True)
                    ca, cb = st.columns(2)
                    with ca: st.markdown(f"<p style='color:#1B3358;margin:4px 0'><strong>Category:</strong> {cat}</p>", unsafe_allow_html=True)
                    with cb: st.markdown(f"<p style='color:#1B3358;margin:4px 0'><strong>Department:</strong> {dept}</p>", unsafe_allow_html=True)

                    st.markdown(f"<p style='font-weight:700;color:#1B3358;margin:10px 0 4px'>Description</p><p style='color:#1A202C;font-size:.9rem;background:rgba(255,255,255,0.7);border-radius:6px;padding:10px 14px'>{desc}</p>", unsafe_allow_html=True)

                    if t.get("ai_suggested_fix"): 
                        st.markdown(f"<div class='fix-box'><strong>AI Suggested Fix</strong><br><span style='font-size:.875rem;white-space:pre-wrap;color:#374151'>{t['ai_suggested_fix']}</span></div>", unsafe_allow_html=True)

                    if role in ["admin", "it_engineer"] and not is_closed:
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Find the correct index for the selectbox
                        status_options = ["Open", "In Progress", "Resolved", "Closed"]
                        current_status_index = status_options.index(s) if s in status_options else 0
                        
                        ns = st.selectbox("Update Status", status_options, index=current_status_index, key=f"sel_{t_id}")
                        
                        if ns == "Closed": 
                            st.warning("Setting to Closed is permanent. This ticket cannot be reopened.")
                            
                        if st.button(f"Update Ticket #{t_id[:8]}", key=f"upd_{t_id}"):
                            d, c = api_put(f"/tickets/{t_id}/update", {"status": ns})
                            if c == 200: 
                                st.success(f"Ticket #{t_id[:8]} updated to {ns}")
                                time.sleep(0.5)
                                st.rerun()
                            else: 
                                st.error(d.get("detail", "Update failed."))
                    elif role in ["admin", "it_engineer"] and is_closed:
                        st.markdown("<div style='background:#FEF2F2;border:1px solid #FCA5A5;border-radius:7px;padding:10px 14px;margin-top:10px;color:#374151;font-size:.875rem'>This ticket is <strong>permanently Closed</strong> and cannot be updated.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# SCREENSHOT
# ══════════════════════════════════════════════════════════════════════════════
def show_screenshot():
    st.markdown("<p class='page-title'>Screenshot Error Analyzer</p><p class='page-sub'>Upload a screenshot of any error — AI reads and diagnoses it instantly.</p>", unsafe_allow_html=True)
    uploaded=st.file_uploader("Upload screenshot (PNG or JPG)",type=["png","jpg","jpeg"])
    if uploaded:
        c1,c2=st.columns(2)
        with c1: st.image(uploaded, caption="Uploaded screenshot", use_column_width=True)
        with c2:
            if st.button("Analyse Screenshot",use_container_width=True):
                with st.spinner("Reading screenshot with Vision AI..."):
                    files={"file":(uploaded.name,uploaded.getvalue(),uploaded.type)}
                    data,code=api_post("/chat/analyze-screenshot",files=files)
                if code==200:
                    if data.get("extracted_text"):
                        with st.expander("Text extracted from screenshot"): st.markdown(f"<p style='color:#374151;font-size:.875rem'>{data['extracted_text']}</p>",unsafe_allow_html=True)
                    if data.get("detected_errors"):
                        st.markdown("<p style='font-weight:600;color:#374151'>Issues detected:</p>",unsafe_allow_html=True)
                        for e in data["detected_errors"]: st.markdown(f"<div style='background:#FEF2F2;border-left:3px solid #DC2626;border-radius:4px;padding:8px 12px;margin:4px 0;color:#374151;font-size:.875rem'>{e}</div>",unsafe_allow_html=True)
                    else: st.info("No known error codes detected.")
                    if data.get("suggested_fix"): st.markdown(f"<div class='fix-box'><strong>Suggested Fix</strong><br><span style='font-size:.875rem;white-space:pre-wrap;color:#374151'>{data['suggested_fix']}</span></div>",unsafe_allow_html=True)
                    st.caption(f"Vision AI Confidence: {data.get('confidence','N/A')}")
                    if st.button("Create Support Ticket from Analysis"):
                        errors=", ".join(data.get("detected_errors",["Unknown error"]))
                        td,tc=api_post("/tickets/create",{"title":f"Screenshot Error: {errors[:80]}", "description":data.get("extracted_text","Screenshot error"), "category":"Software","department":"General"})
                        if tc==200: st.success(f"Ticket #{td.get('ticket_id')} created.")
                else: st.error("Analysis failed. Please try again.")

# ══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE 
# ══════════════════════════════════════════════════════════════════════════════
def show_knowledge():
    role=st.session_state.user_role
    st.markdown("<p class='page-title'>Knowledge Base</p>",unsafe_allow_html=True)
    kb = api_get("/knowledge/files")

    if role == "employee":
        st.markdown("<p class='page-sub'>Browse and search the company IT knowledge base.</p>",unsafe_allow_html=True)
        st.markdown(f"<div class='kpi' style='display:inline-block;margin-bottom:16px;min-width:180px'><div class='kpi-n' style='color:#1B3358'>{kb.get('total_indexed_chunks',0)}</div><div class='kpi-l'>Indexed Knowledge Chunks</div></div>",unsafe_allow_html=True)
        
        for idx, f in enumerate(kb.get("files", [])):
            f_name = f.get('name', 'Unknown')
            f_type = f.get('type', 'UNK')
            f_size = round(f.get('size', 0)/1024, 1)
            
            st.markdown(f"<div class='doc-row'><span style='font-size:1.3rem'>📄</span><span style='font-weight:500;color:#1B3358'>{f_name}</span><span style='color:#64748B;font-size:.8rem;margin-left:auto'>{f_type} &bull; {f_size} KB</span></div>",unsafe_allow_html=True)
            act_container = st.container()
            v_col1, v_col2, _ = act_container.columns([1.2, 1, 4])
            view_state_key = f"view_active_emp_{idx}"
            if view_state_key not in st.session_state: st.session_state[view_state_key] = False

            with v_col1:
                if st.button("👁️ View Document", key=f"emp_btn_v_{idx}"): st.session_state[view_state_key] = not st.session_state[view_state_key]
            with v_col2:
                try:
                    h = {"Authorization": f"Bearer {st.session_state.token}"}
                    res = requests.get(f"{API_URL}/knowledge/download/{urllib.parse.quote(f_name)}", headers=h, timeout=20)
                    if res.status_code == 200: st.download_button("📥 Download", data=res.content, file_name=f_name, key=f"emp_d_{idx}")
                    else: st.button("📥 Download Unavailable", key=f"emp_d_fail_{idx}", disabled=True)
                except Exception: st.button("📥 Connection Error", key=f"emp_d_err_{idx}", disabled=True)

            if st.session_state[view_state_key]:
                with st.spinner("Loading file content..."):
                    h = {"Authorization": f"Bearer {st.session_state.token}"}
                    res = requests.get(f"{API_URL}/knowledge/download/{urllib.parse.quote(f_name)}", headers=h, timeout=25)
                    if res.status_code == 200:
                        if f_name.lower().endswith('.pdf'): st.markdown(f'<div style="width:100%; max-width:820px; margin:12px auto; border:2px solid #CBD5E1; border-radius:8px; overflow:hidden; background-color:#525659; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"><embed src="data:application/pdf;base64,{base64.b64encode(res.content).decode("utf-8")}" type="application/pdf" width="100%" height="1000px" style="border:none; display:block;"></embed></div>', unsafe_allow_html=True)
                        elif f_name.lower().endswith(('.md', '.txt')): st.markdown(f"""<div style='background:#fff; padding:24px; border-radius:8px; border:2px solid #CBD5E1; color:#1A202C; font-family:"Courier New", Courier, monospace; max-height:700px; width:100%; max-width:820px; margin:12px auto; overflow-y:auto; white-space:pre-wrap; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>{res.content.decode('utf-8', errors='ignore')}</div>""", unsafe_allow_html=True)
                    else: st.error("Failed to render preview window.")
            st.markdown("<br>", unsafe_allow_html=True)

        if not kb.get("files"): st.info("No documents uploaded by the IT team yet.")
        st.markdown("---")
        st.markdown("<p class='sec-hdr'>Search Knowledge Base</p>",unsafe_allow_html=True)
        q=st.text_input("Ask a question:",placeholder="e.g. How do I reset my network password?")
        if st.button("Search") and q.strip():
            with st.spinner("Searching..."):
                d,c=api_post("/chat/ask",{"message":q.strip(),"use_knowledge_base":True})
            if c==200: st.markdown(f'<div class="bubble-ai"><strong>AI Assistant</strong><br>{d.get("answer","")}</div>', unsafe_allow_html=True)
        return

    tab1,tab2=st.tabs(["Upload Documents","Browse Files"])
    with tab1:
        doc=st.file_uploader("Select PDF, TXT or Markdown file",type=["pdf","txt","md"])
        if doc and st.button("Upload and Index",use_container_width=True):
            with st.spinner("Uploading and indexing..."):
                data,code=api_post("/knowledge/upload",files={"file":(doc.name,doc.getvalue(),"application/octet-stream")})
            if code==200: st.success(f"{data.get('message')} — {data.get('chunks_created',0)} chunks indexed.")
            else: st.error("Upload failed.")
        if st.button("Reload All Knowledge Base Files"):
            with st.spinner("Reloading..."): data,_=api_post("/knowledge/reload")
            st.success(f"Reloaded {data.get('files_processed',0)} files.")
            
    with tab2:
        st.metric("Total Indexed Chunks", kb.get("total_indexed_chunks", 0))
        for idx, f in enumerate(kb.get("files",[])):
            f_name = f.get('name', 'Unknown')
            f_type = f.get('type', 'UNK')
            f_size = round(f.get('size', 0)/1024, 1)
            
            st.markdown(f"<div class='doc-row'><span style='font-size:1.3rem'>📄</span><span style='font-weight:500;color:#1B3358'>{f_name}</span><span style='color:#64748B;font-size:.8rem;margin-left:auto'>{f_type} &bull; {f_size} KB</span></div>",unsafe_allow_html=True)
            adm_act_box = st.container()
            act_1, act_2, act_3, _ = adm_act_box.columns([1.2, 1, 1.2, 3])
            view_state_key_adm = f"view_active_adm_{idx}"
            if view_state_key_adm not in st.session_state: st.session_state[view_state_key_adm] = False

            with act_1:
                if st.button("👁️ View Frame", key=f"adm_btn_v_{idx}"): st.session_state[view_state_key_adm] = not st.session_state[view_state_key_adm]
            with act_2:
                try:
                    h = {"Authorization": f"Bearer {st.session_state.token}"}
                    res = requests.get(f"{API_URL}/knowledge/download/{urllib.parse.quote(f_name)}", headers=h, timeout=20)
                    if res.status_code == 200: st.download_button("📥 Download", data=res.content, file_name=f_name, key=f"adm_d_{idx}")
                    else: st.button("📥 Download Unavailable", key=f"adm_d_fail_{idx}", disabled=True)
                except Exception: st.button("📥 Connection Error", key=f"adm_d_err_{idx}", disabled=True)
            with act_3:
                if st.button("🗑️ Delete File", key=f"adm_del_{idx}"):
                    success = False
                    with st.spinner("Purging database nodes..."):
                        try:
                            res = requests.delete(f"{API_URL}/knowledge/delete/{urllib.parse.quote(f_name)}", headers={"Authorization": f"Bearer {st.session_state.token}"}, timeout=15)
                            if res.status_code == 200: st.success(f"Successfully purged: {f_name}"); success = True
                            else: st.error("Failed to delete from server storage.")
                        except Exception as e: st.error(f"Network error: {str(e)}")
                    if success: time.sleep(1); st.rerun()

            if st.session_state[view_state_key_adm]:
                with st.spinner("Compiling visual preview matrix..."):
                    res = requests.get(f"{API_URL}/knowledge/download/{urllib.parse.quote(f_name)}", headers={"Authorization": f"Bearer {st.session_state.token}"}, timeout=25)
                    if res.status_code == 200:
                        if f_name.lower().endswith('.pdf'): st.markdown(f'<div style="width:100%; max-width:820px; margin:12px auto; border:2px solid #CBD5E1; border-radius:8px; overflow:hidden; background-color:#525659; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"><embed src="data:application/pdf;base64,{base64.b64encode(res.content).decode("utf-8")}" type="application/pdf" width="100%" height="1000px" style="border:none; display:block;"></embed></div>', unsafe_allow_html=True)
                        elif f_name.lower().endswith(('.md', '.txt')): st.markdown(f"""<div style='background:#fff; padding:24px; border-radius:8px; border:2px solid #CBD5E1; color:#1A202C; font-family:"Courier New", Courier, monospace; max-height:700px; width:100%; max-width:820px; margin:12px auto; overflow-y:auto; white-space:pre-wrap; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>{res.content.decode('utf-8', errors='ignore')}</div>""", unsafe_allow_html=True)
                    else: st.error("Failed to compile preview canvas framework.")
            st.markdown("<br>", unsafe_allow_html=True)
        if not kb.get("files"): st.info("No documents uploaded yet.")

# ══════════════════════════════════════════════════════════════════════════════
# ASSETS
# ══════════════════════════════════════════════════════════════════════════════
def show_assets():
    st.markdown("<p class='page-title'>Asset Manager</p><p class='page-sub'>Track and manage all IT hardware assets.</p>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Add Asset", "View Assets"])

    with tab1:
        with st.form("aa", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                tag = st.text_input("Asset Tag *", placeholder="LAPTOP-001")
                atype = st.selectbox("Type", ["Laptop", "Desktop", "Printer", "Monitor", "Server", "Network Device", "Phone", "Other"])
                brand = st.text_input("Brand", placeholder="Dell / HP / Lenovo")
            with c2:
                model = st.text_input("Model", placeholder="Latitude 5520")
                serial = st.text_input("Serial Number")
                dept = st.text_input("Department")
            astatus = st.selectbox("Status", ["Available", "Assigned", "In Repair", "Retired"])
            notes = st.text_area("Notes")
            if st.form_submit_button("Add Asset", use_container_width=True):
                data, code = api_post("/assets/add", {
                    "asset_tag": tag, "asset_type": atype, "brand": brand, 
                    "model": model, "serial_number": serial, "department": dept, 
                    "status": astatus, "notes": notes
                })
                if code == 200: 
                    st.success(f"Asset {tag} added successfully.")
                    time.sleep(0.5)
                    st.rerun() 
                else: 
                    st.error(data.get("detail", "Failed to add asset."))

    with tab2:
        assets = api_get("/assets/all") or []
        
        if not assets: 
            st.info("No assets found.")
        else:
            for a in assets:
                t_id = a.get("id")
                tag = a.get("asset_tag", "Unknown")
                current_status = a.get("status", "Available")
                
                # Check if the status is valid to prevent index errors
                status_options = ["Available", "Assigned", "In Repair", "Retired"]
                if current_status not in status_options:
                    current_status = "Available"
                
                with st.expander(f"📦 {tag} | Type: {a.get('asset_type', 'N/A')} | Status: {current_status}"):
                    # Form details just for display logic
                    st.markdown(f"**Brand:** {a.get('brand', 'N/A')} &nbsp; | &nbsp; **Model:** {a.get('model', 'N/A')} &nbsp; | &nbsp; **Serial:** {a.get('serial_number', 'N/A')}")
                    
                    # Update Section
                    new_s = st.selectbox("Change Status", status_options, 
                                         index=status_options.index(current_status),
                                         key=f"s_{t_id}")
                    
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        if st.button("Update Status", key=f"upd_{t_id}"):
                            d, c = api_put(f"/assets/{t_id}", {"status": new_s})
                            if c == 200:
                                st.toast("Status updated!")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("Failed to update status.")
                    
                    with c2:
                        if st.button("🗑️ Delete Asset", key=f"del_{t_id}"):
                            d, c = api_delete(f"/assets/{t_id}")
                            if c == 200:
                                st.toast("Asset deleted!")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("Failed to delete asset.")

# ══════════════════════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
def show_analytics():
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    st.markdown("<p class='page-title'>Analytics Dashboard</p><p class='page-sub'>Ticket trends and operational insights.</p>",unsafe_allow_html=True)

    stats=api_get("/tickets/stats/summary")
    raw  =api_get("/tickets/all") or []

    c1,c2,c3,c4=st.columns(4)
    for col,val,lbl,cl in [(c1,stats.get("total",0),"Total","#1B3358"), (c2,stats.get("open",0),"Open","#D97706"), (c3,stats.get("in_progress",0),"In Progress","#7C3AED"), (c4,stats.get("resolved",0),"Resolved","#16A34A")]:
        with col: st.markdown(f"<div class='kpi'><div class='kpi-n' style='color:{cl}'>{val}</div><div class='kpi-l'>{lbl}</div></div>",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    ca,cb=st.columns(2)
    with ca:
        st.markdown("<p class='sec-hdr'>Tickets by Category</p>",unsafe_allow_html=True)
        cats=stats.get("categories",{})
        if cats:
            fig=px.bar(x=list(cats.keys()),y=list(cats.values()), color=list(cats.values()),color_continuous_scale=[[0,"#DBEAFE"],[1,"#1B3358"]])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#1A202C",family="Inter"),height=280,showlegend=False, margin=dict(t=10,b=10),xaxis=dict(color="#374151"),yaxis=dict(color="#374151"))
            st.plotly_chart(fig,use_container_width=True)
        else: st.info("No data yet.")
    with cb:
        st.markdown("<p class='sec-hdr'>Tickets by Priority</p>",unsafe_allow_html=True)
        prios=stats.get("priorities",{})
        if prios:
            clr={"Critical":"#DC2626","High":"#EA580C","Medium":"#D97706","Low":"#16A34A"}
            fig=go.Figure(data=[go.Pie(labels=list(prios.keys()),values=list(prios.values()), marker=dict(colors=[clr.get(k,"#1B3358") for k in prios]), hole=0.45,textinfo="label+percent")])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#1A202C",family="Inter"), height=280,margin=dict(t=10,b=10),legend=dict(font=dict(color="#1A202C")))
            st.plotly_chart(fig,use_container_width=True)
        else: st.info("No data yet.")

    if raw:
        st.markdown("<p class='sec-hdr'>All Ticket Records</p>",unsafe_allow_html=True)
        df=pd.DataFrame([{"ID":t["id"],"Title":t["title"][:50],"Priority":t.get("priority",""), "Status":t.get("status",""),"Category":t.get("category",""),"Department":t.get("department","")} for t in raw])
        st.dataframe(df,use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# USER MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def show_user_management():
    st.markdown("<p class='page-title'>User Management</p><p class='page-sub'>Approve registrations and manage user access.</p>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Pending Approvals", "All Users"])

    with tab1:
        pending = api_get("/auth/pending") or []
        if not pending: 
            st.success("No pending registrations. All accounts have been reviewed.")
        else:
            st.info(f"{len(pending)} registration(s) awaiting your approval.")
            for u in pending:
                u_id = u.get('id')
                u_name = u.get('name', 'Unknown')
                u_email = u.get('email', 'N/A')
                u_dept = u.get('department', 'General')
                u_role = u.get('role', 'employee').replace('_', ' ').title()
                u_created = str(u.get('created_at', ''))[:16]
                
                st.markdown(f"""
                <div class='pcard'>
                    <strong>{u_name}</strong>
                    <span style='float:right;background:#FEF3C7;color:#D97706;padding:2px 9px;border-radius:4px;font-size:.72rem;font-weight:600'>Pending</span><br>
                    <span style='color:#374151;font-size:.875rem'>{u_email}</span> &bull; {u_dept} &bull; {u_role}<br>
                    <span style='color:#94A3B8;font-size:.78rem'>Registered {u_created}</span>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, _ = st.columns([1, 1, 3])
                with c1:
                    if st.button("Approve", key=f"ap_{u_id}"):
                        d, c = api_put(f"/auth/approve/{u_id}", {"approve": True})
                        if c == 200: st.rerun()
                        else: st.error("Error approving user.")
                with c2:
                    if st.button("Reject", key=f"rj_{u_id}"):
                        d, c = api_put(f"/auth/approve/{u_id}", {"approve": False})
                        if c == 200: st.rerun()
                        else: st.error("Error rejecting user.")
                st.markdown("---")

    with tab2:
        users = api_get("/auth/all-users") or []
        rc_ = {"admin": "#DC2626", "it_engineer": "#D97706", "employee": "#16A34A"}
        
        for u in users:
            u_id = u.get('id')
            if not u_id: continue
            
            ok = u.get("is_approved", False) and u.get("is_active", True)
            u_role = u.get("role", "employee")
            rc = rc_.get(u_role, "#64748B")
            role_text = u_role.replace('_', ' ').title()
            
            c1, c2 = st.columns([5, 1])
            with c1:
                bg = "#DCFCE7" if ok else "#FEE2E2"
                txt = "#15803D" if ok else "#DC2626"
                status = "Active" if ok else "Inactive"
                st.markdown(f"""
                <div class='ucard'>
                    <strong>{u.get('name')}</strong>
                    <span style='background:{rc}22;color:{rc};padding:1px 8px;border-radius:4px;font-size:.72rem;font-weight:600;margin-left:8px'>{role_text}</span>
                    <span style='background:{bg};color:{txt};padding:1px 8px;border-radius:4px;font-size:.72rem;font-weight:600;margin-left:4px'>{status}</span><br>
                    <span style='color:#64748B;font-size:.85rem'>{u.get('email')} &bull; {u.get('department')}</span>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if u_role != "admin":
                    if st.button("🗑️ Delete", key=f"del_{u_id}"):
                        d, c = api_delete(f"/auth/delete/{u_id}")
                        if c == 200: st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# CHANGE PASSWORD
# ══════════════════════════════════════════════════════════════════════════════
def show_change_password():
    st.markdown("<p class='page-title'>Change Password</p><p class='page-sub'>Update your account password securely.</p>",unsafe_allow_html=True)
    st.markdown("<div style='max-width: 500px;'>", unsafe_allow_html=True)
    with st.form("change_password_form", clear_on_submit=True):
        curr_pw = st.text_input("Current Password *", type="password")
        new_pw = st.text_input("New Password *", type="password")
        confirm_pw = st.text_input("Confirm New Password *", type="password")
        sub = st.form_submit_button("Update Password", use_container_width=True)
        if sub:
            if not curr_pw or not new_pw or not confirm_pw: st.error("All fields are required.")
            elif new_pw != confirm_pw: st.error("New passwords do not match.")
            elif len(new_pw) < 6: st.error("New password must be at least 6 characters long.")
            else:
                with st.spinner("Updating password..."): 
                    d, c = api_post("/auth/change-password", {
                        "email": st.session_state.user_email, 
                        "current_password": curr_pw, 
                        "new_password": new_pw
                    })
                if c == 200: st.success("Password updated successfully!")
                else: st.error(d.get("detail", "Failed to update password. Check your current password."))
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    if not st.session_state.authenticated: show_login(); return
    show_sidebar()
    role, page = st.session_state.user_role, st.session_state.page

    if page=="User Management" and role!="admin": st.error("Administrator access required."); return
    if page in {"Assets","Analytics"} and role not in ["admin","it_engineer"]: st.error("IT Engineer or Administrator access required."); return

    {"Dashboard":show_dashboard,"AI Chat":show_chat,"Voice Assistant":show_voice,"Tickets":show_tickets,"Screenshot Analyzer":show_screenshot,"Knowledge Base":show_knowledge,"Assets":show_assets,"Analytics":show_analytics,"User Management":show_user_management,"Change Password":show_change_password}.get(page, show_dashboard)()

if __name__=="__main__": main()