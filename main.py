import numpy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from model import Cuckoo
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
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
    cuckoo_sol, cuckoo_val, cuckoo_weight, cuckoo_time = cuckoo.process()
    real_sol, real_val, real_weight, real_time = cuckoo.blind_search()
    response = dict()
    print('cuckoo sol', cuckoo_sol)
    print('cuckoo val', cuckoo_val)
    print('cuckoo weight', cuckoo_weight)
    print('cuckoo time', cuckoo_time)

    print('real sol', real_sol)
    print('real val', real_val)
    print('real weight', real_weight)
    print('real time', real_time)

    response.update({"cuckoo_sol": cuckoo_sol.tolist()})
    response.update({"cuckoo_val": cuckoo_val.__int__()})
    response.update({"cuckoo_weight": cuckoo_weight.__int__()})
    response.update({"cuckoo_time": cuckoo_time.__float__()})

    response.update({"real_sol": real_sol})
    response.update({"real_val": real_val.__int__()})
    response.update({"real_weight": real_weight.__int__()})
    response.update({"real_time": real_time.__float__()})

    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)