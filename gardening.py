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
    def __init__(self):
        harvest_yield = random.randint(2, 5)
        super().__init__("Tomato", harvest_yield)
        self.growth_stages.insert(-1, "fruiting")
        
class Lettuce(Plant):
    def __init__(self):
        harvest_yield = random.randint(1, 3)
        super().__init__("Lettuce", harvest_yield)
        self.growth_stages = ['seed', 'sprout', 'harvest_ready']
        
plant_dict = {"Tomato": Tomato,
              "Lettuce": Lettuce}  
plant_list = list(plant_dict.keys())
      
def select_item(items):
    """Displays items with numbers and lets the player select one."""
    if not items:
        print("No items available.")
        return None

    items_list = list(items.keys()) if isinstance(items, dict) else items

    for idx, item in enumerate(items_list, 1):
        print(f"{idx}. {item}")

    while True:
        select = input("Which item do you want to plant? ")
        try:
            number = int(select) - 1
            if 0 <= number < len(items_list):
                return items_list[number]
            else:
                print(f"Please enter a number between 1 and {len(items_list)}.")
        except ValueError:
            print("Invalid input")

class Gardener:
    """Models a gardener who can plant, tend, and harvest plants.
    Keeps track of planted plants and the gardener's inventory."""
    
    def __init__(self, name):
        self.name = name
        self.planted_plants = []
        self.inventory = {"seeds":{}, "harvested":{}}

    def plant(self):
        """Choose a specific plant from your inventory, using it up (reducing its count), 
        and adding it to a list of growing plants."""
        
        available_seeds = {k: v for k, v in self.inventory["seeds"].items() if v > 0}
        if not available_seeds:
            print("You don't have any seeds to plant.")
            return None
        choice = select_item(available_seeds)
        self.inventory["seeds"][choice] -= 1
        plant_class = plant_dict[choice]
        plant = plant_class()
        self.planted_plants.append(plant)
        print(f"{self.name} planted a {choice}.")
        return plant

    def tend(self):
        """ This method represents the ongoing care your plants need, and as a result, 
        they progress through different growth stages."""
        if not self.planted_plants:
            return "No plants to tend."
        for plant in self.planted_plants:
            plant.grow()
        return f"You tended the plants. They are growing!"

    def harvest(self):
        """Once a plant is ready, harvest it and adds it to the inventory. """
        harvested = []
        for plant in self.planted_plants[:]:
            if plant.harvestable:
                self.planted_plants.remove(plant)
                harvested.append(plant)
                self.inventory["harvested"][plant.name] = self.inventory["harvested"].get(plant.name, 0) + plant.harvest_yield
                print(f"You harvested {plant.harvest_yield} {plant.name}(s).")
    
        if not harvested:
            return "No plants are ready to harvest."
    
        return f"You harvested {len(harvested)} plant(s) successfully."
    
    def forage_for_seeds(self):
        """Randomly find a seed and add it to the gardener's inventory."""
        found_seed = random.choice(plant_list)
        self.inventory["seeds"][found_seed] = self.inventory["seeds"].get(found_seed, 0) + 1
        print(f"{self.name} went foraging and found a {found_seed} seed!")  


# --- Game Loop ---

# 1. Capture player's name
player_name = ""
while not player_name.isalpha():
    player_name = input("What's your name? ").strip()
    if not player_name.isalpha():
        print("Please enter a valid name")
# 2. Initialize gardener
gardener = Gardener(player_name)

# 3. Define valid actions
actions = ["forage", "plant", "tend", "harvest", "backpack", "help", "exit"]

# 4. Welcome message
print(f"Hello {player_name}! Your garden awaits.")
print("Type 'help' at any time to see the list of available actions.")

# 5. Start game loop
while True:
    action = input("What would you like to do? ").strip().lower()

    if action not in actions:
        print("Invalid action. Type 'help' to see available options.")
        continue

    if action == "help":
        print(f"Available actions: {', '.join(actions)}")
    elif action == "exit":
        print(f"Goodbye, {player_name}! Thanks for gardening today.")
        break
    elif action == "forage":
        gardener.forage_for_seeds()
    elif action == "plant":
        gardener.plant()
    elif action == "tend":
        print(gardener.tend())
    elif action == "harvest":
        print(gardener.harvest())
    elif action == "backpack":
        seeds = gardener.inventory["seeds"]
        harvested = gardener.inventory["harvested"]

        if not seeds and not harvested:
            print("Your backpack is empty.")
        else:
            if seeds:
                print("Seeds:")
                for seed, count in seeds.items():
                    print(f"  {seed}: {count}")
            if harvested:
                print("Harvested plants:")
                for plant, count in harvested.items():
                    print(f"  {plant}: {count}")
        
