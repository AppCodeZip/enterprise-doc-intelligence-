def build_prompt(context, question):
    return f"""
You are an enterprise AI assistant.
Answer ONLY using the context below.
If the answer is not present, say:
"I don't have enough information from the documents."

Context:
{context}

Question:
{question}
"""
