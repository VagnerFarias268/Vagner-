# Directory Structure and Import Paths

## Current Project Structure

```
/home/ubuntu/projects/Vagner-/          ← PROJECT ROOT (run from here!)
├── .env
├── .env.example
├── .gitignore
├── run.py                              ← Entry point (recommended)
├── requirements.txt
├── app/                                ← Python package
│   ├── __init__.py
│   ├── main.py                         ← FastAPI application
│   ├── config.py
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── utils/
├── scripts/
│   └── init_kb.py
└── materials/
    ├── pdfs/
    ├── media/
    └── temp/
```

## Why the Import Error Happens

### ❌ Running from INSIDE app/ directory:

```bash
ubuntu@server:~$ cd /home/ubuntu/projects/Vagner-/app/
ubuntu@server:~/projects/Vagner-/app$ python3 main.py
```

**What Python sees:**
- Current directory: `/home/ubuntu/projects/Vagner-/app/`
- Looking for: `app.config` module
- Python searches in: `/home/ubuntu/projects/Vagner-/app/app/config.py`
- Result: ❌ **ModuleNotFoundError: No module named 'app'**

### ✅ Running from PROJECT ROOT:

```bash
ubuntu@server:~$ cd /home/ubuntu/projects/Vagner-/
ubuntu@server:~/projects/Vagner-$ python3 run.py
```

**What Python sees:**
- Current directory: `/home/ubuntu/projects/Vagner-/`
- Looking for: `app.config` module
- Python searches in: `/home/ubuntu/projects/Vagner-/app/config.py`
- Result: ✅ **Import successful!**

## The Import Chain

When you run from the project root:

```python
# run.py (at root level)
from app.config import get_settings  # ✅ Finds app/config.py

# app/main.py
from app.config import get_settings  # ✅ Finds ../config.py
from app.api.routes import webhook    # ✅ Finds api/routes/webhook.py
from app.core.kb.manager import ...   # ✅ Finds core/kb/manager.py
```

## Quick Reference

### Always use these commands:

```bash
# Navigate to project root
cd /home/ubuntu/projects/Vagner-

# Activate virtual environment  
source venv/bin/activate

# Start server (pick one)
python3 run.py                          # Recommended
python3 -m app.main                     # Alternative
uvicorn app.main:app --reload           # Direct uvicorn

# Initialize knowledge base
python3 scripts/init_kb.py

# Run any other script
python3 scripts/other_script.py
```

### Never do this:

```bash
cd /home/ubuntu/projects/Vagner-/app/   # ❌ Wrong!
python3 main.py                          # ❌ Will fail!

cd /home/ubuntu/projects/Vagner-/scripts/  # ❌ Wrong!
python3 init_kb.py                          # ❌ Will fail!
```
