### 🤖 Multimodal PDF Knowledge Bot & RAG System

A production-ready, interactive web application that enables semantic searching, pinpoint Q&A, and high-level summarization over uploaded PDF documents. This project leverages **Google Gemini 1.5 Flash** for natural language understanding and **ChromaDB** as a vector database to achieve Retrieval-Augmented Generation (RAG). 

🌐 **[Live Demo Link](https://your-app-name.streamlit.app)** | 📂 **Repository:** https://github.com/yourusername/your-repo-name 

### 🚀 Key Features

* **Semantic Q&A (RAG):** Uses a sliding context window to fetch the top 3 most relevant data fragments matching a user's question, passing them securely to the LLM.
* **Global Context Summarization:** Leverages Gemini 1.5 Flash's native 1M token context window to parse and summarize full documents in a single, high-fidelity pass.
* **Conversational Memory:** Preserves a sliding conversational history window across 5 turns to intelligently resolve relative pronouns and follow-up prompts.
* **Source Material Tracking:** Extracts and caches PDF page numbers as document metadata to display concrete citations for every generated answer.
* **Clean UI Layout:** Designed using Streamlit to offer a lightweight, fully dynamic chat bubble interface and persistent session variables.

### 🏗️ Architecture Flow

text

[ User Query ] ──> [ Query Embedding (Gemini embedding-001) ]
                           │
                           ▼
                    [ ChromaDB Lookup ] ──> (Extracts text chunks + metadata)
                           │
                           ▼
[ Chat History ] ──> [ Prompt Assembler ]
                           │
                           ▼
                 [ Gemini 1.5 Flash ] ──> [ Cohesive Response + Citations ]

Use code with caution.

### 🛠️ Tech Stack

* **Core Engine:** Python 3.11+
* **Large Language Model API:** Google Generative AI (gemini-1.5-flash)
* **Embedding Vector Space:** Google AI (embedding-001)
* **Vector Database:** ChromaDB (Local Persistent Engine)
* **Frontend / Interface:** Streamlit Framework
* **Document Processing:** PyPDF Extraction Engine

### 📦 File & Project Layout

text

my-pdf-chatbot/
│
├── .env                  # Local environment API variables (git-ignored)
├── .gitignore            # Production safety filters
├── requirements.txt      # Engine dependency manifests
│
├── app.py                # Main Entrypoint: Streamlit UI routing & runtime states
├── database.py           # Infrastructure: ChromaDB vector collections & file ingestion
├── llm_service.py        # Brain Core: Gemini prompt engineering & history handlers
│
└── my_vector_db/         # Automatically created database storage binaries

Use code with caution.

### ⚙️ Quick Local Configuration

### 1. Repository Setup & Installations

bash

git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt

Use code with caution.

### 2. Environment Variables

Create a .env file in the root folder and register your developer token: 

env

GEMINI_API_KEY=your_google_ai_studio_api_key

Use code with caution.

### 3. Launch the Application

bash

streamlit run app.py

Use code with caution.

### ☁️ Deployment Guidelines (Streamlit Community Cloud)

1. Commit changes to your GitHub profile (ensuring .env and my_vector_db/ are skipped by your .gitignore).
2. Log into [share.streamlit.io](https://share.streamlit.io/) via GitHub.
3. Establish a **New App** tracking your designated repository code path.
4. Open **Advanced Settings > Secrets** and paste your credentials securely: 

toml

GEMINI_API_KEY = "your_actual_api_key_here"

Use code with caution.
5. Click **Deploy**.

### 📄 License

Distributed under the MIT License. See LICENSE for more information.
