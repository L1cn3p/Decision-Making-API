import json
import math


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
        
        self.assets = [
            ["Fire Engine A", 80, ["Oil","Chemical","Electrical"], 5, ["Supress","Control"]],
            ["Fire Engine B", 90, ["Chemical","Electrical"], 3, ["Supress","Control"]],
            ["Fire Fast Response", 100, ["Electrical"], 2, ["Control"]],
            ["Ambulance", 80, ["Injury-Serious", "Injury-Light"], 5, ["Control", "Evacuate"]],
            ["Medical Fast Response", 100, ["Injury-Light"], 2, ["Control"]],
            ["Police Patrol Car", 100, ["Robbery","Breakin","TrafficAccident","TrafficControl"], 5, ["Investigate","Arrest","Control"]],
            ["Traffic Police Bike", 120, ["TrafficAccident","TrafficControl"], 2, ["Investigate","Control"]]
            ]

    def _MakeFireEngineA(self, location, quantity):
         
        if quantity > 0:
            self.asset_list.append(Asset(*self.assets[0], location=location))
            self._MakeFireEngineA(location=location, quantity=quantity-1)
        return 

    def _MakeFireEngineB(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*self.assets[1], location=location))
            self._MakeFireEngineB(location=location, quantity=quantity-1)
        return 

    def _MakeFireFastResponse(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*self.assets[2], location=location))
            self._MakeFireFastResponse(location=location, quantity=quantity-1)
        return 

    def _MakeAmbulance(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*self.assets[3], location=location))
            self._MakeAmbulance(location=location, quantity=quantity-1)
        return 

    def _MakeMedicalFastResponse(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*self.assets[4], location=location))
            self._MakeMedicalFastResponse(location=location, quantity=quantity-1)
        return 

    def _MakePolicePatrolCar(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*self.assets[5], location=location))
            self._MakePolicePatrolCar(location=location, quantity=quantity-1)
        return 

    def _MakeTrafficPoliceBike(self, location, quantity):
        
        if quantity > 0:
            self.asset_list.append(Asset(*self.assets[6], location=location))
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
it will output some kind of response object with all the problems and their assigned assets
"""

# This method calculates the total distance between the location of the asset and
# the location of the problem by comparing the coordinates
def calculate_distance(asset,problem):
    x1 = asset.location[0]
    y1 = asset.location[1]
    x2 = problem.location[0]
    y2 = problem.location[1]
    dist = math.sqrt(abs((x2 - x1)**2 + (y2 - y1)**2))
    return dist

def calculate_time(asset, problem):
    distance = calculate_distance(asset,problem)
    preparation_time = asset.prep_time
    asset_speed = asset.speed/60
    travel_time = distance/asset_speed
    time = preparation_time + travel_time
    return time


# Checks the efficiency of the response, by penalizing for every asset in the
# response. This will make the algorithm favor smaller responses
def check_response_efficiency(response):
    return sum(response)

# checks if the response meets the time constraint
def check_response_time(assigned_assets):
    time_violation = 0
    # total time allows us to favor faster responses
    total_time = 0
    for (asset, problem) in assigned_assets:
        time = calculate_time(asset, problem)
        total_time += time
        time_cons = problem.time_constraint
        print(f"time for {asset.name} at {asset.location} to reach {problem.name} with limit {time_cons} at location {problem.location} = {time}")
        if time > time_cons:
            time_violation += time - time_cons
            # this way the violation is proportional to how late the response is
    return time_violation, total_time

# adding a multiplier to validity violations to signify their importabnce
VALIDITY_VIOLATION_MULTIPLIER = 10
# checks if the response meets requirements for the actions we want to be performed on the problem
def check_response_validity(response,problem_list):
    resp = response.copy()
    assigned_assets = []
    n_correct_responses = 0
    response_magnitude = 0
    for problem in problem_list:
        prob_type = problem.name
        action = problem.action
        response_magnitude += problem.severity
        for _ in range(problem.severity):
            for n,asset in enumerate(resp):
                if asset != 0:
                    if (asset_dict[n].capability.count(prob_type)) and (asset_dict[n].effectiveness.count(action)):
                        n_correct_responses += 1
                        assigned_assets.append((asset_dict[n], problem))
                        resp[n] = 0
                        break
    validity_violation = (response_magnitude-n_correct_responses) * VALIDITY_VIOLATION_MULTIPLIER
    return validity_violation, assigned_assets

HARD_CONSTRAINT_PENALTY = 2
# Penalty multiplier for the hard constraints in getCost method
def getCost(response, problem_list):
    """
    Calculates the total cost of the various violations in the given schedule
    ...
    :param response: a list of binary values describing the given asset response
    :param problem_list: a list of objects of class Problem()
    :return: the calculated cost
    """

    # count the various violations:
    validity_violations, assigned_assets = check_response_validity(response, problem_list)
    time_violations, total_time = check_response_time(assigned_assets)
    efficiency_violations = check_response_efficiency(response)
    # print(f"Validity violations: {validity_violations}")
    # print(f"time violations: {time_violations}")
    # print(f"efficiency violations: {efficiency_violations}")

    # calculate the cost of the violations:
    hardContstraintViolations = validity_violations + time_violations
    softContstraintViolations = efficiency_violations

    return HARD_CONSTRAINT_PENALTY * hardContstraintViolations + softContstraintViolations, total_time


