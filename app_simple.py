from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

PRIX = {"mais":280,"coton":310,"manioc":150,"soja":450,"arachide":600,"riz":500,"voandzou":800,"tomate":400,"piment":1200,"oignon":650}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        q = qs.get('q',[''])[0].lower()

        self.send_response(200)
        self.send_header("Content-type","text/html; charset=utf-8")
        self.end_headers()

        if parsed.path == "/prix":
            self.wfile.write(json.dumps(PRIX, ensure_ascii=False).encode())
            return
        if parsed.path.startswith("/search"):
            res = {"query": q, "prix": {}, "conseil": ""}
            for k,v in PRIX.items():
                if k in q:
                    res["prix"][k]=v
            if "chenille" in q or "mais" in q:
                res["conseil"]="Neem + surveillance tous les 2j si >2 chenilles/plant. Risque élevé saison pluies."
            if not res["prix"] and not res["conseil"]:
                res["conseil"]=f"Essaie: mais, coton, voandzou, soja, tomate"
            self.send_header("Content-type","application/json; charset=utf-8")
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode())
            return

        html = f"""
        <html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
        <style>body{{font-family:sans-serif;padding:20px}}input{{padding:10px;width:70%}}button{{padding:10px}}</style>
        </head><body>
        <h1>🌱 NOUNKOUN V7 - Local OK</h1>
        <h3>Abomey-Calavi - 37 cultures - Sans FastAPI</h3>
        <form action="/search"><input name="q" placeholder="ex: chenille mais, prix coton"><button>Rechercher</button></form>
        <p><b>Prix du jour:</b> {PRIX}</p>
        <p>API: <a href="/prix">/prix</a> | <a href="/search?q=mais">/search?q=mais</a></p>
        <p style="color:green">Python {self.server_version} tourne sans pydantic!</p>
        </body></html>
        """
        self.wfile.write(html.encode('utf-8'))

print("Lancement Nounkoun sur http://0.0.0.0:8000...")
HTTPServer(("0.0.0.0",8000), Handler).serve_forever()
