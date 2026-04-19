import sys
import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# Ajuste de path para o Orquestrador
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# --- CONFIGURAÇÃO DE AMBIENTE PARA EXECUÇÃO LOCAL ---
# Forçamos o host do banco para localhost, já que estamos fora do Docker
os.environ["DB_HOST"] = "127.0.0.1"

from src.orquestrador.orchestrator_aeris import OrchestratorAeris

app = FastAPI(title="AERIS Web Bridge")
templates = Jinja2Templates(directory="/opt/AERIS/src/api/templates")

# Iniciamos o cérebro
aeris = OrchestratorAeris()

MASTER_USER = "geninho"
MASTER_PASS = "Smg955fd!@"

@app.get("/")
async def login_page(request: Request):
    # NOVA SINTAXE: O request vai como primeiro argumento direto
    return templates.TemplateResponse(request, "login.html", {})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == MASTER_USER and password == MASTER_PASS:
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/?erro=1", status_code=303)

@app.get("/dashboard")
async def dashboard(request: Request):
    # NOVA SINTAXE: O request vai como primeiro argumento direto
    return templates.TemplateResponse(request, "dashboard.html", {})

@app.post("/executar")
async def executar(comando: str = Form(...)):
    resultado, status = aeris.pipeline_de_execucao(comando)
    return {"resultado": resultado, "status": status}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
