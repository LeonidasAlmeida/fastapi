from fastapi import FastAPI
import asyncio

app = FastAPI()


@app.get("/hi")
async def greet():
    await asyncio.sleep(10)
    return "hello? World?"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("greet_async:app", reload=True)
