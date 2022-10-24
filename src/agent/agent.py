from utils import Pos, SSetting, WorldEvent
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
    __sex_halt = None


    def __init__(self, pos: Pos, world):
        self.__pos = pos
        self.__world = world
        self.__brain = Brain(7, 4)
        self.__health = random.uniform(
            (SSetting.max_health()*0.3), 
            SSetting.max_health())
        self.__hunger = random.uniform(
            int(SSetting.max_hunger()*0.3), 
            SSetting.max_hunger())
        self.__vision = random.uniform(SSetting.min_vision(), SSetting.max_vision())
        self.__sex = Sex.MALE if random.random() > (1.0-SSetting.male_gender_probability()) else Sex.FEMALE
        self.__life_span = random.uniform(
            SSetting.min_life_span_random(),
            SSetting.max_life_span_random())
        self.__sex_halt = 0
    

    def is_dead(self) -> bool:
        res = self.__health <= 0
        if res:
            self.__world.trigger_event(WorldEvent.TOTAL_DEAD)
        return res

    
    def get_sex(self) -> Sex:
        return self.__sex
    

    def get_pos(self) -> Pos:
        return self.__pos

    
    def move(self, dir: Dir) -> None:
        state = self()
        hit_wall_dmg = SSetting.hit_wall_damage()
        walk_hunger = SSetting.walking_hunger()
        if dir == Dir.TOP:
            if state[3] == 1:
                self.damage(hit_wall_dmg)
            else:
                self.__pos.set_y(self.__pos.y()-1)
                self.hungry(walk_hunger)
        if dir == Dir.RIGHT:
            if state[4] == 1:
                self.damage(hit_wall_dmg)
            else:
                self.__pos.set_x(self.__pos.x()+1)
                self.hungry(walk_hunger)
        if dir == Dir.BOTTOM:
            if state[5] == 1:
                self.damage(hit_wall_dmg)
            else:
                self.__pos.set_y(self.__pos.y()+1)
                self.hungry(walk_hunger)
        if dir == Dir.LEFT:
            if state[6] == 1:
                self.damage(hit_wall_dmg)
            else:
                self.__pos.set_x(self.__pos.x()-1)
                self.hungry(walk_hunger)
    

    def get_mate(self):
        res = None

        for agent in self.__world.get_agents():
            if agent == self:
                continue
            if Pos.distance(self.__pos, agent.get_pos()) <= SSetting.mate_distance():
                return agent
        return res
    

    def get_sex_halt(self):
        return self.__sex_halt
    

    def set_sex_halt(self, n):
        self.__sex_halt = n

    
    def update(self) -> None:
        self.__life_span -= 1
        if self.__life_span <= 0:
            if random.random() >= (1.0 - SSetting.kill_end_lifespan_threshold()):
                self.__health = 0
                self.__hunger = 0
            else:
                self.damage(SSetting.eldery_damage())

        if self.__hunger < SSetting.unhealthy_hunger():
            self.damage(SSetting.unhealthy_hunger_damage())
        if self.__health < SSetting.good_diet_heal_health_less() and self.__hunger > SSetting.good_diet_heal_hunger_more():
            self.heal(SSetting.good_diet_heal_amount())
            self.hungry(SSetting.good_diet_heal_hunger_amount())

        
        if self.__sex_halt > 0:
            self.__sex_halt -= 1


        # Sex
        horniness = (1.0 - SSetting.sex_horny_hunger_horny()) if self.__hunger < SSetting.sex_horny_hunger() else (1.0 - SSetting.sex_horniness())
        horny = random.random() > horniness
        if horny and self.__sex_halt<=0:
            mate = self.get_mate()
            if mate and mate.get_sex_halt()<=0:
                is_gay = mate.get_sex() == self.__sex
                if not is_gay:
                    sex_min_health = SSetting.sex_min_health()
                    if self.__health > sex_min_health and mate.get_health() > sex_min_health:
                        # Make baby
                        is_healthy_parents = \
                            self.get_health() + mate.get_health() >= SSetting.sex_good_parent_health_sum() and \
                            self.get_hunger() + mate.get_hunger() >= SSetting.sex_good_parent_hunger_sum()
                        if is_healthy_parents:
                            for _ in range(SSetting.sex_good_parent_min_baby(), SSetting.sex_good_parent_max_baby()+1):
                                if random.random() <= SSetting.normal_parent_baby_dead():
                                    self.__world.trigger_event(WorldEvent.DEAD_CHILD)
                                else:
                                    self.__world.add_agent(Agent(self.__pos.copy(), self.__world))
                                    self.__world.trigger_event(WorldEvent.BIRTH)
                        else:
                            if random.random() < (1.0 - SSetting.sex_bad_parent_died_baby()):
                                self.__world.add_agent(Agent(self.__pos.copy(), self.__world))
                                self.__world.trigger_event(WorldEvent.BIRTH)
                            else:
                                self.__world.trigger_event(WorldEvent.DEAD_CHILD)

                        self.hungry(SSetting.sex_norm_hunger())
                        mate.hungry(SSetting.sex_norm_hunger())
                        
                        # Damage female
                        if self.__sex == Sex.FEMALE:
                            self.damage(SSetting.sex_female_damage())
                        elif mate.get_sex() == Sex.FEMALE:
                            mate.damage(SSetting.sex_female_damage())
                elif is_gay:
                    # Gay sex
                    # self.__world.trigger_event(WorldEvent.GAY_SEX)
                    # self.hungry(SSetting.sex_norm_hunger())
                    # mate.hungry(SSetting.sex_norm_hunger())
                    ...

                mate.set_sex_halt(SSetting.sex_halt_steps())
                self.__sex_halt = SSetting.sex_halt_steps()

            else:
                # Mastribate
                # self.__world.trigger_event(WorldEvent.SOLO_SEX)
                # self.hungry(SSetting.sex_mast_hunger())
                # self.__sex_halt = SSetting.sex_halt_steps()
                ...


        # Choose action
        eps = SSetting.eps_greed()
        dice = random.random()
        if self.__world.is_food_at(self.__pos, True):
            self.heal(SSetting.heal_after_food())
            self.eat(SSetting.eat_after_food())

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
            inx = random.uniform(0, 4)
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
        if self.__health > SSetting.max_health():
            self.__health = SSetting.max_health()
    

    def hungry(self, amount):
        self.__hunger = self.__hunger - amount
        if self.__hunger < 0:
            self.__hunger = 0
    

    def eat(self, amount) -> None:
        self.__hunger = self.__hunger + abs(amount)
        if self.__hunger > SSetting.max_hunger():
            self.__hunger = SSetting.max_hunger()
    

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
