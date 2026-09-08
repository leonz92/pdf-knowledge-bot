import os
import streamlit as st
from dotenv import load_dotenv
from database import get_vector_db_collection, process_and_store_pdf
from llm_service import ask_gemini_with_memory, ask_gemini_with_raw_text, summarize_entire_pdf

# Establish page shell configuration layout props
st.set_page_config(page_title="Multimodal Knowledge Engine", page_icon="🤖", layout="centered")
st.title("🤖 Multimodal Knowledge Bot")
st.caption("Perform deep document searches, high-level summaries, and context-driven chats")

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
  try:
    if "GEMINI_API_KEY" in st.secrets:
      api_key = st.secrets['GEMINI_API_KEY']
  except FileNotFoundError:
    pass

if not api_key:
  st.error("Missing Gemini API key. Configure keys inside your Streamlit Secrets portal or local '.env' file.")
  st.stop()

# Use caching wrappers to make DB objects persistent across runtime UI reloads
@st.cache_resource
def load_db():
  return get_vector_db_collection(api_key)

collection = load_db()

# Add messages memory to user runtime state
if "messages" not in st.session_state:
  st.session_state.messages = []

# Sidebar Layout Component
with st.sidebar:
  st.header("Select Data Source")
  tab1, tab2 = st.tabs(["📁 Upload PDF", "📝 Paste Text"])

  with tab1:
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file:
      if "loaded file" not in st.session_state or st.session_state.loaded_file != uploaded_file.name:
        with st.spinner("Processing PDF and vectorizing chunks..."):
          process_and_store_pdf(collection, uploaded_file)
          st.session_state.loaded_file = uploaded_file.name
          st.session_state.pasted_text = None
          st.success(f"Processed {uploaded_file.name}!")

    if uploaded_file and "loaded_file" in st.session_state and st.session_state.loaded_file == uploaded_file.name:
      st.write("---")
      if st.button("✨ Summarize Entire Document", use_container_width=True):
        with st.spinner("Reading full file content paths..."):
          full_summary = summarize_entire_pdf(uploaded_file, api_key)
          st.session_state.messages.append({"role": "assistant", "content": f"### 📝 Full Document Summary\n{full_summary}"})

  with tab2:
    MAX_CHARS = 250000
    user_pasted_text = st.text_area("Paste background context or source transcripts:", height=250, placeholder="Paste data pools here...")

    if user_pasted_text:
      current_len = len(user_pasted_text)
      if current_len > MAX_CHARS:
        st.error(f"❌ Input bound limit exceeded! {current_len:,}/{MAX_CHARS:,} chars used.")
        st.session_state.pasted_text = None
      else:
        st.info(f"📝 {current_len:,} / {MAX_CHARS:,} characters stored.")
        st.session_state.pasted_text = user_pasted_text
        st.session_state.loaded_file = "Pasted Text Document"

  st.write("---")
  if st.button("Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if user_query := st.chat_input("Ask a question regarding your uploaded data..."):
  if "loaded_file" not in st.session_state:
    st.warning("Provide data first! Upload a PDF or paste text content inside the left panel.")
    st.stop()

  with st.chat_message("user"):
    st.markdown(user_query)

  st.session_state.messages.append({"role": "user", "content": user_query})

  history_mapping = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]

  with st.chat_message("assistant"):
    with st.spinner("Analyzing structural data patterns..."):

        # ROUTE A: High Context Direct Window Routing
        if st.session_state.get("pasted_text"):
            answer = ask_gemini_with_raw_text(user_query, st.session_state.pasted_text, history_mapping, api_key)
            sources = None

        # ROUTE B: ChromaDB Similarity Chunk Tracking Routing
        else:
            answer, sources = ask_gemini_with_memory(collection, user_query, history_mapping, api_key)

        full_response = answer
        if sources:
            full_response += f"\n\n*Sources: Extracted from internal PDF Page(s) {', '.join(map(str, sources))}*"

        st.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
