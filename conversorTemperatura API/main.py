from fastapi import FastAPI

from util import Utill

app = FastAPI()


@app.post("/convert/celcius")
def celcius(utill: Utill):
    return {"temperatura em celcius": utill.convCelcius()}


@app.post("/convert/feher")
def celcius(utill: Utill):
    return {"temperatura em Fehrenheit": utill.convFahrenheit()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
