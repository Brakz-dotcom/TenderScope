# 📄 TenderScope: Smart Contract & Tender Compliance Auditor
An end-to-end Retrieval-Augmented Generation (RAG) system built to audit commercial leases, agreements, and tender documents with deterministic source-grounded citations.

## ⚡ Features
- **Deterministic Citation Grounding:** Binds every finding directly to exact page metadata (`[Source: Page X]`), suppressing hallucinations on critical financial and liability terms.
- **Sub-Second RAG Inference:** Utilizes HuggingFace `sentence-transformers` for dense semantic embeddings and Groq LPU inference (`openai/gpt-oss-120b`).
- **Interactive Audit Presets:** One-click automated clause extraction for Liquidated Damages, Site Maintenance/Fuel obligations, and Equipment Lease Scope.
- **Deduplicated Source Inspection:** Inspectable source drawer displaying verbatim retrieved text passages without duplicate chunk clutter.

## 🛠️ Tech Stack
- **Framework:** Python, LangChain (LCEL)
- **Frontend:** Streamlit
- **PDF Extraction:** PyMuPDF (`fitz`)
- **Vector Database:** ChromaDB
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Inference Engine:** Groq Cloud API

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Brakz-dotcom/TenderScope.git](https://github.com/Brakz-dotcom/TenderScope.git)
cd TenderScope
   ```

2. **Set up a virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**  
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the auditor:**
   ```bash
   streamlit run app.py
   ```
