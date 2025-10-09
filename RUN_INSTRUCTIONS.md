# How to Run the Application

## ⚠️ Important: Always Run from Project Root

The application MUST be run from: `/home/ubuntu/projects/Vagner-/`

**DO NOT** run it from inside the `app/` directory!

## 3 Ways to Run the Application

### Method 1: Using run.py (Recommended)
```bash
cd /home/ubuntu/projects/Vagner-
source venv/bin/activate
python3 run.py
```

### Method 2: Using Python module syntax
```bash
cd /home/ubuntu/projects/Vagner-
source venv/bin/activate
python3 -m app.main
```

### Method 3: Using uvicorn directly
```bash
cd /home/ubuntu/projects/Vagner-
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Why You Got the Error

❌ **What you did:**
```bash
cd /home/ubuntu/projects/Vagner-/app/  # Wrong directory!
python3 main.py  # Error: ModuleNotFoundError: No module named 'app'
```

✅ **What you should do:**
```bash
cd /home/ubuntu/projects/Vagner-/  # Project root!
python3 run.py  # Works perfectly!
```

## The Same Rule Applies to Other Scripts

### Running init_kb.py
```bash
cd /home/ubuntu/projects/Vagner-
source venv/bin/activate
python3 scripts/init_kb.py
```

### General Rule
**Always run scripts from the project root** so Python can find the `app` module.

## Quick Start Commands

```bash
# Navigate to project root
cd /home/ubuntu/projects/Vagner-

# Activate virtual environment
source venv/bin/activate

# Start the server
python3 run.py

# Or initialize knowledge base
python3 scripts/init_kb.py
```
