"""
Initialize Knowledge Base
Ingests PDFs, URLs, and media files into Pinecone

Note: PDFs are automatically scanned for URLs, and any found URLs
      will be scraped and their content will be added to the KB as well.
"""
import os
import json
import sys

# Get the project root directory (parent of scripts/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
from app.core.kb.manager import add_file_to_kb, add_url_to_kb, add_media_to_kb

load_dotenv()


def ingest_pdfs():
    """
    Ingest all PDF files from the PDFs folder
    
    Note: The system automatically detects URLs in PDFs and scrapes their content.
    This provides richer context by including both the PDF and referenced web pages.
    """
    pdf_folder = os.getenv("PDF_FOLDER", "materials/pdfs")

    # Convert relative path to absolute (relative to PROJECT_ROOT, not cwd)
    if not os.path.isabs(pdf_folder):
        pdf_folder = os.path.join(PROJECT_ROOT, pdf_folder)
    

    print(f"PDF folder: {pdf_folder}");
    
    if not os.path.exists(pdf_folder):
        print(f'⚠️ PDF folder not found: {pdf_folder}')
        return
    
    print(f"\n📚 Ingesting PDFs from {pdf_folder}...")
    count = 0
    
    for filename in os.listdir(pdf_folder):
        file_path = os.path.join(pdf_folder, filename)
        if filename.lower().endswith(('.pdf', '.txt', '.doc', '.docx')):
            print(f"  Processing: {filename}")
            add_file_to_kb(file_path)
            count += 1
    
    print(f"✅ Ingested {count} documents")


def ingest_urls():
    """Ingest URLs (add your URLs here)"""
    print("\n🌐 Ingesting URLs...")
    
    # Add your landing pages, product pages, or affiliate URLs here
    urls = [
        # Example:
        # 'https://example.com/product-page',
        # 'https://example.com/about',
    ]
    
    if not urls:
        print("⚠️ No URLs configured. Edit scripts/init_kb.py to add URLs.")
        return
    
    for url in urls:
        print(f"  Processing: {url}")
        add_url_to_kb(url)
    
    print(f"✅ Ingested {len(urls)} URLs")


def ingest_media():
    """Ingest media files with captions from dataset"""
    media_folder = os.getenv("MEDIA_FOLDER", "materials/media")
    dataset_path = 'materials/media_dataset.json'
    
    # Convert relative paths to absolute (relative to PROJECT_ROOT, not cwd)
    if not os.path.isabs(media_folder):
        media_folder = os.path.join(PROJECT_ROOT, media_folder)
    if not os.path.isabs(dataset_path):
        dataset_path = os.path.join(PROJECT_ROOT, dataset_path)
    
    if not os.path.exists(dataset_path):
        print(f'⚠️ Media dataset not found: {dataset_path}')
        print('   Create materials/media_dataset.json with format:')
        print('   [{"file": "image.jpg", "caption": "Description"}]')
        return
    
    print(f"\n🎨 Ingesting media from {dataset_path}...")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    count = 0
    for entry in dataset:
        file_path = os.path.join(media_folder, entry['file'])
        caption = entry.get('caption', entry['file'])
        
        if os.path.exists(file_path):
            print(f"  Processing: {entry['file']}")
            add_media_to_kb(file_path, caption)
            count += 1
        else:
            print(f"  ⚠️ Missing: {file_path}")
    
    print(f"✅ Ingested {count} media files")


def main():
    """Main ingestion pipeline"""
    print("=" * 60)
    print("🚀 Initializing Knowledge Base")
    print("=" * 60)
    
    try:
        ingest_pdfs()
        ingest_urls()
        ingest_media()
        
        print("\n" + "=" * 60)
        print("✅ Knowledge Base initialization complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        raise


if __name__ == '__main__':
    main()

