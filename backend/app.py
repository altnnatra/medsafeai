import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import fitz  # PyMuPDF

app = FastAPI()

# Разрешаем доступ с фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Пути
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_dir = os.path.join(base_dir, "front", "static")
index_file = os.path.join(base_dir, "front", "index.html")

# Подключаем статику
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(index_file, encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# Модель запроса от пользователя
class MedRequest(BaseModel):
    drug_name: str

# Извлечение текста из PDF
def extract_text_from_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Обработка запроса на препарат из PDF
@app.post("/check")
async def check_medicine(info: MedRequest):
    drug_name = info.drug_name.lower().strip()

    # Путь к PDF
    pdf_path = os.path.join(base_dir, "backend", "pdfs", "your_file.pdf")
    pdf_text = extract_text_from_pdf(pdf_path)

    if not pdf_text.strip():
        return {"error": "PDF is empty or unreadable."}

    # Приведение PDF текста к нижнему регистру для поиска
    pdf_text_lower = pdf_text.lower()

    # Проверяем, содержится ли название препарата в PDF
    if drug_name not in pdf_text_lower:
        return {
            "answer": f"The medicine is either not found in the official list or is prohibited in the UAE."
        }

    # Ограничим длину текста
    short_text = pdf_text[:2000]

    # Prompt для Ollama
    prompt_text = f"""
You're given an excerpt from a medical document. Based only on the content provided,
extract the following about {info.drug_name}:

You are a medical AI assistant working under UAE regulations. You have access only to the medicines listed in the document titled "List of Medicines". This list represents the official and approved medications in the UAE.

Rules:
Try your best to extract any partial relevant data from the document, even if the full section is missing. Avoid answering "No information" unless nothing can be inferred at all.

If the user enters only numbers or digits, respond with:
"There is no medicine in the list."

If the medicine is not in the official list, respond with:
"The medicine is either not found in the official list or is prohibited in the UAE."

If the medicine is in the approved list, provide the following sections:

Contraindications:
- Who should not take this drug.
- Medical conditions or scenarios to avoid.

How to use / Dosage guidelines:
- Basic dosage instructions (e.g., adult/child doses).
- How the drug should be taken.

Possible side effects:
- Common and rare side effects.

Should not be combined with:
- Dangerous interactions with other medications, foods, or substances.

Please use these exact section titles and format clearly with each section on its own line. Do not use markdown or HTML formatting. Keep it plain text.

If specific information is absolutely unavailable, then write:
"No information available for this section."

Always present your answer clearly using bullet points under each section.

Document:
{short_text}
    """

    print("=== Отправляем в Ollama ===")
    print(prompt_text[:1000])
    print("===========================")

    try:
        response = requests.post("http://localhost:11434/api/chat", json={
            "model": "mistral",
            "messages": [{"role": "user", "content": prompt_text}],
            "stream": False
        })
        data = response.json()
        return {"answer": data["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
