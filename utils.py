import json
import math


ASSETS = [
    ["Fire Engine A", 80, ["Oil","Chemical","Electrical"], 5, ["Supress","Control"]],
    ["Fire Engine B", 90, ["Chemical","Electrical"], 3, ["Supress","Control"]],
    ["Fire Fast Response", 100, ["Electrical"], 2, ["Control"]],
    ["Ambulance", 80, ["Injury-Serious", "Injury-Light"], 5, ["Control", "Evacuate"]],
    ["Medical Fast Response", 100, ["Injury-Light"], 2, ["Control"]],
    ["Police Patrol Car", 100, ["Robbery","Breakin","TrafficAccident","TrafficControl"], 5, ["Investigate","Arrest","Control"]],
    ["Traffic Police Bike", 120, ["TrafficAccident","TrafficControl"], 2, ["Investigate","Control"]]
    ]

class Asset:

    def __init__(self, name: str, speed: float, capability: list, prep_time: float, effectiveness: list, location: tuple ):
        self.name = name
        self.speed = speed
        self.capability = capability
        self.prep_time = prep_time
        self.effectiveness = effectiveness
        self.location = location


"""
To use this class initialize it and call create_asset_dict with a list of json objects as an argument
see object.json for an example of what the inputted list in this method should look like.
factory = AssetFactory()
asset_dict = factory.create_asset_dict(request)
returns a dictionary of the assets we want with an int as a key.
This key will correspond to the index of its respective asset in the "individual" we use in the algorithm.
"""

class AssetFactory:
    def __init__(self):
        self.asset_list = []

    def _MakeFireEngineA(self, location, quantity):
         
        if quantity > 0:
            self.asset_list.append(Asset(*ASSETS[0], location=location))
            self._MakeFireEngineA(location=location, quantity=quantity-1)
        return 

    def _MakeFireEngineB(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*ASSETS[1], location=location))
            self._MakeFireEngineB(location=location, quantity=quantity-1)
        return 

    def _MakeFireFastResponse(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*ASSETS[2], location=location))
            self._MakeFireFastResponse(location=location, quantity=quantity-1)
        return 

    def _MakeAmbulance(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*ASSETS[3], location=location))
            self._MakeAmbulance(location=location, quantity=quantity-1)
        return 

    def _MakeMedicalFastResponse(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*ASSETS[4], location=location))
            self._MakeMedicalFastResponse(location=location, quantity=quantity-1)
        return 

    def _MakePolicePatrolCar(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*ASSETS[5], location=location))
            self._MakePolicePatrolCar(location=location, quantity=quantity-1)
        return 

    def _MakeTrafficPoliceBike(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*ASSETS[6], location=location))
            self._MakeTrafficPoliceBike(location=location, quantity=quantity-1)
        return 
    
    def create_asset_dict(self, assets_list):
        self.asset_dict = {}
        for asset in assets_list:
            _type = asset["type"]
            location = asset["location"]
            quantity = int(asset["quantity"])

            if _type ==  "Fire Engine A":
                self._MakeFireEngineA(location=location, quantity=quantity)
            elif _type ==  "Fire Engine B":
                self._MakeFireEngineB(location=location, quantity=quantity)
            elif _type ==  "Fire Fast Response":
                self._MakeFireFastResponse(location=location, quantity=quantity)
            elif _type ==  "Ambulance":
                self._MakeAmbulance(location=location, quantity=quantity)
            elif _type ==  "Medical Fast Response":
                self._MakeMedicalFastResponse(location=location, quantity=quantity)
            elif _type ==  "Police Patrol Car":
                self._MakePolicePatrolCar(location=location, quantity=quantity)
            elif _type ==  "Traffic Police Bike":
                self._MakeTrafficPoliceBike(location=location, quantity=quantity)

        for i, asset in enumerate(self.asset_list):
            self.asset_dict[i] = asset
        return self.asset_dict


"""
To create a problem scenario: first create an instance of Problem factory.
call create_problem_list with arg situation_list: a list of json objects.
See object.json for an example of the json object structure.
The method returns a list of Problem objects

problem_factory = ProblemFactory()
problem_list = problem_factory.create_problem_list(situation_list)
"""

class Problem:
    def __init__(self, name, severity, action, location, time_constraint):
        self.name = name
        self.severity = severity
        self.action = action
        self.location = location
        self.time_constraint = time_constraint

class ProblemFactory:
    
    def create_problem_list(self,situation_list):
        self.problem_list = []
        for problem in situation_list:
            name = problem["type"]
            severity = problem["severity"]
            action = problem["action"]
            location = problem["location"]
            time_constraint = problem["time_constraint"]

            problem = Problem(name, severity, action, location, time_constraint)
            self.problem_list.append(problem)

        return self.problem_list

"""
The API takes the users assets and problems as inputs - the algorithm generates 
a list of length = len(asset_dict.keys())
the class iterate through the problems and assign each problem to an asset if it meets
the required criteria
it will output some kind of response object with all the problems and their assigned assets
the time it will take for the asset to reach the problem
and a list of the remaining unsolved problems - if any
"""
class AssetAllocator:
    def __init__(self, asset_dict, problem_list):
        self.assets = asset_dict
        self.problems = problem_list

    # This method calculates the total distance between the location of the asset and
    # the location of the problem by comparing the coordinates
    def calculate_distance(self,asset,problem):
        x1 = asset.location[0]
        y1 = asset.location[1]
        x2 = problem.location[0]
        y2 = problem.location[1]
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

    # Checks if the asset has the intended capability - returns a boolean
    def check_response_validity(self,asset,problem):
        capability = asset.capability
        intent = problem.action
        return intent in capability

    # Calculates the total time it takes for each asset to reach its target (in minutes)
    def check_response_time(self,asset, problem):
        distance = self.calculate_distance(asset, problem)
        speed = asset.speed
        preparation_time = asset.prep_time
        response_time = (distance / speed*60) + preparation_time
        return response_time

    # Checks the efficiency of the response, gives penalty for redundant assets sent
    # after assigning each problem an asset, use the remaining unused assets to
    # add an efficiency penalty
    def check_response_efficiency(self,response, problem):
        pass



    

if __name__ == "__main__":
    with open('object.json', 'r') as f:
        data = json.load(f)
    assets_list = data["assets_list"]
    situation_list = data["situation_list"]

    asset_factory = AssetFactory()
    problem_factory = ProblemFactory()

    asset_dict = asset_factory.create_asset_dict(assets_list)
    problem_list = problem_factory.create_problem_list(situation_list)
    # print(asset_dict.items())
    # print(problem_list)
    print(vars(asset_dict[0]))
    print(vars(problem_list[0]))

