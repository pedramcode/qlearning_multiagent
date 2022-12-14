from .world_settings import WorldSettings
from utils import Size, Pos, SSetting, WorldEvent
from enum import Enum
import json
from agent import Agent, Sex
import random
import numpy as np
import math


class World(object):
    """
    The main world objects responsible to managing rendering and grid system
    """

    __settings: WorldSettings = None
    __is_mouse_down = False
    __draw_cursor = False
    __map_path = None
    __blocks = []
    __foods = []
    __agents = []
    __state = []
    __step = 0
    __event_list = {}

    def __init__(self, _input):
        """
            Initialize the world
            _input is a WorldSetting or string of map path
        """

        if type(_input) == WorldSettings:
            self.__settings = __settings
        else:
            self.__map_path = _input
            data = {}
            with open(_input, "r") as file:
                data = json.load(file)
            self.__settings = WorldSettings(
                data["name"], 
                data["size"][0], 
                data["size"][1], 
                data["grid"][0], 
                data["grid"][1])
            
            for blc in data["blocks"]:
                self.__blocks.append(Pos.from_list(blc))
            for fod in data["foods"]:
                self.__foods.append(Pos.from_list(fod))

        for i in range(0, SSetting.init_pop()):
            agent_x = Agent(self.get_free_pos(), self)
            self.add_agent(agent_x)
        
        self.__init_event()
    

    def terminated(self) -> bool:
        return len(self.__agents) == 0
    

    def trigger_event(self, event, val=1):
        self.__event_list[event] += val
    

    def reset(self):
        if self.__map_path:
            self.__state = []
            data = {}
            with open(self.__map_path, "r") as file:
                data = json.load(file)
            self.__settings = WorldSettings(
                data["name"], 
                data["size"][0], 
                data["size"][1], 
                data["grid"][0], 
                data["grid"][1])
            
            for blc in data["blocks"]:
                self.__blocks.append(Pos.from_list(blc))
            for fod in data["foods"]:
                self.__foods.append(Pos.from_list(fod))

            for i in range(0, SSetting.init_pop()):
                agent_x = Agent(self.get_free_pos(), self)
                self.add_agent(agent_x)
    

    def is_food_at(self, pos: Pos, remove=False) -> bool:
        for i in range(len(self.__foods)-1, -1, -1):
            food = self.__foods[i]
            if food.x() == pos.x() and food.y() == pos.y():
                if remove:
                    del self.__foods[i]
                return True
        return False


    def get_free_pos(self) -> Pos:
        max_tries = 5
        i = 0
        x = None
        y = None
        while(True):
            x = random.randrange(0, math.floor(self.get_size().width()/self.get_grid_size().width())-1)
            y = random.randrange(0, math.floor(self.get_size().height()/self.get_grid_size().height())-1)

            not_block = True
            not_food = True

            for block in self.__blocks:
                if block.x() == x and block.y() == y:
                    not_block = False
                    break
            
            for food in self.__foods:
                if food.x() == x and food.y() == y:
                    not_food = False
                    break
            
            if i > max_tries or not_block and not_food:
                break
            i+=1

        return Pos(x, y) if not (x==None or y==None) else None
    

    def __init_event(self):
        self.__event_list = {
            WorldEvent.BIRTH: 0,
            WorldEvent.DEAD_CHILD: 0,
            WorldEvent.TOTAL_DEAD: 0,
        }
                     

    
    def add_block(self, pos: Pos):
        self.__blocks.append(pos)
    

    def add_food(self, pos: Pos):
        self.__foods.append(pos)

    
    def add_agent(self, agent: Agent):
        self.__agents.append(agent)

    
    def draw_cursor(self, state: bool) -> None:
        self.__draw_cursor = state
    

    def get_size(self) -> Size:
        """
        Returns the world size in tuple (width, height)
        """
        return self.__settings.get_size()
    

    def get_grid_size(self) -> Size:
        """
        Returns the Grid size in tuple (width, height)
        """
        return self.__settings.get_grid()
    

    def __norm_pos_to_grid_pos(self, norm_pos: Pos):
        x = floor(norm_pos.x() / self.__settings.get_grid().width())
        y = floor(norm_pos.y() / self.__settings.get_grid().height())
        return Pos(x, y)
    

    def get_foods(self) -> list:
        return self.__foods
    

    def get_blocks(self) -> list:
        return self.__blocks
    

    def get_agents(self) -> list:
        return self.__agents

    
    def get_last_state(self):
        if len(self.__state) == 0:
            return Noneavg
        return self.__state[len(self.__state)-1]
    

    def get_state(self) -> list:
        return self.__state
    

    def mean_health(self) -> float:
        return round(np.nan_to_num(np.average([x.get_health() for x in self.__agents])), 2)
    

    def mean_hunger(self) -> float:
        return round(np.nan_to_num(np.average([x.get_hunger() for x in self.__agents])), 2)
    

    def update(self, details=False) -> None:
        if random.random() > (1.0-SSetting.food_gen()):
            for i in range(SSetting.food_min(), SSetting.food_max()):
                free_space = self.get_free_pos()
                if(free_space):
                    self.add_food(free_space)

        if len(self.__agents) != 0:
            for i in range(len(self.__agents)-1, -1, -1):
                agent = self.__agents[i]
                agent.update()
                if agent.is_dead():
                    del self.__agents[i]
                    continue
                
        male_c = len([0 for x in self.__agents if x.get_sex() == Sex.MALE])
        self.__state.append({
            "step": self.__step,
            "pop": len(self.__agents),
            "pop_health": self.mean_health(),
            "pop_hunger": self.mean_hunger(),
            "food_count": len(self.__foods),
            "male_count": male_c,
            "female_count": abs(len(self.__agents)-male_c),
            "total_dead": self.__event_list[WorldEvent.TOTAL_DEAD],
            "dead_born": self.__event_list[WorldEvent.DEAD_CHILD],
            "birth": self.__event_list[WorldEvent.BIRTH],
        })

        self.__init_event()

        if details:
            print(self.get_last_state())

        self.__step += 1
    

    def get_step(self) -> int:
        return self.__step
