from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    """root endpoint"""
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
