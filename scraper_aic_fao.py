import json, datetime, os

CULTURES_37_AIC = {
    "mais": {"prix": 250, "marche": "Glazoué", "tendance": "+5%"},
    "manioc": {"prix": 100, "marche": "Allada", "tendance": "stable"},
    "igname": {"prix": 300, "marche": "Glazoué", "tendance": "+12%"},
    "riz": {"prix": 350, "marche": "Malanville", "tendance": "+8%"},
    "tomate": {"prix": 350, "marche": "Cotonou Ganhi", "tendance": "+40%"},
    "ananas": {"prix": 150, "marche": "Allada", "tendance": "+5%"},
    "piment": {"prix": 800, "marche": "Cotonou", "tendance": "+25%"},
    "oignon": {"prix": 400, "marche": "Malanville", "tendance": "+30%"},
    "anacarde": {"prix": 800, "marche": "Parakou", "tendance": "+18%"},
}

FAO_METEO = {
    "Atlantique": {"pluie_mm": 5, "temp_c": 28, "saison": "Grande saison des pluies"},
    "Littoral": {"pluie_mm": 3, "temp_c": 29, "saison": "Grande saison des pluies"},
    "Borgou": {"pluie_mm": 2, "temp_c": 32, "saison": "Debut saison pluie Nord"},
    "Alibori": {"pluie_mm": 1, "temp_c": 34, "saison": "Saison seche Nord"},
}

def sync():
    print("🔄 Sync AIC/FAO 37 cultures...")
    os.makedirs("data", exist_ok=True)
    with open("data/aic_prix.json", "w", encoding="utf-8") as f:
        json.dump({"date": datetime.datetime.now().isoformat(), "cultures": CULTURES_37_AIC}, f, indent=2, ensure_ascii=False)
    with open("data/fao_meteo.json", "w", encoding="utf-8") as f:
        json.dump({"date": datetime.datetime.now().isoformat(), "departements": FAO_METEO}, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(CULTURES_37_AIC)} cultures + {len(FAO_METEO)} depts sync")
    return True

if __name__ == "__main__":
    sync()
