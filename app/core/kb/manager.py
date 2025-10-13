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
def extract_urls_from_text(text: str) -> list[str]:
    """Extract all URLs from text using regex"""
    # Pattern to match http/https URLs
    url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    urls = re.findall(url_pattern, text)
    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    return unique_urls


def scrape_url_content(url: str) -> str:
    """Scrape text content from a URL"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        print(f"  🌐 Scraping URL: {url}")
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text from relevant tags
        texts = " ".join(
            element.get_text(separator=" ", strip=True) 
            for element in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "article", "section"])
        )
        
        if texts:
            print(f"    ✅ Scraped {len(texts)} characters from {url}")
            return texts
        else:
            print(f"    ⚠️ No text extracted from {url}")
            return ""
            
    except Exception as e:
        print(f"    ❌ Failed to scrape {url}: {e}")
        return ""


def add_file_to_kb_with_urls(file_path: str, scrape_urls: bool = True):
    """
    Add a PDF file to the knowledge base.
    If scrape_urls=True, extracts URLs from the PDF and scrapes their content as well.
    
    Args:
        file_path: Path to the PDF file
        scrape_urls: Whether to scrape URLs found in the PDF (default: True)
    """
    try:
        from PyPDF2 import PdfReader
        
        # Extract text from PDF
        reader = PdfReader(file_path)
        texts = [p.extract_text() for p in reader.pages if p.extract_text()]
        full_text = " ".join(texts)
        
        if not full_text:
            print(f"⚠️ No text extracted from {file_path}")
            return
        
        # Check for URLs in the PDF
        urls_found = []
        scraped_content = []
        
        if scrape_urls:
            urls_found = extract_urls_from_text(full_text)
            
            if urls_found:
                print(f"📎 Found {len(urls_found)} URL(s) in {file_path}")
                
                # Scrape each URL
                for url in urls_found:
                    content = scrape_url_content(url)
                    if content:
                        scraped_content.append({
                            'url': url,
                            'content': content
                        })
        
        # Chunk the PDF text
        pdf_chunks = [full_text[i:i+800] for i in range(0, len(full_text), 800)]
        
        # Chunk the scraped content
        all_chunks = pdf_chunks.copy()
        scraped_chunks_metadata = []
        
        for scraped in scraped_content:
            url = scraped['url']
            content = scraped['content']
            url_chunks = [content[i:i+800] for i in range(0, len(content), 800)]
            
            # Track which chunks came from which URL
            for chunk in url_chunks:
                all_chunks.append(chunk)
                scraped_chunks_metadata.append(url)
        
        if not all_chunks:
            print(f"⚠️ No content to vectorize from {file_path}")
            return
        
        # Vectorize all chunks
        vectors = _embed_texts(all_chunks)
        
        # Prepare vectors for upsert
        to_upsert = []
        timestamp = int(time.time())
        
        # Add PDF chunks
        for i in range(len(pdf_chunks)):
            to_upsert.append((
                f"{timestamp}_{i}", 
                vectors[i], 
                {"source": file_path, "type": "pdf"}
            ))
        
        # Add scraped URL chunks
        for i in range(len(pdf_chunks), len(all_chunks)):
            url_source = scraped_chunks_metadata[i - len(pdf_chunks)]
            to_upsert.append((
                f"{timestamp}_url_{i}", 
                vectors[i], 
                {"source": url_source, "type": "url_from_pdf", "pdf_source": file_path}
            ))
        
        # Upsert to Pinecone
        _upsert(to_upsert)
        
        pdf_chunk_count = len(pdf_chunks)
        url_chunk_count = len(all_chunks) - len(pdf_chunks)
        
        print(f"✅ Added file {file_path}")
        print(f"   📄 PDF chunks: {pdf_chunk_count}")
        if url_chunk_count > 0:
            print(f"   🌐 URL chunks: {url_chunk_count} (from {len(scraped_content)} URLs)")
        
    except Exception as e:
        print(f"❌ add_file_to_kb_with_urls error: {e}")
        import traceback
        traceback.print_exc()


def add_file_to_kb(file_path: str):
    """
    Legacy function - now calls add_file_to_kb_with_urls with default settings.
    Kept for backwards compatibility.
    """
    add_file_to_kb_with_urls(file_path, scrape_urls=True)


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

