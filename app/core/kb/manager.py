"""Knowledge Base manager for Pinecone operations"""
import os
import time
import re
from dotenv import load_dotenv

# langchain document types
try:
    from langchain.schema import Document
except Exception:
    from langchain_core.documents import Document

# Embeddings
try:
    from langchain.embeddings import OpenAIEmbeddings
except Exception:
    try:
        from langchain_openai import OpenAIEmbeddings
    except Exception:
        raise ImportError("Could not import OpenAIEmbeddings from langchain. Install/upgrade langchain.")

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", None)
INDEX_NAME = os.getenv("PINECONE_INDEX", "sales-agent-kb")
EMBED_DIM = 1536  # matches text-embedding-3-small

# initialize embeddings
emb = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)

# ---------------------------
# ---------------------------
try:
    from pinecone import Pinecone, ServerlessSpec
except Exception as e:
    raise ImportError("Missing pinecone>=5.0.0. Run: pip install pinecone") from e

_index = None
_pc = None


def _init_pinecone_client():
    global _index, _pc

    try:
        # Initialize Pinecone v5.x client
        _pc = Pinecone(api_key=PINECONE_KEY)
        
        # List existing indexes
        existing_indexes = _pc.list_indexes()
        index_names = [idx.name for idx in existing_indexes]
        
        if INDEX_NAME not in index_names:
            print(f"Creating index '{INDEX_NAME}' with Pinecone v5.x API...")
            # Create serverless index (adjust cloud/region as needed)
            _pc.create_index(
                name=INDEX_NAME,
                dimension=EMBED_DIM,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=PINECONE_ENV or "us-east-1"
                )
            )
            print(f"✅ Index '{INDEX_NAME}' created successfully")
        
        _index = _pc.Index(INDEX_NAME)
        
    except Exception as e:
        raise RuntimeError(
            f"Failed to initialize Pinecone index. "
            f"Check PINECONE_API_KEY and PINECONE_ENV. Error: {str(e)}"
        ) from e


# initialize on import
_init_pinecone_client()
index = _index


def init_pinecone_if_needed():
    """Compatibility wrapper used by main.py"""
    if index is None:
        _init_pinecone_client()
    print(f"✅ Pinecone index ready: {INDEX_NAME}")
    return index


# -------------------
# Text normalization / embedding helpers
# -------------------
def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _embed_text(text: str):
    return emb.embed_query(normalize_text(text))


def _embed_texts(texts: list[str], batch_size: int = 20):
    vectors = []
    for i in range(0, len(texts), batch_size):
        batch = [normalize_text(t) for t in texts[i:i+batch_size]]
        batch_vecs = emb.embed_documents(batch)
        vectors.extend(batch_vecs)
    return vectors


# -------------------
# Pinecone helpers
# -------------------
def _upsert(vectors, batch_size: int = 20):
    if not vectors:
        return
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        try:
            # Pinecone v5.x uses index.upsert() directly
            index.upsert(vectors=batch)
        except Exception as e:
            print("❌ _upsert failed:", e)
            raise


def _query(vector, top_k, include_metadata=True):
    try:
        return index.query(vector=vector, top_k=top_k, include_metadata=include_metadata)
    except Exception:
        return index.query(vector=vector, top_k=top_k)


# -------------------
# Add to KB functions
# -------------------
def add_file_to_kb(file_path: str):
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        texts = [p.extract_text() for p in reader.pages if p.extract_text()]
        chunks = [t[i:i+800] for t in texts for i in range(0, len(t), 800)]

        if not chunks:
            print(f"⚠️ No text extracted from {file_path}")
            return

        vectors = _embed_texts(chunks)
        to_upsert = [
            (f"{int(time.time())}_{i}", vec, {"source": file_path, "type": "text"})
            for i, vec in enumerate(vectors)
        ]
        _upsert(to_upsert)
        print(f"✅ added file {file_path}, chunks={len(to_upsert)}")
    except Exception as e:
        print("❌ add_file_to_kb error:", e)


def add_url_to_kb(url: str):
    try:
        import requests
        from bs4 import BeautifulSoup
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        texts = " ".join(p.get_text(separator=" ", strip=True) for p in soup.find_all(["p", "h1", "h2", "h3", "li"]))

        if not texts:
            print(f"⚠️ No text extracted from {url}")
            return

        chunks = [texts[i:i+800] for i in range(0, len(texts), 800)]
        vectors = _embed_texts(chunks)
        to_upsert = [
            (f"{int(time.time())}_u_{i}", vec, {"source": url, "type": "url"})
            for i, vec in enumerate(vectors)
        ]
        _upsert(to_upsert)
        print(f"✅ added url {url}, chunks={len(to_upsert)}")
    except Exception as e:
        print("❌ add_url_to_kb error:", e)


def add_media_to_kb(file_path: str, caption: str):
    try:
        vec = _embed_text(caption)
        meta = {"file_path": file_path, "type": "media", "caption": caption}
        _upsert([(f"media_{int(time.time())}", vec, meta)])
        print(f"✅ added media {file_path}")
    except Exception as e:
        print("❌ add_media_to_kb error:", e)


def add_chat_to_kb(user_msg: str, ai_reply: str, phone: str = None):
    try:
        if phone:
            text = f"Cliente ({phone}): {user_msg}\nAgente: {ai_reply}"
            key = f"chat_{phone}_{int(time.time())}"
            meta = {"source": "chat_history", "phone": phone}
        else:
            text = f"Cliente: {user_msg}\nAgente: {ai_reply}"
            key = f"chat_{int(time.time())}"
            meta = {"source": "chat_history"}

        vec = _embed_text(text)
        _upsert([(key, vec, meta)])
        print(f"✅ Chat archived {('for ' + phone) if phone else ''}")
    except Exception as e:
        print("❌ add_chat error:", e)


def query(text: str, top_k: int = 3):
    try:
        vec = _embed_text(text)
        res = _query(vec, top_k=top_k, include_metadata=True)
        docs = []
        matches = res.get("matches", res.get("results", [])) if isinstance(res, dict) else []
        for match in matches:
            md = match.get("metadata", {}) or match.get("meta", {})
            content = md.get("caption") or md.get("source") or ""
            docs.append(Document(page_content=content, metadata=md))
        return docs
    except Exception as e:
        print("❌ query error:", e)
        return []

