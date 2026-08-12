import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from core.pipeline import normalise_labels, make_sample_data
from ui.styles import inject_css, hero_html, section, metrics_row
from ui.tabs import (
    render_data_explorer,
    render_model_training,
    render_performance,
    render_keyword_insights,
    render_predictions,
    render_live_predict,
)
from auth import get_current_user, show_auth_ui, show_profile_section, logout

# ═══════════════════════════════════════════════════════════════════════════
#  AUTHENTICATION CHECK
# ═══════════════════════════════════════════════════════════════════════════
user = get_current_user()
if not user:
    show_auth_ui()

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SentimentIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ═══════════════════════════════════════════════════════════════════════════
#  SIDEBAR FIX — force toggle always visible + clear collapsed localStorage
# ═══════════════════════════════════════════════════════════════════════════
components.html("""
<script>
  // Clear Streamlit's saved sidebar collapsed state so it always opens expanded
  try {
    const keys = Object.keys(localStorage);
    keys.forEach(k => {
      if (k.toLowerCase().includes('sidebar')) {
        localStorage.removeItem(k);
      }
    });
  } catch(e) {}
</script>
""", height=0)

st.markdown("""
<style>
/* ── Always show the sidebar collapse/expand arrow ── */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999 !important;
}

/* Make toggle arrow pop with brand colour */
[data-testid="collapsedControl"] svg {
    color: #00f5c4 !important;
    fill: #00f5c4 !important;
}

/* Ensure collapsed sidebar never fully disappears */
section[data-testid="stSidebar"][aria-expanded="false"] {
    margin-left: 0 !important;
}

/* ── Sidebar background & scrollbar ── */
section[data-testid="stSidebar"] {
    background: #0b0f1a !important;
    border-right: 0.5px solid #1a2235 !important;
}
section[data-testid="stSidebar"]::-webkit-scrollbar {
    width: 4px;
}
section[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
    background: #1e2d45;
    border-radius: 99px;
}

/* ── File uploader refinement ── */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #0d1525 !important;
    border: 1px dashed #2a3a5c !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] label {
    color: #4e5a72 !important;
    font-size: .72rem !important;
}

/* ── Slider accent colour ── */
section[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {
    background: #00f5c4 !important;
    border-color: #00f5c4 !important;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div {
    background: #00f5c4 !important;
}

/* ── Toggle accent ── */
section[data-testid="stSidebar"] [data-testid="stToggle"] input:checked + div {
    background: #00c49a !important;
}

/* ── Sample data button style ── */
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #00f5c4 0%, #0080ff 100%) !important;
    color: #050810 !important;
    font-weight: 700 !important;
    font-size: .78rem !important;
    border: none !important;
    border-radius: 7px !important;
    letter-spacing: .02em !important;
    transition: opacity .15s, transform .1s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    opacity: .9 !important;
    transform: translateY(-1px) !important;
}
section[data-testid="stSidebar"] .stButton > button:active {
    transform: translateY(0px) scale(.98) !important;
}

/* ── Divider colour ── */
section[data-testid="stSidebar"] hr {
    border-color: #1a2235 !important;
    margin: .6rem 0 !important;
}
</style>
""", unsafe_allow_html=True)

show_profile_section(user)

# ═══════════════════════════════════════════════════════════════════════════
#  SESSION STATE DEFAULTS
# ═══════════════════════════════════════════════════════════════════════════
_DEFAULTS = dict(
    df=None, results=None,
    text_col=None, label_col=None, classes=None,
    preproc=None, X_clean=None, X_test=None, y_test=None,
    uploaded_filename=None,
)
for k, v in _DEFAULTS.items():
    st.session_state.setdefault(k, v)

# ═══════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Brand header ──────────────────────────────────────
    st.markdown("""
    <div style="padding:.2rem 0 1rem;">
      <div style="font-family:'Outfit',sans-serif;font-size:1.2rem;font-weight:800;
        color:#fff;letter-spacing:-.02em;display:flex;align-items:center;gap:8px;">
        🧠 SentimentIQ
      </div>
      <div style="font-family:'DM Mono',monospace;font-size:.57rem;color:#3d4a63;
        letter-spacing:.15em;text-transform:uppercase;margin-top:4px;">
        Configuration Panel
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Upload Dataset ────────────────────────────────────
    st.markdown("""
    <p style="font-family:'DM Mono',monospace;font-size:.63rem;color:#4e5a72;
      text-transform:uppercase;letter-spacing:.12em;margin-bottom:.5rem;font-weight:600;">
      📁 &nbsp;Upload Dataset
    </p>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "CSV / TSV / XLSX",
        type=["csv", "tsv", "xlsx"],
        help="Must contain a text column and a sentiment label column.",
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

    use_sample = st.button("📦  Load Sample Data", use_container_width=True)

    st.divider()

    # ── Pipeline Settings ─────────────────────────────────
    st.markdown("""
    <p style="font-family:'DM Mono',monospace;font-size:.63rem;color:#4e5a72;
      text-transform:uppercase;letter-spacing:.12em;margin-bottom:.75rem;font-weight:600;">
      ⚙️ &nbsp;Pipeline Settings
    </p>
    """, unsafe_allow_html=True)

    test_size = st.slider(
        "Test Split %", 10, 40, 20,
        help="Percentage of data held out for evaluation."
    ) / 100

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    # ── Preprocessing Toggles ─────────────────────────────
    st.markdown("""
    <p style="font-family:'DM Mono',monospace;font-size:.63rem;color:#4e5a72;
      text-transform:uppercase;letter-spacing:.12em;margin-bottom:.5rem;font-weight:600;">
      🔧 &nbsp;Preprocessing
    </p>
    """, unsafe_allow_html=True)

    rm_sw    = st.toggle("Remove Stopwords",    value=True)
    rm_num   = st.toggle("Remove Numbers",      value=False)
    rm_punct = st.toggle("Remove Punctuation",  value=True)

    st.divider()

    # ── Footer stack ──────────────────────────────────────
    st.markdown("""
    <div style="font-family:'DM Mono',monospace;font-size:.6rem;
      color:#2a3a5c;line-height:2.1;padding-bottom:.5rem;">
      <span style="color:#3d4a63;">SentimentIQ v2.0</span><br>
      <span style="color:#1e3a55;background:#0d1622;padding:2px 7px;border-radius:4px;
        border:0.5px solid #1a3555;margin:2px 1px;display:inline-block;">LogReg</span>
      <span style="color:#1e3a55;background:#0d1622;padding:2px 7px;border-radius:4px;
        border:0.5px solid #1a3555;margin:2px 1px;display:inline-block;">MultinomialNB</span>
      <span style="color:#1e3a55;background:#0d1622;padding:2px 7px;border-radius:4px;
        border:0.5px solid #1a3555;margin:2px 1px;display:inline-block;">LinearSVM</span><br>
      <span style="color:#1e3a55;background:#0d1622;padding:2px 7px;border-radius:4px;
        border:0.5px solid #1a3555;margin:2px 1px;display:inline-block;">TF-IDF</span>
      <span style="color:#1e3a55;background:#0d1622;padding:2px 7px;border-radius:4px;
        border:0.5px solid #1a3555;margin:2px 1px;display:inline-block;">CountVec</span>
      <span style="color:#1e3a55;background:#0d1622;padding:2px 7px;border-radius:4px;
        border:0.5px solid #1a3555;margin:2px 1px;display:inline-block;">bigrams</span><br>
      <span style="color:#2a3a5c;">Zero external NLP deps</span>
    </div>
    """, unsafe_allow_html=True)

sidebar_cfg = dict(test_size=test_size, rm_sw=rm_sw, rm_num=rm_num, rm_punct=rm_punct)

# ═══════════════════════════════════════════════════════════════════════════
#  DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════
if use_sample:
    st.session_state.df        = make_sample_data()
    st.session_state.text_col  = "text"
    st.session_state.label_col = "sentiment"
    st.session_state.results   = None
    st.toast("Sample dataset loaded!", icon="📦")

if uploaded and not use_sample:
    is_new = (st.session_state.uploaded_filename != uploaded.name)
    try:
        ext = uploaded.name.rsplit(".", 1)[-1].lower()
        df_loaded = (
            pd.read_csv(uploaded)         if ext == "csv"  else
            pd.read_csv(uploaded, sep="\t") if ext == "tsv"  else
            pd.read_excel(uploaded)
        )
        st.session_state.df = df_loaded
        st.session_state.uploaded_filename = uploaded.name
        if is_new:
            st.session_state.results = None
            st.toast(f"Loaded `{uploaded.name}` — {len(df_loaded):,} rows", icon="✅")
    except Exception as e:
        st.error(f"Could not load file: {e}")

# ═══════════════════════════════════════════════════════════════════════════
#  HERO
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(hero_html(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  NO DATA STATE
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state.df is None:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;">
      <div style="font-size:3.5rem;margin-bottom:1rem;">📂</div>
      <div style="font-family:'Outfit',sans-serif;font-size:1.4rem;font-weight:700;
        color:#fff;margin-bottom:.5rem;">No dataset loaded</div>
      <div style="color:#4e5a72;font-size:.9rem;max-width:380px;margin:0 auto;line-height:1.6;">
        Upload a <strong style="color:#00f5c4;">CSV / TSV / XLSX</strong> via the sidebar,
        or click <strong style="color:#00f5c4;">Load Sample Data</strong> to explore instantly.
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
#  COLUMN SELECTION (auto or manual)
# ═══════════════════════════════════════════════════════════════════════════
df   = st.session_state.df
cols = list(df.columns)

if not (
    st.session_state.text_col  and st.session_state.label_col and
    st.session_state.text_col  in cols and
    st.session_state.label_col in cols
):
    st.markdown(section("🗂️", "Column Mapping"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        tc = st.selectbox("Text column",  cols, index=0)
    with c2:
        lc = st.selectbox("Label column", cols, index=min(1, len(cols) - 1))
    if st.button("Confirm columns →"):
        st.session_state.text_col  = tc
        st.session_state.label_col = lc
        st.rerun()
    st.stop()

text_col  = st.session_state.text_col
label_col = st.session_state.label_col

# ── Clean & normalise ─────────────────────────────────────────────────────
df = df.dropna(subset=[text_col, label_col]).copy()
df[text_col]  = df[text_col].astype(str)
df[label_col] = normalise_labels(df[label_col])
classes = sorted(df[label_col].unique().tolist())
st.session_state.classes = classes

# ═══════════════════════════════════════════════════════════════════════════
#  OVERVIEW METRICS (always visible)
# ═══════════════════════════════════════════════════════════════════════════
vc      = df[label_col].value_counts()
avg_len = int(df[text_col].str.split().str.len().mean())
st.markdown(
    metrics_row([
        ("Total Records",    f"{len(df):,}",   "in dataset",            "g"),
        ("Classes",          str(len(classes)), ", ".join(classes),      "b"),
        ("Avg Token Length", str(avg_len),      "words per sample",      "p"),
        ("Dominant Class",
            vc.index[0] if len(vc) else "—",
            f"{vc.iloc[0]:,} samples" if len(vc) else "",               "y"),
    ]),
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════════
#  TABSdir

# ═══════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "📊  Data Explorer",
    "🤖  Model Training",
    "📈  Performance",
    "🔑  Keyword Insights",
    "🎯  Predictions",
    "⚡  Live Predict",
])

with tabs[0]:
    render_data_explorer(df, text_col, label_col)

with tabs[1]:
    render_model_training(df, text_col, label_col, classes, sidebar_cfg)

with tabs[2]:
    if st.session_state.results is None:
        st.info("Train models in the **Model Training** tab first.")
    else:
        render_performance(st.session_state.results, classes)

with tabs[3]:
    if st.session_state.results is None or st.session_state.preproc is None:
        st.info("Train models first to unlock keyword insights.")
    else:
        render_keyword_insights(
            df, text_col, label_col, classes,
            st.session_state.results, st.session_state.preproc,
        )

with tabs[4]:
    if st.session_state.results is None or st.session_state.preproc is None:
        st.info("Train models first to generate predictions.")
    else:
        render_predictions(
            df, text_col, label_col,
            st.session_state.results, st.session_state.preproc,
        )

with tabs[5]:
    if st.session_state.results is None or st.session_state.preproc is None:
        st.info("Train models first to enable live prediction.")
    else:
        render_live_predict(
            st.session_state.results, classes, st.session_state.preproc
        )

# ═══════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    "<hr>"
    "<div style=\"text-align:center;font-family:'DM Mono',monospace;"
    "font-size:.62rem;color:#1c2030;padding:.8rem 0;\">"
    f"SENTIMENTIQ v2.0 · STREAMLIT · SCIKIT-LEARN · "
    f"Logged in as {user['username'] if user else 'Guest'}"
    "</div>",
    unsafe_allow_html=True,
)