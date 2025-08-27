import random

class Plant:
    def __init__(self, name, harvest_yield):
        self.name = name
        self.harvest_yield = harvest_yield
        self.growth_stages = ['seed','sprout','plant','flower','harvest_ready']
        self.current_growth_stage = self.growth_stages[0]
        self.harvestable = False
        
    def grow(self):
        if self.current_growth_stage != self.growth_stages[-1]:
            next_stage = self.growth_stages.index(self.current_growth_stage) + 1
            self.current_growth_stage = self.growth_stages[next_stage]
            if self.current_growth_stage == "harvest_ready":
                self.harvestable = True
                print(f"The {self.name} can be harvested!")
        else:
            print(f"{self.name} cannot grow further.")
    
    def harvest(self):
        if self.harvestable:
            self.harvestable = False
            print(f"{self.name} has been harvested successfully.")
            return True
        else:
            print(f"{self.name} is not ready to harvest.")
            return False
        
class Tomato(Plant):
    def __init__(self, harvest_yield):
        super().__init__("Tomato", harvest_yield)
        self.growth_stages.insert(-1, "fruiting")

class Lettuce(Plant):
    def __init__(self, harvest_yield):
        super().__init__("Lettuce", harvest_yield)
        
        
class Gardener:
    """
    Models a gardener who can plant, tend, and harvest plants.
    Keeps track of planted plants and the gardener's inventory.
    """
    
    plant_dict = {
        "Tomato": Tomato,
        "Lettuce": Lettuce
    }
    
    def __init__(self, name):
        self.name = name
        self.planted_plants = []
        self.inventory = {}

