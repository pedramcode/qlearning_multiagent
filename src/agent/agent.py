from utils import Pos
from p5 import *
from .brain import Brain
import random
from enum import Enum


class Dir(Enum):
    TOP=0
    RIGHT=1
    BOTTOM=2
    LEFT=3


class Agent(object):
    __pos = None
    __health = 100
    __hunger = 100
    __world = None
    __brain = None


    def __init__(self, pos: Pos, world):
        self.__pos = pos
        self.__world = world
        self.__brain = Brain(7, 4)
    

    def is_dead(self) -> bool:
        return self.__health <= 0
    

    def get_pos(self) -> Pos:
        return self.__pos

    
    def move(self, dir: Dir) -> None:
        state = self()
        if dir == Dir.TOP:
            if state[3] == 1:
                self.damage(5)
            else:
                self.__pos.set_y(self.__pos.y()-1)
                self.hungry(1)
        if dir == Dir.RIGHT:
            if state[4] == 1:
                self.damage(5)
            else:
                self.__pos.set_x(self.__pos.x()+1)
                self.hungry(1)
        if dir == Dir.BOTTOM:
            if state[5] == 1:
                self.damage(5)
            else:
                self.__pos.set_y(self.__pos.y()+1)
                self.hungry(1)
        if dir == Dir.LEFT:
            if state[6] == 1:
                self.damage(5)
            else:
                self.__pos.set_x(self.__pos.x()-1)
                self.hungry(1)

    
    def update(self) -> None:
        if self.__hunger < 40:
            self.damage(1)
        if self.__health < 90 and self.__hunger > 90:
            self.heal(1)
            self.hungry(1)
        
        eps = 0.2
        dice = random.random()

        if self.__world.is_food_at(self.__pos, True):
            self.heal(10)
            self.eat(10)

        if dice > eps:
            res = self.__brain.pulse(self())
            max_val = 0
            max_index = 0
            i = 0
            for x in res:
                if x > max_val:
                    max_val = x
                    max_index = i
                i += 1
            
            if max_index == 0:
                self.move(Dir.TOP)
            elif max_index == 1:
                self.move(Dir.RIGHT)
            elif max_index == 2:
                self.move(Dir.BOTTOM)
            elif max_index == 3:
                self.move(Dir.LEFT)
        else:
            inx = random.randrange(0, 4)
            if inx == 0:
                self.move(Dir.TOP)
            elif inx == 1:
                self.move(Dir.RIGHT)
            elif inx == 2:
                self.move(Dir.BOTTOM)
            elif inx == 3:
                self.move(Dir.LEFT)


    def get_health(self):
        return self.__health
    

    def get_hunger(self):
        return self.__hunger
    

    def damage(self, amount) -> None:
        self.__health = self.__health - amount
        if self.__health < 0:
            self.__health = 0
    

    def heal(self, amount) -> None:
        self.__health = self.__health + abs(amount)
        if self.__health > 100:
            self.__health = 100
    

    def hungry(self, amount):
        self.__hunger = self.__hunger - amount
        if self.__hunger < 0:
            self.__hunger = 0
    

    def eat(self, amount) -> None:
        self.__hunger = self.__hunger + abs(amount)
        if self.__hunger > 100:
            self.__hunger = 100
    

    def render(self):
        push()

        x1 = self.__pos.x() * self.__world.get_grid_size().width()
        y1 = self.__pos.y() * self.__world.get_grid_size().height()
        grid_w = self.__world.get_grid_size().width()
        grid_h = self.__world.get_grid_size().height()

        # Draw body
        rect_mode(CORNER)
        stroke_weight(1)

        pct_diff = 1.0 - (self.__health / 100)
        red = min(255, pct_diff * 2 * 255)
        green = min(255, (self.__health / 100) * 2 * 255)
        fill(red, green, 0, self.__hunger)

        stroke(30, 120, 40)
        rect((x1, y1), grid_w, grid_h)

        pop()
    

    def __call__(self):
        # Returns the state
        # health, hunger, closest food distance, top, right, bottom, left
        state = [
            self.__health,
            self.__hunger,
        ]

        pos = self.__pos

        foods = self.__world.get_foods()
        closest_food = None
        for food in foods:
            dist = floor(math.sqrt(math.pow(pos.x() - food.x(), 2) + math.pow(pos.y() - food.y(), 2)))
            if closest_food == None:
                closest_food = dist
            if dist < closest_food:
                closest_food = dist
        state.append(closest_food)

        top_blocked = 0
        right_blocked = 0
        bottom_blocked = 0
        left_blocked = 0

        for block in self.__world.get_blocks():
            if block.x() == pos.x() and block.y() == pos.y()-1:
                top_blocked = 1
            if block.x() == pos.x()+1 and block.y() == pos.y():
                right_blocked = 1
            if block.x() == pos.x() and block.y() == pos.y()+1:
                bottom_blocked = 1
            if block.x() == pos.x()-1 and block.y() == pos.y():
                left_blocked = 1

        state.append(top_blocked)
        state.append(right_blocked)
        state.append(bottom_blocked)
        state.append(left_blocked)

        return state
