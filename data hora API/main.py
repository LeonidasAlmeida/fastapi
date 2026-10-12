from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/")
def datahora():
    return {"Data "}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
