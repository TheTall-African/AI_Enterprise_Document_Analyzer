import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_rag_answer(question, retrieved_chunks):
    """This generates an answer using only retrieved document chunks."""

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an enterprise risk and controls assistant.
Answer the user's question using ONLY the document context provided below.

Rules:
-Do not use outside knowledge.
-Do not invent information.
-If the answer cannot be found in the context, say:
    "I could not find enough information in the uploaded documents."
-Keep the answer clear and concise.
-Base every factual statement on the supplied context.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}  """


    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    return response.output_text