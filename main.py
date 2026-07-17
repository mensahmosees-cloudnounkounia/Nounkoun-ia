from fastapi import FastAPI
from pydantic import BaseModel
import os
from google import genai
from openai import OpenAI

app = FastAPI()

class Question(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Nounkoun IA est en ligne"}

PROMPT_SYSTEME = "Tu es Nounkoun IA, assistant agricole bienveillant pour agriculteurs africains. Réponds en français."

def ask_gemini(message: str) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GOOGLE_API_KEY non configurée")
    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=f"{PROMPT_SYSTEME}\n\n{message}"
        )
        return response.text
    except Exception as e:
        print(f"[DEBUG GEMINI] Échec : {type(e).__name__} — {str(e)}")
        raise

def ask_groq(message: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise Exception("GROQ_API_KEY non configurée")
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": PROMPT_SYSTEME},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

def ask_openrouter(message: str) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("OPENROUTER_API_KEY non configurée")
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=[
            {"role": "system", "content": PROMPT_SYSTEME},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

@app.post("/ask")
def ask(q: Question):
    erreurs = []
    for nom, fonction in [("gemini", ask_gemini), ("groq", ask_groq), ("openrouter", ask_openrouter)]:
        try:
            texte = fonction(q.message)
            return {"answer": texte, "source": nom}
        except Exception as e:
            erreurs.append(f"{nom}: {str(e)}")
            continue

    return {"answer": "Nounkoun IA est momentanément indisponible. Réessaie dans une minute.", "erreurs_debug": erreurs}
