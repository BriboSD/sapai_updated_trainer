import gym
from gymnasium import spaces
import numpy as np
from sapai import Player, Pet, Food, Battle
from sklearn.preprocessing import OneHotEncoder

class sapenv(gym.Env):

    ALL_PETS = ["pet-ant", "pet-duck", "pet-otter", "pet-pig", "pet-ant", "pet-mosquito", "pet-fish", "pet-cricket", "pet-horse"]
    ALL_FOOD = ["food-apple", "food-honey"]
    ALL_STATUS = ["status-honey-bee"]
    MAX_PET_SHOP_SLOTS = 16
    MAX_FOOD_SHOP_SLOTS = 2
    MAX_TEAM_SLOTS = 5
    MAX_LIVES = 10
    MAX_GOLD = 10
    MAX_TROPHIES = 10
    ANIMAL_STATS_MULTIPLIER = 4 #so space can represent each animal's tier, attack, health, and type
    metadata = {'render.modes': ['human']}


    def __init__(self):
        super().__init__()
        self.total_animal_slots = self.MAX_TEAM_SLOTS + self.MAX_PET_SHOP_SLOTS
        self.obs_space_shape = (len(self.ALL_PETS) * self.total_animal_slots)*self.ANIMAL_STATS_MULTIPLIER + (len(self.ALL_STATUS) * self.MAX_TEAM_SLOTS) + (self.MAX_FOOD_SHOP_SLOTS * len(self.ALL_FOOD)) + (self.MAX_PET_SHOP_SLOTS + self.MAX_FOOD_SHOP_SLOTS) + self.MAX_GOLD + self.MAX_LIVES + self.MAX_TROPHIES 
       
       #use uint8 as dtype because we only are using 1s, and uint8 is less storage space than int
        self.observation_space = spaces.Box(0, 1, shape=(self.obs_space_shape,), dtype = np.uint8)
        '''
        calculating num actions the computer can take:
            - end turn: 1
            - roll:: 1
            - buy pet: MAX_PET_SHOP_SLOTS (can buy any of the pets in the shop)
            - buy food; MAX_FOOD_SHO_SLOTS * MAX_TEAM_SLOTS (can buy any of the shop food for any of the pets on the team)
            - sell: MAX_TEAM_SLOTS (can sell any pets on team)
            - combine_from_team: MAX_TEAM_SLOTS * (MAX_TEAM_SLOTS-1) (can potentially combine any pet on team into any other slot on team)
            - freeze: MAX_SHOP_SPETS + MAX_FOOD_PETS (can freeze any shop pet or food)
            - unfreeze: MAX_SHOP_SPETS + MAX_FOOD_PETS (can unfreeze any shop pet)
            - reorder; MAX_TEAM_SIZE! (can swap any pet with any other pet, not repeating, through combinatorics)
                NOTE: reorder will usually be 120 different possible actions, assuming team size of 5
        '''

        #will have to adjust this manually, because building it using the constants will result in long lists of addition at the end
        self.act_space_nums = {
            "end_turn": 0,
            "roll": 1,
            "buy_pet": 2,
            "buy_food": 8,
            "sell": 13,
            "combine": 18,
            "freeze": 38,
            "unfreeze": 44,
            "reorder": 50
        }
        self.action_space = spaces.Discrete(170)

        self.player = Player()

        self.reset()

    def reset(self, options=None):
        '''
        reset player to have no pets,
        '''
        self.player = Player()
        self.encode_game_state()
    
    def encode_game_state(self):
        pet_pass_list = list()
        foot_pass_list = list()
        shop_pass_list = list()

        #encode team pets
        for slot in self.player.team:
            pet_pass_list.append(slot.pet)
        encoded_pet_list = self.encode_pets(pet_pass_list)

        shop_pets = self.player.shop.pets
        shop_food = self.player.shop.foods

        #pad unfilled shop spaces
        while len(shop_pets) < 6:
            shop_pets.append(Pet("pet-none"))
        while len(shop_food) < 3:
            shop_food.append(Food("food-none"))
        
        #encode shop pets, then add an encoding representing frozen slots
        encoded_shop_pet_list = self.encode_pets(shop_pets)
        for shopSlot in self.player.shop:
            if 
        #next step is to write code for freezing being encoded
            

    def encode_pets(self, pets):
        returnList = list()
        category = np.array(self.ALL_PETS)
        stat_category = np.array(self.ALL_STATUS)

        for pet in pets:
            #in order, we add vectors for animal type, the attack/health/tier, and status
            if pet.name == "pet-none":
                #append zero vectors for animal type, health, attack, and tier
                returnList.append(np.zeros(len(self.ALL_PETS)))
                returnList.append(np.zeros(3,))
                returnList.append(np.zeros(len(self.ALL_STATUS)))
            else:
                returnList.append(self.sub_encode(category, pet.name))
                returnList.append(np.array(pet.tier/3, pet.health/50, pet.attack/50))
                if pet.status == "none":
                    returnList.append(np.zeros(len(self.ALL_STATUS)))
                else:
                    returnList.append(self.sub_encode(stat_category, pet.status))
        return returnList
    
    def encode_shop_pets(self, pets):
        returnList = list()
        category = np.array(self.ALL_PETS)

        
                
    def sub_encode(self, category, value):
        #pass it a category to encode over and a value to encode, and it'll give back an array with a one representing that value, to be added to the overall array that is read by the computer
        valueFit = np.array([[value]])
        encoder = OneHotEncoder(categories=[category], sparse_output=False)
        encodedData = encoder.fit_transform(valueFit)
        condensedData = np.sum(encodedData, axis = 0)
        return condensedData
        

    def encode_

        