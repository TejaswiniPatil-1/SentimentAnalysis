"""
ui/styles.py
────────────
All CSS injected via st.markdown(…, unsafe_allow_html=True).
Single call:  inject_css()
HTML snippet helpers live here too.
"""

from __future__ import annotations

GLOBAL_CSS = """
<style>
/* ─────────────────────────────────────────────
   IMPORTS
───────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ─────────────────────────────────────────────
   TOKENS
───────────────────────────────────────────── */
:root {
  --bg:        #07080d;
  --s1:        #0e1117;
  --s2:        #141720;
  --s3:        #191d27;
  --border:    #1c2030;
  --border2:   #252b3b;
  --text:      #dde3ef;
  --muted:     #4e5a72;
  --muted2:    #6b7a96;
  --accent:    #00f5c4;
  --accent2:   #ff4d7d;
  --accent3:   #4d9fff;
  --warn:      #ffd166;
  --pos:       #00e5a0;
  --neg:       #ff5370;
  --neu:       #b084ff;
  --font-head: 'Outfit', sans-serif;
  --font-mono: 'DM Mono', monospace;
  --r-sm:      8px;
  --r-md:      12px;
  --r-lg:      18px;
}

/* ─────────────────────────────────────────────
   RESET
───────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: var(--font-head);
  background: var(--bg);
  color: var(--text);
}
.main { background: var(--bg); }
.block-container {
  padding: 1.8rem 2.5rem 5rem;
  max-width: 1420px;
}

/* ─────────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--s1) !important;
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stSlider .stMarkdown { color: var(--muted2) !important; }

/* compact sidebar spacing */
[data-testid="stSidebar"] .css-1d391kg,
[data-testid="stSidebar"] .css-1v0mbdj,
[data-testid="stSidebar"] .stButton,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stTextInput,
[data-testid="stSidebar"] .stToggle {
  margin: 0.2rem 0 !important;
  padding: 0 !important;
}

/* tighter components to minimize padding gaps */
[data-testid="stSidebar"] .stButton>button {
  font-size: 0.9rem !important;
  padding: 0.5rem 0.75rem !important;
  line-height: 1.3 !important;
}
[data-testid="stSidebar"] .stSlider .stSlider > div,
[data-testid="stSidebar"] .stSlider .stMarkdown {
  margin-top: 0.2rem !important;
  margin-bottom: 0.2rem !important;
}

/* ─────────────────────────────────────────────
   HERO
───────────────────────────────────────────── */
.hero {
  position: relative;
  overflow: hidden;
  background: var(--s1);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 2.6rem 3.2rem 2.6rem;
  margin-bottom: 2rem;
}
/* Noise overlay */
.hero::after {
  content: '';
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  mix-blend-mode: overlay;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse at 10% 60%, rgba(0,245,196,.07) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 15%, rgba(77,159,255,.05) 0%, transparent 50%),
    radial-gradient(ellipse at 60% 90%, rgba(255,77,125,.04) 0%, transparent 45%);
  pointer-events: none;
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  font-family: var(--font-mono);
  font-size: .62rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--accent);
  background: rgba(0,245,196,.08);
  border: 1px solid rgba(0,245,196,.2);
  border-radius: 4px;
  padding: .22rem .7rem;
  margin-bottom: 1.1rem;
}
.hero-eyebrow::before {
  content: '';
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--accent);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { opacity: 1; transform: scale(1); }
  50%      { opacity: .4; transform: scale(.7); }
}
.hero-title {
  font-family: var(--font-head);
  font-size: 3rem;
  font-weight: 900;
  letter-spacing: -.03em;
  color: #fff;
  line-height: 1.05;
  margin: 0 0 .6rem;
}
.hero-title em {
  font-style: normal;
  background: linear-gradient(90deg, var(--accent) 0%, var(--accent3) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  color: var(--muted2);
  font-size: .95rem;
  font-weight: 400;
  max-width: 500px;
  line-height: 1.65;
  margin: 0;
}
.hero-chips {
  display: flex;
  gap: .5rem;
  margin-top: 1.4rem;
  flex-wrap: wrap;
}
.h-chip {
  font-family: var(--font-mono);
  font-size: .62rem;
  letter-spacing: .08em;
  color: var(--muted2);
  background: var(--s2);
  border: 1px solid var(--border2);
  border-radius: 20px;
  padding: .22rem .75rem;
}

/* ─────────────────────────────────────────────
   METRIC CARDS (ENHANCED)
───────────────────────────────────────────── */
.mc-row { display: flex; gap: 1.2rem; margin-bottom: 2.2rem; flex-wrap: wrap; }
.mc {
  flex: 1;
  min-width: 160px;
  background: linear-gradient(135deg, var(--s1) 0%, rgba(14,17,23,.8) 100%);
  border: 2px solid var(--border);
  border-radius: var(--r-md);
  padding: 1.8rem 1.6rem;
  position: relative;
  overflow: hidden;
  transition: border-color .3s cubic-bezier(.2,.6,.8,1), transform .3s, box-shadow .3s;
  cursor: default;
  box-shadow: 0 4px 12px rgba(0,0,0,.5);
}
.mc:hover {
  border-color: var(--accent);
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 8px 24px rgba(0,245,196,.2);
}
.mc::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
}
.mc-g::before { background: linear-gradient(90deg, var(--pos), transparent); }
.mc-b::before { background: linear-gradient(90deg, var(--accent3), transparent); }
.mc-p::before { background: linear-gradient(90deg, var(--accent2), transparent); }
.mc-y::before { background: linear-gradient(90deg, var(--warn), transparent); }
.mc-label {
  font-family: var(--font-mono);
  font-size: .65rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--muted2);
  margin-bottom: .8rem;
  font-weight: 600;
}
.mc-value {
  font-family: var(--font-head);
  font-size: 2.4rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: .4rem;
  letter-spacing: -.02em;
  animation: slideInValue .6s ease-out;
}
@keyframes slideInValue {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.mc-sub { 
  font-size: .8rem; 
  color: var(--muted2);
  font-weight: 500;
}
.mc-g .mc-value { color: var(--pos); }
.mc-b .mc-value { color: var(--accent3); }
.mc-p .mc-value { color: var(--accent2); }
.mc-y .mc-value { color: var(--warn); }

/* ─────────────────────────────────────────────
   SECTION HEADER (ENHANCED)
───────────────────────────────────────────── */
.sec {
  font-family: var(--font-head);
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text);
  margin: 2.2rem 0 1.4rem;
  display: flex;
  align-items: center;
  gap: .7rem;
  letter-spacing: -.01em;
  animation: fadeInSection .5s ease-out;
}
@keyframes fadeInSection {
  from { opacity: 0; transform: translateX(-10px); }
  to { opacity: 1; transform: translateX(0); }
}
.sec-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 10px var(--accent), 0 0 20px rgba(0,245,196,.3);
  flex-shrink: 0;
  animation: pulse 2.5s ease-in-out infinite;
}

/* ─────────────────────────────────────────────
   PANEL
───────────────────────────────────────────── */
.panel {
  background: var(--s1);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 1.3rem 1.5rem;
  margin-bottom: 1rem;
}

/* ─────────────────────────────────────────────
   TABS
───────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  gap: .35rem;
  background: var(--s1);
  border-radius: var(--r-md);
  padding: .3rem;
  border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
  font-family: var(--font-head) !important;
  font-weight: 600 !important;
  font-size: .85rem !important;
  color: var(--muted2) !important;
  background: transparent !important;
  border-radius: var(--r-sm) !important;
  padding: .4rem 1.1rem !important;
  transition: all .2s !important;
  border: none !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--accent), #00c9a0) !important;
  color: #07080d !important;
  box-shadow: 0 2px 12px rgba(0,245,196,.25) !important;
}

/* ─────────────────────────────────────────────
   BUTTONS
───────────────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, var(--accent), #00c9a0) !important;
  color: #07080d !important;
  font-family: var(--font-head) !important;
  font-weight: 700 !important;
  font-size: .88rem !important;
  border: none !important;
  border-radius: var(--r-sm) !important;
  padding: .55rem 1.6rem !important;
  letter-spacing: .02em !important;
  transition: opacity .2s, transform .15s !important;
  box-shadow: 0 4px 16px rgba(0,245,196,.18) !important;
}
.stButton > button:hover {
  opacity: .88 !important;
  transform: translateY(-1px) !important;
}

/* ─────────────────────────────────────────────
   INPUTS
───────────────────────────────────────────── */
.stTextArea textarea,
.stTextInput input {
  background: var(--s2) !important;
  border: 1px solid var(--border2) !important;
  color: var(--text) !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--font-head) !important;
  transition: border-color .2s !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(0,245,196,.12) !important;
}
.stSelectbox > div > div {
  background: var(--s2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--r-sm) !important;
  color: var(--text) !important;
}

/* ─────────────────────────────────────────────
   PREDICTION RESULT (ENHANCED - PROMINENT)
───────────────────────────────────────────── */
.pred-box {
  border-radius: var(--r-lg);
  padding: 2.4rem 2.2rem;
  text-align: center;
  margin: 1.5rem 0;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,.6);
  backdrop-filter: blur(10px);
  animation: popIn .5s cubic-bezier(.34,1.56,.64,1);
  border: 2px solid;
}
@keyframes popIn {
  0% { opacity: 0; transform: scale(.9); }
  100% { opacity: 1; transform: scale(1); }
}
.pred-box::before {
  content: '';
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.08'/%3E%3C/svg%3E");
  pointer-events: none;
}
.pred-pos { 
  background: linear-gradient(135deg, rgba(0,229,160,.12) 0%, rgba(0,229,160,.04) 100%);
  border-color: rgba(0,229,160,.5);
  box-shadow: 0 8px 32px rgba(0,229,160,.15);
}
.pred-neg { 
  background: linear-gradient(135deg, rgba(255,83,112,.12) 0%, rgba(255,83,112,.04) 100%);
  border-color: rgba(255,83,112,.5);
  box-shadow: 0 8px 32px rgba(255,83,112,.15);
}
.pred-neu { 
  background: linear-gradient(135deg, rgba(176,132,255,.12) 0%, rgba(176,132,255,.04) 100%);
  border-color: rgba(176,132,255,.5);
  box-shadow: 0 8px 32px rgba(176,132,255,.15);
}
.pred-emoji { 
  font-size: 4.2rem; 
  display: block; 
  margin-bottom: .8rem;
  animation: bounce 2s ease-in-out infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}
.pred-label {
  font-family: var(--font-head);
  font-size: 3rem;
  font-weight: 950;
  letter-spacing: -.03em;
  margin-bottom: .6rem;
  text-transform: uppercase;
}
.pred-label-pos { color: var(--pos); text-shadow: 0 0 20px rgba(0,229,160,.4); }
.pred-label-neg { color: var(--neg); text-shadow: 0 0 20px rgba(255,83,112,.4); }
.pred-label-neu { color: var(--neu); text-shadow: 0 0 20px rgba(176,132,255,.4); }
.pred-meta { 
  font-size: .85rem; 
  color: var(--muted2); 
  margin-top: .6rem;
  font-weight: 500;
}

/* ─────────────────────────────────────────────
   PIPELINE STEPS
───────────────────────────────────────────── */
.steps { display: flex; gap: 0; flex-wrap: wrap; margin-bottom: 1rem; }
.step {
  display: flex;
  align-items: center;
  gap: .5rem;
  background: var(--s2);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  padding: .55rem .9rem;
  font-size: .78rem;
  color: var(--muted2);
  flex: 1;
  min-width: 90px;
  position: relative;
}
.step:not(:last-child)::after {
  content: '→';
  position: absolute;
  right: -12px;
  color: var(--muted);
  font-size: .75rem;
  z-index: 1;
}
.step-icon { font-size: 1rem; }
.step strong { color: var(--text); font-size: .78rem; display: block; }

/* ─────────────────────────────────────────────
   MODEL CARD
───────────────────────────────────────────── */
.model-cards { 
  display: flex; 
  gap: 1.2rem; 
  margin-bottom: 1.5rem; 
  flex-wrap: wrap;
}
.model-card {
  flex: 1; 
  min-width: 180px;
  background: linear-gradient(135deg, var(--s1), rgba(20,23,32,.8));
  border: 2px solid var(--border);
  border-radius: var(--r-md);
  padding: 1.6rem 1.5rem;
  transition: border-color .3s, transform .3s, box-shadow .3s;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,.4);
}
.model-card:hover { 
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 8px 24px rgba(0,0,0,.5);
}
.model-card-best { 
  border-color: var(--accent);
  box-shadow: 0 0 20px rgba(0,245,196,.2), 0 4px 12px rgba(0,0,0,.4);
}
.model-card-best::before {
  content: '★ BEST';
  display: block;
  font-family: var(--font-mono);
  font-size: .62rem;
  letter-spacing: .18em;
  color: var(--accent);
  margin-bottom: .8rem;
  font-weight: 600;
  text-transform: uppercase;
}
.model-name {
  font-weight: 800; 
  font-size: 1.05rem; 
  margin-bottom: .8rem;
  letter-spacing: -.01em;
}
.model-stat {
  display: flex; 
  justify-content: space-between;
  border-top: 1px solid var(--border);
  padding-top: .8rem; 
  margin-top: .8rem;
  gap: .6rem;
}
.model-stat-label { 
  font-family: var(--font-mono); 
  font-size: .65rem; 
  color: var(--muted2); 
  letter-spacing: .12em; 
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: .4rem;
}
.model-stat-value { 
  font-family: var(--font-head); 
  font-size: 1.4rem; 
  font-weight: 800;
  letter-spacing: -.01em;
}

/* ─────────────────────────────────────────────
   CHIP CLOUD
───────────────────────────────────────────── */
.chip-cloud { display: flex; flex-wrap: wrap; gap: .3rem; margin-bottom: .8rem; }
.chip {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: .68rem;
  color: var(--muted2);
  background: var(--s2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: .18rem .6rem;
  transition: border-color .2s;
}
.chip:hover { border-color: var(--border2); }
.chip-g { border-color: rgba(0,229,160,.25); color: var(--pos); background: rgba(0,229,160,.06); }
.chip-r { border-color: rgba(255,83,112,.25); color: var(--neg); background: rgba(255,83,112,.06); }
.chip-v { border-color: rgba(176,132,255,.25); color: var(--neu); background: rgba(176,132,255,.06); }

/* ─────────────────────────────────────────────
   DATA TABLE
───────────────────────────────────────────── */
[data-testid="stDataFrame"] { border-radius: var(--r-md); overflow: hidden; }

/* ─────────────────────────────────────────────
   PROGRESS
───────────────────────────────────────────── */
.stProgress > div > div {
  background: linear-gradient(90deg, var(--accent), var(--accent3)) !important;
  border-radius: 4px !important;
}

/* ─────────────────────────────────────────────
   FILE UPLOADER
───────────────────────────────────────────── */
[data-testid="stFileUploader"] {
  border: 2px dashed var(--border2) !important;
  border-radius: var(--r-md) !important;
  background: var(--s2) !important;
  transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent) !important; }

/* ─────────────────────────────────────────────
   EXPANDER
───────────────────────────────────────────── */
.streamlit-expanderHeader {
  font-family: var(--font-head) !important;
  font-weight: 600 !important;
  background: var(--s2) !important;
  border-radius: var(--r-sm) !important;
  color: var(--text) !important;
}

/* ─────────────────────────────────────────────
   SCROLLBAR
───────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ─────────────────────────────────────────────
   DIVIDER
───────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* ─────────────────────────────────────────────
   TOASTS / INFO / SUCCESS
───────────────────────────────────────────── */
.stAlert { border-radius: var(--r-sm) !important; }
"""

# ── HTML snippet helpers ─────────────────────────────────────────────────────

def hero_html() -> str:
    return """
<div class="hero">
  <div class="hero-eyebrow">NLP · ML PIPELINE · REAL-TIME PREDICTION</div>
  <h1 class="hero-title">Sentiment<em>IQ</em></h1>
  <p class="hero-sub">
    Upload a dataset, train three competing models,
    explore keyword patterns, and predict sentiment in real-time.
  </p>
  <div class="hero-chips">
    <span class="h-chip">TF-IDF Bigrams</span>
    <span class="h-chip">Logistic Regression</span>
    <span class="h-chip">Naive Bayes</span>
    <span class="h-chip">Linear SVM</span>
    <span class="h-chip">Keyword Insights</span>
    <span class="h-chip">Live Prediction</span>
  </div>
</div>
"""


def section(icon: str, title: str) -> str:
    return (
        f'<div class="sec"><div class="sec-dot"></div>'
        f'<span>{icon}&nbsp;&nbsp;{title}</span></div>'
    )


def metrics_row(items: list[tuple[str, str, str, str]]) -> str:
    """items: [(label, value, sub, class_suffix), ...]"""
    cards = ""
    for label, value, sub, cls in items:
        cards += f"""
        <div class="mc mc-{cls}">
          <div class="mc-label">{label}</div>
          <div class="mc-value">{value}</div>
          <div class="mc-sub">{sub}</div>
        </div>"""
    return f'<div class="mc-row">{cards}</div>'


def model_cards_html(results: dict, best_name: str) -> str:
    cards = ""
    for name, res in results.items():
        is_best = name == best_name
        cls = "model-card-best" if is_best else ""
        clr = {"Logistic Regression": "#00f5c4",
               "Naive Bayes": "#ff4d7d",
               "Linear SVM": "#4d9fff"}.get(name, "#00f5c4")
        cards += f"""
        <div class="model-card {cls}" style="border-top: 2px solid {clr}40;">
          <div class="model-name" style="color:{clr};">{name}</div>
          <div class="model-stat">
            <div>
              <div class="model-stat-label">Accuracy</div>
              <div class="model-stat-value" style="color:{clr};">{res['accuracy']:.3f}</div>
            </div>
            <div>
              <div class="model-stat-label">F1</div>
              <div class="model-stat-value">{res['f1']:.3f}</div>
            </div>
            <div>
              <div class="model-stat-label">Time</div>
              <div class="model-stat-value">{res['train_time']*1000:.0f}ms</div>
            </div>
          </div>
        </div>"""
    return f'<div class="model-cards">{cards}</div>'


def pipeline_steps_html() -> str:
    steps = [
        ("🧹", "Clean", "URLs, HTML, punct"),
        ("✂️", "Tokenise", "Split + stopwords"),
        ("📐", "TF-IDF", "Bigrams, 20k feat"),
        ("🔤", "Count Vec", "For Naive Bayes"),
        ("⚖️", "Split", "Stratified 80/20"),
        ("🤖", "Train", "3 models"),
        ("📊", "Evaluate", "Acc · F1 · CM"),
    ]
    inner = "".join(
        f'<div class="step"><span class="step-icon">{ic}</span>'
        f'<div><strong>{t}</strong>{d}</div></div>'
        for ic, t, d in steps
    )
    return f'<div class="steps">{inner}</div>'


def pred_result_html(pred: str, model_name: str) -> str:
    p = str(pred).lower()
    if "pos" in p:
        cls, emoji, label_cls = "pred-pos", "😊", "pred-label-pos"
    elif "neg" in p:
        cls, emoji, label_cls = "pred-neg", "😞", "pred-label-neg"
    else:
        cls, emoji, label_cls = "pred-neu", "😐", "pred-label-neu"
    return f"""
<div class="pred-box {cls}">
  <span class="pred-emoji">{emoji}</span>
  <div class="pred-label {label_cls}">{str(pred).upper()}</div>
  <div class="pred-meta">via {model_name}</div>
</div>"""


def chip_cloud_html(words: list[tuple[str, int | float]], cls_name: str) -> str:
    chip_cls = (
        "chip-g" if "pos" in cls_name else
        "chip-r" if "neg" in cls_name else
        "chip-v"
    )
    chips = " ".join(
        f'<span class="chip {chip_cls}">{w} <b>{int(c) if isinstance(c, float) and c == int(c) else f"{c:.2f}"}</b></span>'
        for w, c in words
    )
    return f'<div class="chip-cloud">{chips}</div>'


def inject_css() -> None:
    """Call once at top of app.py."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)