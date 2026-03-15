import google.generativeai as genai
import fitz
from pathlib import Path

GEMINI_API_KEY = "AIzaSyDsxQa6HlxU9PQS65M4lhsdkw8fXVMwER8"

def signup():
    print("\n" + "="*60)
    print("🚀 GEMINI 2.5 FLASH PDF SUMMARIZER")
    print("Using your model: models/gemini-2.5-flash")
    print("="*60)
    username = input("👤 Username: ").strip() or "User"
    email = input("📧 Email: ").strip()
    return username, email

def extract_pdf(pdf_path):
    print("\n📖 Extracting PDF...")
    doc = fitz.open(pdf_path)
    print(f"📄 {len(doc)} pages found")
    
    text = ""
    for i, page in enumerate(doc, 1):
        text += page.get_text()
        print(f"Page {i} ✓")
    
    doc.close()
    safe_text = text[:15000]  # Safe for free tier
    print(f"✅ {len(safe_text):,} chars ready for Gemini")
    return safe_text

def summarize_with_gemini(text, username):
    """Use YOUR working model: models/gemini-2.5-flash"""
    genai.configure(api_key=GEMINI_API_KEY)
    
    try:
        # YOUR FIRST WORKING MODEL (from your list)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        prompt = f"""
Summarize this document clearly for {username}:

{text}

Provide:
1. Main purpose
2. Key points (3-5 bullets)  
3. Important details
"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        return f"Error: {e}"

def main():
    username, email = signup()
    
    pdf_path = input("\n📁 PDF path: ").strip()
    if not Path(pdf_path).exists():
        print("❌ File not found!")
        return
    
    text = extract_pdf(pdf_path)
    summary = summarize_with_gemini(text, username)
    
    print("\n" + "="*80)
    print("📋 GEMINI 2.5 FLASH SUMMARY")
    print("="*80)
    print(summary)
    print(f"\n🎉 SUCCESS for {username} using gemini-2.5-flash!")

if __name__ == "__main__":
    main()