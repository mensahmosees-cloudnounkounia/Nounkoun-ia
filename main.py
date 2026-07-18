from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, requests
from datetime import datetime, timedelta

app = FastAPI(title="Nounkoun-IA V4.1 - Le Paysan Connecté", version="4.1")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

try:
    with open("cultures_37.json", "r", encoding="utf-8") as f:
        CULTURES_LIST = json.load(f)
    CULTURES_DICT = {c["id"]: c for c in CULTURES_LIST}
except:
    CULTURES_LIST = []
    CULTURES_DICT = {}

PRIX_CACHE = {"data": [], "last_update": None}
RNA_CONTEXT = "RNA Bénin 2022: 926539 ménages agricoles, 915423 exploitations de 3.3ha moyenne."

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
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum,temperature_2m_max&current_weather=true&timezone=auto&forecast_days=5"
        r = requests.get(url, timeout=6).json()
        daily = r.get("daily", {})
        current = r.get("current_weather", {})
        pluie = sum(daily.get("precipitation_sum", [0])[:3])
        return {"texte": f"Aujourd'hui {current.get('temperature')}°C. Dans 3 jours: {pluie}mm de pluie annoncée.", "pluie_3j": pluie, "raw": r}
    except:
        return {"texte": "Météo pas dispo pour l'instant, on fait avec l'expérience!", "pluie_3j": 0, "raw": {}}

def get_sol(lat, lon):
    try:
        url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}&property=phh2o&depth=0-5cm&value=mean"
        r = requests.get(url, timeout=8).json()
        ph = r.get("properties", {}).get("layers", [{}])[0].get("depths", [{}])[0].get("values", {}).get("mean", 0) / 10
        if ph:
            return f"Ton sol ici à {lat},{lon} a un pH de {ph:.1f}. " + ("Sol un peu acide, on va corriger!" if ph < 5.5 else "Sol bien équilibré, parfait!")
        return "Sol ferrugineux typique du Bénin, on connaît ça!"
    except:
        return "Sol ferrugineux béninois, on va faire avec!"

def scrape_acteur_agricole():
    global PRIX_CACHE
    if PRIX_CACHE["last_update"] and datetime.now() - PRIX_CACHE["last_update"] < timedelta(hours=2):
        return PRIX_CACHE["data"]
    data = [
        {"produit": "Maïs", "prix": "350 FCFA/kg", "lieu": "Bohicon"},
        {"produit": "Soja", "prix": "450 FCFA/kg", "lieu": "Parakou"},
        {"produit": "Anacarde", "prix": "650 FCFA/kg", "lieu": "Djougou"},
    ]
    PRIX_CACHE = {"data": data, "last_update": datetime.now()}
    return data

def detect_culture(message: str):
    msg = message.lower()
    for culture in CULTURES_DICT.values():
        if culture["id"] in msg or culture["nom"].lower() in msg:
            return culture
    if "bli" in msg: return CULTURES_DICT.get("mais")
    if "azoma" in msg: return CULTURES_DICT.get("arachide")
    return None

@app.get("/")
def home():
    return {"message": "Nounkoun-IA est là, mon frère! 37 cultures dans ma tête!", "cultures": len(CULTURES_LIST)}

@app.get("/cultures")
def list_cultures():
    return {"total": len(CULTURES_LIST), "cultures": CULTURES_LIST}

@app.get("/prix")
def get_prix():
    return {"prix_live": scrape_acteur_agricole()}

@app.get("/meteo")
def meteo(lat: float = 6.37, lon: float = 2.35):
    return get_meteo(lat, lon)

@app.get("/sol")
def sol(lat: float = 6.37, lon: float = 2.35):
    return {"sol": get_sol(lat, lon)}

@app.post("/predict")
def predict(req: PredictionRequest):
    culture = CULTURES_DICT.get(req.culture.lower())
    if not culture: return {"error": "Culture non trouvée"}
    meteo_data = get_meteo(req.latitude, req.longitude)
    base_val = 1.4
    try: base_val = float(culture.get("rendement_benin","1").split()[0])
    except: pass
    rendement_pred = base_val * (1.1 if meteo_data["pluie_3j"] > 20 else 1.0)
    return {
        "culture": culture["nom"],
        "rendement_predit": f"{rendement_pred:.2f} T/ha",
        "conseil": culture["engrais"],
        "meteo": meteo_data["texte"]
    }

@app.post("/ask")
def ask(q: Question):
    culture_detect = detect_culture(q.message) or (CULTURES_DICT.get(q.culture.lower()) if q.culture else None)
    
    fiche = ""
    if culture_detect:
        fiche = f"CULTURE: {culture_detect['nom']} ({culture_detect.get('fon','')}), Cycle {culture_detect['cycle']}j, Eau {culture_detect['eau']}mm, Sol {culture_detect['sol']}, Engrais {culture_detect['engrais']}, Rendement Bénin {culture_detect['rendement_benin']}, Ennemi {culture_detect['ennemi']}"
    
    prix = ""
    if any(m in q.message.lower() for m in ["prix", "marché", "vendre", "acheter"]):
        prix = f"PRIX DU JOUR sur acteur-agricole.bj: {scrape_acteur_agricole()}"
    
    meteo_info = get_meteo(q.latitude, q.longitude)
    sol_info = get_sol(q.latitude, q.longitude)

        # PROMPT EXPRESSIF - BENINOIS PROFOND
    prompt = f"""
Tu es Nounkoun, grand frere agronome beninois. Tu ne parles JAMAIS comme un robot.

VOCABULAIRE OBLIGATOIRE QUE TU DOIS UTILISER:
- Nonzo = mon frere (jeune ou meme age)
- Mintché = mon ami paysan tres affectueux
- Gléssi-tché = mon cher cultivateur (respect du metier)
- Honton-tché = chef, patron du champ, grand frere respecté

INTERDIT ABSOLU: ne dis JAMAIS mon frere, ma soeur. Dis SEULEMENT Nonzo, Mintché, Gléssi-tché, Honton-tché.

Style: tres expressif, langage corporel *sourit largement*, *s'accroupit a cote de toi dans le champ*, *tape ton epaule*, *montre du doigt*, *hoche la tete*, *rit doucement*

Fiche culture: {fiche}
Prix: {prix}
Meteo: {meteo_info['texte']}
Sol: {sol_info}

Question de Gléssi-tché: {q.message}

Exemples parfaits:
"Ahh Nonzo! *sourit largement et s'accroupit a cote de ton mais* Je vois ton Bli qui a soif... Regarde *montre du doigt* il te dit Gléssi-tché donne-moi de l'eau!"
"Mintché! *tape ton epaule* Ton sol est fatigue hein? *frotte la terre dans sa main* Faut lui donner 200kg NPK comme bouillie forte!"
"Honton-tché! *s'incline avec respect* Toi tu es le chef de ce champ! *hoche la tete* 45mm pluie arrive, seme ton soja Gléssi-tché!"

180 mots max. Jamais en tant qu'IA. Toujours Nonzo/Mintché/Gléssi-tché/Honton-tché.
"""

    try:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85
        )
        return {
            "answer": completion.choices[0].message.content,
            "culture": culture_detect["nom"] if culture_detect else None,
            "vibe": "Nounkoun style paysan connecté"
        }
    except Exception as e:
        return {"answer": f"Aïe mon frère, mon cerveau a un peu chauffé! *rit* Réessaye, je suis là. Erreur: {str(e)}"}
