### 🤖 Hybrid Document Knowledge Bot & RAG System

A production-ready, interactive web application that enables semantic searching, pinpoint conversational Q&A, and full-context summarization over both uploaded PDF documents and pasted raw text blocks. This project leverages **Google Gemini 3.5 Flash** for reasoning, **ChromaDB** for vector storage, and an offline **Sentence-Transformers** model to execute token-efficient Retrieval-Augmented Generation (RAG). 

🌐 **[Live Demo Link](https://pdf-knowledge-bot.streamlit.app/)** | 📂 **Repository:** https://github.com/leonz92/pdf-knowledge-bot

### 🚀 Key Features

* **Dual-Ingestion Pipelines:** Symmetrical support for processing structurally rigid, multi-page PDFs alongside ephemeral, unformatted pasted text blocks.
* **Semantic Q&A (Local RAG):** Automatically parses documents, generates 384-dimensional vector mappings locally via all-MiniLM-L6-v2, and injects the top 3 contextual fragments to the LLM.
* **Full-Context Summarization Tracker:** Bypasses database text segmentation to leverage Gemini’s native high-context memory window, providing full executive summaries for PDFs or raw copy-paste data with a single click.
* **Conversational Session Memory:** Employs a sliding context window capped at the last 5 turns to intelligently track coreferences and relative pronouns without inflating API costs.
* **Page-Level Citation Tracking:** Unpacks and flattens nested metadata elements returned by ChromaDB queries to supply explicit source page references for generated answers.
* **Defensive Data Constraints:** Configured with real-time character limit warnings (up to 250,000 characters) and page thresholds to protect free-tier API rate caps.

### 🏗️ Architecture Design & Logic Routing

```
                                  ┌───► [ PDF Upload ] ───► Local Embeddings ───► ChromaDB Vector Lookup
                                  │                                                   │
[ User Context ] ──► [ UI Router ]──┤                                                 ▼
                                  │                                           [ Prompt Assembler ] ──► [ Gemini LLM Engine ]
                                  └───► [ Pasted Text ] ──────────────────────────────┘
```

### 🛠️ Tech Stack & Environment Design

* **Runtime Environment:** Python 3.11.x / 3.12.x *(Intentionally pinned to avoid dependency conflicts with PyTorch/Sentence-Transformers wheels on experimental versions).*
* **Large Language Model API:** Google Generative AI (gemini-2.5-flash or newer)
* **Local Embedding Vector Space:** Sentence-Transformers (all-MiniLM-L6-v2)
* **Vector Database:** ChromaDB (Local Persistent SQLite-backed Storage)
* **Frontend Framework:** Streamlit Layout Platform
* **Document Processing:** PyPDF Extraction Engine

### 📦 File & Project Layout

```
my-pdf-chatbot/
│
├── .env                  # Local environment API keys (git-ignored)
├── .gitignore            # Production git exclusions filter
├── requirements.txt      # Stable dependency pinning manifest
├── .python-version       # Local pyenv version pin (e.g., 3.11.9)
│
├── app.py                # Controller: Streamlit web UI layouts & state machine
├── database.py           # Infrastructure: Local ChromaDB collection logic & PDF parsers
├── llm_service.py        # Core Engine: Gemini prompts templates & history handlers
│
└── my_vector_db/         # Automatically created database storage binaries
```

### ⚙️ Quick Local Configuration

### 1. Version Pinning & Virtual Environment Setup

Ensure your working directory is running Python 3.11 or 3.12 to match production dependency paths: 

```
git clone https://github.com/leonz92/pdf-knowledge-bot.git
cd pdf-knowledge-bot

# Configure pyenv local constraint
pyenv install 3.11.9
pyenv local 3.11.9

# Install pinned software manifests
pip install -r requirements.txt
```

### 2. Environment Variables Configuration

Generate a .env file in the root folder of your project workspace and register your developer token: 

```
GEMINI_API_KEY=your_google_ai_studio_api_key_here
```

### 3. Launch the Application UI

```
streamlit run app.py
```

### 📄 License

Distributed under the MIT License. See LICENSE for more details.
