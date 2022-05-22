# from utils import *
import DMO
import utils
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
    asset_factory = utils.AssetFactory()
    problem_factory = utils.ProblemFactory()
    asset_dict = asset_factory.create_asset_dict(assets_list)
    problem_list = problem_factory.create_problem_list(situation_list)
    utils.asset_dict = asset_dict
    utils.problem_list = problem_list
    DMO.asset_dict = asset_dict
    DMO.problem_list = problem_list
    best_individual = DMO.make_decision(asset_dict, problem_list)
    print(asset_dict[0].name)
    print(problem_list)
    response = []
    for i, val in enumerate(best_individual):
        if val != 0:
            print(f'deploy {asset_dict[i].name} at: {asset_dict[i].location} \n')
            response.append(f'deploy {asset_dict[i].name} at: {asset_dict[i].location}')
    return {"message": response}


