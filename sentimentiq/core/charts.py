"""
core/charts.py
──────────────
All Plotly figure factories.
Pure functions: data in → Figure out. Zero Streamlit imports.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Design tokens ────────────────────────────────────────────────────────────
C = dict(
    bg="#07080d",
    surface="#0e1117",
    surface2="#141720",
    border="#1c2030",
    text="#dde3ef",
    muted="#4e5a72",
    accent="#00f5c4",      # neon mint
    accent2="#ff4d7d",     # hot pink
    accent3="#4d9fff",     # electric blue
    warn="#ffd166",
    pos="#00e5a0",
    neg="#ff5370",
    neu="#b084ff",
)

PALETTE = [C["accent"], C["accent2"], C["accent3"], C["warn"], C["neu"]]

BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'Outfit', 'DM Sans', sans-serif", color=C["muted"], size=12),
    margin=dict(l=12, r=12, t=44, b=12),
    colorway=PALETTE,
)

AXIS = dict(
    gridcolor=C["border"],
    linecolor=C["border"],
    tickcolor=C["muted"],
    tickfont=dict(color=C["muted"], size=11),
    zeroline=False,
)

TITLE_FONT = dict(color=C["text"], size=14, family="'Outfit', sans-serif")


def _color_for(label: str) -> str:
    l = str(label).lower()
    if "pos" in l:  return C["pos"]
    if "neg" in l:  return C["neg"]
    if "neu" in l:  return C["neu"]
    return PALETTE[abs(hash(l)) % len(PALETTE)]


def _rgba(color: str, alpha: float) -> str:
    """Convert a hex/rgb/rgba color string to rgba with the requested opacity."""
    if isinstance(color, str):
        c = color.strip()
        if c.startswith("#"):
            h = c.lstrip("#")
            if len(h) == 3:
                h = ''.join([ch * 2 for ch in h])
            if len(h) != 6:
                raise ValueError(f"Invalid hex color: {color}")
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            return f"rgba({r},{g},{b},{alpha})"
        if c.startswith("rgba("):
            inner = c[5:-1].split(",")
            if len(inner) >= 3:
                return f"rgba({inner[0].strip()},{inner[1].strip()},{inner[2].strip()},{alpha})"
        if c.startswith("rgb("):
            inner = c[4:-1].split(",")
            if len(inner) >= 3:
                return f"rgba({inner[0].strip()},{inner[1].strip()},{inner[2].strip()},{alpha})"
    raise ValueError(f"Unsupported color format for _rgba: {color}")


# ── 1. Class Distribution ────────────────────────────────────────────────────
def plot_class_dist(df: pd.DataFrame, label_col: str) -> go.Figure:
    counts = df[label_col].value_counts().reset_index()
    counts.columns = ["label", "count"]
    colors = [_color_for(l) for l in counts["label"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=counts["label"].astype(str),
        y=counts["count"],
        marker=dict(color=colors, line_width=0,
                    opacity=0.9),
        text=counts["count"],
        textposition="outside",
        textfont=dict(color=C["text"], size=12, family="'DM Mono', monospace"),
        hovertemplate="<b>%{x}</b><br>Count: %{y:,}<extra></extra>",
    ))
    fig.update_layout(
        **BASE,
        title=dict(text="Class Distribution", font=TITLE_FONT, x=0.0, xanchor="left"),
        xaxis=dict(**AXIS, categoryorder="total descending"),
        yaxis=dict(**AXIS),
        bargap=0.35,
        showlegend=False,
    )
    return fig


# ── 2. Text Length Violin ────────────────────────────────────────────────────
def plot_text_length(df: pd.DataFrame, text_col: str, label_col: str) -> go.Figure:
    df2 = df.copy()
    df2["length"] = df2[text_col].str.split().str.len()
    fig = go.Figure()
    for cls in df2[label_col].unique():
        sub = df2[df2[label_col] == cls]["length"]
        color = _color_for(str(cls))
        fig.add_trace(go.Violin(
            y=sub, name=str(cls),
            fillcolor=_rgba(color, 0.18),
            line_color=color, opacity=1,
            box_visible=True, meanline_visible=True,
            hovertemplate=f"<b>{cls}</b><br>Words: %{{y}}<extra></extra>",
        ))
    fig.update_layout(
        **BASE,
        title=dict(text="Token Length by Class", font=TITLE_FONT, x=0.0, xanchor="left"),
        yaxis=dict(**AXIS, title="word count"),
        xaxis=dict(**AXIS),
        violingap=0.3,
        showlegend=False,
    )
    return fig


# ── 3. Model Comparison Grouped Bar ─────────────────────────────────────────
def plot_model_comparison(results: Dict) -> go.Figure:
    names = list(results.keys())
    metrics = [("accuracy", "Accuracy"), ("f1", "F1"),
               ("precision", "Precision"), ("recall", "Recall")]
    colors = [C["accent"], C["accent2"], C["accent3"], C["warn"]]

    fig = go.Figure()
    for (key, label), color in zip(metrics, colors):
        vals = [results[n][key] for n in names]
        fig.add_trace(go.Bar(
            name=label, x=names, y=vals,
            marker=dict(color=color, line_width=0, opacity=0.88),
            text=[f"{v:.3f}" for v in vals],
            textposition="outside",
            textfont=dict(color=C["text"], size=10),
            hovertemplate=f"<b>%{{x}}</b><br>{label}: %{{y:.4f}}<extra></extra>",
        ))
    fig.update_layout(
        **BASE,
        barmode="group",
        title=dict(text="Model Performance", font=TITLE_FONT, x=0.0, xanchor="left"),
        xaxis=dict(**AXIS),
        yaxis=dict(**AXIS, range=[0, 1.18]),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=C["muted"])),
        bargroupgap=0.12,
    )
    return fig


# ── 4. Radar Chart ───────────────────────────────────────────────────────────
def plot_radar(results: Dict) -> go.Figure:
    cats = ["Accuracy", "F1 Score", "Precision", "Recall"]
    colors = [C["accent"], C["accent2"], C["accent3"]]
    fig = go.Figure()
    for (name, res), color in zip(results.items(), colors):
        vals = [res["accuracy"], res["f1"], res["precision"], res["recall"]]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=cats + [cats[0]],
            fill="toself",
            name=name,
            line=dict(color=color, width=2),
            fillcolor=_rgba(color, 0.10),
            opacity=0.9,
            hovertemplate="<b>%{theta}</b>: %{r:.3f}<extra></extra>",
        ))
    fig.update_layout(
        **BASE,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[0, 1], gridcolor=C["border"],
                            tickfont=dict(color=C["muted"], size=9),
                            linecolor=C["border"]),
            angularaxis=dict(gridcolor=C["border"],
                             tickfont=dict(color=C["text"], size=11),
                             linecolor=C["border"]),
        ),
        title=dict(text="Radar — All Metrics", font=TITLE_FONT, x=0.0, xanchor="left"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=C["muted"])),
    )
    return fig


# ── 5. Confusion Matrix ──────────────────────────────────────────────────────
def plot_confusion(cm, classes: List[str], model_name: str) -> go.Figure:
    fig = px.imshow(
        cm,
        x=[str(c) for c in classes],
        y=[str(c) for c in classes],
        color_continuous_scale=[[0, C["surface"]], [0.45, "#0a2a3a"], [1, C["accent"]]],
        text_auto=True, aspect="auto",
        labels=dict(x="Predicted", y="Actual"),
    )
    fig.update_traces(textfont=dict(color=C["text"], size=14, family="'DM Mono', monospace"))
    fig.update_layout(
        **BASE,
        title=dict(text=f"CM — {model_name}", font=TITLE_FONT, x=0.0, xanchor="left"),
        coloraxis_showscale=False,
        xaxis=dict(tickfont=dict(color=C["text"])),
        yaxis=dict(tickfont=dict(color=C["text"])),
    )
    return fig


# ── 6. Horizontal Word Bar ───────────────────────────────────────────────────
def plot_word_bar(words: List[Tuple[str, int | float]],
                  title: str, color: str, score_label: str = "count") -> go.Figure:
    labels = [w[0] for w in words]
    vals = [float(w[1]) for w in words]
    fig = go.Figure(go.Bar(
        x=vals[::-1], y=labels[::-1],
        orientation="h",
        marker=dict(
            color=vals[::-1],
            colorscale=[[0, C["surface2"]], [1, color]],
            line_width=0,
        ),
        hovertemplate=f"<b>%{{y}}</b><br>{score_label}: %{{x:.4f}}<extra></extra>",
    ))
    fig.update_layout(
        **BASE,
        title=dict(text=title, font=TITLE_FONT, x=0.0, xanchor="left"),
        height=400,
        xaxis=dict(**AXIS, title=score_label),
        yaxis={**AXIS, 'tickfont': dict(color=C["text"], size=10)},
    )
    return fig


# ── 7. Training Time ─────────────────────────────────────────────────────────
def plot_train_time(results: Dict) -> go.Figure:
    names = list(results.keys())
    times = [results[n]["train_time"] * 1000 for n in names]   # → ms
    colors = [C["accent"], C["accent2"], C["accent3"]]
    fig = go.Figure(go.Bar(
        x=names, y=times,
        marker=dict(color=colors, line_width=0, opacity=0.85),
        text=[f"{t:.0f} ms" for t in times],
        textposition="outside",
        textfont=dict(color=C["text"], size=11),
        hovertemplate="<b>%{x}</b><br>%{y:.1f} ms<extra></extra>",
    ))
    fig.update_layout(
        **BASE,
        title=dict(text="Training Time", font=TITLE_FONT, x=0.0, xanchor="left"),
        xaxis=dict(**AXIS),
        yaxis=dict(**AXIS, title="milliseconds"),
        showlegend=False,
        bargap=0.4,
    )
    return fig


# ── 8. Confidence Gauge (live predict) ───────────────────────────────────────
def plot_confidence_bars(conf_df: pd.DataFrame) -> go.Figure:
    """Horizontal bars for class-level confidence scores."""
    colors = [_color_for(c) for c in conf_df["class"]]
    fig = go.Figure(go.Bar(
        x=conf_df["score"].tolist(),
        y=conf_df["class"].tolist(),
        orientation="h",
        marker=dict(color=colors, line_width=0, opacity=0.85),
        text=conf_df["pct"].tolist(),
        textposition="outside",
        textfont=dict(color=C["text"], size=12, family="'DM Mono', monospace"),
        hovertemplate="<b>%{y}</b>: %{x:.4f}<extra></extra>",
    ))
    fig.update_layout(**{
        **BASE,
        'margin': dict(l=12, r=40, t=44, b=12),
        'title': dict(text="Confidence Breakdown", font=TITLE_FONT, x=0.0, xanchor="left"),
        'xaxis': dict(**AXIS, range=[0, 1.18]),
        'yaxis': {**AXIS, 'tickfont': dict(color=C["text"], size=12)},
        'height': 200,
        'showlegend': False,
    })
    return fig