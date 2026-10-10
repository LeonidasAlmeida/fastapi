from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def greeting(request):
    return JSONResponse("Hello? World?")


app = Starlette(
    debug=True,
    routes=[
        Route("/hi", greeting),
    ],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("starlette_hello:app", reload=True)
