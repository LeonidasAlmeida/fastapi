from fastapi import FastAPI, Body

app = FastAPI()


@app.post("/hi/")
def greet(who: str = Body(embed=True)):
    return f"hello {who}"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("urlpath3:app", reload=True)
