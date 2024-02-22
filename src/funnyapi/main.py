from fastapi import FastAPI

from funnyapi.users.router import router as user_router

app = FastAPI()
app.include_router(user_router)


@app.get("/hello-world")
def hello_world():
    return "hello world"
