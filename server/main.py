from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from server.routes.upload_route import router as upload_router
from server.routes.status_route import router as status_router
from server.routes.download_route import router as download_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(status_router)
app.include_router(download_router)
app.mount("/static", StaticFiles(directory="static"), name="static")