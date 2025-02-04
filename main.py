from fastapi import FastAPI, Request
import uvicorn
from pydantic import BaseModel
from typing import List, Optional


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running on port 8000!"}

@app.get("/{name}")
def read_name(name: str):
    return {"message": f"Hello, {name}!"}

class PayloadModel(BaseModel):
    name: str  # Example field, adjust as needed
    value: str  # Example field, adjust as needed

@app.post("/payloads")
async def update_name(payload: PayloadModel):
    """Handles incoming JSON payloads"""
    print(payload.dict())  # Log the received payload
    return {"status": "Success", "received": payload}

class CommitInfo(BaseModel):
    branch: str
    before_commit: str
    after_commit: str
    repo_name: str
    commit_message: str
    commit_url: str
    author_name: str
    added_files: List[str]
    modified_files: List[str]
    removed_files: List[str]

@app.post("/github-webhook")
async def github_webhook(payload: dict):
    """
    Handles GitHub webhook events and extracts required information.
    """
    try:
        extracted_data = CommitInfo(
            branch=payload.get("ref", "").replace("refs/heads/", ""),
            before_commit=payload.get("before", ""),
            after_commit=payload.get("after", ""),
            repo_name=payload.get("repository", {}).get("full_name", ""),
            commit_message=payload.get("head_commit", {}).get("message", ""),
            commit_url=payload.get("head_commit", {}).get("url", ""),
            author_name=payload.get("head_commit", {}).get("author", {}).get("name", ""),
            added_files=payload.get("head_commit", {}).get("added", []),
            modified_files=payload.get("head_commit", {}).get("modified", []),
            removed_files=payload.get("head_commit", {}).get("removed", [])
        )

        # Print or log extracted information
        print(f"New commit pushed to {extracted_data.branch} branch of {extracted_data.repo_name}")
        print(f"Commit Message: {extracted_data.commit_message}")
        print(f"Commit URL: {extracted_data.commit_url}")
        print(f"Author: {extracted_data.author_name}")
        print(f"Added Files: {extracted_data.added_files}")
        print(f"Modified Files: {extracted_data.modified_files}")
        print(f"Removed Files: {extracted_data.removed_files}")

        return {"status": "success", "data": extracted_data.dict()}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
