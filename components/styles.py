"""
FIREWISE-X Custom Styling & Design System
Injects professional deep-space dark navy glassmorphic theme and mission-control styling.
"""

import streamlit as st

def apply_custom_theme():
    """Injects high-contrast, space-science design system into Streamlit app."""
    st.markdown(
        """
        <style>
        /* Google Fonts Import */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* Root color system */
        :root {
            --bg-void: #070b19;
            --bg-surface: #0e152d;
            --bg-surface-elevated: #141f42;
            --border-glow: rgba(0, 210, 255, 0.22);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --neon-cyan: #00d2ff;
            --neon-blue: #0077fe;
            --flame-orange: #ff6b4a;
            --flame-gold: #f7b731;
            --toxic-amber: #fa8231;
            --status-green: #20bf6b;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
        }

        /* Main application background */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #101c44 0%, #070b19 80%);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #090e21 !important;
            border-right: 1px solid rgba(0, 210, 255, 0.15) !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
        }

        /* Sidebar Navigation Links (Guarantee High Visibility) */
        [data-testid="stSidebarNav"] {
            padding: 8px 0 !important;
        }
        [data-testid="stSidebarNav"] ul {
            gap: 4px !important;
        }
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNavLink"],
        [data-testid="stPageLink-NavLink"] {
            color: #e2e8f0 !important;
            background: rgba(14, 21, 45, 0.8) !important;
            border: 1px solid rgba(0, 210, 255, 0.22) !important;
            border-radius: 6px !important;
            padding: 8px 12px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            display: flex !important;
            align-items: center !important;
            text-decoration: none !important;
            transition: all 0.2s ease !important;
            margin-bottom: 5px !important;
        }
        [data-testid="stSidebarNav"] a:hover,
        [data-testid="stSidebarNavLink"]:hover,
        [data-testid="stPageLink-NavLink"]:hover {
            background: rgba(0, 210, 255, 0.22) !important;
            color: #00d2ff !important;
            border-color: #00d2ff !important;
            box-shadow: 0 0 10px rgba(0, 210, 255, 0.3) !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"],
        [data-testid="stSidebarNavLink"][aria-current="page"] {
            background: linear-gradient(90deg, rgba(0, 210, 255, 0.28) 0%, rgba(14, 21, 45, 0.9) 100%) !important;
            color: #00d2ff !important;
            border-color: #00d2ff !important;
            font-weight: 700 !important;
        }
        [data-testid="stSidebarNav"] span,
        [data-testid="stSidebarNavLink"] span,
        [data-testid="stPageLink-NavLink"] span {
            color: inherit !important;
            font-weight: inherit !important;
        }

        /* Header hero and cards */
        .hero-banner {
            background: linear-gradient(135deg, rgba(14, 21, 45, 0.95) 0%, rgba(20, 31, 66, 0.85) 100%);
            border: 1px solid rgba(0, 210, 255, 0.28);
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(0, 210, 255, 0.1);
            border-radius: 12px;
            padding: 24px 28px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
        }

        .hero-banner::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 250px;
            height: 100%;
            background: radial-gradient(circle at 100% 0%, rgba(0, 210, 255, 0.12) 0%, transparent 70%);
            pointer-events: none;
        }

        /* Metric card styling */
        .glass-card {
            background: rgba(14, 21, 45, 0.75);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 210, 255, 0.16);
            border-radius: 10px;
            padding: 16px 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .glass-card:hover {
            border-color: rgba(0, 210, 255, 0.4);
            box-shadow: 0 6px 24px rgba(0, 210, 255, 0.15);
            transform: translateY(-2px);
        }

        /* Pulse status badge */
        .pulse-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #20bf6b;
            box-shadow: 0 0 0 rgba(32, 191, 107, 0.7);
            animation: pulse 1.8s infinite;
            margin-right: 6px;
            vertical-align: middle;
        }

        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(32, 191, 107, 0.7);
            }
            70% {
                box-shadow: 0 0 0 8px rgba(32, 191, 107, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(32, 191, 107, 0);
            }
        }

        /* Typography & Metrics */
        div[data-testid="stMetricValue"] {
            color: #00d2ff !important;
            font-family: 'JetBrains Mono', Consolas, monospace !important;
            font-weight: 700 !important;
            font-size: 1.85rem !important;
            letter-spacing: -0.5px;
        }
        div[data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(14, 21, 45, 0.6);
            padding: 6px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            border-radius: 6px;
            color: #94a3b8;
            font-weight: 500;
            border: 1px solid transparent;
            padding: 0 16px;
            background-color: transparent;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 210, 255, 0.12) !important;
            color: #00d2ff !important;
            border-color: rgba(0, 210, 255, 0.3) !important;
            font-weight: 600 !important;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(180deg, #16244d 0%, #0e1736 100%) !important;
            color: #00d2ff !important;
            border: 1px solid rgba(0, 210, 255, 0.35) !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 8px 18px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.25s ease !important;
        }
        .stButton>button:hover {
            background: linear-gradient(180deg, #00d2ff 0%, #0088cc 100%) !important;
            color: #070b19 !important;
            border-color: #00d2ff !important;
            box-shadow: 0 0 18px rgba(0, 210, 255, 0.45) !important;
            transform: translateY(-1px);
        }

        /* Inputs & Selectboxes */
        div[data-baseweb="select"] > div {
            background-color: #0e152d !important;
            border-color: rgba(0, 210, 255, 0.2) !important;
            color: #e2e8f0 !important;
            border-radius: 6px !important;
        }
        .stTextInput>div>div>input {
            background-color: #0e152d !important;
            border-color: rgba(0, 210, 255, 0.2) !important;
            color: #e2e8f0 !important;
            border-radius: 6px !important;
        }
        .stTextInput>div>div>input:focus {
            border-color: #00d2ff !important;
            box-shadow: 0 0 10px rgba(0, 210, 255, 0.3) !important;
        }

        /* Dataframe table aesthetic */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(0, 210, 255, 0.15);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }

        /* Login submit button in form - Gold/Orange Orbit button */
        div[data-testid="stForm"] .stButton>button,
        div[data-testid="stFormSubmitButton"]>button,
        button[kind="secondaryFormSubmit"],
        button[kind="primaryFormSubmit"] {
            background: linear-gradient(90deg, #f7b731 0%, #ff9f43 50%, #fa8231 100%) !important;
            color: #070b19 !important;
            font-weight: 800 !important;
            font-size: 1.05rem !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            box-shadow: 0 4px 18px rgba(255, 159, 67, 0.45) !important;
            transition: all 0.25s ease !important;
        }
        div[data-testid="stForm"] .stButton>button:hover,
        div[data-testid="stFormSubmitButton"]>button:hover,
        button[kind="secondaryFormSubmit"]:hover,
        button[kind="primaryFormSubmit"]:hover {
            background: linear-gradient(90deg, #ff9f43 0%, #f7b731 100%) !important;
            box-shadow: 0 0 25px rgba(255, 159, 67, 0.75) !important;
            color: #000000 !important;
            transform: translateY(-2px) !important;
        }
        div[data-testid="stFormSubmitButton"] p,
        div[data-testid="stFormSubmitButton"] span {
            color: #070b19 !important;
            font-weight: 800 !important;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background-color: rgba(14, 21, 45, 0.7) !important;
            border-radius: 6px !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            font-weight: 600 !important;
            color: #e2e8f0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
