from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from model import Cuckoo

app = FastAPI()

class RequestBody(BaseModel):
    val: list
    weight: list
    capacity: int
    N: int
    pa: float
    maxiter: int

# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:8081",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.post("/api")
async def api(request: RequestBody):
    print(request)
    cuckoo = Cuckoo(request.val, request.weight, request.capacity, request.N, request.pa, request.maxiter)
    cuckoo.process()
    response = dict()
    response.update({"best_solution": cuckoo.get_best_solution().tolist()})
    response.update({"best_value": cuckoo.out(cuckoo.get_best_solution()).__int__()})
    response.update({"weight": cuckoo.get_weight().__int__()})
    return response