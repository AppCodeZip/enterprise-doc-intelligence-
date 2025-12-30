

# PDF → chunks → embeddings → FAISS → top-K relevant chunks

# Why it’s called a “Chain”
# In LangChain-style thinking, a chain is:
# Context → Prompt → LLM → Answer








from rag.prompt import build_prompt

#build_prompt → formats the input for the LLM
import subprocess   #subprocess → runs a local LLM via Ollama

class QAChain:
    def __init__(self):
        pass

    def run(self, context_docs, question):
        context = "\n".join(
            [doc["text"] for doc in context_docs]
        )

        prompt = build_prompt(context, question)

        # Using Ollama (Llama3 / Mistral)
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            text=True,
            capture_output=True
        )

        return {
            "answer": result.stdout,
            "sources": list({
                f'{doc["metadata"]["source"]} (page {doc["metadata"]["page"]})'
                for doc in context_docs
            })
        }




# 🔥 Best FREE local LLMs (2025)
'''| Model            | Why                       |
| ---------------- | ------------------------- |
| **LLaMA-3 (8B)** | Best reasoning, strong QA |
| **Mistral 7B**   | Very fast, lightweight    |
| **Gemma 2**      | Clean answers             |
| **Phi-3**        | Small, very efficient     |

👉 For your use case:
LLaMA-3 (via Ollama) is an excellent choice.


☁️ Best cloud LLMs (paid, optional)

| Model      | Best for         |
| ---------- | ---------------- |
| GPT-4o     | Highest accuracy |
| Claude 3   | Long documents   |
| Gemini 1.5 | Huge context     |

🧠🧠 Why local LLM is a great choice here
✔ Free
✔ No data leaves your machine
✔ No rate limits
✔ Perfect for enterprise documents


'''

