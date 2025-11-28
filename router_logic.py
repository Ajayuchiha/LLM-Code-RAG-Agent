from local_llama3 import get_local_llama3

llm = get_local_llama3()

def decide_route(query: str):
    prompt = f"""
You are a router. Classify the user intent into one of two buckets:

- "rag" → if the user is asking for knowledge, documentation, explanation, definitions, or retrieval
- "code" → if the user is asking to write, modify, debug, or execute code

User query: {query}
Respond with only one word: rag or code.
"""

    resp = str(llm.invoke(prompt).content).strip().lower()

    if "code" in resp:
        return "code"
    return "rag"
