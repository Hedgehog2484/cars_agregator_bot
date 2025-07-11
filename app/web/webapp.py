import asyncio

import uvicorn

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.utils.process_user_settings import save_user_settings
from app.services.database.implementations.postgres import PostgresDAO

app = FastAPI()


# app.mount("/static", StaticFiles(directory="static", html=True), name='static')

def get_db():
    pass


# @app.get("/", response_class=FileResponse)
#async def send_page(request: Request):
#    return FileResponse("web/index.html")


@app.post("/save_settings")
async def get_user_settings(request: Request, db: PostgresDAO = Depends(get_db)):
    await save_user_settings(await request.json(), db)
    return {"message": "ok"}


def start_webapp(db):
    # app = FastAPI()
    app.dependency_overrides[get_db] = lambda: db
    app.mount("/", StaticFiles(directory="web/static", html=True), name="static")

    # app.router.get("/", response_class=FileResponse)(send_page)
    # app.router.post("/save_settings")(get_user_settings)
    # uvicorn.run(app, host="0.0.0.0", port=8432, ssl_keyfile="./0.0.0.0-key.pem", ssl_certfile="./0.0.0.0.pem")
    uvicorn.run(
        app, host="pepepu.ru", port=443, ssl_keyfile="web/key.pem", ssl_certfile="web/certificate.crt"
    )
