import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="Nounkoun IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

class Question(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Nounkoun IA est en ligne", "message": "Envoyez POST /ask"}

@app.post("/ask")
def ask(q: Question):
    if not os.getenv("GEMINI_API_KEY"):
        return {"answer": "Erreur: GEMINI_API_KEY manquante sur Render"}
    try:
        prompt = f"Tu es Nounkoun IA, assistant agricole pour les paysans du Bénin. Réponds simple, en français, conseils pratiques, courts. Question: {q.message}"
        response = model.generate_content(prompt)
        return {"answer": response.text}
    except Exception as e:
        return {"answer": f"Erreur: {str(e)}"}
