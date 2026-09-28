import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_document(document_text: str) -> dict:  #here we use dictionary to create the structured outputs of the prompt and immediately keeping similar information together.
    prompt = f"""
    You are an enterprise risk and controls analyst.
    Analyze the document below and return only valid JSON.

    Use this exact structure:
    {{
        "document_type": "",
        "business_function": "",
        "risks": [],
        "controls": [],
        "control_owners": [],
        "approval_authorities": [],
        "monetary_thresholds": [],
        "exceptions": [],
        "follow_up_questions": []
    }}

    Rules:
    - Only use information found in the document.
    - Do not invent missing details.
    - Use empty lists when information is not available.
    - Do not include any additional text or explanations outside of the JSON structure.
   
    DOCUMENT:
    {document_text}
    
    """

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )
    raw_output = response.output_text 

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return{
            "error": "Model did not return valid JSON. Please check document and try again.",
            "raw_output": raw_output
        }

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_text(uploaded_file):
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)

    return ""


if __name__ == "__main__":
    sample = """
Payments above $100,000 require cfo approval. Payments between 25,000 and 100,000 require approval from the business unit head. Payments below $25,000 can be approved by the department manager. All payments must be reviewed for compliance with company policies.
"""

    result = analyze_document(sample)

    print(result)