# Enterprise AI Knowledge Assistant & Copilot 💼🔍

> Production-grade RAG pipeline and executive audit dashboard engineered for automated corporate filing analysis, financial disclosures (Form 10-K, 20-F, Annual Reports), and strategic risk management.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Vector_DB-ChromaDB-FFA000" alt="ChromaDB">
  <img src="https://img.shields.io/badge/LLM-Gemini_3.8_Flash-4285F4?logo=google&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/Architecture-RAG_%26_Grounding-informational" alt="Architecture">
</p>

---

## 📌 Executive Summary

Enterprise analysts and auditors spend hundreds of hours manually cross-referencing complex annual reports, regulatory filings, and corporate governance decks. Traditional LLM query approaches suffer from non-deterministic outputs, contextual hallucinations, and a complete absence of traceable proof.

**Enterprise AI Copilot** addresses these enterprise constraints by pairing an embedded, high-throughput vector store (**ChromaDB**) with **Google Gemini 3.8 Flash** via strict schema validation.

Every response enforces a deterministic JSON structure containing quantified findings, categorized operational risk matrices, and audit-grade citations pinpointing exact source documents, page numbers, and verbatim quotes.

## 🏛 System Architecture

The platform follows a modular Retrieval-Augmented Generation (RAG) architecture, separating document ingestion, semantic indexing, retrieval, reasoning, and executive reporting.

<img width="2620" height="2810" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/c9532d0c-fbc5-44d1-bf94-8a0337793375" />


## ✨ Key Enterprise Capabilities

### 1. Zero-Hallucination Guardrails
- Restricts model-generated conclusions to retrieved document context.
- Explicitly flags missing or unsupported information as unverified.
- Prevents unsupported assumptions from being presented as factual findings.

### 2. Audit-Grade Citations
- Every extracted financial metric is linked to its originating document.
- Page-level references for traceability.
- Verbatim quotations supporting extracted findings.
- Evidence-based financial and operational risk assessments.

### 3. Resilient API Architecture
- Exponential backoff and transient retry mechanisms.
- Handles temporary API overload and HTTP 503 errors.
- Modular backend architecture using FastAPI.

### 4. Strict Type Safety
- Pydantic v2 schema enforcement.
- Structured JSON responses.
- Validation between the LLM reasoning engine and presentation layer.

### 5. Executive Briefing Export
- One-click Markdown report generation.
- C-suite-ready executive summaries.
- Quantified financial findings.
- Categorized risk assessments.
- Supporting audit evidence.

## 📂 Project Structure

```text
enterprise-rag-copilot/
│
├── .env.example            # Environment variables template
├── .gitignore              # Secrets and environment exclusions
├── app.py                  # FastAPI backend endpoints
├── dashboard.py            # Streamlit executive dashboard
├── rag_engine.py           # RAG pipeline and Gemini reasoning engine
├── requirements.txt        # Runtime dependencies
└── README.md               # Architecture documentation
```

## 🛠 Tech Stack

| Layer | Component | Technology |
|---|---|---|
| LLM & Reasoning | Generative AI | Google Gemini 3.8 Flash |
| AI Integration | SDK | google-genai |
| Vector Database | Persistent Vector Store | ChromaDB |
| Embeddings | Local Semantic Embeddings | ChromaDB ONNX |
| Validation | Schema Enforcement | Pydantic v2 |
| Frontend | Executive Dashboard | Streamlit |
| API Backend | REST Service | FastAPI / Uvicorn |
| Document Parser | PDF Processing | PyPDF |
| Language | Runtime | Python 3.11 / 3.12 |

## 🚀 Quickstart Guide

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.11 or 3.12
- Git
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### 2. Clone the Repository

```bash
git clone https://github.com/XPPET/enterprise-rag-copilot.git

cd enterprise-rag-copilot
```

### 3. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv venv

.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv venv

source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create your local environment file:

```bash
cp .env.example .env
```

For Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and insert your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Security Note:** Never commit your `.env` file or expose API credentials in public repositories.

### 6. Launch the Application

**Option A: Interactive Executive Dashboard (Recommended)**

```bash
streamlit run dashboard.py
```

Open your browser:

```text
http://localhost:8501
```

**Option B: REST API Service**

```bash
uvicorn app:app --reload --port 8000
```

Interactive Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🧪 Production Verification & Benchmarks

The system was validated against a real-world corporate filing:

**Test Dataset:** Danaos Corporation 2024 Annual Report / Form 20-F

| Benchmark | Result |
|---|---|
| Document Length | 40+ pages |
| Indexed Chunks | 193 |
| Local ChromaDB Retrieval Latency | ~250 ms |
| Gemini Generation & Schema Parsing | ~2.5 seconds |
| Context Accuracy | 100% on the reported verification sample |

### Sample Structured Analysis

The following is an illustrative excerpt of the reported validation output:

```json
{
  "executive_summary": "Danaos Corporation reported historic performance in 2024, surpassing $1B in operating revenues with a contracted backlog of $3.4B, while navigating Red Sea security disruptions and tariffs.",
  "detailed_findings": [
    "Operating revenues reached $1.01B; Adjusted EBITDA stood at $723M; Adjusted Net Income at $532M.",
    "Contracted revenue backlog increased to $3.4B (average duration of 3.7 years).",
    "Net Debt to Adjusted EBITDA leverage maintained at a conservative 0.4x with $807M in total liquidity."
  ],
  "risk_flags": [
    {
      "risk_level": "HIGH",
      "description": "Red Sea transit disruptions driven by Houthi attacks impacting international supply lines."
    },
    {
      "risk_level": "HIGH",
      "description": "Shifting US trade and tariff frameworks introducing macro freight unpredictability."
    }
  ]
}
```

### Performance Highlights

- **Retrieval:** Approximately 250 ms for local ChromaDB similarity search.
- **Generation:** Approximately 2.5 seconds for Gemini generation and schema parsing.
- **Context Accuracy:** 100% verified against primary SEC disclosures in the reported test sample.

*Benchmark figures are project-reported measurements and may vary depending on hardware, document size, retrieval configuration, and API conditions.*

## 🔒 Security & Data Hygiene

Security and data isolation are essential for enterprise document processing.

- **No Secrets Committed:** `.env` and sensitive configurations are excluded through `.gitignore`.
- **Isolated Vector Indices:** Local vector databases and uploaded document stores are excluded from version control.
- **Credential Isolation:** API credentials are managed through environment variables.
- **Evidence Traceability:** Findings retain source-document references for audit review.
- **Validated Outputs:** Pydantic schemas enforce structured response validation.

## 🎯 Business Value

Enterprise AI Copilot is designed to reduce the manual effort associated with:

- Financial statement analysis.
- Annual report and SEC filing reviews.
- Corporate governance assessments.
- Operational and strategic risk identification.
- Executive reporting and audit preparation.
- Cross-document information retrieval.

The result is a document intelligence workflow that combines semantic search, grounded AI reasoning, and structured executive reporting.

## 🔮 Future Enhancements

Potential extensions for the platform include:

- Multi-document comparative financial analysis.
- SEC EDGAR automated filing ingestion.
- Hybrid retrieval combining semantic and keyword search.
- Role-based access control (RBAC).
- Enterprise authentication and audit logging.
- Multi-agent financial analysis workflows.
- Docker-based deployment and cloud infrastructure integration.
- Automated monitoring and evaluation of retrieval quality.

## 👨‍💻 Author & Repository

**Project:** Enterprise AI Knowledge Assistant & Copilot

**GitHub:** [XPPET/enterprise-rag-copilot](https://github.com/XPPET/enterprise-rag-copilot)

---

<p align="center">
  <b>Built for evidence-driven enterprise intelligence.</b><br>
  <i>From corporate filings to actionable executive insights.</i>
</p>
