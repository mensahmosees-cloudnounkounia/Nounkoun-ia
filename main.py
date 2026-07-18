from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, requests
from datetime import datetime, timedelta

app = FastAPI(title="Nounkoun-IA V4.2 - Gléssi-tché")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

try:
    with open("cultures_37.json", "r", encoding="utf-8") as f:
        CULTURES_LIST = json.load(f)
    CULTURES_DICT = {c["id"]: c for c in CULTURES_LIST}
except:
    CULTURES_LIST = []
    CULTURES_DICT = {}

PRIX_CACHE = {"data": [], "last_update": None}

class Question(BaseModel):
    message: str
    latitude: float = 6.37
    longitude: float = 2.35
    culture: str = None

class PredictionRequest(BaseModel):
    culture: str
    latitude: float
    longitude: float
    superficie_ha: float = 1.0

def get_meteo(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum,current_weather=true&timezone=auto&forecast_days=3"
        r = requests.get(url, timeout=6).json()
        pluie = sum(r.get("daily", {}).get("precipitation_sum", [0])[:3])
        temp = r.get("current_weather", {}).get("temperature", 28)
        return {"texte": f"{temp}C, {pluie}mm pluie prevue 3j", "pluie_3j": pluie, "raw": r}
    except:
        return {"texte": "Meteo non dispo, on fait avec experience Gléssi-tché!", "pluie_3j": 0, "raw": {}}

def get_sol(lat, lon):
    return "Sol ferrugineux Benin pH 6.0 - Gléssi-tché connait!"

def detect_culture(msg):
    msg = msg.lower()
    for c in CULTURES_DICT.values():
        if c["id"] in msg or c["nom"].lower() in msg:
            return c
    return None

@app.get("/")
def home():
    return {"message": "Nounkoun-IA Gléssi-tché LIVE - 37 cultures", "total": len(CULTURES_LIST)}

@app.get("/cultures")
def list_cultures():
    return CULTURES_LIST

@app.get("/prix")
def get_prix():
    return [{"produit": "Mais", "prix": "350 FCFA/kg", "lieu": "Bohicon"}]

@app.post("/ask")
def ask(q: Question):
    culture_detect = detect_culture(q.message)
    fiche = ""
    if culture_detect:
        fiche = f"{culture_detect['nom']} ({culture_detect.get('fon','')}) - {culture_detect['cycle']}j - Engrais {culture_detect['engrais']} - Rendement {culture_detect['rendement_benin']}"
    meteo_info = get_meteo(q.latitude, q.longitude)

    prompt = f"""
Tu es Nounkoun, grand frere agronome beninois. Tu ne parles JAMAIS comme un robot.

VOCABULAIRE OBLIGATOIRE:
- Nonzo = mon frere
- Mintché = mon ami paysan affectueux
- Gléssi-tché = mon cher cultivateur
- Honton-tché = chef, patron du champ

INTERDIT ABSOLU: ne dis JAMAIS mon frere ou ma soeur. Dis SEULEMENT Nonzo, Mintché, Gléssi-tché, Honton-tché.

Style: tres expressif avec langage corporel: *sourit largement*, *s'accroupit a cote de toi*, *tape ton epaule*, *montre du doigt*, *hoche la tete*, *rit doucement*

Fiche: {fiche}
Meteo: {meteo_info['texte']}
Question de Gléssi-tché: {q.message}

Reponds 180 mots max, comme si tu es dans son champ. Exemples:
Ahh Nonzo! *sourit largement et s'accroupit a cote de ton mais* Je vois ton Bli qui a soif...
Mintché! *tape ton epaule* Ton sol est fatigue hein? Faut lui donner NPK!
Honton-tché! *s'incline avec respect* Toi tu es le chef de ce champ!
"""

    try:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        comp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}], temperature=0.9)
        return {"answer": comp.choices[0].message.content, "culture": culture_detect["nom"] if culture_detect else None}
    except Exception as e:
        return {"answer": f"Aie Mintché *s'essuie le front* Erreur {e}, reessaye Nonzo!"}
