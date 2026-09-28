# Enterprise Risk AI Document Analyzer

## Overview

The Enterprise Risk AI Document Analyzer is a Python and Streamlit application that uses generative AI to review enterprise policy, risk, and control documents.

It extracts structured information such as:

* Risks
* Controls
* Control owners
* Approval authorities
* Monetary thresholds
* Exceptions
* Follow-up questions

The goal is to reduce the amount of manual review required when working with enterprise risk, audit, compliance, and policy documentation.

---

## Current Features

### Phase 1: AI Document Analysis

* Manual text input
* LLM API integration
* Structured JSON output
* Risk and control extraction
* Prompt guardrails
* Evaluation testing

### Phase 2: Document Processing

* TXT and PDF uploads
* Multiple document uploads
* Text extraction from files
* Individual analysis of each document
* Document previews
* Pandas results tables
* CSV exports
* Error handling

---

## How It Works

```text
User uploads document
        ↓
Text is extracted
        ↓
AI analyzes document
        ↓
Structured information is returned
        ↓
Results are displayed in Streamlit
        ↓
Results can be exported as CSV
```

For multiple uploads, each document is analyzed separately.

---

## Example Output

The application returns structured results such as:

```json
{
  "document_type": "Authorization Policy",
  "business_function": "Finance",
  "risks": [
    "Unauthorized financial transactions"
  ],
  "controls": [
    "Transactions above $100,000 require CFO approval"
  ],
  "control_owners": [
    "Finance"
  ],
  "approval_authorities": [
    "Chief Financial Officer"
  ],
  "monetary_thresholds": [
    "$100,000"
  ],
  "exceptions": [],
  "follow_up_questions": []
}
```

---

## Technologies

* Python
* Streamlit
* Pandas
* LLM API
* Prompt Engineering
* PDF/TXT Processing
* Git / GitHub

---

## Project Structure

```text
AI_Document_Analyzer/
│
├── app.py
├── analyzer.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── sample_docs/
└── evaluations/
```

---

## Evaluation and Safety

The project includes evaluation tests that compare expected document information with model output.

The AI is instructed to:

* Use only information found in the document
* Avoid inventing missing information
* Return empty values when information is unavailable
* Separate extracted facts from follow-up recommendations

---

## Roadmap

### Phase 3: Retrieval-Augmented Generation

Next steps:

* Document chunking
* Embeddings
* Vector database
* Semantic search
* Multi-document question answering
* Source citations

### Phase 4

* PostgreSQL integration
* Store risks, controls, and document metadata
* SQL analysis

### Phase 5

* Agentic AI
* Document search tools
* SQL tools
* Automated tool selection

### Phase 6

* Expanded AI evaluation
* Governance controls
* Logging
* Prompt injection testing
* Human review workflows

---

## Long-Term Goal

The long-term goal is to develop the application into an enterprise AI assistant capable of searching structured and unstructured risk information, answering questions across multiple documents, and providing source-grounded responses.
