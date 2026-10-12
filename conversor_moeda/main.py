from fastapi import FastAPI

from util import Utill

app = FastAPI()


@app.post("/cambio")
def celcius(utill: Utill):
    return {f"o cambio do valor {utill.valor} kz em {utill.para} = ": utill.convertMoeda()}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
