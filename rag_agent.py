# rag_agent.py
"""
Backend module: ingestion + persistent Chroma + RAG chain builder + run_rag.
Uses OllamaEmbeddings with model "nomic-embed-text".
"""

import os
import subprocess
from typing import List

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate

# Your local wrapper — must provide an LCEL-compatible LLM (get_local_llama3())
from local_llama3 import get_local_llama3

# -------------------------
# Config
# -------------------------
DB_PATH = "vector_db"
COLLECTION_NAME = "devrag-docs"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
K_RETRIEVE = 4
EMBED_MODEL = "nomic-embed-text"

# -------------------------
# Helper: ensure embedding model exists (attempt to pull via ollama if missing)
# -------------------------
def _ollama_has_model(model_name: str) -> bool:
    """Return True if ollama lists model_name locally (uses `ollama list`)."""
    try:
        out = subprocess.check_output(["ollama", "list"], stderr=subprocess.STDOUT, text=True)
        # simple substring match against the output table; fine for pragmatic check
        return model_name in out
    except Exception:
        return False

def _try_pull_ollama_model(model_name: str) -> bool:
    """Attempt to pull model_name via ollama. Returns True on likely success."""
    try:
        subprocess.check_call(["ollama", "pull", model_name])
        return _ollama_has_model(model_name)
    except Exception:
        return False

# -------------------------
# Create embeddings (with auto-pull fallback)
# -------------------------
def _init_embeddings(model_name: str):
    """Initialize OllamaEmbeddings, attempt to pull model if missing."""
    try:
        return OllamaEmbeddings(model="nomic-embed-text")
    except Exception as e:
        # Try to auto-pull via ollama CLI if available
        if not _ollama_has_model("nomic-embed-text"):
            pulled = _try_pull_ollama_model("nomic-embed-text")
            if pulled:
                return OllamaEmbeddings(model="nomic-embed-text")
        raise RuntimeError(
            "Failed to initialize OllamaEmbeddings('nomic-embed-text'). "
            "Ensure the model is installed: ollama pull nomic-embed-text"
        ) from e

embeddings = _init_embeddings("nomic-embed-text")


# -------------------------
# Splitter + Vectorstore (persistent)
# -------------------------
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

# instantiate Chroma (persistent)
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=DB_PATH,
)

# -------------------------
# Ingestion helpers
# -------------------------
def _load_documents_from_path(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(path)
    elif ext in [".txt", ".md"]:
        loader = TextLoader(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return loader.load()

def ingest_file(path: str) -> str:
    """Load file, chunk, embed and persist into Chroma."""
    docs = _load_documents_from_path(path)
    chunks = text_splitter.split_documents(docs)

    if not chunks:
        return "No content extracted from file."

    vectorstore.add_documents(chunks)
    # call persist if available
    try:
        vectorstore.persist()
    except Exception:
        pass

    return f"Successfully ingested {len(chunks)} chunks from {os.path.basename(path)}"

# -------------------------
# RAG chain builder
# -------------------------
def create_rag_chain(k: int = K_RETRIEVE):
    """Create LCEL-style RAG chain that expects {'query': str} input."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    # Convert retrieved Document objects into a single plain string context.
    def retriever_to_text(query: str) -> str:
        # Use the retriever's helper if available; otherwise fallback to get_relevant_documents
        docs = []
        if hasattr(retriever, "get_relevant_documents"):
            docs = retriever.get_relevant_documents(query)
        elif hasattr(retriever, "retrieve"):
            docs = retriever.retrieve(query)  # unlikely but defensive
        else:
            # last-resort: try calling retriever with invoke-like signature
            try:
                docs = retriever.invoke(query)
            except Exception:
                docs = []

        # If docs are returned as a dict or other structure, normalize conservatively
        texts = []
        for d in docs:
            # support both Document-like objects and simple dicts
            text = None
            if hasattr(d, "page_content"):
                text = d.page_content
            elif isinstance(d, dict) and "page_content" in d:
                text = d["page_content"]
            elif isinstance(d, str):
                text = d
            else:
                # best-effort stringify
                text = str(d)
            texts.append(text)
        return "\n\n".join(texts)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the provided context to answer exactly."),
        ("human", "Query: {query}\n\nContext:\n{context}")
    ])

    llm = get_local_llama3()

    # Build the LCEL pipeline: map query -> context (string) -> prompt -> llm
    rag_chain = (
        {
            "query": lambda x: x["query"],
            "context": lambda x: retriever_to_text(x["query"])
        }
        | prompt
        | llm
    )
    return rag_chain

# -------------------------
# Run query helper
# -------------------------
def run_rag(query: str) -> str:
    """Convenience function: build chain and execute a query, returning a string."""
    rag_chain = create_rag_chain()
    out = rag_chain.invoke({"query": query})
    try:
        return out.content if hasattr(out, "content") else str(out)
    except Exception:
        return str(out)
