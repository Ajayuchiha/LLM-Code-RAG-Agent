import os
import streamlit as st

from rag_agent import ingest_file, run_rag

# UI settings
DB_PATH = "vector_db"
UPLOAD_DIR = "uploads"

st.set_page_config(page_title="RAG Streamlit UI", layout="wide")
st.title("Your RAG Buddy")

with st.expander("Vector DB status"):
    st.write(f"Persist directory: {DB_PATH}")
    try:
        files = os.listdir(DB_PATH) if os.path.exists(DB_PATH) else []
        st.write(f"Files in persist dir: {len(files)}")
    except Exception as e:
        st.write("Cannot inspect directory:", e)

# File upload + ingestion
uploaded_file = st.file_uploader("Upload a PDF, TXT or MD to ingest", type=["pdf", "txt", "md"])
if uploaded_file is not None:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(safe_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Saved upload — ingesting now...")
    try:
        msg = ingest_file(safe_path)
        st.success(msg)
    except Exception as e:
        st.error(f"Ingestion failed: {e}")

st.markdown("---")
query = st.text_input("Ask a question using the ingested documents")
if st.button("Run RAG") and query.strip():
    with st.spinner("Running RAG..."):
        try:
            answer = run_rag(query)
            st.subheader("Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"RAG failed: {e}")

with st.expander("Developer diagnostics"):
    st.write("Uploads folder:", UPLOAD_DIR)
    st.write("Persist folder:", DB_PATH)
    st.write("Retriever k (default): 4")
