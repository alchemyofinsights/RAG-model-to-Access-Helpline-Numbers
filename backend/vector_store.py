# vector_store.py
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import pickle
import os
from langchain_community.embeddings import SentenceTransformerEmbeddings

# ---------- Config ----------
EXCEL_PATH = "helpliness.xlsx"  # make sure your Excel file path is correct
VECTOR_STORE_PATH = "helplines_faiss.pkl"

# ---------- Load Excel ----------
df = pd.read_excel(EXCEL_PATH)

# Clean important fields
df['state'] = df['state'].astype(str).str.strip().str.lower()
df['age_min'] = pd.to_numeric(df['age_min'], errors='coerce').fillna(0)
df['age_max'] = pd.to_numeric(df['age_max'], errors='coerce').fillna(100)

# ---------- Initialize embedding model ----------
embed_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# ---------- Create documents for FAISS ----------
documents = []
for _, row in df.iterrows():
    content = row.get("example_scenarios", "") or row.get("description", "")
    if not isinstance(content, str):
        content = str(content)
    metadata = row.to_dict()
    documents.append(Document(page_content=content, metadata=metadata))

# ---------- Build or load FAISS vector store ----------
if os.path.exists(VECTOR_STORE_PATH):
    print("Loading existing vector store...")
    with open(VECTOR_STORE_PATH, "rb") as f:
        vector_store = pickle.load(f)
else:
    print("Creating new vector store...")
    vector_store = FAISS.from_documents(documents, embed_model)
    with open(VECTOR_STORE_PATH, "wb") as f:
        pickle.dump(vector_store, f)
    print("Vector store saved to", VECTOR_STORE_PATH)

# ---------- Retrieval function ----------
# vector_store.py (retrieval part)
def retrieve_helplines_rag(age, state, scenario, top_k=5, filter_state_age=True):
    """
    Retrieve helplines based on semantic similarity and age/state filter.
    National helplines are shown first, then state-specific ones.
    """
    results = vector_store.similarity_search(scenario, k=top_k)
    national = []
    state_specific = []

    for doc in results:
        meta = doc.metadata
        # Check age filter
        if filter_state_age and not (meta["age_min"] <= age <= meta["age_max"]):
            continue

        # Separate national vs state-specific
        if str(meta["state"]).strip().lower() in ["all", "any", "none", ""]:
            national.append(meta)
        elif meta["state"].strip().lower() == state.strip().lower():
            state_specific.append(meta)

    # If semantic search returned nothing, fallback: return top national numbers anyway
    if not national and not state_specific:
        print("No semantic match found. Returning national helplines as fallback.")
        for doc in vector_store.similarity_search("", k=top_k):  # empty query = fallback top
            meta = doc.metadata
            if str(meta["state"]).strip().lower() in ["all", "any", "none", ""]:
                national.append(meta)

    # Combine: national first, then state-specific
    final_list = national + state_specific
    return final_list
