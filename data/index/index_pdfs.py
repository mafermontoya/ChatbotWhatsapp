# index_pdfs.py
import os, json, glob
from pathlib import Path
from typing import List, Dict
import numpy as np
import faiss
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# Directorios de entrada/salida
PDF_DIR = os.getenv("PDF_DIR", "data/pdfs")
OUT_DIR = os.getenv("RAG_INDEX_DIR", "data/index")
DOCSTORE_PATH = os.path.join(OUT_DIR, "docstore.json")
FAISS_PATH = os.path.join(OUT_DIR, "index.faiss")

# Modelo de embeddings de Gemini
EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "text-embedding-004")

# Parámetros de chunking
CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "1200"))     # caracteres por chunk
CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "200"))

def read_pdf_text(path: str) -> List[Dict]:
    reader = PdfReader(path)
    out = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        out.append({"page": i + 1, "text": t})
    return out

def chunk_text(text: str, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> List[str]:
    text = text.strip().replace("\r", "")
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += max(1, size - overlap)
    return chunks

def embed_many(texts: List[str]) -> np.ndarray:
    vecs = []
    for t in texts:
        res = genai.embed_content(model=EMBED_MODEL, content=t)
        v = np.array(res["embedding"], dtype="float32")
        v = v / (np.linalg.norm(v) + 1e-12)
        vecs.append(v)
    return np.vstack(vecs)

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ Falta GEMINI_API_KEY en tu .env")
    genai.configure(api_key=api_key)

    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    files = sorted(glob.glob(os.path.join(PDF_DIR, "*.pdf")))
    if not files:
        print(f"⚠️ No hay PDFs en {PDF_DIR}")
        return

    docs, raw_texts = [], []
    idx = 0
    for f in files:
        for p in read_pdf_text(f):
            for ci, ch in enumerate(chunk_text(p["text"])):
                docs.append({
                    "id": idx,
                    "file": os.path.basename(f),
                    "page": p["page"],
                    "chunk_id": ci,
                    "text": ch
                })
                raw_texts.append(ch)
                idx += 1

    if not docs:
        print("⚠️ No se generaron chunks")
        return

    print(f"🧠 Generando embeddings de {len(docs)} chunks…")
    mat = embed_many(raw_texts)  # (N, D)
    d = mat.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(mat)

    faiss.write_index(index, FAISS_PATH)
    with open(DOCSTORE_PATH, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    print(f"✅ Índice guardado en {OUT_DIR}")

if __name__ == "__main__":
    main()
