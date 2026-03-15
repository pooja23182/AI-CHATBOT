import fitz  # PyMuPDF
import google.generativeai as genai

# ==========================
# ENTER YOUR GEMINI API KEY
# ==========================
GEMINI_API_KEY = "AIzaSyDsxQa6HlxU9PQS65M4lhsdkw8fXVMwER8"

genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")


# ==========================
# USER SIGNUP
# ==========================
def signup():
    print("\n===== USER SIGNUP =====")
    username = input("Enter Username: ")
    email = input("Enter Email: ")

    print("\nSignup Successful!")
    print(f"Welcome {username}\n")

    return username, email


# ==========================
# PDF TEXT EXTRACTION
# ==========================
def extract_pdf_text(pdf_path):

    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception as e:
        print("Error reading PDF:", e)

    return text


# ==========================
# SUMMARIZE USING GEMINI
# ==========================
def summarize_text(text):

    print("\nSummarizing PDF using Gemini AI...\n")

    prompt = f"""
    Summarize the following document clearly.
    Provide a structured summary.

    DOCUMENT:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text


# ==========================
# MAIN PROGRAM
# ==========================
def main():

    username, email = signup()

    pdf_path = input("Enter PDF file path: ")

    print("\nReading PDF...\n")

    pdf_text = extract_pdf_text(pdf_path)

    if not pdf_text.strip():
        print("PDF seems empty or unreadable.")
        return

    summary = summarize_text(pdf_text)

    print("\n===== PDF SUMMARY =====\n")
    print(summary)


# Run program
if __name__ == "__main__":
    main()