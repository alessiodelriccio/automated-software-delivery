import os
from fastapi import FastAPI

app = FastAPI()

TOKEN = os.getenv('ACCESS_TOKEN')
REPO_NAME = "tensorflow/tensorflow"
CSV_FILE = 'commit_data.csv'
CSV_RESULTS_FILE = 'results.csv'

@app.get("/repo-commits")
async def get_commits():
    # Implementare funzione che estrae i commit dal repo e salva i dati in un CSV
    pass

@app.get("/filter-commit")
async def get_vulnerability_commit():
    # Implementare funzione che filtra i commit che riguardano vulnerabilità
    pass

@app.get("/major_contributors")
async def major_contributors():
    # Implementare funzione che restituisce i principali contributori
    pass

@app.get("/top_contributors")
async def top_contributors():
    # Implementare funzione che restituisce i 10 autori che hanno cotribuito maggiormente a fare fix di vulnerabilità
    pass