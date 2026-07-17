import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="Nounkoun IA")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class Question(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Nounkoun IA est en ligne", "message": "Envoyez POST /ask"}

@app.post("/ask")
def ask(q: Question):
    if not os.getenv("GEMINI_API_KEY"):
        return {"answer": "Erreur: GEMINI_API_KEY manquante sur Render"}
    
    prompt = f"Tu es Nounkoun IA, assistant agricole pour les paysans du Bénin. Réponds simple, en français, conseils pratiques et locaux: {q.message}"
    
    # Liste des modèles gratuits du plus léger au plus puissant
    modeles = ["gemini-1.5-flash-8b", "gemini-1.5-flash", "gemini-2.0-flash-lite"]
    
    for model_name in modeles:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return {"answer": response.text}
        except Exception as e:
            # Si quota dépassé, essaie le suivant
            if "429" in str(e) or "quota" in str(e).lower():
                continue
            return {"answer": f"Erreur: {str(e)}"}
    
    return {"answer": "Désolé, quota Google atteint. Réessaie dans 1 minute, ou crée une nouvelle clé sur aistudio.google.com"}
