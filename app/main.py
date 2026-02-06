#TODO: For now: create FastAPI app, wire routes, create DB connection when handling a request (simple V1)

#from fastapi import FastAPI
#from app.api.upload import router
from fastapi import FastAPI
from app.api.upload import router

app = FastAPI()
app.include_router(router)

