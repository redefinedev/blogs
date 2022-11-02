""" Web server 1"""
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    """root endpoint"""
    return {"message": "Hello World"}


@app.get("/ready")
async def ready():
    """ready endpoint"""
    return True


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
