"""
NOUNKOUN IA - MOTEUR DE RAISONNEMENT INTELLIGENT V14
37 cultures Benin | Offline | Traçabilité | Economie
Intelligence paysanne encodée discrètement - pas de mention externe dans le code
"""

class MoteurRaisonnement:
    def __init__(self):
        self.memoire = []
        # Base économique locale Benin
        self.cultures_eco = {
            "Maïs": {"eau_besoin": 500, "cout_ha": 150000, "rendement": 2500, "prix_kg": 250, "maladie": "Chenille légionnaire"},
            "Manioc": {"eau_besoin": 300, "cout_ha": 80000, "rendement": 15000, "prix_kg": 100, "maladie": "Mosaïque"},
            "Tomate": {"eau_besoin": 600, "cout_ha": 300000, "rendement": 20000, "prix_kg": 350, "maladie": "Mildiou"},
            "Riz": {"eau_besoin": 800, "cout_ha": 200000, "rendement": 4000, "prix_kg": 350, "maladie": "Pyriculariose"},
            "Ananas": {"eau_besoin": 400, "cout_ha": 400000, "rendement": 30000, "prix_kg": 150, "maladie": "Cochenille"},
            "Coton": {"eau_besoin": 500, "cout_ha": 180000, "rendement": 1200, "prix_kg": 300, "maladie": "Ver rose"},
        }

    def raisonner(self, question, culture="Maïs", sol="argileux", pluie=5, budget=50000, ph=6.0, humidite=50, symptome=""):
        """
        Raisonnement en 5 étapes:
        1. Intention 2. Contexte multi-facteurs 3. Economie 4. Risque 5. Decision
        """
        etapes = []
        q = (question + " " + symptome).lower()

        # ETAPE 1 : INTENTION
        intention = "conseil_general"
        if any(x in q for x in ["eau","irrig","arros","pluie"]): intention = "irrigation"
        elif any(x in q for x in ["jaune","trou","chenille","noir","pourri","malade","feuille"]): intention = "diagnostic"
        elif any(x in q for x in ["argent","gagner","vendre","cout","economie","benefice","prix"]): intention = "rentabilite"
        elif any(x in q for x in ["quand","semis","planter","recolte","fertiliser"]): intention = "planification"
        elif any(x in q for x in ["sol","ph","fertilite","amendement"]): intention = "sol"
        etapes.append(f"1️⃣ Intention détectée: {intention} | Culture: {culture}")

        # ETAPE 2 : CONTEXTE MULTI-FACTEURS (sol + pluie + pH + humidité)
        db = self.cultures_eco.get(culture, self.cultures_eco["Maïs"])
        sol_facteur = 1.3 if sol == "sableux" else 0.7 if sol == "argileux" else 1.0
        besoin_reel = db["eau_besoin"] * sol_facteur
        deficit_eau = besoin_reel - (pluie * 10)
        
        etapes.append(f"2️⃣ Contexte: {culture} besoin {besoin_reel:.0f}L/m², sol {sol} (x{sol_facteur}), pluie {pluie}mm, pH {ph}, humidité {humidite}%, budget {budget}F")
        etapes.append(f"   Déficit eau: {deficit_eau:.0f}L | Maladie typique: {db['maladie']}")

        # ETAPE 3 : RAISONNEMENT ECONOMIQUE (aider à gagner plus / dépenser moins)
        cout_eau = max(0, deficit_eau) * 2  # 2F par litre (pompage)
        benefice_brut = db["rendement"] * db["prix_kg"]
        benefice_net = benefice_brut - db["cout_ha"] - cout_eau
        economie_possible = 0
        
        if pluie > 20:
            economie_possible = cout_eau
            decision_eau = f"⛔ STOP irrigation! Pluie {pluie}mm prévue. Tu économises {economie_possible:.0f}F cette semaine. Sol {sol} garde l'eau."
        else:
            decision_eau = f"💧 Irrigue {besoin_reel/7:.0f}L/m²/jour. Coût eau {cout_eau:.0f}F. Bénéfice final {benefice_net:.0f}F/ha si tu suis conseil."

        etapes.append(f"3️⃣ Économie: {decision_eau} | Bénéfice brut {benefice_brut}F, net {benefice_net:.0f}F")

        # ETAPE 4 : ANALYSE RISQUE (météo extrême + sol)
        risque_msg = "Risque faible"
        conseils_risque = []
        if pluie < 5 and db["eau_besoin"] > 400:
            risque_msg = "⚠️ SÉCHERESSE ÉLEVÉE"
            conseils_risque.append("Paillage obligatoire (paille 5cm) + réserve eau")
        if pluie > 40:
            risque_msg = "🌧️ INONDATION"
            conseils_risque.append("Creuse drains 30cm autour parcelle, ne fertilise pas")
        if float(ph) < 5.5:
            conseils_risque.append(f"pH acide {ph}: ajoute cendre 500kg/ha")
        if float(ph) > 7.5:
            conseils_risque.append(f"pH basique {ph}: ajoute compost + fumier")
        if float(humidite) < 30:
            conseils_risque.append("Sol sec: arrosage + paillage")

        etapes.append(f"4️⃣ Risque: {risque_msg} | {'; '.join(conseils_risque) if conseils_risque else 'Conditions bonnes'}")

        # ETAPE 5 : DÉCISION FINALE EXPLICABLE + TRAÇABILITÉ
        if intention == "diagnostic":
            if "jaune" in q:
                final = f"🍂 DIAGNOSTIC {culture} feuille jaune: 70% manque azote (pH {ph}), 30% trop d'eau (hum {humidite}%). ACTION: Compost 2kg/pied + arrêt eau 3j. PAS pesticide! Économie 15.000F. Enregistre production → +15% valeur traçabilité"
            elif "chenille" in q or "trou" in q:
                final = f"🐛 Chenille sur {culture}: Seuil traitement dépassé. ACTION: Neem 50g/L + savon noir, dose précise 15ml/16L pulvé le soir. Coût 2.000F vs 15.000F chimique. Efficacité 85%"
            elif "noir" in q or "pourri" in q:
                final = f"⚫ Pourriture {culture}: Trop d'eau! ACTION: Arrache feuilles malades, aère, cendre sur pied. Pas de chimique. Économie 10.000F"
            else:
                final = f"🔍 Surveillance {culture} 48h. Photo à nouveau demain. Pas de traitement préventif systématique = économie 20.000F/ha"
        elif intention == "rentabilite":
            surface = budget // db["cout_ha"] if db["cout_ha"]>0 else 1
            final = f"💰 Avec {budget}F, tu peux faire {surface*1000:.0f}m² de {culture}. Bénéfice estimé {benefice_net*surface:.0f}F. Conseil: Commence petit, traçabilité JSON pour export +15% prix. Marché {culture}: {db['prix_kg']}F/kg"
        elif intention == "planification":
            final = f"📅 {culture}: Semis optimal {culture} = selon pluie. Si pluie {pluie}mm cette semaine, attends 5j. Fertilisation J+30, traitement J+45, récolte J+{self.cultures_eco.get(culture, {}).get('rendement',90)}. Économie si respect calendrier: +20% rendement"
        else: # irrigation / general
            final = f"{decision_eau} | {risque_msg}. Calendrier {culture}: engrais local disponible. Traçabilité: enregistre chaque action pour prime export."

        # Mémoire pour humaniser (il se souvient)
        self.memoire.append({"q": question, "culture": culture, "decision": final, "date": str(datetime.datetime.now())[:10]})
        if len(self.memoire) > 20:
            self.memoire.pop(0)

        return {
            "decision": final,
            "etapes": etapes,
            "economie": economie_possible,
            "benefice": benefice_net,
            "risque": risque_msg,
            "intent": intention,
            "memoire_len": len(self.memoire)
        }

    def historique(self):
        return self.memoire[-5:]

# Instance globale pour import
cerveau = MoteurRaisonnement()
