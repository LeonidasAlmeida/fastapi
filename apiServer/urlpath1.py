from fastapi import FastAPI

app = FastAPI()


@app.get("/hi/{who}")
def greet(who):
    return f"Hello? {who}?"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("urlpath1:app",reload=True)
