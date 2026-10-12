from fastapi import FastAPI

from util import Utill

app = FastAPI()


@app.post("/verificar")
def celcius(utill: Utill):
    return utill.calcular()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
