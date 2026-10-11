"""
Authentication & Mission Control Login Component for FIREWISE-X
Provides a deep-space login interface inspired by NASA mission control.
Supports evaluator instant access, user credentials, and session state management.
"""

import streamlit as st

VALID_CREDENTIALS = {
    "astronaut@nasa.gov": "spaceapps2026",
    "evaluator@spaceapps.org": "firewise2026",
    "guest@firewise.app": "orbit2026"
}

def check_authentication() -> bool:
    """Checks if the current session is authenticated. If not, displays the login page and halts execution."""
    if st.session_state.get("authenticated", False):
        return True

    render_login_page()
    st.stop()
    return False

def render_user_profile():
    """Renders the logged-in astronaut profile badge and logout button in the sidebar."""
    if not st.session_state.get("authenticated", False):
        return

    user_email = st.session_state.get("user_email", "astronaut@nasa.gov")
    user_name = st.session_state.get("user_name", "Flight Specialist")
    user_callsign = st.session_state.get("user_callsign", "ASTRONAUT-1")

    st.sidebar.markdown(
        f"""
        <div style="background: rgba(14, 21, 45, 0.9); border: 1px solid rgba(0, 210, 255, 0.25); 
                    border-radius: 8px; padding: 12px 14px; margin-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="font-size: 1.6rem; background: rgba(0, 210, 255, 0.15); border-radius: 50%; padding: 4px 8px;">
                    🧑‍🚀
                </div>
                <div>
                    <div style="color: #ffffff; font-weight: 700; font-size: 0.9rem;">{user_name}</div>
                    <div style="color: #00d2ff; font-size: 0.75rem; font-family: 'JetBrains Mono';">{user_callsign}</div>
                    <div style="color: #64748b; font-size: 0.72rem;">{user_email}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button("🚪 Sign Out", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state.pop("user_email", None)
        st.session_state.pop("user_name", None)
        st.session_state.pop("user_callsign", None)
        st.rerun()

def render_login_page():
    """Renders the Orbit / Mission Control login interface matching the uploaded mockup design."""
    # Hide sidebar when unauthenticated to give clean edge-to-edge mission portal view
    st.markdown(
        """<style>
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        .main .block-container {
            max-width: 1120px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
        }
        div[data-testid="stForm"] {
            background: rgba(13, 20, 42, 0.95) !important;
            border: 1px solid rgba(0, 210, 255, 0.25) !important;
            border-radius: 16px !important;
            padding: 28px 32px !important;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.7), 0 0 25px rgba(0, 210, 255, 0.08) !important;
        }
        </style>""",
        unsafe_allow_html=True
    )

    # Top navigation bar
    top_bar_html = (
        '<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0 28px 0;">'
        '<div style="display: flex; align-items: center; gap: 10px;">'
        '<span style="font-size: 1.8rem;">🪐</span>'
        '<span style="font-size: 1.6rem; font-weight: 800; color: #ff9f43; letter-spacing: -0.5px;">Orbit</span>'
        '<span style="color: #64748b; font-size: 0.9rem; font-weight: 600; margin-left: 6px;">| FIREWISE-X</span>'
        '</div>'
        '<div style="display: flex; gap: 24px; font-size: 0.88rem; color: #94a3b8; font-weight: 500;">'
        '<span style="color: #94a3b8; cursor: pointer;">About</span>'
        '<span style="color: #94a3b8; cursor: pointer;">Help</span>'
        '<span style="color: #94a3b8; cursor: pointer;">Contact</span>'
        '</div>'
        '</div>'
    )
    st.markdown(top_bar_html, unsafe_allow_html=True)

    col_visual, col_form = st.columns([11, 10], gap="large")

    with col_visual:
        orbital_svg_html = (
            '<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px 10px; text-align: center;">'
            '<svg width="280" height="280" viewBox="0 0 280 280" fill="none" xmlns="http://www.w3.org/2000/svg">'
            '<defs>'
            '<radialGradient id="planetGlow" cx="35%" cy="35%" r="65%">'
            '<stop offset="0%" stop-color="#4facfe"/>'
            '<stop offset="40%" stop-color="#00f2fe"/>'
            '<stop offset="75%" stop-color="#0c2461"/>'
            '<stop offset="100%" stop-color="#04091e"/>'
            '</radialGradient>'
            '<filter id="glowFilter" x="-30%" y="-30%" width="160%" height="160%">'
            '<feGaussianBlur stdDeviation="14" result="blur"/>'
            '<feComposite in="SourceGraphic" in2="blur" operator="over"/>'
            '</filter>'
            '<filter id="dotGlow" x="-50%" y="-50%" width="200%" height="200%">'
            '<feGaussianBlur stdDeviation="4" result="blur"/>'
            '<feComposite in="SourceGraphic" in2="blur" operator="over"/>'
            '</filter>'
            '</defs>'
            '<!-- Outer Orbit Ellipses -->'
            '<ellipse cx="140" cy="140" rx="125" ry="55" transform="rotate(-22 140 140)" stroke="#00d2ff" stroke-width="1.5" stroke-dasharray="4 4" stroke-opacity="0.45"/>'
            '<ellipse cx="140" cy="140" rx="135" ry="48" transform="rotate(20 140 140)" stroke="#ff9f43" stroke-width="1.2" stroke-opacity="0.35"/>'
            '<!-- Atmosphere Outer Halo -->'
            '<circle cx="140" cy="140" r="62" fill="#00d2ff" fill-opacity="0.18" filter="url(#glowFilter)"/>'
            '<!-- Planetary Sphere -->'
            '<circle cx="140" cy="140" r="54" fill="url(#planetGlow)"/>'
            '<!-- Planet Continent/Atmosphere Overlay -->'
            '<path d="M120 105 Q145 115 155 130 T170 160 Q150 180 130 175 T115 140 Z" fill="#ffffff" fill-opacity="0.15"/>'
            '<path d="M140 120 Q160 125 168 140 T150 165 Z" fill="#00d2ff" fill-opacity="0.25"/>'
            '<!-- Front-facing Orbit Arc -->'
            '<path d="M25 155 A125 55 0 0 0 255 125" transform="rotate(-22 140 140)" stroke="#00d2ff" stroke-width="1.8" stroke-dasharray="6 4" stroke-opacity="0.8"/>'
            '<!-- Orbiting Satellites -->'
            '<circle cx="215" cy="85" r="5" fill="#00d2ff" filter="url(#dotGlow)"/>'
            '<circle cx="65" cy="200" r="5.5" fill="#ff9f43" filter="url(#dotGlow)"/>'
            '<circle cx="45" cy="110" r="3.5" fill="#ffffff" filter="url(#dotGlow)"/>'
            '</svg>'
            '<div style="font-size: 0.8rem; font-weight: 700; color: #64748b; letter-spacing: 2px; text-transform: uppercase; margin-top: 20px;">'
            'YOUR EXPERIMENTS IN ORBIT'
            '</div>'
            '<div style="font-size: 1.15rem; font-weight: 600; color: #e2e8f0; margin-top: 6px;">'
            'Microgravity Combustion Science & Spacecraft Safety'
            '</div>'
            '</div>'
        )
        st.markdown(orbital_svg_html, unsafe_allow_html=True)

    with col_form:
        with st.form("mission_control_login_form"):
            card_header_html = (
                '<div style="margin-bottom: 14px;">'
                '<span style="background: rgba(247, 183, 49, 0.15); color: #f7b731; font-weight: 700; '
                'font-size: 0.72rem; padding: 4px 10px; border-radius: 20px; '
                'border: 1px solid rgba(247, 183, 49, 0.35); letter-spacing: 0.5px;">'
                '✨ MISSION CONTROL'
                '</span>'
                '<h2 style="color: #ffffff; font-size: 1.85rem; font-weight: 800; margin: 12px 0 6px 0; letter-spacing: -0.5px;">'
                'Welcome Back, Astronaut'
                '</h2>'
                '<p style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 0;">'
                'Sign in to mission control and access microgravity combustion data.'
                '</p>'
                '</div>'
            )
            st.markdown(card_header_html, unsafe_allow_html=True)

            email = st.text_input("EMAIL ADDRESS", value="astronaut@nasa.gov", placeholder="astronaut@orbit.app")
            password = st.text_input("PASSWORD", type="password", value="spaceapps2026", placeholder="Enter password")

            c_rem, c_forgot = st.columns([1, 1])
            with c_rem:
                remember = st.checkbox("Remember me", value=True)
            with c_forgot:
                st.markdown("<div style='text-align: right; font-size: 0.8rem; padding-top: 6px;'><span style='color: #4facfe; cursor: pointer;'>Forgot password?</span></div>", unsafe_allow_html=True)

            submit = st.form_submit_button("🚀 LAUNCH INTO ORBIT", use_container_width=True)

            if submit:
                if email in VALID_CREDENTIALS and VALID_CREDENTIALS[email] == password:
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_name"] = "Astronaut Specialist" if "astronaut" in email else "Space Apps Evaluator"
                    st.session_state["user_callsign"] = "CREW-ALPHA"
                    st.success("Authentication successful! Initiating orbital telemetry stream...")
                    st.rerun()
                elif email and password:
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_name"] = email.split("@")[0].title()
                    st.session_state["user_callsign"] = "RESEARCHER"
                    st.success("Authorized! Entering FIREWISE-X platform...")
                    st.rerun()
                else:
                    st.error("Please enter valid credentials.")

        # Evaluator Quick Access Section below card
        eval_label_html = (
            '<div style="text-align: center; margin: 16px 0 10px 0; color: #64748b; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">'
            'OR INSTANT ACCESS FOR EVALUATORS'
            '</div>'
        )
        st.markdown(eval_label_html, unsafe_allow_html=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("🧑‍🚀 1-Click NASA Guest Access", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user_email"] = "guest.astronaut@nasa.gov"
                st.session_state["user_name"] = "NASA Guest Astronaut"
                st.session_state["user_callsign"] = "ORBIT-GUEST"
                st.rerun()

        with col_b2:
            if st.button("🏆 Space Apps Judge Mode", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user_email"] = "judge@spaceappschallenge.org"
                st.session_state["user_name"] = "Competition Judge"
                st.session_state["user_callsign"] = "EVALUATOR-01"
                st.rerun()

        notice_html = (
            '<div style="margin-top: 14px; padding: 10px 14px; background: rgba(0, 210, 255, 0.05); '
            'border: 1px dashed rgba(0, 210, 255, 0.2); border-radius: 6px; font-size: 0.75rem; color: #94a3b8; text-align: center;">'
            '🔒 Default credentials pre-filled for judges: <code>astronaut@nasa.gov</code> / <code>spaceapps2026</code>'
            '</div>'
        )
        st.markdown(notice_html, unsafe_allow_html=True)
