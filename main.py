from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
EMO={"content":("😊🎉","Merci Mitché! Tu es content, force! 💪"),"triste":("😔💔","Je comprends ta peine 😔. On va trouver solution."),"fier":("💪😎","Tu dis Nounkoun fort? C'est toi le fort!"),"neutre":("🤔🌾","Je t'écoute Mitché.")}
def detect(t):
 t=t.lower()
 if any(x in t for x in ["merci","content","fort","genial"]): return "content"
 if any(x in t for x in ["perdu","mort","triste","difficile"]): return "triste"
 if "nounkoun fort" in t or "reussi" in t: return "fier"
 return "neutre"
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  q=urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('q',[''])[0]; e=detect(q) if q else "neutre"; emoji,txt=EMO[e]
  self.send_response(200);self.send_header("Content-type","text/html; charset=utf-8");self.end_headers()
  h=f"<html><head><meta charset=utf-8><meta name=viewport content='width=device-width'><style>body{{background:#f0fdf4;padding:10px;font-family:sans-serif}}.card{{background:#fff;padding:14px;border-radius:12px;margin:10px 0}}</style></head><body><h1>NOUNKOUN V11 COEUR {emoji}</h1><div class=card style='font-size:40px;text-align:center'>{emoji} {e.upper()}</div><div class=card><form><input name=q value='{q}' style='padding:12px;width:70%'><button>OK</button></form></div><div class=card><b>Nonzo:</b> {txt}</div></body></html>"
  self.wfile.write(h.encode())
print("V11 COEUR sur 8000");HTTPServer(("0.0.0.0",8000), H).serve_forever()
