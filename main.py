from fastapi import FastAPI
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

class Question(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Nounkoun IA est en ligne"}

@app.post("/ask")
def ask(q: Question):
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return {"answer": "Erreur: GOOGLE_API_KEY non configurée sur Render"}
        
        client = genai.Client(api_key=api_key)
        
        prompt = f"Tu es Nounkoun IA, assistant agricole bienveillant pour agriculteurs africains. Réponds en français simple. Question: {q.message}"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        return {"answer": response.text}
    except Exception as e:
        return {"answer": f"Erreur: {str(e)}"}
