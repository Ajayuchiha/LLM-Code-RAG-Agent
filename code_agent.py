from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import Tool
from local_llama3 import get_local_llama3
from tools import list_files, read_file, write_file, apply_diff, python_repl


# 1. Load Local LLaMA3 (Ollama)
llm = get_local_llama3()


# 2. Modern Tool Registry (NO decorators, NO legacy API)
tools = [
    Tool.from_function(
        func=list_files,
        name="list_files",
        description="List project files."
    ),
    Tool.from_function(
        func=read_file,
        name="read_file",
        description="Read a file."
    ),
    Tool.from_function(
        func=write_file,
        name="write_file",
        description="Write content to a file."
    ),
    Tool.from_function(
        func=apply_diff,
        name="apply_diff",
        description="Apply a diff patch."
    ),
    python_repl,   # Already a Tool instance
]


def code_executor(query: str):
    """
    Executes developer instructions using:
    - Local LLaMA3 (via Ollama)
    - Tool-calling (LCEL style)
    - File editing + Python REPL
    """
    
    messages = [
        SystemMessage(content="You are a senior software engineer. Use tools to inspect or modify project files."),
        HumanMessage(content=query),
    ]

    # Attach tools to LLM
    runnable = llm.bind_tools(tools)

    # LLM response (may be plain text or tool calls)
    response = runnable.invoke(messages)

    # If LLaMA3 requested tool calls
    if hasattr(response, "tool_calls") and response.tool_calls:
        outputs = []

        for call in response.tool_calls:
            tool_name = call["name"]
            tool_args = call["args"]

            tool = next(t for t in tools if t.name == tool_name)
            result = tool.invoke(tool_args)

            outputs.append(f"[{tool_name}] → {result}")

        return "\n".join(outputs)

    # If LLaMA3 responded normally
    return response.content
