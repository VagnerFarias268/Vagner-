# 🚀 QUICK START GUIDE

## The Error You Got

```bash
cd /home/ubuntu/projects/Vagner-/app/    # ❌ WRONG DIRECTORY!
python3 main.py
# Error: ModuleNotFoundError: No module named 'app'
```

## ✅ THE FIX (3 Simple Steps)

### Step 1: Go to Project Root
```bash
cd /home/ubuntu/projects/Vagner-
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 3: Run the Application
```bash
python3 run.py
```

That's it! 🎉

## Alternative Ways to Run

All of these work (from project root):

```bash
# Method 1: Using run.py (recommended)
python3 run.py

# Method 2: Using Python module syntax
python3 -m app.main

# Method 3: Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Method 4: Using the start script
./start.sh
```

## Other Common Commands

### Initialize Knowledge Base
```bash
cd /home/ubuntu/projects/Vagner-
source venv/bin/activate
python3 scripts/init_kb.py
```

### Install Dependencies
```bash
cd /home/ubuntu/projects/Vagner-
source venv/bin/activate
pip install -r requirements.txt
```

## Remember: ALWAYS Run from `/home/ubuntu/projects/Vagner-/`

Never run Python scripts from inside subdirectories like `app/` or `scripts/`!
