from pypdf import PdfReader
import google.generativeai as genai
from django.conf import settings

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text
genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def ask_ai(prompt):
    response = model.generate_content(prompt)

    return response.text