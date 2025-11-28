import streamlit as st

def chat_box():
    return st.text_area("Ask DevRAG (knowledge or code):", height=180)

def display_response(resp):
    st.markdown("### Response")
    if resp is None:
        st.write("No response.")
        return
    # If it's a dict or list, pretty-print
    if isinstance(resp, (dict, list)):
        st.json(resp)
    else:
        # code block for long text
        text = str(resp)
        if len(text) > 300:
            st.code(text)
        else:
            st.write(text)

def file_inspector(base="codebase"):
    import os
    files = []
    for root, _, fs in os.walk(base):
        for f in fs:
            if f.endswith((".py", ".md", ".txt", ".json")):
                files.append(os.path.join(root, f))
    if not files:
        st.info(f"No files found in `{base}`")
        return None
    choice = st.selectbox("Inspect file", files)
    if choice:
        try:
            with open(choice, "r", encoding="utf-8") as fh:
                content = fh.read()
            st.code(content)
        except Exception as e:
            st.error(f"Could not read {choice}: {e}")
    return None
