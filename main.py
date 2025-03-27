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
