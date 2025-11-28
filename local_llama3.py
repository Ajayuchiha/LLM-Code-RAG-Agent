from langchain_ollama import ChatOllama

def get_local_llama3():
    
    return ChatOllama(
        model="llama3",
        temperature=0.1,
        top_p=0.9,
        num_ctx=8192,
    )
