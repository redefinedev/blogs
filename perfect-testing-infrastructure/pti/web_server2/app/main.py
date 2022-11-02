""" Web server 2 """
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/is_odd")
async def is_odd(number: int):
    return number % 2 > 0


@app.get("/ready")
async def ready():
    """ready endpoint"""
    return True


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
