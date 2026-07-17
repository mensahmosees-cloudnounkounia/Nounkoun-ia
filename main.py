from fastapi import FastAPI
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

class Question(BaseModel):
    message: str

# Récupère la clé API
API_KEY = os.environ.get("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)

@app.get("/")
def home():
    return {"status": "Nounkoun IA est en ligne"}

@app.post("/ask")
def ask(q: Question):
    try:
        prompt = f"Tu es Nounkoun IA, assistant agricole bienveillant pour agriculteurs africains. Réponds en français simple. Question: {q.message}"
        
        # On utilise le nouveau modèle qui marche à 100%
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        return {"answer": response.text}
    except Exception as e:
        return {"answer": f"Erreur: {str(e)}"}
