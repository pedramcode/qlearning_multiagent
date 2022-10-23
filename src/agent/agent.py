from utils import Pos
from .brain import Brain
import random
from enum import Enum


class Dir(Enum):
    TOP=0
    RIGHT=1
    BOTTOM=2
    LEFT=3


class Sex(Enum):
    MALE=0
    FEMALE=1


class Agent(object):
    __pos = None
    __health = None
    __hunger = None
    __world = None
    __brain = None
    __vision = None
    __sex = None
    __life_span = None


    def __init__(self, pos: Pos, world):
        self.__pos = pos
        self.__world = world
        self.__brain = Brain(7, 4)
        self.__health = random.randrange(10, 101)
        self.__hunger = random.randrange(10, 101)
        self.__vision = random.randrange(1, 30)
        self.__sex = Sex.MALE if random.random() > 0.5 else Sex.FEMALE
        self.__life_span = random.randrange(15, 100)
    

    def is_dead(self) -> bool:
        return self.__health <= 0

    
    def get_sex(self) -> Sex:
        return self.__sex
    

    def get_pos(self) -> Pos:
        return self.__pos

    
    def move(self, dir: Dir) -> None:
        state = self()
        if dir == Dir.TOP:
            if state[3] == 1:
                self.damage(1)
            else:
                self.__pos.set_y(self.__pos.y()-1)
                self.hungry(0.3)
        if dir == Dir.RIGHT:
            if state[4] == 1:
                self.damage(1)
            else:
                self.__pos.set_x(self.__pos.x()+1)
                self.hungry(0.3)
        if dir == Dir.BOTTOM:
            if state[5] == 1:
                self.damage(1)
            else:
                self.__pos.set_y(self.__pos.y()+1)
                self.hungry(0.3)
        if dir == Dir.LEFT:
            if state[6] == 1:
                self.damage(1)
            else:
                self.__pos.set_x(self.__pos.x()-1)
                self.hungry(0.3)
    

    def get_mate(self):
        res = None

        for agent in self.__world.get_agents():
            if agent == self:
                continue
            if Pos.distance(self.__pos, agent.get_pos()) <= 2:
                return agent
        return res

    
    def update(self) -> None:
        self.__life_span -= 1
        if self.__life_span <= 0:
            if random.random() > 0.9:
                self.__health = 0
                self.__hunger = 0
            else:
                self.damage(1)

        if self.__hunger < 40:
            self.damage(0.3)
        if self.__health < 90 and self.__hunger > 90:
            self.heal(5)
            self.hungry(3)
        

        # Sex
        horniness = 0 if self.__world.mean_hunger() < 30 else 0.4
        horny = random.random() > horniness
        if horny:
            mate = self.get_mate()
            if mate:
                is_gay = mate.get_sex() == self.__sex
                if not is_gay:
                    if self.__health > 60 and mate.get_health() > 60:
                        # Make baby
                        self.__world.add_agent(Agent(self.__pos.copy(), self.__world))
                        self.hungry(2)
                        mate.hungry(2)
                        
                        # Damage female
                        if self.__sex == Sex.FEMALE:
                            self.damage(3)
                        elif mate.get_sex() == Sex.FEMALE:
                            mate.damage(3)
                elif is_gay:
                    # Gay sex
                    self.hungry(2)
                    mate.hungry(2)
            else:
                # Mastribate
                self.hungry(2.1)


        # Choose action
        eps = 0.2
        dice = random.random()
        if self.__world.is_food_at(self.__pos, True):
            self.heal(5)
            self.eat(5)

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
    

    def __call__(self):
        # Returns the state
        # health, hunger, closest food distance, top, right, bottom, left
        state = [
            self.__health,
            self.__hunger,
        ]

        pos = self.__pos

        foods = self.__world.get_foods()
        closest_food = -1
        for food in foods:
            dist = Pos.distance(pos, food)
            if dist < closest_food and dist <= self.__vision:
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
