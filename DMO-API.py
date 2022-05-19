# from utils import *
from DMO import *
from fastapi import FastAPI, Request


"""
This API will reveive an json request (see object.json for example)
and will send this request to be procossed by the alogrithm.
It should respond with a json object of the appropriate response to each situation
"""

app = FastAPI()

@app.post("/DMO")
async def submit(request: Request):
    data = await request.json()
    
    assets_list = data["assets_list"]
    situation_list = data["situation_list"]

    asset_factory = AssetFactory()
    problem_factory = ProblemFactory()

    asset_dict = asset_factory.create_asset_dict(assets_list)
    problem_list = problem_factory.create_problem_list(situation_list)

    response = str(asset_dict) + str(problem_list)

    
    return {"message": response}


