# RAG-model-to-Access-Helpline-Numbers
This Project aims in using **Retrieval-Augmented Generation (RAG)** to efficiently access helpline numbers for users . As there are a lot of helpline numbers available , as users , during the times of turmoil , we may not be able to access the right helpline when needed. This is the motive behind this project , to make helpline numbers more accessible , by giving simple user prompts and designed to provide **calm, safe, and relevant guidance** during emergency or distress situations, along with **verified helpline numbers** based on the user’s scenario, age, and state.This project combines **AI reasoning + structured helpline data**, making it suitable for real-world social impact use cases.

---

##  Features : 

-  **RAG-based AI advice generation**
-  **State-specific helpline recommendations**
-  Semantic search over helpline data
-  Automatic vector store (`.pkl`) creation
-  Clean web interface

---

##  Architecture Overview :


---

## Directory & File Structure : 

helpline_rag/
│
├── backend/
│   ├── app.py                 # Flask API entry point
│   ├── rag_graph.py           # RAG orchestration logic
│   ├── vector_store.py        # Vector store (PKL) handling
│   ├── hf_llm.py              # LLM wrapper
│   ├── helplines.xlsx         # Source helpline dataset
│   │
│   ├── templates/
│   │   └── index.html         # HTML template (Flask-rendered)
│   │
│   └── static/
│       ├── style.css          # CSS styling
│       └── script.js          # Frontend logic
│
└── README.md

---



