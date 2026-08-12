import warnings
warnings.filterwarnings("ignore")

import streamlit as st
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

show_profile_section(user)

# Profile widget (top-left transparent)

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
    st.markdown(
        '<div style="font-family:\'Outfit\',sans-serif;font-size:1.25rem;font-weight:800;'
        'color:#fff;margin-bottom:.15rem;letter-spacing:-.02em;">🧠 SentimentIQ</div>'
        '<div style="font-family:\'DM Mono\',monospace;font-size:.58rem;color:#4e5a72;'
        'letter-spacing:.15em;text-transform:uppercase;margin-bottom:1rem;">'
        'CONFIGURATION PANEL</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("**Upload Dataset**")
    uploaded = st.file_uploader(
        "CSV / TSV / XLSX", type=["csv", "tsv", "xlsx"],
        help="Must contain a text column and a sentiment label column.",
    )

    st.markdown("---")
    use_sample = st.button("📦  Load Sample Data", use_container_width=True)

    st.markdown("---")
    st.markdown("**Pipeline Settings**")
    test_size = st.slider("Test Split %", 10, 40, 20) / 100
    rm_sw     = st.toggle("Remove Stopwords",  value=True)
    rm_num    = st.toggle("Remove Numbers",    value=False)
    rm_punct  = st.toggle("Remove Punctuation",value=True)

    st.markdown("---")
    st.markdown(
        '<div style="font-size:.65rem;color:#374151;line-height:1.8;">'
        'SentimentIQ v2.0<br>'
        'LogReg · MultinomialNB · LinearSVM<br>'
        'TF-IDF + CountVec bigrams<br>'
        'Zero external NLP deps'
        '</div>',
        unsafe_allow_html=True,
    )

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
            pd.read_csv(uploaded) if ext == "csv" else
            pd.read_csv(uploaded, sep="\t") if ext == "tsv" else
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
#  NO DATA
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state.df is None:
    st.markdown(
        '<div style="text-align:center;padding:5rem 2rem;">'
        '<div style="font-size:3.5rem;margin-bottom:1rem;">📂</div>'
        '<div style="font-family:\'Outfit\',sans-serif;font-size:1.4rem;font-weight:700;'
        'color:#fff;margin-bottom:.5rem;">No dataset loaded</div>'
        '<div style="color:#4e5a72;font-size:.9rem;max-width:380px;margin:0 auto;line-height:1.6;">'
        'Upload a CSV / TSV / XLSX via the sidebar, or click '
        '<strong style="color:#00f5c4;">Load Sample Data</strong> to explore instantly.'
        '</div></div>',
        unsafe_allow_html=True,
    )
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
#  COLUMN SELECTION (auto or manual)
# ═══════════════════════════════════════════════════════════════════════════
df   = st.session_state.df
cols = list(df.columns)

if not (
    st.session_state.text_col and st.session_state.label_col and
    st.session_state.text_col in cols and st.session_state.label_col in cols
):
    st.markdown(section("🗂️", "Column Mapping"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        tc = st.selectbox("Text column",  cols, index=0)
    with c2:
        lc = st.selectbox("Label column", cols, index=min(1, len(cols)-1))
    if st.button("Confirm columns →"):
        st.session_state.text_col  = tc
        st.session_state.label_col = lc
        st.rerun()
    st.stop()

text_col  = st.session_state.text_col
label_col = st.session_state.label_col

# Clean & normalise
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
        ("Total Records",   f"{len(df):,}",       "in dataset",            "g"),
        ("Classes",         str(len(classes)),     ", ".join(classes),      "b"),
        ("Avg Token Length",str(avg_len),          "words per sample",      "p"),
        ("Dominant Class",  vc.index[0] if len(vc) else "—",
                            f"{vc.iloc[0]:,} samples" if len(vc) else "",   "y"),
    ]),
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════════
#  TABS
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
# if st.button("🚪 Logout", key="logout_btn", help="Logout", use_container_width=True):
#     logout()
#     st.rerun()

st.markdown(
    '<hr>'
    '<div style="text-align:center;font-family:\'DM Mono\',monospace;'
    'font-size:.62rem;color:#1c2030;padding:.8rem 0;">'
    f'SENTIMENTIQ v2.0 · STREAMLIT · SCIKIT-LEARN · Logged in as {user["username"] if user else "Guest"}'
    '</div>',
    unsafe_allow_html=True,
)
