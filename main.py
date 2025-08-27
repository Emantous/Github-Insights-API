from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI
import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI(title="GitHub Insights API")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "github-insights-api",
        "version": os.getenv("APP_VERSION", "0.1.0")
    }

@app.get("/{owner}/{repo}/languages")
def repo_language(owner: str, repo: str):
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/languages", headers={"accept" : "application/vnd.github+json"})
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return 'heh'

@app.get("/{owner}/{repo}/contributors")
def repo_contributors(owner: str, repo: str):
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contributors", headers={"accept" : "application/vnd.github+json"})
    data = response.json()
    if response.status_code == 200:
        transofrmed_contributors = []
        for member in data:
            transofrmed_contributors.append((member['login'], member['contributions']))
        return transofrmed_contributors
    else:
        return 'heh'

@app.get("/{owner}/{repo}/overview")
def repo_overview(owner: str, repo: str):
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers={"accept" : "application/vnd.github+json"})
    data = response.json()
    if response.status_code == 200:
        repo_info = {}
        repo_info["stars"] = data["stargazers_count"]
        repo_info["watchers"] = data["watchers_count"]
        repo_info["main_language"] = data["language"]
        repo_info["forks"] = data["forks_count"]
        repo_info["open issues"] = data["open_issues_count"]
        return repo_info
    else:
        return 'heh'

@app.get("/{owner}/{repo}/stars")
def repo_stars(owner: str, repo: str):
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/stargazers", headers={"accept" : "application/vnd.github+json"})
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return 'heh'

@app.get("/{owner}/{repo}/issues")
def repo_issues(owner: str, repo: str):
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues", headers={"accept" : "application/vnd.github+json"})
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return 'heh'

@app.get("/{owner}/{repo}/issues/{number}")
def repo_issue_timeline(owner: str, repo: str, number: int):
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues/{number}/timeline", headers={"accept" : "application/vnd.github+json"})
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return 'heh'

@app.post("/analyze")
def repo_overview(owner: str, repo: str):
    return f"Get repo {repo} from {owner}"

@app.delete("/{owner}/{repo}")
def repo_overview(owner: str, repo: str):
    return f"Get repo {repo} from {owner}"