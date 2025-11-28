<a href="#"><img src="https://img.shields.io/badge/Framework-LangChain%20%7C%20LangGraph-blue?style=for-the-badge"></a>
<a href="#"><img src="https://img.shields.io/badge/LLM-LLaMA3%208B-orange?style=for-the-badge"></a>
<a href="#"><img src="https://img.shields.io/badge/VectorDB-ChromaDB-green?style=for-the-badge"></a>
<a href="#"><img src="https://img.shields.io/badge/UI-Streamlit-red?style=for-the-badge"></a>
<a href="#"><img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"></a>

</p>

# 🚀 DevRAG — AI Developer + Knowledge Intelligence Agent

DevRAG is a **context-aware AI agent** that merges:

- 🔹 **Local LLaMA3 (fast, offline inference)**
- 🔹 **LangGraph multi-node routing**
- 🔹 **ChromaDB RAG for knowledge retrieval**
- 🔹 **Tool-calling code execution**
- 🔹 **File inspector UI**
- 🔹 **Streamlit app interface**

This system provides **both**:
- **RAG-based knowledge answers**
- **Intelligent coding assistance with real file operations**

---

## 🧠 Core Features

### ✅ **LangGraph Router**
Intelligently routes queries to:
- **RAG Agent** → Knowledge & documentation answers  
- **Code Agent** → File edits, code generation, Python execution  

### ✅ **Code Agent**
- Reads/writes files  
- Applies diffs  
- Executes Python with sandboxed REPL  

### ✅ **RAG Agent**
- Custom ingestion pipeline  
- Nomic embeddings via Ollama  
- ChromaDB vector store  
- Local inference  

### ✅ **Streamlit UI**
- Chat interface  
- File explorer panel  
- Auto-refresh responses  

---

## 🔧 Tech Stack

| Component | Technology |
|----------|------------|
| LLM | LLaMA3 (Ollama) |
| Framework | LangChain, LangGraph |
| Vector Store | ChromaDB |
| Embeddings | Nomic Embed |
| UI | Streamlit |
| Backend | Python |
| Testing | PyTest |
| CI | GitHub Actions |

## 🚀 Running Locally