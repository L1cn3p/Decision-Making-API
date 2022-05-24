# from utils import *
import DMO
import utils
from fastapi import FastAPI, Request


"""
This API will reveive a json request (see object.json for example)
and will send this request to be procossed by the alogrithm.
It should respond with suggestion list containing which assets should be deployed,
and from which location.
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
    response = []
    __ , assigned_assets = utils.check_response_validity(best_individual, problem_list)
    for (asset, problem) in assigned_assets:
        time = utils.calculate_time(asset, problem)
        line = f"Deploy {asset.name} from {asset.location} to {problem.name} at {problem.location} - (est. duration: {round(time)} minutes)"
        print(line + "\n")
        response.append(line)
    return {"Response": response}


