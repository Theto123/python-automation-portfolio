from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API running"}

@app.get("/square/{n}")
def square(n: int):
    return {"result": n*n}