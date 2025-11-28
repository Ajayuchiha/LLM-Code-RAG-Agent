# fastapi_app.py
import sys, os
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import asyncio

# Ensure imports work
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from local_llama3 import get_local_llama3
from router_graph import graph

app = FastAPI(title="DevRAG API (Local LLaMA3)")

# Use a single LLM instance for streaming attempts
LLM = get_local_llama3()

def _try_stream(llm, prompt: str):
    """
    Attempt to return a generator that yields text chunks.
    If the model exposes a stream API, iterate it. Otherwise, yield the full response once.
    """
    # Defensive: many adapters expose .stream or .stream_chat — try common names
    for stream_attr in ("stream", "stream_chat", "astream", "generate_stream"):
        if hasattr(llm, stream_attr):
            stream_fn = getattr(llm, stream_attr)
            try:
                for chunk in stream_fn(prompt):
                    # chunk shape can vary; handle common cases
                    text = ""
                    if hasattr(chunk, "content"):
                        text = getattr(chunk, "content")
                    elif isinstance(chunk, dict) and "text" in chunk:
                        text = chunk["text"]
                    else:
                        text = str(chunk)
                    yield text
                return
            except Exception:
                break

    # Fallback: synchronous generate/invoke
    try:
        resp = llm.invoke(prompt)
        # try to extract text
        if hasattr(resp, "content"):
            yield resp.content
        elif isinstance(resp, dict) and "text" in resp:
            yield resp["text"]
        else:
            yield str(resp)
    except Exception as e:
        yield f"[ERROR] {e}"

@app.get("/chat/stream")
async def chat_stream(q: str = Query(..., description="User query")):
    """
    Server-Sent Events (SSE)-style streaming response.
    Clients can connect and receive chunks of text.
    """
    prompt = q
    generator = _try_stream(LLM, prompt)

    async def event_generator():
        loop = asyncio.get_event_loop()
        for chunk in generator:
            # small safety delay and yield
            await asyncio.sleep(0.01)
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")

@app.get("/chat")
async def chat(q: str = Query(..., description="User query")):
    """
    Non-streaming simple API that executes the LangGraph router and returns JSON.
    This is safer for programmatic clients.
    """
    if not q or q.strip() == "":
        raise HTTPException(status_code=400, detail="Query missing")
    try:
        out = graph.invoke({"query": q})
        return JSONResponse(content={"response": out.get("response")})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
