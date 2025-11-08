## MedSafeAI — Offline AI Assistant for Medication Safety

**MedSafeAI** is an offline AI-based web application designed to extract and summarize drug safety information from official medical PDF documents.
The system provides structured data about medication dosage, contraindications, and side effects through a local large language model (LLM) without requiring an internet connection.

Drug safety information is often contained in long, complex, and non-searchable PDF documents.
Such data can be difficult to access and interpret, especially in regulated environments where online medical databases have limited availability.
This limits both healthcare providers and patients in obtaining accurate and timely drug guidance.
MedSafeAI provides a local, AI-powered solution that automatically reads, analyzes, and summarizes medical documentation.
The user enters the name of a medication and receives organized information about dosage, contraindications, and side effects in a concise format.


### System Design

* **Frontend (HTML, CSS, JavaScript):**
  User interface for entering drug names and displaying structured results.

* **Backend (FastAPI):**
  Handles API routing, static file serving, and communication with the local LLM.

* **PDF Parser (PyMuPDF):**
  Extracts and processes raw text from official medical PDFs.

* **LLM Engine (Ollama + Mistral):**
  Performs local inference to identify relevant medical details and generate human-readable output.

---

### Tech Stack

| Component      | Technology            |
| -------------- | --------------------- |
| Frontend       | HTML, CSS, JavaScript |
| Backend        | FastAPI (Python)      |
| PDF Processing | PyMuPDF               |
| Model          | Mistral via Ollama    |
| Deployment     | Offline / Local       |

