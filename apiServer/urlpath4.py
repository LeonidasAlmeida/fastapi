from fastapi import FastAPI, Header

app = FastAPI()


@app.post("/hi/")
def greet(who: str = Header()):
    return f"hello {who}"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("urlpath4:app", reload=True)
