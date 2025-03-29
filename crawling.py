"""
Modulo per l'aggiornamento dei dati dei commit di un repository GitHub.

Funzioni:
- update_commit_data(repo, file_path): Recupera e aggiorna i commit salvati in un file CSV.
"""

import os
from datetime import datetime

import pandas as pd
from tqdm import tqdm

def update_commit_data(repo, file_path):
    """Recupera i commit più recenti da un repository e li salva in un file CSV.

    Args:
        repo: Oggetto repository di GitHub.
        file_path (str): Percorso del file CSV dove salvare i commit.

    Returns:
        str: Percorso del file CSV aggiornato.
    """
    new_commit_data = []
    existing_commits = []

    if os.path.exists(file_path):
        data_frame = pd.read_csv(file_path)
        existing_commits = data_frame.to_dict("records")
    else:
        data_frame = pd.DataFrame(columns=["author", "date", "hash", "message"])

    if existing_commits:
        latest_commit_date = max(
            datetime.strptime(commit["date"], "%Y-%m-%d %H:%M:%S") for commit in existing_commits
        )
        latest_commits = repo.get_commits(since=latest_commit_date)
    else:
        latest_commits = repo.get_commits()

    for commit in tqdm(latest_commits):
        commit_info = {
            "author": commit.commit.author.name,
            "date": commit.commit.author.date.strftime("%Y-%m-%d %H:%M:%S"),
            "hash": commit.sha,
            "message": commit.commit.message,
        }
        new_commit_data.append(commit_info)

    new_commit_data.extend(existing_commits)
    data_frame = pd.DataFrame(new_commit_data)
    data_frame.to_csv(file_path, index=False)
    return file_path
