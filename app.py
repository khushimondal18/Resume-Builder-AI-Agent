import streamlit as st

st.set_page_config(
    page_title="AI Resume Builder Agent",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.big-title {font-size: 46px; font-weight: 800; margin-bottom: 0px;}
.subtitle {font-size: 20px; color: #b6b6b6; margin-top: 4px;}
.card {padding: 22px; border-radius: 16px; background-color: #111827; border: 1px solid #263244;}
.small-card {padding: 16px; border-radius: 14px; background-color: #102235; border: 1px solid #25415c;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📄 Resume Agent")
st.sidebar.info("Use these pages to build, preview, and later generate your resume.")

st.markdown('<div class="big-title">🤖 AI Resume Builder Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Streamlit UI → CrewAI Crew → Resume Writer + ATS Optimizer + Resume Formatter → DOCX Download</div>', unsafe_allow_html=True)

st.write("")
st.write("")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="small-card">📝 <b>Step 1</b><br>Fill resume information</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="small-card">🤖 <b>Step 2</b><br>AI agents process it</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="small-card">📄 <b>Step 3</b><br>Download DOCX resume</div>', unsafe_allow_html=True)

st.write("")
st.success("Start by filling your details on the Build Resume page.")
