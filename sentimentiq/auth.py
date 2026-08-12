import json
import hashlib
import secrets
import datetime
import streamlit as st
from typing import Optional, Dict, Any
from pathlib import Path

USERS_FILE = Path("users.json")

# ── Design Tokens & CSS ─────────────────────────────────────────────────────
_AUTH_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

:root {
  --bg:           #0d0f14;
  --surface:      #13161e;
  --surface-2:    #1a1e2a;
  --border:       rgba(255,255,255,0.07);
  --border-hover: rgba(212,175,90,0.35);
  --gold:         #d4af5a;
  --gold-dim:     rgba(212,175,90,0.15);
  --gold-glow:    rgba(212,175,90,0.08);
  --text:         #e8e6e0;
  --text-2:       #9a9690;
  --text-3:       #5c5a56;
  --error:        #e07070;
  --success:      #70b490;
  --font-display: 'DM Serif Display', Georgia, serif;
  --font-body:    'DM Sans', system-ui, sans-serif;
  --radius:       12px;
  --radius-sm:    8px;
  --shadow:       0 24px 64px rgba(0,0,0,0.55);
}

/* ── Reset & Page ── */
html, body, .stApp { background: var(--bg) !important; font-family: var(--font-body) !important; color: var(--text) !important; }
header[data-testid="stHeader"], footer, #MainMenu, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Hero Panel (right side via st.markdown) ── */
.auth-hero {
  padding: 3.5rem 2.5rem;
  background:
    radial-gradient(ellipse 70% 55% at 60% 30%, rgba(212,175,90,0.09) 0%, transparent 65%),
    #1a1e2a;
  border-left: 1px solid var(--border);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.auth-hero::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, var(--gold) 45%, transparent 100%);
  opacity: 0.6;
}

.auth-hero::after {
  content: '';
  position: absolute;
  width: 320px; height: 320px;
  border-radius: 50%;
  border: 1px solid rgba(212,175,90,0.08);
  bottom: -100px; right: -100px;
  pointer-events: none;
}

.auth-eyebrow {
  font-size: .68rem;
  font-weight: 600;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 1rem;
}

.auth-title {
  font-family: var(--font-display);
  font-size: 3.4rem;
  line-height: 1.05;
  color: var(--text);
  margin: 0 0 1.25rem;
}

.auth-title em { font-style: italic; color: var(--gold); }

.auth-description {
  font-size: .88rem;
  line-height: 1.75;
  color: var(--text-2);
  max-width: 340px;
  margin-bottom: 2.5rem;
}

.auth-features { display: flex; flex-direction: column; gap: .75rem; }

.auth-feature {
  display: flex;
  align-items: center;
  gap: .7rem;
  font-size: .82rem;
  font-weight: 500;
  color: var(--text-2);
}

.auth-feature-icon {
  width: 32px; height: 32px;
  border-radius: 7px;
  background: var(--gold-dim);
  border: 1px solid rgba(212,175,90,0.2);
  display: flex; align-items: center; justify-content: center;
  font-size: .9rem;
  flex-shrink: 0;
}

/* ── Left panel wrapper ── */
.auth-left-wrap {
  min-height: 100vh;
  padding: 3.5rem 2.75rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: var(--surface);
  position: relative;
}

.auth-left-wrap::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, var(--gold) 45%, transparent 100%);
  opacity: 0.5;
}

.auth-section-label {
  font-size: .7rem;
  font-weight: 600;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 1.5rem;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
  gap: 0 !important;
  border-bottom: 1px solid var(--border) !important;
  background: transparent !important;
  margin-bottom: 1.75rem !important;
}

[data-testid="stTabs"] button[role="tab"] {
  font-family: var(--font-body) !important;
  font-size: .78rem !important;
  font-weight: 500 !important;
  letter-spacing: .04em !important;
  color: var(--text-2) !important;
  padding: .6rem 1.1rem !important;
  border-radius: 0 !important;
  border: none !important;
  background: transparent !important;
  transition: color .2s !important;
}

[data-testid="stTabs"] button[role="tab"]:hover { color: var(--text) !important; }

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom: 2px solid var(--gold) !important;
}

/* ── Inputs ── */
.stTextInput > label {
  font-family: var(--font-body) !important;
  font-size: .68rem !important;
  font-weight: 600 !important;
  letter-spacing: .1em !important;
  text-transform: uppercase !important;
  color: var(--text-3) !important;
}

.stTextInput input {
  font-family: var(--font-body) !important;
  font-size: .88rem !important;
  color: var(--text) !important;
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  padding: .65rem .9rem !important;
  transition: border-color .2s, box-shadow .2s !important;
}

.stTextInput input:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px var(--gold-glow) !important;
}

.stTextInput input::placeholder { color: var(--text-3) !important; }

/* ── Primary Button ── */
.stButton > button {
  font-family: var(--font-body) !important;
  font-size: .8rem !important;
  font-weight: 600 !important;
  letter-spacing: .08em !important;
  text-transform: uppercase !important;
  color: #0d0f14 !important;
  background: linear-gradient(135deg, #d4af5a 0%, #b8843a 100%) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: .75rem 1.5rem !important;
  margin-top: .75rem !important;
  width: 100% !important;
  transition: opacity .2s, transform .15s, box-shadow .2s !important;
  box-shadow: 0 4px 20px rgba(212,175,90,0.3) !important;
}

.stButton > button:hover {
  opacity: .88 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 32px rgba(212,175,90,0.4) !important;
}

.stButton > button:active { transform: translateY(0) !important; }

/* ── Alerts ── */
.stAlert {
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-body) !important;
  font-size: .82rem !important;
  margin-top: .75rem !important;
}

/* ── Profile Badge ── */
.profile-badge {
  position: fixed;
  top: 1rem; right: 1.25rem;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: .75rem;
  padding: .5rem .85rem .5rem .65rem;
  background: rgba(19,22,30,0.82);
  backdrop-filter: blur(20px) saturate(1.5);
  -webkit-backdrop-filter: blur(20px) saturate(1.5);
  border: 1px solid rgba(212,175,90,0.2);
  border-radius: 100px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 1px 0 rgba(212,175,90,0.1) inset;
  transition: border-color .25s, box-shadow .25s;
}

.profile-badge:hover {
  border-color: rgba(212,175,90,0.4);
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}

.profile-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4af5a 0%, #b8843a 100%);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-display);
  font-size: .9rem;
  color: #0d0f14;
  font-weight: 700;
  flex-shrink: 0;
}

.profile-info { display: flex; flex-direction: column; gap: .1rem; }

.profile-name {
  font-family: var(--font-body);
  font-size: .8rem;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  line-height: 1;
}

.profile-meta {
  font-family: var(--font-body);
  font-size: .65rem;
  color: var(--text-3);
  letter-spacing: .03em;
  line-height: 1;
}

.profile-divider { width: 1px; height: 22px; background: var(--border); flex-shrink: 0; }

/* ── Logout button override (small, ghost style) ── */
[data-testid="stButton"][key="logout_btn"] > button,
.logout-btn button {
  background: transparent !important;
  color: var(--text-2) !important;
  font-size: .72rem !important;
  padding: .3rem .6rem !important;
  margin: 0 !important;
  box-shadow: none !important;
  border: 1px solid var(--border) !important;
  border-radius: 100px !important;
  text-transform: none !important;
  letter-spacing: .02em !important;
  width: auto !important;
}

.logout-btn button:hover {
  color: var(--text) !important;
  border-color: var(--border-hover) !important;
  transform: none !important;
}
</style>
"""

# ── Core Logic ───────────────────────────────────────────────────────────────

def init_users() -> None:
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}")

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()

def hash_pii(data: str) -> str:
    return hashlib.sha256(data.lower().encode()).hexdigest()

def load_users() -> Dict[str, Dict[str, str]]:
    init_users()
    try:
        return json.loads(USERS_FILE.read_text())
    except Exception:
        return {}

def save_users(users: Dict[str, Dict[str, str]]) -> None:
    USERS_FILE.write_text(json.dumps(users, indent=2))

def signup(username: str, email: str, password: str) -> tuple[bool, str]:
    if not username.strip():
        return False, "Username cannot be empty."
    if not email.strip() or "@" not in email:
        return False, "Please enter a valid email."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    users = load_users()
    if username in users:
        return False, "Username already taken. Please choose another."

    salt = secrets.token_hex(16)
    users[username] = {
        "salt": salt,
        "hashed_pass": hash_password(password, salt),
        "email_hash": hash_pii(email),
        "joined": datetime.datetime.now().isoformat(),
    }
    save_users(users)
    return True, "Account created! You can now sign in."

def login(username: str, password: str) -> tuple[bool, str]:
    if not username.strip() or not password.strip():
        return False, "Please enter your username and password."

    users = load_users()
    if username not in users:
        return False, "Invalid username or password."

    user_data = users[username]
    if hash_password(password, user_data["salt"]) != user_data["hashed_pass"]:
        return False, "Invalid username or password."

    st.session_state.current_user = {
        "username": username,
        "joined": user_data["joined"],
    }
    return True, "Welcome back!"

def logout() -> None:
    st.session_state.pop("current_user", None)

def get_current_user() -> Optional[Dict[str, Any]]:
    return st.session_state.get("current_user")

# ── Auth UI ──────────────────────────────────────────────────────────────────

def show_auth_ui() -> None:
    """
    Two-column auth screen.
    LEFT  → Streamlit column with forms (widgets render correctly here).
    RIGHT → Streamlit column with a full-height HTML hero panel.
    Both columns sit inside a Streamlit columns() call so layout is controlled
    by Streamlit itself — no broken HTML grids wrapping interactive widgets.
    """
    st.markdown(_AUTH_CSS, unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1], gap="small")

    # ── LEFT: form panel ──────────────────────────────────────────────────
    with left_col:
        st.markdown('<div class="auth-left-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="auth-section-label">Welcome back</div>', unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔑  Login", "📝  Create Account"])

        with tab_login:
            username = st.text_input("Username", placeholder="your_username", key="li_user")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="li_pass")
            if st.button("Sign in →", key="login_btn"):
                ok, msg = login(username, password)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with tab_signup:
            su_user  = st.text_input("Username",         placeholder="choose_a_username",  key="su_user")
            su_email = st.text_input("Email",             placeholder="you@example.com",    key="su_email")
            su_pass  = st.text_input("Password",          type="password", placeholder="min. 6 characters", key="su_pass")
            su_conf  = st.text_input("Confirm Password",  type="password", placeholder="repeat password",   key="su_conf")
            if st.button("Create account →", key="signup_btn"):
                if su_pass != su_conf:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = signup(su_user, su_email, su_pass)
                    st.success(msg) if ok else st.error(msg)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: hero panel (pure HTML — no widgets, so no breakage) ────────
    with right_col:
        st.markdown("""
        <div class="auth-hero">
          <div class="auth-eyebrow">AI-Powered Sentiment Intelligence</div>
          <h1 class="auth-title">Sentiment<em>IQ</em></h1>
          <p class="auth-description">
            Transform raw text into actionable insights. Train state-of-the-art
            ensemble models on your data, uncover hidden keyword patterns, and
            receive lightning-fast predictions with confidence scores.
          </p>
          <div class="auth-features">
            <div class="auth-feature">
              <div class="auth-feature-icon">🤖</div>
              <span>Ensemble ML Models</span>
            </div>
            <div class="auth-feature">
              <div class="auth-feature-icon">📊</div>
              <span>Keyword Intelligence</span>
            </div>
            <div class="auth-feature">
              <div class="auth-feature-icon">⚡</div>
              <span>Real-Time Prediction</span>
            </div>
            <div class="auth-feature">
              <div class="auth-feature-icon">🔒</div>
              <span>Enterprise Security</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# ── Profile Badge ─────────────────────────────────────────────────────────────

def show_profile_section(user: Dict[str, Any]) -> None:
    """Fixed pill badge at top-right + accessible logout button."""
    st.markdown(_AUTH_CSS, unsafe_allow_html=True)

    initial = user["username"][0].upper()
    joined  = user["joined"][:10]

    st.markdown(f"""
    <div class="profile-badge">
      <div class="profile-avatar">{initial}</div>
      <div class="profile-info">
        <span class="profile-name">{user['username']}</span>
        <span class="profile-meta">Member since {joined}</span>
      </div>
      <div class="profile-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    # Logout button — floated right via columns
    _, btn_col = st.columns([0.88, 0.12])
    with btn_col:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("Sign out", key="logout_btn"):
            logout()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ── Entry point (example usage) ──────────────────────────────────────────────

if __name__ == "__main__":
    st.set_page_config(page_title="SentimentIQ", layout="wide", initial_sidebar_state="collapsed")

    user = get_current_user()
    if not user:
        show_auth_ui()
    else:
        show_profile_section(user)
        st.title(f"Welcome, {user['username']} 👋")
        st.write("Your dashboard goes here.")