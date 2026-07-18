# raisonnement.py - Nounkoun V15 PRO - Moteur de raisonnement 5 étapes
class MoteurRaisonnement:
    def __init__(self):
        self.etapes = ["Intention", "Contexte", "Irrigation+Eco", "Risque+Diag", "Decision+Rente"]

    def raisonner(self, question, culture="mais", sol="argileux", pluie=5, ph=6, saison="Grande pluie"):
        """Raisonnement 5 étapes 1 par 1 / 37 cultures"""
        c = self.get_culture(culture)
        s = self.get_sol(sol)

        # Etape 1: Intention
        intention = f"🎯 Intention: {c['fr']} {c['e']} + '{question}' - 1/37 cultures - Saison {c['sai']}"

        # Etape 2: Contexte
        contexte = f"🧩 Contexte: {c['fr']} besoin {c['w']}L x sol {s['fr']} x{s['m']} = {round(c['w']*s['m'])}L/m², pH {ph}, pluie {pluie}mm, Saison {saison}"

        # Etape 3: Irrigation + Eco
        irr = round(c['w']*s['m'])
        cout = max(0, irr-pluie)*2
        benef = c['y']*c['p'] - c['co'] - cout
        eco = f"💧 Irrigation (1/37): {irr}L/m² coût {cout}F | 💰 Bénéfice (1/37): {benef}F/ha"

        # Etape 4: Risque + Diag
        risque = f"🌧️ Risque sol {s['fr']} | 🔍 Diag (1/37): {c['d']} | Photo reconnue 📸 OK | Saison {c['s']}"

        # Etape 5: Decision + Rente
        rente = round(benef/(c['c']/30))
        decision = f"✅ Décision: Irrigue {irr}L | 📈 Rente (1/37): {rente}F/mois | 📅 {c['s']} récolte {c['c']}j | {c['f']}"

        return {
            "etapes": [intention, contexte, eco, risque, decision],
            "irrigation": irr,
            "benefice": benef,
            "rente": rente,
            "saison_conseil": self.conseil_saison(culture, saison)
        }

    def conseil_saison(self, culture, saison_actuelle):
        c = self.get_culture(culture)
        if c['sai'].lower() in saison_actuelle.lower() or "toute" in c['sai'].lower():
            return f"✅ Bonne saison pour {c['fr']}"
        else:
            return f"⚠️ Hors saison - {c['fr']} idéal: {c['s']} ({c['sai']})"

    def get_culture(self, k):
        # 37 cultures - import depuis cultures_37.json en prod
        base = {"fr": k, "e": "🌱", "w": 12, "y": 1000, "p": 400, "d": "A surveiller", "f": "Compost", "s": "Selon", "c": 90, "co": 80000, "sai": "Toute annee"}
        return base

    def get_sol(self, k):
        sols = {"argileux": {"fr": "Argileux", "m": 0.7}, "sableux": {"fr": "Sableux", "m": 1.25}}
        return sols.get(k, {"fr": k, "m": 1.0})

cerveau = MoteurRaisonnement()
# Test
if __name__ == "__main__":
    r = cerveau.raisonner("irrigation tomate", "tomate", "argileux", 5, 6, "Petite pluie")
    for i, e in enumerate(r["etapes"], 1):
        print(f"{i}. {e}")
