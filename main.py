from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
