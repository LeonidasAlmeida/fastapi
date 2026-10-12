from fastapi import FastAPI, Body
import random

app = FastAPI()


@app.post("/sorteio")
def celcius(sorte: list = Body(embed=True)):
    return random.choice(sorte)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
