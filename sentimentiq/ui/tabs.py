"""
ui/tabs.py
──────────
One render_* function per tab.  Each function receives only what it needs
from session state — no global imports of st at module level would be needed,
but Streamlit must be imported locally to keep things clear.

Functions:
  render_data_explorer(df, text_col, label_col)
  render_model_training(df, text_col, label_col, classes, sidebar_cfg)
  render_performance(results, classes)
  render_keyword_insights(df, text_col, label_col, classes, results, preproc)
  render_predictions(df, text_col, label_col, results, preproc)
  render_live_predict(results, classes, preproc)
"""

from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split

from core.pipeline import (
    TextPreprocessor, predict_batch, predict_live,
    run_training, top_words, model_feature_importance,
)
from core.charts import (
    plot_class_dist, plot_text_length, plot_model_comparison,
    plot_radar, plot_confusion, plot_word_bar,
    plot_train_time, plot_confidence_bars, C,
)
from ui.styles import (
    section, metrics_row, model_cards_html,
    pipeline_steps_html, pred_result_html, chip_cloud_html,
)

_CFG = dict(displayModeBar=False, responsive=True)

_LABEL_COLOR = {"positive": C["pos"], "negative": C["neg"], "neutral": C["neu"]}
def _lc(l: str) -> str:
    l = str(l).lower()
    for k, v in _LABEL_COLOR.items():
        if k in l:
            return v
    return C["accent3"]


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · DATA EXPLORER
# ─────────────────────────────────────────────────────────────────────────────
def render_data_explorer(df: pd.DataFrame, text_col: str, label_col: str) -> None:
    st.markdown(section("📊", "Dataset Overview"), unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:rgba(77,159,255,.06);border:1px solid rgba(77,159,255,.25);border-radius:12px;padding:1.2rem;margin-bottom:1.5rem;">
      <div style="font-weight:700;color:#4d9fff;margin-bottom:.5rem;font-size:1rem;">📋 About Your Dataset</div>
      <div style="color:var(--muted2);font-size:.9rem;line-height:1.6;">
        Below you'll see the distribution of sentiment classes and the text length analysis. 
        These visualizations help understand your data before training models.
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.plotly_chart(plot_class_dist(df, label_col),
                        use_container_width=True, config=_CFG)
    with c2:
        st.plotly_chart(plot_text_length(df, text_col, label_col),
                        use_container_width=True, config=_CFG)

    st.markdown(section("🗂️", "Sample Records"), unsafe_allow_html=True)
    n = st.slider("Rows to preview", 5, 50, 10, key="explorer_n")
    st.dataframe(df[[text_col, label_col]].head(n),
                 use_container_width=True, height=280, hide_index=True)

    with st.expander("📋 Column Statistics"):
        st.dataframe(df.describe(include="all"), use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · MODEL TRAINING
# ─────────────────────────────────────────────────────────────────────────────
def render_model_training(
    df: pd.DataFrame,
    text_col: str,
    label_col: str,
    classes: List[str],
    sidebar_cfg: Dict,
) -> None:
    st.markdown(section("🔧", "Pipeline Architecture"), unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:rgba(0,245,196,.06);border:1px solid rgba(0,245,196,.25);border-radius:12px;padding:1.3rem;margin-bottom:1.5rem;">
      <div style="font-weight:700;color:#00f5c4;margin-bottom:.6rem;font-size:1rem;">⚙️ Training Process</div>
      <div style="color:var(--muted2);font-size:.9rem;line-height:1.6;">
        Your data will be preprocessed, split into training (80%) and testing (20%), and then three different ML models 
        will be trained in parallel. This typically takes 30-60 seconds depending on dataset size.
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(pipeline_steps_html(), unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="panel" style="font-family:var(--font-mono);font-size:.8rem;
             color:var(--muted2);line-height:2;border-left:2px solid var(--accent);">
          <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
            <div><span style="color:var(--accent);font-weight:600;">●</span> Test Split → {sidebar_cfg['test_size']:.0%}</div>
            <div><span style="color:var(--accent);font-weight:600;">●</span> Stopwords → {'enabled' if sidebar_cfg['rm_sw'] else 'disabled'}</div>
            <div><span style="color:var(--accent);font-weight:600;">●</span> Numbers → {'removed' if sidebar_cfg['rm_num'] else 'kept'}</div>
            <div><span style="color:var(--accent);font-weight:600;">●</span> Punctuation → {'removed' if sidebar_cfg['rm_punct'] else 'kept'}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🚀  Run Training Pipeline", key="train_btn"):
        preproc = TextPreprocessor(
            remove_stopwords=sidebar_cfg["rm_sw"],
            remove_numbers=sidebar_cfg["rm_num"],
            remove_punctuation=sidebar_cfg["rm_punct"],
        )

        with st.spinner("Preprocessing text…"):
            X_clean = preproc.transform(df[text_col].tolist())
            y = df[label_col].tolist()

        X_train, X_test, y_train, y_test = train_test_split(
            X_clean, y,
            test_size=sidebar_cfg["test_size"],
            random_state=42,
            stratify=y,
        )

        _bar = st.progress(0)

        def _progress(frac: float, msg: str) -> None:
            _bar.progress(frac, text=msg)

        results = run_training(X_train, X_test, y_train, y_test, classes, _progress)
        _bar.empty()

        # Persist to session
        st.session_state.results = results
        st.session_state.X_clean = X_clean
        st.session_state.X_test = X_test
        st.session_state.y_test = y_test
        st.session_state.preproc = preproc

        best = max(results, key=lambda k: results[k]["accuracy"])
        st.success(
            f"✅ Pipeline complete!  Best → **{best}** "
            f"({results[best]['accuracy']:.1%} accuracy)"
        )

    if st.session_state.get("results") is None:
        st.info("Configure options in the sidebar, then click **Run Training Pipeline**.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────
def render_performance(results: Dict, classes: List[str]) -> None:
    best_name = max(results, key=lambda k: results[k]["accuracy"])
    best = results[best_name]

    # Performance overview
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(0,245,196,.08),rgba(77,159,255,.08));border:1px solid rgba(0,245,196,.25);border-radius:12px;padding:1.4rem;margin-bottom:1.8rem;">
      <div style="font-weight:700;color:#00f5c4;margin-bottom:.6rem;font-size:1.05rem;">📈 Model Performance Summary</div>
      <div style="color:var(--muted2);font-size:.9rem;line-height:1.6;">
        Below are the key metrics for all trained models. <strong>{}</strong> achieved the highest accuracy at <strong>{:.1%}</strong>.
        Compare their metrics to understand which model performs best for your needs.
      </div>
    </div>
    """.format(best_name, best['accuracy']), unsafe_allow_html=True)

    # Top-level metrics
    st.markdown(
        metrics_row([
            ("Best Accuracy", f"{best['accuracy']:.1%}", best_name, "g"),
            ("Best F1",       f"{best['f1']:.3f}",       "weighted", "b"),
            ("Best Precision",f"{best['precision']:.3f}","weighted", "p"),
            ("Best Recall",   f"{best['recall']:.3f}",   "weighted", "y"),
        ]),
        unsafe_allow_html=True,
    )

    # Model scorecards
    st.markdown(section("🏆", "Model Scorecards"), unsafe_allow_html=True)
    st.markdown(model_cards_html(results, best_name), unsafe_allow_html=True)

    # Charts
    st.markdown(section("📈", "Comparative Charts"), unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.plotly_chart(plot_model_comparison(results),
                        use_container_width=True, config=_CFG)
    with c2:
        st.plotly_chart(plot_radar(results),
                        use_container_width=True, config=_CFG)

    st.plotly_chart(plot_train_time(results),
                    use_container_width=True, config=_CFG)

    # Confusion matrices
    st.markdown(section("🔲", "Confusion Matrices"), unsafe_allow_html=True)
    cm_cols = st.columns(len(results), gap="small")
    for col, (name, res) in zip(cm_cols, results.items()):
        with col:
            st.plotly_chart(
                plot_confusion(res["confusion_matrix"], classes, name),
                use_container_width=True, config=_CFG,
            )

    # Per-class reports
    st.markdown(section("📋", "Classification Reports"), unsafe_allow_html=True)
    for name, res in results.items():
        with st.expander(f"📋  {name}"):
            rows = []
            for cls in classes:
                r = res["report"].get(str(cls), {})
                if r:
                    rows.append({
                        "Class":     cls,
                        "Precision": f"{r.get('precision', 0):.3f}",
                        "Recall":    f"{r.get('recall', 0):.3f}",
                        "F1":        f"{r.get('f1-score', 0):.3f}",
                        "Support":   int(r.get("support", 0)),
                    })
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 · KEYWORD INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
def render_keyword_insights(
    df: pd.DataFrame,
    text_col: str,
    label_col: str,
    classes: List[str],
    results: Dict,
    preproc: TextPreprocessor,
) -> None:
    st.markdown("""
    <div style="background:rgba(255,77,125,.06);border:1px solid rgba(255,77,125,.25);border-radius:12px;padding:1.2rem;margin-bottom:1.5rem;">
      <div style="font-weight:700;color:#ff4d7d;margin-bottom:.5rem;font-size:1rem;">🔑 Keyword Analysis</div>
      <div style="color:var(--muted2);font-size:.9rem;line-height:1.6;">
        Explore the most important words and features for each sentiment class. 
        These insights show what the models learned to distinguish between different sentiments.
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ── Word frequency bars ──────────────────────────────────────────────────
    st.markdown(section("☁️", "Top Words per Class"), unsafe_allow_html=True)
    freq_cols = st.columns(len(classes), gap="small")
    for col, cls in zip(freq_cols, classes):
        with col:
            subset = df[df[label_col] == cls][text_col].tolist()
            cleaned = preproc.transform(subset)
            tw = top_words(cleaned, 20)
            st.plotly_chart(
                plot_word_bar(tw, f"{cls.capitalize()}", _lc(cls), "frequency"),
                use_container_width=True, config=_CFG,
            )

    # ── Model feature importance ─────────────────────────────────────────────
    st.markdown(section("🔑", "Model Feature Importance"), unsafe_allow_html=True)
    for model_name, res in results.items():
        important = model_feature_importance(res["pipeline"], classes, 15)
        if not important:
            continue
        score_label = "log-probability" if model_name == "Naive Bayes" else "coefficient"
        with st.expander(f"🔑  {model_name}  —  top {score_label}s per class",
                         expanded=(model_name == "Logistic Regression")):
            imp_cols = st.columns(len(important), gap="small")
            for col, (cls, words) in zip(imp_cols, important.items()):
                with col:
                    st.plotly_chart(
                        plot_word_bar(words, cls.capitalize(), _lc(cls), score_label),
                        use_container_width=True, config=_CFG,
                    )

    # ── Chip clouds ───────────────────────────────────────────────────────────
    st.markdown(section("💠", "Keyword Cloud"), unsafe_allow_html=True)
    for cls in classes:
        subset = df[df[label_col] == cls][text_col].tolist()
        cleaned = preproc.transform(subset)
        tw = top_words(cleaned, 35)
        label_style = (
            "color:var(--pos)" if "pos" in cls else
            "color:var(--neg)" if "neg" in cls else
            "color:var(--neu)"
        )
        st.markdown(
            f'<div style="{label_style};font-weight:700;font-size:.8rem;'
            f'text-transform:uppercase;letter-spacing:.1em;margin-bottom:.35rem;">'
            f'{cls}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(chip_cloud_html(tw, cls), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 · SAMPLE PREDICTIONS
# ─────────────────────────────────────────────────────────────────────────────
def render_predictions(
    df: pd.DataFrame,
    text_col: str,
    label_col: str,
    results: Dict,
    preproc: TextPreprocessor,
) -> None:
    st.markdown(section("🎯", "Sample Predictions"), unsafe_allow_html=True)

    sel = st.selectbox("Model", list(results.keys()), key="pred_model_sel")
    n = st.slider("Number of samples", 5, 40, 15, key="pred_n")

    pipe = results[sel]["pipeline"]
    sample_df = predict_batch(df, text_col, label_col, pipe, preproc, n)

    # Style correct/incorrect rows
    def _row_style(row):
        base = "background-color: rgba(0,229,160,.07)" if row["correct"] \
               else "background-color: rgba(255,83,112,.07)"
        return [base] * len(row)

    st.dataframe(
        sample_df.style.apply(_row_style, axis=1),
        use_container_width=True,
        height=460,
        hide_index=True,
    )

    acc = sample_df["correct"].mean()
    nc = int(sample_df["correct"].sum())
    st.markdown(
        metrics_row([
            ("Sample Accuracy", f"{acc:.0%}", f"{nc}/{n} correct", "g"),
            ("Model Used", sel, f"F1: {results[sel]['f1']:.3f}", "b"),
        ]),
        unsafe_allow_html=True,
    )

    csv = sample_df.to_csv(index=False).encode()
    st.download_button("⬇️  Download predictions CSV", csv,
                       "predictions.csv", "text/csv")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 · LIVE PREDICTION
# ─────────────────────────────────────────────────────────────────────────────
def render_live_predict(
    results: Dict,
    classes: List[str],
    preproc: TextPreprocessor,
) -> None:
    st.markdown(section("⚡", "Real-time Sentiment Prediction"), unsafe_allow_html=True)

    # ── Instructions ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:rgba(0,245,196,.06);border:1px solid rgba(0,245,196,.25);border-radius:12px;padding:1.2rem;margin-bottom:1.8rem;">
      <div style="font-weight:700;color:#00f5c4;margin-bottom:.6rem;font-size:1rem;">📋 How to Use</div>
      <div style="color:var(--muted2);font-size:.9rem;line-height:1.6;">
        <strong>1.</strong> Select a model from the dropdown (each trained on the same dataset).<br>
        <strong>2.</strong> Enter your text in the box below or click a quick example.<br>
        <strong>3.</strong> Click <strong>"Analyse Sentiment"</strong> to get instant predictions and confidence scores.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c_in, c_out = st.columns([1.2, 0.8], gap="large")

    with c_in:
        st.markdown('<div style="font-weight:700;margin-bottom:.8rem;font-size:1.05rem;">⚙️ Configuration</div>', unsafe_allow_html=True)
        live_model = st.selectbox(
            "Choose Model", list(results.keys()), key="live_model_sel", help="Select which trained model to use for prediction"
        )
        
        st.markdown('<div style="font-weight:700;margin:1.2rem 0 .8rem;font-size:1.05rem;">✍️ Input Text</div>', unsafe_allow_html=True)
        user_text = st.text_area(
            "Enter text",
            placeholder="Type or paste any review, tweet, comment, feedback, or any text you want to analyze…",
            height=140,
            label_visibility="collapsed",
            key="live_text_area",
        )

        # Quick examples
        st.markdown(
            '<div style="font-size:.8rem;color:var(--muted2);margin:1.2rem 0 .6rem;font-weight:600;">💡 Quick Examples:</div>',
            unsafe_allow_html=True,
        )
        ex_cols = st.columns(3)
        examples = [
            ("😊 Positive", "This product is absolutely fantastic! Best purchase ever."),
            ("😞 Negative", "Terrible quality. Broke on first use. Complete waste."),
            ("😐 Neutral",  "It's okay, does what it says but nothing special."),
        ]
        for (lbl, txt), ec in zip(examples, ex_cols):
            with ec:
                if st.button(lbl, key=f"ex_{lbl}", use_container_width=True):
                    st.session_state["_live_example"] = txt

        # Resolve example injection
        if st.session_state.get("_live_example") and not user_text:
            user_text = st.session_state["_live_example"]

        analyse = st.button("🔍  Analyse Sentiment", key="analyse_btn",
                            use_container_width=True)

    with c_out:
        st.markdown('<div style="font-weight:700;margin-bottom:.8rem;font-size:1.05rem;">📊 Results</div>', unsafe_allow_html=True)
        if analyse and user_text and user_text.strip():
            pipe = results[live_model]["pipeline"]
            with st.spinner("🔄  Analysing your text…"):
                pred, conf_df = predict_live(user_text, pipe, preproc, classes)

            st.markdown(pred_result_html(pred, live_model), unsafe_allow_html=True)

            if conf_df is not None:
                st.markdown('<div style="font-size:.85rem;color:var(--muted2);margin:.8rem 0 .4rem;font-weight:600;text-align:center;">Confidence Breakdown</div>', unsafe_allow_html=True)
                st.plotly_chart(
                    plot_confidence_bars(conf_df),
                    use_container_width=True, config=_CFG,
                )

            with st.expander("🔍 View Preprocessed Tokens"):
                st.code(preproc.clean(user_text), language=None)

        elif analyse and not (user_text and user_text.strip()):
            st.warning("⚠️  Please enter some text to analyze.")
        else:
            st.markdown(
                '<div style="text-align:center;padding:3rem 1rem;color:var(--muted);">'
                '<div style="font-size:3.2rem;margin-bottom:1rem;">👇</div>'
                '<div style="font-size:.95rem;line-height:1.6;">Results will appear here after analysis<br>'
                '<span style="color:var(--muted2);font-size:.85rem;">Enter text on the left and click "Analyse"</span></div>'
                '</div>',
                unsafe_allow_html=True,
            )

    # ── Batch multi-line prediction ───────────────────────────────────────────
    st.markdown(section("📦", "Batch Prediction"), unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:rgba(77,159,255,.06);border:1px solid rgba(77,159,255,.25);border-radius:12px;padding:1.2rem;margin-bottom:1.2rem;">
      <div style="font-weight:700;color:#4d9fff;margin-bottom:.6rem;font-size:.95rem;">ℹ️ Batch Mode</div>
      <div style="color:var(--muted2);font-size:.85rem;">Analyze multiple texts at once. Enter one text per line below.</div>
    </div>
    """, unsafe_allow_html=True)
    
    batch_input = st.text_area(
        "One text per line",
        placeholder="I love this!\nTerrible product...\nIt's okay I guess.",
        height=120,
        label_visibility="collapsed",
        key="batch_input",
    )
    if st.button("📊  Run Batch Analysis", key="batch_btn"):
        lines = [l.strip() for l in batch_input.strip().splitlines() if l.strip()]
        if not lines:
            st.warning("⚠️  Enter at least one line of text.")
        else:
            pipe = results[live_model]["pipeline"]
            cleaned = preproc.transform(lines)
            preds = pipe.predict(cleaned)
            batch_df = pd.DataFrame({"Text": lines, "Sentiment": preds})
            st.markdown('<div style="font-weight:700;margin:.8rem 0 .4rem;">Batch Results</div>', unsafe_allow_html=True)
            st.dataframe(batch_df, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Download batch results",
                batch_df.to_csv(index=False).encode(),
                "batch_predictions.csv", "text/csv",
            )