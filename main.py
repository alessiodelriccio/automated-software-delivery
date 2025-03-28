import os

from fastapi import FastAPI
from github import Github
from starlette.responses import HTMLResponse

from crawling import update_commit_data
from filtering import filter_and_save_results, get_major_contributors, get_author_occurrences, \
    generate_top10_contributors_html
from get_data import get_results

app = FastAPI()

TOKEN = os.getenv('ACCESS_TOKEN')
REPO_NAME = "tensorflow/tensorflow"
CSV_FILE = 'commit_data.csv'
CSV_RESULTS_FILE = 'results.csv'

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)


@app.get("/repo-commits")
async def get_commits():
    update_commit_data(repo, CSV_FILE)
    html_table = get_results(CSV_FILE, 30)
    return HTMLResponse(content=html_table, media_type="text/html")


@app.get("/filter-commit")
async def get_vulnerability_commit():
    filter_and_save_results(CSV_FILE, CSV_RESULTS_FILE)
    html_table = get_results(CSV_RESULTS_FILE, 80)
    return HTMLResponse(content=html_table, media_type="text/html")


@app.get("/major_contributors")
async def major_contributors():
    return get_major_contributors()


@app.get("/top_contributors")
async def top_contributors():
    top_authors = get_author_occurrences()
    html_list = generate_top10_contributors_html(top_authors)
    return HTMLResponse(content=html_list, media_type="text/html")