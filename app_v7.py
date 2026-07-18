from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
PRIX={"mais":280,"coton":310,"manioc":150,"soja":450,"arachide":600,"riz":500,"voandzou":800,"tomate":400,"piment":1200,"oignon":650}
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  parsed=urllib.parse.urlparse(self.path)
  q=urllib.parse.parse_qs(parsed.query).get('q',[''])[0]
  ql=q.lower()
  self.send_response(200);self.send_header("Content-type","text/html; charset=utf-8");self.end_headers()
  prix={k:v for k,v in PRIX.items() if k in ql}
  conseil="Neem 50g/L + surveillance" if "mais" in ql or "chenille" in ql else ""
  html=f"<html><body style='font-family:sans-serif;padding:15px;background:#f0fdf4'><h1>NOUNKOUN V7 Creme</h1><p>Abomey-Calavi - Local 100% OK</p><form><input name=q value='{q}'><button>OK</button></form><div><b>{q}</b>: {prix} {conseil}</div><div>Prix: {PRIX}</div><p>200 OK - Sans FastAPI</p></body></html>"
  self.wfile.write(html.encode())
print("V7 sur http://0.0.0.0:8000")
HTTPServer(("0.0.0.0",8000), Handler).serve_forever()
