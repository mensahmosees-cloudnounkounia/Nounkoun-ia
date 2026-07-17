nano main.pyimport os, base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"status": "Nounkoun IA OK - Abomey-Calavi"}

@app.post("/diagnostiquer")
async def diag(photo: UploadFile = File(...), loc: str = Form("Abomey-Calavi")):
    img = base64.b64encode(await photo.read()).decode()
    prompt = f"Paysan à {loc} Bénin. Diagnostique cette plante. Réponds en JSON avec: diagnostic_court, perte_fcfa_estimee, solution_bio_neem_0f, vendeur_calavi, conseil_urgent"
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":[{"type":"text","text":prompt},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img}"}}]}],
        response_format={"type":"json_object"}
    )
    return r.choices[0].message.content
