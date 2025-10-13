#!/usr/bin/env python3
"""
Test script for PDF URL extraction and scraping functionality

This script demonstrates how to use the new add_file_to_kb_with_urls function
to process PDFs that contain web URLs.
"""
import os
import sys

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from app.core.kb.manager import add_file_to_kb_with_urls, extract_urls_from_text


def test_url_extraction():
    """Test URL extraction from sample text"""
    print("=" * 60)
    print("Testing URL Extraction")
    print("=" * 60)
    
    sample_text = """
    Check out our website at https://example.com for more information.
    You can also visit http://www.openai.com or https://github.com/langchain-ai/langchain
    For documentation, see https://docs.python.org/3/
    """
    
    urls = extract_urls_from_text(sample_text)
    print(f"\nExtracted {len(urls)} URLs:")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")
    
    print()


def test_pdf_processing(pdf_path: str = None):
    """Test PDF processing with URL scraping"""
    print("=" * 60)
    print("Testing PDF Processing with URL Scraping")
    print("=" * 60)
    
    if not pdf_path:
        # Try to find a PDF in the materials/pdfs folder
        pdf_folder = os.path.join(PROJECT_ROOT, "materials", "pdfs")
        if os.path.exists(pdf_folder):
            pdfs = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
            if pdfs:
                pdf_path = os.path.join(pdf_folder, pdfs[0])
            else:
                print("⚠️ No PDF files found in materials/pdfs/")
                return
        else:
            print("⚠️ PDF folder not found")
            return
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"\n📄 Processing: {pdf_path}\n")
    
    # Process with URL scraping enabled (default)
    print("\n--- WITH URL SCRAPING (default) ---")
    add_file_to_kb_with_urls(pdf_path, scrape_urls=True)
    
    print("\n✅ Test completed!")


def main():
    """Main test function"""
    print("\n🧪 PDF URL Extraction & Scraping Test Suite\n")
    
    # Test 1: URL extraction
    test_url_extraction()
    
    # Test 2: PDF processing
    # You can pass a specific PDF path as argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        test_pdf_processing(pdf_path)
    else:
        print("\n💡 To test with a specific PDF, run:")
        print(f"   python {os.path.basename(__file__)} /path/to/your/file.pdf")
        print("\n   Or it will automatically find a PDF in materials/pdfs/\n")
        test_pdf_processing()


if __name__ == "__main__":
    main()

