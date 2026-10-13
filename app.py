
import html

import streamlit as st

from query_graph import (
    get_schemes_for_crop,
    search_schemes_by_keyword,
)
from rag_answer import generate_answer


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Scheme Navigator AI",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CUSTOM DESIGN SYSTEM
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --navy: #101A2C;
        --navy-light: #19283D;
        --teal: #087F70;
        --teal-light: #D9F5EC;
        --saffron: #E9A23B;
        --text: #172437;
        --muted: #68778B;
        --surface: #FFFFFF;
        --background: #F4F7FB;
        --border: #E2E8F0;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(244, 247, 251, 0.92);
    }

    [data-testid="stSidebar"] {
        background: var(--navy);
        border-right: 1px solid #27364B;
    }

    [data-testid="stSidebar"] * {
        color: #E7EDF6;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #C3CFDE;
    }

    [data-testid="stSidebar"] hr {
        border-color: #344257;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }

    .brand-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 15px;
        background: #203D4B;
        font-size: 25px;
    }

    .brand-title {
        font-family: 'Manrope', sans-serif;
        font-size: 18px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.3;
    }

    .brand-caption {
        font-size: 11px;
        color: #A8B9CC;
        margin-top: 3px;
    }

    .sidebar-label {
        color: #8FA5BE;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin: 24px 0 10px 0;
    }

    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(
            130deg, #101A2C 0%, #172C42 60%, #164D51 100%
        );
        border-radius: 24px;
        padding: 38px 38px 32px 38px;
        margin: 8px 0 24px 0;
        color: white;
        border: 1px solid #263D51;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -75px;
        top: -105px;
        border-radius: 50%;
        border: 1px solid rgba(102, 227, 196, 0.20);
        box-shadow: 0 0 0 30px rgba(102, 227, 196, 0.035),
                    0 0 0 60px rgba(102, 227, 196, 0.025);
        pointer-events: none;
    }

    .hero-eyebrow {
        display: inline-block;
        padding: 7px 11px;
        border: 1px solid rgba(102, 227, 196, 0.35);
        border-radius: 20px;
        background: rgba(102, 227, 196, 0.09);
        color: #80E8CE;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin-bottom: 18px;
    }

    .hero h1 {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(29px, 4vw, 44px);
        font-weight: 800;
        line-height: 1.2;
        letter-spacing: -1.4px;
        color: #FFFFFF;
        max-width: 680px;
        margin: 0 0 15px 0;
    }

    .hero p {
        color: #C5D3E1;
        font-size: 15px;
        line-height: 1.8;
        max-width: 650px;
        margin: 0;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin: 0 0 28px 0;
    }

    .feature-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px;
        min-height: 116px;
    }

    .feature-icon {
        font-size: 23px;
        margin-bottom: 11px;
    }

    .feature-title {
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
        font-size: 13px;
        color: #172437;
        margin-bottom: 5px;
    }

    .feature-description {
        font-size: 12px;
        color: #738196;
        line-height: 1.5;
    }

    .section-heading {
        font-family: 'Manrope', sans-serif;
        font-size: 21px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: var(--text);
        margin: 18px 0 5px 0;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 17px;
    }

    .scheme-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 19px;
        margin: 10px 0;
        box-shadow: 0 3px 12px rgba(16, 26, 44, 0.025);
    }

    .scheme-tag {
        display: inline-block;
        background: #E4F7F0;
        color: #087F70;
        border-radius: 6px;
        padding: 5px 9px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }

    .scheme-title {
        font-family: 'Manrope', sans-serif;
        font-size: 16px;
        font-weight: 800;
        line-height: 1.5;
        color: #172437;
        margin-bottom: 8px;
    }

    .scheme-meta {
        font-size: 12px;
        color: #68778B;
        line-height: 1.7;
        overflow-wrap: anywhere;
    }

    .scheme-meta a {
        color: #087F70;
        text-decoration: none;
        font-weight: 700;
    }

    .assistant-note {
        background: #EAF7F3;
        border-left: 3px solid #087F70;
        border-radius: 0 10px 10px 0;
        padding: 13px 15px;
        color: #285A50;
        font-size: 12px;
        line-height: 1.7;
        margin: 14px 0;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid var(--border);
        border-radius: 17px;
        padding: 15px 18px;
        background: white;
        margin-bottom: 14px;
    }

    [data-testid="stChatInput"] {
        border-radius: 16px;
    }

    [data-testid="stChatInput"] textarea {
        font-family: 'DM Sans', sans-serif;
    }

    .stButton > button {
        border-radius: 11px;
        font-weight: 600;
        border: 1px solid #DCE5EC;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #087F70;
        color: #087F70;
        background: #F0FAF7;
    }

    .stLinkButton > a {
        border-radius: 10px;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: #8491A2;
        font-size: 11px;
        padding: 26px 0 12px 0;
        line-height: 1.8;
    }

    @media (max-width: 700px) {
        .hero {
            padding: 26px 22px;
            border-radius: 18px;
        }

        .feature-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def detect_crop(question):
    """Return a supported crop name when one is mentioned."""
    question_lower = question.lower()

    crop_keywords = [
        ("maize", ("maize",)),
        ("pulses", ("pulse", "pulses")),
        ("oilseeds", ("oilseed", "oilseeds", "oil seed", "oil seeds")),
        ("groundnut", ("groundnut", "ground nuts")),
    ]

    for crop, keywords in crop_keywords:
        if any(keyword in question_lower for keyword in keywords):
            return crop

    return None


def get_search_keyword(question):
    """Keep the existing keyword-search fallback for other questions."""
    question_lower = question.lower()

    if "women" in question_lower or "woman" in question_lower:
        return "women"
    if "farmer" in question_lower or "farmers" in question_lower:
        return "farmer"
    if "seed" in question_lower or "seeds" in question_lower:
        return "seeds"

    return question_lower


def retrieve_schemes(question):
    """Use crop relationships where possible, otherwise use keyword search."""
    crop_name = detect_crop(question)

    if crop_name:
        schemes = get_schemes_for_crop(crop_name)
        retrieval_method = f"Knowledge Graph · {crop_name.title()}"
    else:
        keyword = get_search_keyword(question)
        schemes = search_schemes_by_keyword(keyword)
        retrieval_method = f"Keyword search · {keyword}"

    return schemes, retrieval_method


def safe_text(value, fallback="Not specified in the available source"):
    """Display missing values clearly and escape text used in HTML."""
    if value is None or not str(value).strip():
        value = fallback
    return html.escape(str(value))


def render_scheme_cards(schemes):
    """Render retrieved records as readable scheme reference cards."""
    for scheme in schemes:
        name = safe_text(scheme.get("scheme"), "Unnamed scheme")
        department = safe_text(scheme.get("department"))
        funding = safe_text(scheme.get("funding"))
        benefits = safe_text(scheme.get("benefits"))
        source_url = scheme.get("source_url") or ""
        safe_url = html.escape(str(source_url), quote=True)

        source_html = ""
        if str(source_url).startswith(("https://", "http://")):
            source_html = (
                f'<a href="{safe_url}" target="_blank" '
                f'rel="noopener noreferrer">View official source ↗</a>'
            )
        else:
            source_html = "Source URL not available"

        st.markdown(
            f"""
            <div class="scheme-card">
                <div class="scheme-tag">Government scheme</div>
                <div class="scheme-title">{name}</div>
                <div class="scheme-meta">
                    <strong>Department:</strong> {department}<br>
                    <strong>Financial assistance:</strong> {funding}<br>
                    <strong>Benefits:</strong> {benefits}<br><br>
                    {source_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def answer_question(question):
    """Retrieve records and generate a grounded answer."""
    schemes, retrieval_method = retrieve_schemes(question)

    if not schemes:
        answer = (
            "I couldn't find matching schemes in the currently indexed "
            "records. Try a crop-specific question or a different keyword. "
            "This does not necessarily mean that no government scheme exists."
        )
    else:
        answer = generate_answer(question, schemes)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "schemes": schemes,
            "retrieval_method": retrieval_method,
        }
    )


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="brand-row">
            <div class="brand-icon">🇮🇳</div>
            <div>
                <div class="brand-title">Scheme Navigator AI</div>
                <div class="brand-caption">Tamil Nadu · Public Services</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown('<div class="sidebar-label">Explore schemes</div>',
                unsafe_allow_html=True)

    sidebar_questions = {
        "🌽 Maize assistance": (
            "What schemes are available for maize farmers, "
            "and what financial assistance do they provide?"
        ),
        "🌱 Pulses assistance": (
            "What financial assistance is available for farmers growing pulses?"
        ),
        "🥜 Groundnut schemes": (
            "What government schemes are related to groundnut?"
        ),
        "🌾 Oilseed schemes": (
            "What schemes support oilseed farmers?"
        ),
    }

    for label, question in sidebar_questions.items():
        if st.button(label, use_container_width=True, key=f"side_{label}"):
            st.session_state.pending_question = question

    st.markdown('<div class="sidebar-label">How it works</div>',
                unsafe_allow_html=True)

    st.markdown(
        """
        1. **Ask** a question in everyday language.
        2. **Retrieve** matching schemes from Neo4j.
        3. **Understand** the results with AI-generated explanations.
        4. **Verify** details using the linked source pages.
        """
    )

    st.divider()

    st.markdown("**Technology stack**")
    st.caption("🕸️ Neo4j Knowledge Graph")
    st.caption("🧠 LangChain + OpenAI")
    st.caption("✨ Streamlit")

    st.markdown(
        """
        <div class="assistant-note">
            <strong>Important</strong><br>
            Scheme details may change. Confirm eligibility, application
            dates, and current benefits with the relevant department.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()


# ---------------------------------------------------------
# MAIN HERO
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">✦ Your AI scheme research assistant</div>
        <h1>Find the support you're looking for.</h1>
        <p>
            Explore Tamil Nadu Government schemes with intelligent search.
            Ask about farmers, crops, financial assistance, benefits, and
            application procedures — all in one place.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🕸️</div>
            <div class="feature-title">Connected knowledge</div>
            <div class="feature-description">
                Discover schemes through relationships between crops and
                government departments.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">✦</div>
            <div class="feature-title">Ask naturally</div>
            <div class="feature-description">
                Use everyday questions instead of complicated search filters.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">↗</div>
            <div class="feature-title">Traceable sources</div>
            <div class="feature-description">
                Open official scheme pages to review the original information.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SUGGESTED QUESTIONS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-heading">What would you like to discover?</div>'
    '<div class="section-subtitle">'
    'Start with a suggested question or enter your own below.'
    '</div>',
    unsafe_allow_html=True,
)

suggestions = [
    ("🌽", "Maize farmer assistance",
     "What schemes are available for maize farmers, and what financial assistance do they provide?"),
    ("🌱", "Pulses support",
     "What financial assistance is available for farmers growing pulses?"),
    ("🥜", "Groundnut schemes",
     "What schemes are related to groundnut?"),
    ("🌾", "Oilseed support",
     "What government schemes support oilseed farmers?"),
]

suggestion_columns = st.columns(4)

for index, (emoji, label, question) in enumerate(suggestions):
    with suggestion_columns[index]:
        if st.button(
            f"{emoji} {label}",
            key=f"suggestion_{index}",
            use_container_width=True,
        ):
            st.session_state.pending_question = question


# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------

st.markdown(
    '<div class="section-heading">Your conversation</div>',
    unsafe_allow_html=True,
)

# Accept a suggested question or a typed question.
typed_question = st.chat_input(
    "Ask about schemes, subsidies, benefits or eligibility..."
)

question_to_process = (
    typed_question
    or st.session_state.pending_question
)

st.session_state.pending_question = None

# Process the new question once.
if question_to_process and question_to_process.strip():
    question_to_process = question_to_process.strip()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question_to_process,
        }
    )

    try:
        with st.spinner(
            "Searching the Knowledge Graph and preparing your answer..."
        ):
            answer_question(question_to_process)

    except Exception as error:
        # Keep implementation details out of the public-facing message.
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    "I couldn't complete that request. Please check your "
                    "Neo4j connection, environment configuration, and "
                    "OpenAI settings, then try again."
                ),
                "schemes": [],
                "retrieval_method": "Request failed",
                "error": str(error),
            }
        )


# Display all messages.
if not st.session_state.messages:
    st.info(
        "👋 Welcome! Choose a suggested question above or type your "
        "question in the chat box below to get started."
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        
    if message["role"] == "assistant":
        schemes = message.get("schemes", [])

        if message.get("retrieval_method"):
            st.markdown(
                f"""
                <div class="assistant-note">
                    <strong>Search complete</strong><br>
                    {len(schemes)} scheme(s) retrieved
                    · {html.escape(message['retrieval_method'])}
                </div>
                """,
                unsafe_allow_html=True,
            )

            if schemes:
                with st.expander(
                    f"📚 View retrieved scheme records ({len(schemes)})"
                ):
                    render_scheme_cards(schemes)

            if message.get("error"):
                with st.expander("Technical details"):
                    st.code(message["error"])


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <strong>Scheme Navigator AI</strong><br>
        Built with Streamlit · Neo4j · LangChain · OpenAI<br>
        An AI-powered discovery tool. Always verify scheme details
        with official government sources.
    </div>
    """,
    unsafe_allow_html=True,
)
