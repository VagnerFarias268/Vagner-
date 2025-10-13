# 🌐 PDF URL Scraping Feature - Quick Reference

## What's New?

Your knowledge base now **automatically scrapes URLs found in PDFs**! When you add a PDF to the knowledge base, the system will:

1. ✅ Extract all text from the PDF
2. 🔍 Find any web URLs (http/https) in the content
3. 🌐 Scrape those websites automatically
4. 💾 Vectorize BOTH the PDF and scraped content
5. 📊 Store everything in Pinecone

**Result:** Your AI agent can answer questions using information from PDFs AND the websites they reference!

## Quick Start

### Basic Usage (Nothing Changes!)

```python
from app.core.kb.manager import add_file_to_kb

# This automatically includes URL scraping now
add_file_to_kb("materials/pdfs/product_guide.pdf")
```

**Sample Output:**
```
📎 Found 2 URL(s) in materials/pdfs/product_guide.pdf
  🌐 Scraping URL: https://example.com
    ✅ Scraped 3421 characters from https://example.com
  🌐 Scraping URL: https://docs.example.com
    ✅ Scraped 2156 characters from https://docs.example.com
✅ Added file materials/pdfs/product_guide.pdf
   📄 PDF chunks: 8
   🌐 URL chunks: 15 (from 2 URLs)
```

### Advanced Usage

```python
from app.core.kb.manager import add_file_to_kb_with_urls

# Enable URL scraping (default behavior)
add_file_to_kb_with_urls("document.pdf", scrape_urls=True)

# Disable URL scraping (original behavior)
add_file_to_kb_with_urls("document.pdf", scrape_urls=False)
```

### Test the Feature

```bash
# Run the test suite
python scripts/test_url_extraction.py

# Test with a specific PDF
python scripts/test_url_extraction.py /path/to/your/document.pdf
```

## Use Cases

### 📦 Product Catalogs
Your PDF catalog references manufacturer websites? The AI now has access to both!

### 📚 Research Documents
Papers with online citations? All referenced content is automatically included!

### 📖 Training Materials
Manuals with documentation links? Everything gets vectorized together!

## Key Features

✅ **Automatic Detection** - No configuration needed  
✅ **Error Handling** - Failed scrapes don't stop processing  
✅ **Smart Chunking** - 800 chars per chunk for optimal retrieval  
✅ **Rich Metadata** - Track content sources (PDF vs web)  
✅ **Backward Compatible** - Existing code works as-is  

## What Gets Scraped?

The scraper extracts text from:
- Paragraphs (`<p>`)
- Headings (`<h1>` - `<h6>`)
- Lists (`<li>`)
- Articles and sections

It automatically removes:
- JavaScript code
- CSS styles
- Navigation menus (when possible)

## Configuration

```python
# In app/core/kb/manager.py

# URL Detection Pattern
url_pattern = r'https?://...'  # Matches http:// and https://

# Scraping Settings
timeout=15 seconds
headers={'User-Agent': 'Mozilla/5.0'}
chunk_size=800 characters
```

## Metadata Structure

**PDF Content:**
```json
{
  "source": "path/to/file.pdf",
  "type": "pdf"
}
```

**Scraped URL Content:**
```json
{
  "source": "https://example.com/page",
  "type": "url_from_pdf",
  "pdf_source": "path/to/file.pdf"
}
```

## Troubleshooting

**No URLs detected?**
- Ensure URLs are text (not images)
- Check they start with `http://` or `https://`

**Scraping fails?**
- Check internet connectivity
- Some sites block automated requests
- URLs may require authentication

**Too slow?**
- Disable: `add_file_to_kb_with_urls(path, scrape_urls=False)`
- Each URL adds ~5-15 seconds

## Functions Available

```python
from app.core.kb.manager import (
    add_file_to_kb,              # Auto-scrapes URLs (NEW behavior)
    add_file_to_kb_with_urls,    # Control scraping on/off
    extract_urls_from_text,       # Extract URLs from text
    scrape_url_content,           # Scrape a single URL
)
```

## Integration

The feature is automatically used by:
- ✅ `scripts/init_kb.py` - Knowledge base initialization
- ✅ All existing PDF ingestion code
- ✅ Manual `add_file_to_kb()` calls

## Examples

### Example 1: Standard PDF Processing
```python
from app.core.kb.manager import add_file_to_kb

# Process with URL scraping (automatic)
add_file_to_kb("catalogs/2024_products.pdf")
```

### Example 2: Extract URLs Only
```python
from app.core.kb.manager import extract_urls_from_text

text = "Visit https://example.com for more info"
urls = extract_urls_from_text(text)
print(urls)  # ['https://example.com']
```

### Example 3: Custom Scraping
```python
from app.core.kb.manager import scrape_url_content

content = scrape_url_content("https://example.com")
print(f"Scraped {len(content)} characters")
```

## Performance Impact

| Scenario | Processing Time | API Calls |
|----------|----------------|-----------|
| PDF only | ~2-3 seconds | N chunks |
| PDF + 1 URL | ~7-18 seconds | (N + M) chunks |
| PDF + 5 URLs | ~30-75 seconds | (N + M*5) chunks |

Where:
- N = PDF chunks (~1 per 800 chars)
- M = Avg chunks per URL (~5-20)

## Learn More

📖 **Full Documentation:** [docs/PDF_URL_SCRAPING.md](docs/PDF_URL_SCRAPING.md)  
🧪 **Test Script:** `scripts/test_url_extraction.py`  
💻 **Source Code:** `app/core/kb/manager.py`

---

**Questions?** Check the main [README.md](README.md) for more information.

