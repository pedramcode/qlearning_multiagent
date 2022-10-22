from p5 import *
from .world_settings import WorldSettings
from utils import Size, Pos
from enum import Enum
import json
from agent import Agent
import random


class WorldEvent(Enum):
    GRID_CLICKED = 0


class World(object):
    """
    The main world objects responsible to managing rendering and grid system
    """

    __settings: WorldSettings = None
    __events = {}
    __is_mouse_down = False
    __draw_cursor = False
    __blocks = []
    __foods = []
    __agents = []

    def __init__(self, _input):
        """
            Initialize the world
            _input is a WorldSetting or string of map path
        """

        if type(_input) == WorldSettings:
            size(__settings.get_size().width(), __settings.get_size().height())
            title(str(__settings))
            self.__settings = __settings
        else:
            data = {}
            with open(_input, "r") as file:
                data = json.load(file)
            self.__settings = WorldSettings(
                data["name"], 
                data["size"][0], 
                data["size"][1], 
                data["grid"][0], 
                data["grid"][1])
            size(self.__settings.get_size().width(), self.__settings.get_size().height())
            title(str(self.__settings))
            
            for blc in data["blocks"]:
                self.__blocks.append(Pos.from_list(blc))
            for fod in data["foods"]:
                self.__foods.append(Pos.from_list(fod))
    

    def listen(self, event: WorldEvent, func) -> None:
        self.__events.update({
            event: func,
        })
    

    def is_food_at(self, pos: Pos, remove=False) -> bool:
        for i in range(len(self.__foods)-1, -1, -1):
            food = self.__foods[i]
            if food.x() == pos.x() and food.y() == pos.y():
                if remove:
                    del self.__foods[i]
                return True
        return False


    def get_free_pos(self) -> Pos:
        while(True):
            x = random.randrange(0, floor(self.get_size().width()/self.get_grid_size().width())-1)
            y = random.randrange(0, floor(self.get_size().height()/self.get_grid_size().height())-1)

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
            
            if not_block and not_food:
                break

        return Pos(x, y)
                     

    
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
    

    def update(self) -> None:
        if len(self.__agents) != 0:
            for i in range(len(self.__agents)-1, -1, -1):
                agent = self.__agents[i]
                agent.update()
                if agent.is_dead():
                    del self.__agents[i]
                    continue
    

    def render(self) -> None:
        """
        Renders the world
        """
        push()
        background(50, 50, 50)
        self.__draw_grid()

        for food in self.__foods:
            push()
            rect_mode(CORNER)
            stroke(20, 120, 10)
            stroke_weight(1)
            fill(10, 50, 200)
            x1 = food.x() * self.__settings.get_grid().width()
            y1 = food.y() * self.__settings.get_grid().height()
            margin_x = floor(self.__settings.get_grid().width() - self.__settings.get_grid().width() * 0.7)
            margin_y = floor(self.__settings.get_grid().height() - self.__settings.get_grid().height() * 0.7)
            rect((x1 + margin_x, y1 + margin_y), self.__settings.get_grid().width() - margin_x * 2, self.__settings.get_grid().height() - margin_y * 2)
            pop()

        for block in self.__blocks:
            push()
            rect_mode(CORNER)
            no_stroke()
            fill(100, 100, 100)
            x1 = block.x() * self.__settings.get_grid().width()
            y1 = block.y() * self.__settings.get_grid().height()
            rect((x1, y1), self.__settings.get_grid().width(), self.__settings.get_grid().height())
            pop()
        
        for agent in self.__agents:
            agent.render()

        if mouse_is_pressed:
            if not self.__is_mouse_down:
                self.__is_mouse_down = True
                if WorldEvent.GRID_CLICKED in self.__events:
                    self.__events[WorldEvent.GRID_CLICKED](
                        self.__norm_pos_to_grid_pos(
                            Pos(
                                mouse_x,
                                mouse_y
                            )
                        )
                    )
        else:
            self.__is_mouse_down = False
        
        if self.__draw_cursor:
            push()
            rect_mode(CORNER)
            no_stroke()
            fill(255)
            grid_pos = self.__norm_pos_to_grid_pos(
                Pos(
                    mouse_x,
                    mouse_y
                )
            )
            x1 = grid_pos.x() * self.__settings.get_grid().width()
            y1 = grid_pos.y() * self.__settings.get_grid().height()
            rect((x1, y1), self.__settings.get_grid().width(), self.__settings.get_grid().height())
            pop()
        pop()
    

    def __draw_grid(self) -> None:
        """
        Draws the main grid of the world
        """

        push()
        stroke_weight(1)
        stroke(120, 120, 120, 100)

        for x in range(
            self.__settings.get_grid().width(), 
            self.__settings.get_size().width(), 
            self.__settings.get_grid().width()):

            line((x, 0), (x, self.__settings.get_size().height()))
        
        for y in range(
            self.__settings.get_grid().height(), 
            self.__settings.get_size().height(), 
            self.__settings.get_grid().height()):
            line((0, y), (self.__settings.get_size().width(), y))

        pop()
