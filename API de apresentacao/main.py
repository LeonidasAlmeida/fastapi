from fastapi import FastAPI
app = FastAPI()
import uvicorn

@app.get("/")
def apresentacao():
    return{
        "nome":"leonidas",
        "idade":"28"
    }
    
if __name__=="__main__":
    uvicorn.run("main:app", reload=True)