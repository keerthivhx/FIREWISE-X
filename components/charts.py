"""
Plotly Scientific Visualizations Component for FIREWISE-X
Professional space-science aesthetics, neon palettes, physical reference thresholds, and dark glass styling.
"""

from typing import Optional, List
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Deep-Space Chart Styling
CHART_THEME = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(10, 16, 35, 0.6)",
    "font": {"color": "#e2e8f0", "family": "Inter, -apple-system, sans-serif"},
    "margin": dict(l=50, r=30, t=55, b=50),
    "xaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.07)",
        "zerolinecolor": "rgba(0, 210, 255, 0.3)",
        "tickfont": {"color": "#94a3b8", "size": 11}
    },
    "yaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.07)",
        "zerolinecolor": "rgba(0, 210, 255, 0.3)",
        "tickfont": {"color": "#94a3b8", "size": 11}
    }
}

PALETTE = ["#00d2ff", "#ff6b4a", "#20bf6b", "#f7b731", "#a55eea", "#fd79a8", "#38ef7d"]

def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    hover_name: Optional[str] = None,
    title: str = "Combustion Parameter Scatter",
    add_trendline: bool = False
) -> go.Figure:
    """Creates a high-contrast scatter plot for physical variables with optional pure-NumPy trendline."""
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        hover_name=hover_name,
        color_discrete_sequence=PALETTE,
        title=f"<b>{title}</b>",
        template="plotly_dark"
    )
    fig.update_layout(**CHART_THEME)
    fig.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=1, color="rgba(255,255,255,0.4)")))

    # Pure NumPy linear regression trendline (Zero statsmodels dependency)
    if add_trendline and len(df) >= 3 and x_col in df.columns and y_col in df.columns:
        x_s = pd.to_numeric(df[x_col], errors="coerce")
        y_s = pd.to_numeric(df[y_col], errors="coerce")
        mask = x_s.notna() & y_s.notna()
        if mask.sum() >= 3 and x_s[mask].std() > 1e-9:
            x_arr = x_s[mask].to_numpy(dtype=float)
            y_arr = y_s[mask].to_numpy(dtype=float)
            try:
                m, b = np.polyfit(x_arr, y_arr, 1)
                y_pred = m * x_arr + b
                ss_res = float(np.sum((y_arr - y_pred) ** 2))
                ss_tot = float(np.sum((y_arr - np.mean(y_arr)) ** 2))
                r2 = max(0.0, 1.0 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0

                sort_idx = np.argsort(x_arr)
                fig.add_trace(
                    go.Scatter(
                        x=x_arr[sort_idx],
                        y=y_pred[sort_idx],
                        mode="lines",
                        name=f"OLS Trend (R²={r2:.2f})",
                        line=dict(color="#00d2ff", width=2, dash="dash"),
                        hoverinfo="text",
                        hovertext=f"OLS: y = {m:.3f}x + {b:.2f} (R²={r2:.3f})"
                    )
                )
            except Exception:
                pass

    # Add physical threshold reference lines if relevant
    if "o2" in y_col.lower() or "o2" in x_col.lower():
        if "o2" in y_col.lower():
            fig.add_hline(y=20.95, line_dash="dash", line_color="#00d2ff",
                          annotation_text="Earth Ambient O₂ (20.95%)", annotation_position="top left",
                          annotation_font_color="#00d2ff", annotation_font_size=10)
    if "co" in y_col.lower() and "co2" not in y_col.lower():
        fig.add_hline(y=50.0, line_dash="dot", line_color="#ff6b4a",
                          annotation_text="Spacecraft Caution Limit (50 ppm)", annotation_position="bottom right",
                          annotation_font_color="#ff6b4a", annotation_font_size=10)

    return fig

def create_histogram(
    df: pd.DataFrame,
    col: str,
    color_col: Optional[str] = None,
    nbins: int = 25,
    title: str = "Distribution"
) -> go.Figure:
    """Creates a scientific distribution histogram with density curve."""
    fig = px.histogram(
        df,
        x=col,
        color=color_col,
        nbins=nbins,
        color_discrete_sequence=PALETTE,
        title=f"<b>{title}</b>",
        template="plotly_dark",
        barmode="overlay",
        opacity=0.75,
        marginal="box"
    )
    fig.update_layout(**CHART_THEME)
    return fig

def create_box_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "Parametric Distribution by Category"
) -> go.Figure:
    """Creates category box & whisker plots."""
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        color_discrete_sequence=PALETTE,
        title=f"<b>{title}</b>",
        template="plotly_dark",
        points="all"
    )
    fig.update_layout(**CHART_THEME, showlegend=False)
    fig.update_traces(jitter=0.3, pointpos=-1.8, marker=dict(size=5, opacity=0.7))
    return fig

def create_correlation_heatmap(corr_df: pd.DataFrame, title: str = "Correlation Matrix (Pearson r)") -> go.Figure:
    """Generates an annotated heatmap for correlation matrices."""
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_df.values,
            x=corr_df.columns,
            y=corr_df.index,
            colorscale=[
                [0.0, "#0984e3"],
                [0.5, "#1e293b"],
                [1.0, "#ff6b4a"]
            ],
            zmin=-1.0,
            zmax=1.0,
            text=corr_df.values,
            texttemplate="%{text:.2f}",
            textfont={"size": 11, "color": "#ffffff", "family": "JetBrains Mono"}
        )
    )
    fig.update_layout(
        title=f"<b>{title}</b>",
        **CHART_THEME
    )
    return fig

def create_anomaly_scatter(
    clean_df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "Multi-Dimensional Anomaly Isolation"
) -> go.Figure:
    """Plots Isolation Forest anomaly distributions with custom high-visibility markers."""
    normal_df = clean_df[~clean_df["is_anomaly"]]
    anom_df = clean_df[clean_df["is_anomaly"]]

    fig = go.Figure()

    # Normal observations
    fig.add_trace(
        go.Scatter(
            x=normal_df[x_col],
            y=normal_df[y_col],
            mode="markers",
            name="Nominal Flight Runs",
            marker=dict(color="#00d2ff", size=8, opacity=0.75, line=dict(width=1, color="rgba(255,255,255,0.3)"))
        )
    )

    # Anomaly observations with glowing rings
    fig.add_trace(
        go.Scatter(
            x=anom_df[x_col],
            y=anom_df[y_col],
            mode="markers",
            name="Flagged Anomalies",
            marker=dict(color="#ff6b4a", size=14, symbol="diamond",
                        line=dict(width=2, color="#ffffff"))
        )
    )

    fig.update_layout(
        title=f"<b>{title}</b>",
        xaxis_title=x_col,
        yaxis_title=y_col,
        **CHART_THEME,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(14, 21, 45, 0.6)"
        )
    )
    return fig
