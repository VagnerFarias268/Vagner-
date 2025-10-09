# Critical Fixes Applied ✅

## Problem 1: Pinecone API Version Mismatch

### Error
```
AttributeError: init is no longer a top-level attribute of the pinecone package.
```

### Root Cause
The code was using the **old Pinecone API** (`pinecone.init()`, `pinecone.Client()`), but `requirements.txt` specifies **Pinecone v5.0.1** which uses a completely different API.

### Solution
Updated `app/core/kb/manager.py` to use the new Pinecone v5.x API:

**Before (Old API - doesn't work):**
```python
import pinecone
pinecone.init(api_key=PINECONE_KEY, environment=PINECONE_ENV)
_index = pinecone.Index(INDEX_NAME)
```

**After (New v5.x API - works!):**
```python
from pinecone import Pinecone, ServerlessSpec

_pc = Pinecone(api_key=PINECONE_KEY)
_index = _pc.Index(INDEX_NAME)
```

### Verification
```bash
✅ Pinecone initialized successfully!
✅ Application started on http://0.0.0.0:8000
✅ Index: sales-agent-kb
```

---

## Problem 2: Path Resolution in init_kb.py

### Error
```
⚠️ PDF folder not found: /home/ubuntu/materials/pdfs
```

### Root Cause
The script used `os.path.abspath()` which converts relative paths based on the **current working directory** where you run the script. This caused the script to look for `materials/pdfs` in the wrong location:

- If run from `/home/ubuntu/projects/Vagner-/` → looks for `/home/ubuntu/projects/Vagner-/materials/pdfs` ✅
- If run from `/home/ubuntu/` → looks for `/home/ubuntu/materials/pdfs` ❌

### Solution
Updated `scripts/init_kb.py` to always use paths relative to the **PROJECT_ROOT** (where the script is located):

**Before:**
```python
pdf_folder = os.path.abspath(pdf_folder)  # Depends on current directory
```

**After:**
```python
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.isabs(pdf_folder):
    pdf_folder = os.path.join(PROJECT_ROOT, pdf_folder)  # Always correct
```

### Verification
Tested by running from different directories:
```bash
# Run from /home/ubuntu (not project root)
cd /home/ubuntu && python3 /home/ubuntu/projects/Vagner-/scripts/init_kb.py

# Results:
✅ PDF folder: /home/ubuntu/projects/Vagner-/materials/pdfs
✅ Processing: 100 IDEIAS PARA @ NO INSTAGRAM _ SECAPS CHÁ.pdf
✅ Ingested 1 documents (7 chunks)
```

---

## Files Modified

### 1. `/app/core/kb/manager.py`
- ✅ Replaced old Pinecone API with v5.x API
- ✅ Updated `_init_pinecone_client()` function
- ✅ Simplified `_upsert()` function
- ✅ Added proper ServerlessSpec for index creation

### 2. `/scripts/init_kb.py`
- ✅ Added `PROJECT_ROOT` variable
- ✅ Fixed `ingest_pdfs()` path resolution
- ✅ Fixed `ingest_media()` path resolution
- ✅ Now works from any directory

---

## How to Use

### Start the Application
```bash
cd /home/ubuntu/projects/Vagner-
source venv/bin/activate
python3 run.py
```

**Expected Output:**
```
✅ Folders initialized
✅ Pinecone initialized
🚀 Application started successfully on 0.0.0.0:8000
```

### Initialize Knowledge Base
```bash
cd /home/ubuntu/projects/Vagner-
source venv/bin/activate
python3 scripts/init_kb.py
```

**Expected Output:**
```
🚀 Initializing Knowledge Base
📚 Ingesting PDFs from /home/ubuntu/projects/Vagner-/materials/pdfs...
✅ Ingested X documents
✅ Knowledge Base initialization complete!
```

---

## API Keys Required

Make sure your `.env` file contains valid values for:

```bash
# Required API Keys
OPENAI_API_KEY=sk-...                    # Get from: https://platform.openai.com/api-keys
PINECONE_API_KEY=pcsk_...                # Get from: https://app.pinecone.io/
PINECONE_ENV=us-east-1                   # Your Pinecone region
WHATSAPP_ACCESS_TOKEN=...                # From Facebook Developers
WHATSAPP_PHONE_ID=...                    # From Facebook Developers  
ELEVENLABS_API_KEY=...                   # Get from: https://elevenlabs.io/
```

---

## Summary

✅ **Both critical issues are now fixed**
✅ **Application starts successfully**
✅ **Pinecone v5.x API working**
✅ **Path resolution working from any directory**
✅ **PDF ingestion working**

Your application is now ready to use! 🚀
