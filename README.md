# Enterprise Risk AI Document Analyzer

## Overview

The **Enterprise Risk AI Document Analyzer** is a Python application that uses generative AI to analyze enterprise risk, policy, compliance, and control documents.

Users can upload documents, receive structured information about their contents, and ask questions across the uploaded files.

The main goal is to reduce the amount of manual work required when reviewing documents such as:

- Risk policies
- Internal controls
- Authorization policies
- Vendor risk policies
- Access-control policies
- Compliance documentation

---

## Current Features

### Phase 1: AI Document Analysis

The first version introduced basic AI document analysis.

Users can:

- Paste document text manually
- Send the text to an LLM
- Extract structured information
- View risks and controls
- Identify control owners
- Identify approval authorities
- Identify monetary thresholds
- Identify exceptions
- Generate follow-up questions

The model is instructed to only use information found in the provided document and avoid inventing missing information.

---

## Phase 2: File and Multi-Document Processing

The application was expanded to support real document uploads.

Current document-processing features include:

- TXT file uploads
- PDF file uploads
- Multiple file uploads
- PDF text extraction
- Document previews
- Individual document analysis
- Structured JSON responses
- Pandas results tables
- CSV downloads
- Error handling

Each uploaded document is analyzed separately so information from different documents is not accidentally mixed together.

### Basic Analysis Flow

```text
Document Upload
      ↓
Text Extraction
      ↓
LLM Analysis
      ↓
Structured Results
      ↓
Streamlit Display
      ↓
CSV Export
```

---

## Phase 3: Retrieval-Augmented Generation (RAG)

The application now includes its first RAG system.

RAG stands for **Retrieval-Augmented Generation**.

Instead of sending every document to the AI whenever a user asks a question, the system first searches for the most relevant parts of the documents.

### Current RAG Flow

```text
Uploaded Documents
        ↓
Text Extraction
        ↓
Document Chunking
        ↓
Embeddings
        ↓
Chroma Vector Database
        ↓
User Question
        ↓
Question Embedding
        ↓
Semantic Search
        ↓
Top Relevant Chunks
        ↓
LLM
        ↓
Grounded Answer
        ↓
Source Documents
```

---

## Document Chunking

Large documents are divided into smaller sections called **chunks**.

This makes it easier for the system to search only the parts of a document that are relevant to a user's question.

The chunking system also uses overlap between chunks so important information near a boundary is less likely to be lost.

---

## Embeddings

Each document chunk is converted into an **embedding**.

An embedding is a numerical representation of the meaning of text.

For example:

```text
"Transactions above $100,000 require CFO approval"

                ↓

[0.018, -0.242, 0.771, ...]
```

The numbers themselves are not meant to be read by a person.

They allow the application to compare the meaning of a user's question with the meaning of different document sections.

---

## Vector Database

The application uses **Chroma** as its local vector database.

Chroma stores:

- Document chunks
- Embeddings
- Source filenames
- Unique chunk IDs

This allows the application to perform semantic searches across previously indexed documents.

The document index can also be cleared from the application.

---

## Semantic Search

When a user asks a question, the question is also converted into an embedding.

The system compares the question embedding against the stored document embeddings and returns the most relevant chunks.

This means the user's wording does not have to exactly match the wording inside the document.

For example:

```text
Question:
"Who approves large financial transactions?"

Possible Matching Document Text:
"Transactions exceeding $100,000 require approval from the Chief Financial Officer."
```

The system can recognize that these statements are related even though they use different wording.

---

## AI Question Answering

After retrieving the most relevant document chunks, the application sends those chunks and the user's question to the LLM.

The model is instructed to:

- Answer only from the retrieved information
- Avoid using unsupported information
- Avoid inventing answers
- State when enough information cannot be found

The user receives:

```text
Question
   ↓
Answer
   ↓
Sources
```

---

## Sources and Retrieval Debugging

The application shows the filenames used to produce an answer.

It also includes an expandable debugging section that shows:

- Retrieved chunks
- Retrieval order
- Source filename
- Vector distance

### Vector Distance

Distance represents how closely a retrieved chunk matches the user's question.

In general:

```text
Lower Distance
      =
Closer Semantic Match
```

This information is mainly used during development to evaluate retrieval quality.

---

## Document Index Management

Because Chroma uses persistent local storage, indexed documents can remain available after the application restarts.

The application now tracks whether documents have been indexed during the current Streamlit session.

Users can also clear the document index.

This helps prevent old documents from being unintentionally included during testing.

---

## Technologies

- Python
- Streamlit
- OpenAI API
- Pandas
- Chroma
- Embeddings
- Retrieval-Augmented Generation
- PDF/TXT Processing
- Prompt Engineering
- Git / GitHub

---

## Main Project Files

```text
AI_Document_Analyzer/
│
├── app.py
├── analyzer.py
├── rag.py
├── chunker.py
├── embeddings.py
├── vector_store.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── sample_docs/
├── evaluations/
└── chroma_db/
```

### `app.py`

Controls the Streamlit user interface and connects the different parts of the application.

### `analyzer.py`

Handles document text extraction and structured AI document analysis.

### `chunker.py`

Splits large documents into smaller searchable chunks.

### `embeddings.py`

Converts document chunks and questions into embedding vectors.

### `vector_store.py`

Stores and searches document embeddings using Chroma.

### `rag.py`

Combines retrieved document information with the user's question and generates a grounded AI response.

---

## Current Project Status

### Phase 1
**Completed**

- LLM integration
- Structured document analysis
- Prompt guardrails
- Evaluation testing

### Phase 2
**Completed**

- TXT/PDF uploads
- Multiple documents
- Text extraction
- Structured results
- Pandas tables
- CSV exports

### Phase 3
**Core RAG Pipeline Completed**

- Document chunking
- Embeddings
- Chroma vector database
- Semantic search
- Top-k retrieval
- RAG answer generation
- Source filenames
- Retrieval debugging
- Persistent index
- Index clearing
- Session-state protection

---

## Next Improvements

The next stage will focus on improving the quality and reliability of the RAG system.

Planned improvements include:

- Source-aware context
- Inline citations
- Better document metadata
- Duplicate-document protection
- Vector database upserts
- Retrieval-quality thresholds
- RAG evaluation tests
- Testing whether generated answers are supported by retrieved evidence

Future phases may also include:

- PostgreSQL integration
- Structured risk and control storage
- SQL queries
- Agentic AI tools
- Automatic tool selection
- AI governance controls
- Logging
- Human review workflows

---

## Long-Term Goal

The long-term goal is to develop the project into an enterprise AI assistant that can search both structured and unstructured risk information.

The finished system should be able to:

1. Analyze enterprise documents
2. Store important risk and control information
3. Search across many documents
4. Answer natural-language questions
5. Show where answers came from
6. Work with structured databases
7. Select tools when needed
8. Maintain human oversight and traceability