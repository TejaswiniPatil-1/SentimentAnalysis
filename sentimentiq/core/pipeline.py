"""
core/pipeline.py
────────────────
Single source of truth for all ML operations.
TextPreprocessor → build_pipelines → run_training → predict helpers.
Zero Streamlit imports — pure Python / sklearn.
"""

from __future__ import annotations

import re
import time
from collections import Counter
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

# ── Stopwords ────────────────────────────────────────────────────────────────
# Deliberately exclude negations + sentiment-critical words
STOPWORDS: set[str] = set("""
a about above after again against all am an and any are as at be because been
before being below between both but by cannot could did do does doing down during
each few for from further get got had has have having he her here hers herself
him himself his how i if in into is it its itself let me more most my myself of
off on once only or other our ours ourselves out over own same she should so some
such than that the their theirs them themselves then there these they this those
through to too under until up was we were what when where which while who whom why
will with would you your yours yourself yourselves
""".split())

# ── Label normalisation map ──────────────────────────────────────────────────
LABEL_MAP: dict[str, str] = {
    "0": "negative", "1": "positive", "2": "neutral",
    "neg": "negative", "pos": "positive", "neu": "neutral",
    "negative": "negative", "positive": "positive", "neutral": "neutral",
    "bad": "negative", "good": "positive", "ok": "neutral", "okay": "neutral",
    "hate": "negative", "love": "positive", "like": "positive",
    "4": "positive", "5": "positive", "3": "neutral",
}


# ═══════════════════════════════════════════════════════════════════════════
#  TEXT PREPROCESSOR
# ═══════════════════════════════════════════════════════════════════════════
class TextPreprocessor:
    """Chainable text cleaning pipeline — no external NLP libs required."""

    def __init__(
        self,
        lowercase: bool = True,
        remove_urls: bool = True,
        remove_html: bool = True,
        remove_punctuation: bool = True,
        remove_numbers: bool = False,
        remove_stopwords: bool = True,
        min_length: int = 2,
    ) -> None:
        self.lowercase = lowercase
        self.remove_urls = remove_urls
        self.remove_html = remove_html
        self.remove_punctuation = remove_punctuation
        self.remove_numbers = remove_numbers
        self.remove_stopwords = remove_stopwords
        self.min_length = min_length

    def clean(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        if self.remove_html:
            text = re.sub(r"<[^>]+>", " ", text)
        if self.remove_urls:
            text = re.sub(r"https?://\S+|www\.\S+", " ", text)
        if self.lowercase:
            text = text.lower()
        # Contraction expansion (before punctuation removal)
        for pat, repl in [
            (r"n't", " not"), (r"'re", " are"), (r"'s", " is"),
            (r"'d", " would"), (r"'ll", " will"), (r"'ve", " have"),
        ]:
            text = re.sub(pat, repl, text)
        if self.remove_punctuation:
            text = re.sub(r"[^\w\s]", " ", text)
        if self.remove_numbers:
            text = re.sub(r"\d+", " ", text)
        tokens = text.split()
        if self.remove_stopwords:
            tokens = [t for t in tokens if t not in STOPWORDS]
        tokens = [t for t in tokens if len(t) >= self.min_length]
        return " ".join(tokens)

    def transform(self, texts: List[str]) -> List[str]:
        return [self.clean(t) for t in texts]


# ═══════════════════════════════════════════════════════════════════════════
#  PIPELINE FACTORY
# ═══════════════════════════════════════════════════════════════════════════
def build_pipelines() -> Dict[str, Pipeline]:
    """Return the three competing sklearn Pipeline objects."""
    tfidf_cfg = dict(
        max_features=20_000, ngram_range=(1, 2), sublinear_tf=False,
        min_df=1, max_df=0.95, strip_accents="unicode", analyzer="word",
    )
    count_cfg = dict(
        max_features=20_000, ngram_range=(1, 2),
        min_df=1, max_df=0.95, strip_accents="unicode", analyzer="word",
    )
    return {
        "Logistic Regression": Pipeline([
            ("tfidf", TfidfVectorizer(**tfidf_cfg)),
            ("clf", LogisticRegression(
                max_iter=2000, C=5.0, solver="saga",
                class_weight="balanced", random_state=42,
            )),
        ]),
        "Naive Bayes": Pipeline([
            ("count", CountVectorizer(**count_cfg)),
            ("clf", MultinomialNB(alpha=0.5)),
        ]),
        "Linear SVM": Pipeline([
            ("tfidf", TfidfVectorizer(**tfidf_cfg)),
            ("clf", LinearSVC(
                max_iter=5000, C=1.0,
                class_weight="balanced", dual=True, random_state=42,
            )),
        ]),
    }


# ═══════════════════════════════════════════════════════════════════════════
#  TRAINING & EVALUATION
# ═══════════════════════════════════════════════════════════════════════════
TrainingResults = Dict[str, Dict]


def run_training(
    X_train: List[str],
    X_test: List[str],
    y_train: List[str],
    y_test: List[str],
    classes: List[str],
    progress_cb=None,           # optional callable(frac, msg)
) -> TrainingResults:
    """
    Train all three pipelines; return per-model metrics dict.
    progress_cb receives (fraction 0-1, message str) for UI feedback.
    """
    pipes = build_pipelines()
    results: TrainingResults = {}
    n = len(pipes)

    for i, (name, pipe) in enumerate(pipes.items()):
        if progress_cb:
            progress_cb(i / n, f"Training {name}…")
        t0 = time.time()
        pipe.fit(X_train, y_train)
        elapsed = time.time() - t0

        y_pred = pipe.predict(X_test)
        results[name] = dict(
            pipeline=pipe,
            accuracy=accuracy_score(y_test, y_pred),
            f1=f1_score(y_test, y_pred, average="weighted", zero_division=0),
            precision=precision_score(y_test, y_pred, average="weighted", zero_division=0),
            recall=recall_score(y_test, y_pred, average="weighted", zero_division=0),
            confusion_matrix=confusion_matrix(y_test, y_pred, labels=classes),
            report=classification_report(y_test, y_pred, output_dict=True, zero_division=0),
            train_time=elapsed,
            y_pred=y_pred,
        )
        if progress_cb:
            progress_cb((i + 1) / n, f"✓ {name}  {results[name]['accuracy']:.1%}")

    return results


# ═══════════════════════════════════════════════════════════════════════════
#  INFERENCE HELPERS
# ═══════════════════════════════════════════════════════════════════════════
def predict_live(
    text: str, pipeline: Pipeline, preproc: TextPreprocessor, classes: List[str]
) -> Tuple[str, Optional[pd.DataFrame]]:
    """
    Returns (predicted_label, confidence_dataframe | None).
    confidence_dataframe has columns: class, score, pct.
    """
    cleaned = preproc.clean(text)
    pred = pipeline.predict([cleaned])[0]
    conf_df = None

    try:
        clf = pipeline.named_steps["clf"]
        cls_names = list(clf.classes_) if hasattr(clf, "classes_") else classes

        # Step 1: try predict_proba on the full pipeline
        if hasattr(pipeline, "predict_proba"):
            proba = pipeline.predict_proba([cleaned])[0]
        elif hasattr(clf, "decision_function"):
            # extract the vectoriser step (may be named 'tfidf' or 'count')
            vec_step = next(
                v for k, v in pipeline.named_steps.items() if k != "clf"
            )
            raw = clf.decision_function(vec_step.transform([cleaned]))[0]
            raw = np.atleast_1d(raw)
            exp = np.exp(raw - raw.max())
            proba = exp / exp.sum()
        else:
            proba = None

        if proba is not None:
            conf_df = pd.DataFrame({
                "class": cls_names,
                "score": proba,
                "pct": [f"{p:.1%}" for p in proba],
            }).sort_values("score", ascending=False).reset_index(drop=True)

    except Exception:
        pass

    return str(pred), conf_df


def predict_batch(
    df: pd.DataFrame,
    text_col: str,
    label_col: str,
    pipeline: Pipeline,
    preproc: TextPreprocessor,
    n: int = 15,
) -> pd.DataFrame:
    """Return a sample prediction DataFrame with correct/incorrect flag."""
    sample = df.sample(min(n, len(df)), random_state=42).copy()
    cleaned = preproc.transform(sample[text_col].tolist())
    sample["predicted"] = pipeline.predict(cleaned)
    sample["correct"] = (
        sample[label_col].astype(str) == sample["predicted"].astype(str)
    )
    return sample[[text_col, label_col, "predicted", "correct"]].reset_index(drop=True)


# ═══════════════════════════════════════════════════════════════════════════
#  KEYWORD / FEATURE IMPORTANCE
# ═══════════════════════════════════════════════════════════════════════════
def top_words(texts: List[str], n: int = 30) -> List[Tuple[str, int]]:
    c: Counter = Counter()
    for t in texts:
        c.update(t.split())
    return c.most_common(n)


def model_feature_importance(
    pipeline: Pipeline, classes: List[str], n: int = 15
) -> Dict[str, List[Tuple[str, float]]]:
    """
    Extract top-n predictive tokens per class from LR coefficients
    or NB log-probabilities.  Handles both 'tfidf' and 'count' step names.
    """
    vec = next(
        (v for k, v in pipeline.named_steps.items() if k != "clf"), None
    )
    clf = pipeline.named_steps["clf"]
    if vec is None:
        return {}
    try:
        features = np.array(vec.get_feature_names_out())
    except Exception:
        return {}

    result: Dict[str, List[Tuple[str, float]]] = {}

    if hasattr(clf, "coef_"):
        coef = clf.coef_
        if coef.shape[0] == 1:
            coef = np.vstack([-coef, coef])
        for i, cls in enumerate(classes[: coef.shape[0]]):
            idx = np.argsort(coef[i])[::-1][:n]
            result[cls] = [(features[j], float(coef[i][j])) for j in idx]

    elif hasattr(clf, "feature_log_prob_"):
        for i, cls in enumerate(classes[: clf.feature_log_prob_.shape[0]]):
            idx = np.argsort(clf.feature_log_prob_[i])[::-1][:n]
            result[cls] = [
                (features[j], float(clf.feature_log_prob_[i][j])) for j in idx
            ]

    return result


# ═══════════════════════════════════════════════════════════════════════════
#  DATA UTILITIES
# ═══════════════════════════════════════════════════════════════════════════
def normalise_labels(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().map(
        lambda x: LABEL_MAP.get(x, x)
    )


def make_sample_data() -> pd.DataFrame:
    pos = [
        "This product is absolutely fantastic and exceeded all my expectations!",
        "I loved every moment of using this service, highly recommend it.",
        "Outstanding quality and superb customer support throughout.",
        "Brilliant! Works perfectly and looks amazing too.",
        "Incredibly useful tool that saved me hours every week.",
        "Best purchase I have made in years, completely satisfied.",
        "Wonderful experience from start to finish, will buy again.",
        "Exceeded expectations in every way possible, great value.",
        "Five stars! Exactly what I needed and more.",
        "Phenomenal product, the quality is second to none.",
        "Very happy with my purchase, fast shipping and great packaging.",
        "Absolutely love it, does everything as advertised.",
        "Smooth, fast and reliable. Could not ask for more.",
        "The team was very helpful and the product works great.",
        "Exceptional quality. I would 100% recommend this to anyone.",
        "Delightful experience overall, very pleased with the result.",
        "Works like a charm! Totally worth every penny spent.",
        "Impressive performance right out of the box.",
        "This is everything I hoped for and then some.",
        "Perfect in every way. My whole family loves it.",
    ]
    neg = [
        "Terrible product, broke after two days of normal use.",
        "Extremely disappointed with the quality, waste of money.",
        "The worst customer service I have ever experienced.",
        "Do not buy this, completely useless and overpriced.",
        "Stopped working after a week, very frustrating experience.",
        "Poor build quality, feels cheap and looks nothing like pictures.",
        "I regret this purchase entirely, should have read reviews first.",
        "Awful! Returned immediately after opening, very disappointed.",
        "Defective product and impossible to get a refund.",
        "Misleading description, nothing like what was advertised.",
        "Absolutely terrible, I would give zero stars if I could.",
        "Broke on first use. The worst product I have ever bought.",
        "Super slow delivery and the item arrived damaged.",
        "Does not work as described, completely let down.",
        "Useless product, total waste of time and money.",
        "Very bad quality, fell apart after minimal use.",
        "Horrible experience, will never shop here again.",
        "Completely broken out of the box. No support offered.",
        "Disappointed. Product does not match the description at all.",
        "Not worth it. The product is fragile and unreliable.",
    ]
    neu = [
        "The product is okay, nothing special but does the job.",
        "Average performance, meets basic requirements adequately.",
        "It is fine, neither great nor terrible in any way.",
        "Decent product for the price, some minor issues.",
        "Mixed feelings about this, some good parts and some bad.",
        "It works as advertised but there is not much to write about.",
        "Pretty standard, similar to other options on the market.",
        "Acceptable but I expected something a bit better.",
        "Not bad but not great either, fairly average overall.",
        "Got the job done but nothing to be excited about.",
        "It is okay. I have seen better but also worse.",
        "Serviceable product, meets minimum expectations.",
        "Moderate quality, some features work well others do not.",
        "It is fine for occasional use but not ideal long term.",
        "Mediocre at best, there are better alternatives available.",
        "Works sometimes, performance is a bit inconsistent.",
        "Nothing remarkable, just an ordinary everyday product.",
        "Adequate for basic tasks but lacks advanced features.",
        "Typical product, nothing stands out positively or negatively.",
        "Middle of the road experience, would not strongly recommend.",
    ]
    rows = (
        [(t, "positive") for t in pos]
        + [(t, "negative") for t in neg]
        + [(t, "neutral") for t in neu]
    )
    np.random.seed(42)
    np.random.shuffle(rows)
    return pd.DataFrame(rows, columns=["text", "sentiment"])