from fastapi import FastAPI

app = FastAPI(title = "My Cool API")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hello!"}