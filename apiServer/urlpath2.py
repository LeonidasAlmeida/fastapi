from fastapi import FastAPI
app = FastAPI()

@app.get("/hi/") ##query parameters
def greet(who):
    return f" hello {who}" 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("urlpath2:app",reload=True)