from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
def mensagem():
    return "Ola mundo"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)