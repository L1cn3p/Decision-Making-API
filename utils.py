import json

"""
for each object in our asset_list we should create an Asset and give it a key (int: this integer refers to the index of the 
individual asset in our algorithm response)
"""

class Asset:

    def __init__(self, name: str, speed: float, capability: list, prep_time: float, effectiveness: list, location ):
        self.name = name
        self.speed = speed
        self.capability = capability
        self.prep_time = prep_time
        self.effectiveness = effectiveness
        self.location = location

        self.assets = [
            ["Fire Engine A", 80, ["Oil","Chemical","Electrical"], 5, ["Supress","Control"]],
            ["Fire Engine B", 90, ["Chemical","Electrical"], 3, ["Supress","Control"]],
            ["Fire Fast Response", 100, ["Electrical"], 2, ["Control"]],
            ["Ambulance", 80, ["Injury-Serious", "Injury-Light"], 5, ["Control", "Evacuate"]],
            ["Medical Fast Response", 100, ["Injury-Light"], 2, ["Control"]],
            ["Police Patrol Car", 100, ["Robbery","Breakin","TrafficAccident","TrafficControl"], 5, ["Investigate","Arrest","Control"]],
            ["Traffic Police Bike", 120, ["TrafficAccident","TrafficControl"], 2, ["Investigate","Control"]]
            ]

class AssetFactory:
    def __init__(self):
        self.asset_list = []

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
    
    def create_asset_list(self, assets_list):
        for asset in assets_list:
            _type = asset["type"]
            location = asset["location"]
            quantity = int(asset["quantity"])

            match _type:
                case "Fire Engine A":
                    self._MakeFireEngineA(location=location, quantity=quantity)
                case "Fire Engine B":
                    self._MakeFireEngineB(location=location, quantity=quantity)
                case "Fire Fast Response":
                    self._MakeFireFastResponse(location=location, quantity=quantity)
                case "Ambulance":
                    self._MakeAmbulance(location=location, quantity=quantity)
                case "Medical Fast Response":
                    self._MakeMedicalFastResponse(location=location, quantity=quantity)
                case "Police Patrol Car":
                    self._MakePolicePatrolCar(location=location, quantity=quantity)
                case "Traffic Police Bike":
                    self._MakeTrafficPoliceBike(location=location, quantity=quantity)

        

factory = AssetFactory()

with open('object.json', 'r') as f:
    data = json.load(f)

request = data["assets_list"]
factory.create_asset_list(request)

print(factory.asset_list)
print(len(factory.asset_list))

