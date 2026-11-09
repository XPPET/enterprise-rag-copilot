import os
import json
import time
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pypdf import PdfReader
import chromadb
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Δεν βρέθηκε API Key στο αρχείο .env!")

client = genai.Client(api_key=api_key)

# 1. Pydantic Schemas για Enterprise Output
class Citation(BaseModel):
    document_name: str = Field(description="Το όνομα του αρχείου προέλευσης")
    page_number: str = Field(description="Ο αριθμός σελίδας")
    quote: str = Field(description="Ακριβές απόσπασμα από το κείμενο")

class RiskFlag(BaseModel):
    risk_level: str = Field(description="Επίπεδο κινδύνου: LOW, MEDIUM, ή HIGH")
    description: str = Field(description="Περιγραφή του κινδύνου ή της ασάφειας")

class EnterpriseResponse(BaseModel):
    executive_summary: str = Field(description="Σύντομη περίληψη 2-3 προτάσεων για στελέχη")
    detailed_findings: List[str] = Field(description="Αναλυτικά σημεία με ακριβή νούμερα και γεγονότα")
    citations: List[Citation] = Field(description="Λίστα με τις ακριβείς πηγές των δεδομένων")
    risk_flags: List[RiskFlag] = Field(description="Πιθανοί επιχειρηματικοί, νομικοί ή οικονομικοί κίνδυνοι")
    action_items: List[str] = Field(description="Προτεινόμενες άμεσες ενέργειες για τη διοίκηση")


# 2. Vector DB (ChromaDB με native built-in embeddings)
CHROMA_PATH = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="enterprise_knowledge")

def index_uploaded_pdf(file_path: str, filename: str, max_pages: int = 40) -> int:
    """Επεξεργασία, chunking και μαζική αποθήκευση στο ChromaDB."""
    reader = PdfReader(file_path)
    total_pages = min(len(reader.pages), max_pages)
    
    docs_to_add = []
    metas_to_add = []
    ids_to_add = []
    
    current_count = collection.count()
    chunk_id = current_count
    
    for page_idx in range(total_pages):
        try:
            text = reader.pages[page_idx].extract_text() or ""
        except Exception:
            continue
        
        for i in range(0, len(text), 800):
            sub_text = text[i:i+900].strip()
            if len(sub_text) > 80:
                docs_to_add.append(sub_text)
                metas_to_add.append({"doc_name": filename, "page": str(page_idx + 1)})
                ids_to_add.append(f"chunk_{chunk_id}")
                chunk_id += 1

    # Μαζική καταχώρηση απευθείας στο ChromaDB (τοπική διανυσματοποίηση)
    if docs_to_add:
        collection.add(
            ids=ids_to_add,
            documents=docs_to_add,
            metadatas=metas_to_add
        )
                
    return len(docs_to_add)


# 3. Query Execution
def query_copilot(query_text: str) -> EnterpriseResponse:
    if collection.count() == 0:
        raise ValueError("Δεν υπάρχουν δεδομένα στη βάση. Παρακαλώ ανέβασε ένα αρχείο PDF πρώτα.")

    # 1. Σημασιολογική αναζήτηση στα 6 πιο σχετικά αποσπάσματα
    search_results = collection.query(
        query_texts=[query_text],
        n_results=min(6, collection.count())
    )

    docs = search_results["documents"][0]
    metas = search_results["metadatas"][0]

    context_blocks = []
    for doc, meta in zip(docs, metas):
        context_blocks.append(
            f"[Doc: {meta['doc_name']} | Page: {meta['page']}]\n{doc}"
        )
    
    context_str = "\n\n---\n\n".join(context_blocks)

    system_instruction = (
        "Είσαι ένας Enterprise AI Copilot για στελέχη της EY και πελατών της. "
        "Απάντησε στο ερώτημα του χρήστη ΑΠΟΚΛΕΙΣΤΙΚΑ βάσει του παρεχόμενου Context. "
        "Αν κάτι δεν αναφέρεται, δήλωσε σαφώς ότι δεν προκύπτει από τα διαθέσιμα έγγραφα. "
        "Συμπερίλαβε πάντα ακριβή citations (έγγραφο, σελίδα, αυτούσιο quote) και εντόπισε risk flags."
    )

    prompt = f"Context:\n{context_str}\n\nΕρώτημα Στελέχους: {query_text}"

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.1,
        response_mime_type="application/json",
        response_schema=EnterpriseResponse,
    )

    # Retry logic αποκλειστικά στο gemini-3.8-flash
    max_retries = 3
    delay = 2

    for attempt in range(max_retries):
        try:
            print(f"-> Κλήση Gemini (προσπάθεια {attempt + 1}/{max_retries})...")
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=config,
            )
            parsed_json = json.loads(response.text)
            return EnterpriseResponse(**parsed_json)
        except Exception as e:
            print(f"-> Προσωρινό σφάλμα: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                raise e