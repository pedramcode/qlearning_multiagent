import math
import os
import toml
from enum import Enum


class WorldEvent(Enum):
    DEAD_CHILD = 0
    BIRTH = 1
    TOTAL_DEAD = 2


class Size():
    """
        General model for size (width, height)
    """

    __width = 0
    __height = 0

    def __init__(self, width, height):
        """
            Initialize size model
        """
        self.__width = width
        self.__height = height

    def width(self):
        """
            Get width
        """
        return self.__width
    
    def height(self):
        """
            Get height
        """
        return self.__height
    
    def set_width(self, width):
        """
            Set width
        """
        self.__width = width
    
    def set_height(self, width):
        """
            Set height
        """
        self.__width = width


class Pos(object):
    """
        General model for pos (width, height)
    """

    __x = 0
    __y = 0

    def __init__(self, _x, _y):
        """
            Initialize pos model
        """
        self.__x = _x
        self.__y = _y
    
    @staticmethod
    def from_list(lst):
        return Pos(lst[0], lst[1])
    

    @staticmethod
    def distance(pos1, pos2) -> int:
        dist = math.floor(math.sqrt(math.pow(pos1.x() - pos2.x(), 2) + math.pow(pos1.y() - pos2.y(), 2)))
        return dist

    def x(self):
        """
            Get x
        """
        return self.__x

    def copy(self):
        return Pos(self.__x, self.__y)
    
    def y(self):
        """
            Get y
        """
        return self.__y
    
    def set_x(self, _x):
        """
            Set x
        """
        self.__x = _x
    
    def set_y(self, _y):
        """
            Set y
        """
        self.__y = _y
    
    def __str__(self):
        return f"({self.__x}, {self.__y})"


class SSetting:
    @staticmethod
    def load_data():
        setting_data = None
        with open("./src/god.toml", "r") as file:
            setting_data = toml.load(file)
        return setting_data

    @staticmethod
    def http_port():
        dt = SSetting.load_data()
        return int(dt["http"].get("HTTP_PORT", "8080"))

    @staticmethod
    def http_host():
        dt = SSetting.load_data()
        return dt["http"].get("HTTP_HOST", "127.0.0.1")
    

    @staticmethod
    def eps_greed():
        dt = SSetting.load_data()
        return float(dt["ai"].get("EPS_GREED", "0.2"))


    @staticmethod
    def max_health():
        dt = SSetting.load_data()
        return float(dt["env"].get("MAX_HEALTH", "100"))

    @staticmethod
    def max_hunger():
        dt = SSetting.load_data()
        return float(dt["env"].get("MAX_HUNGER", "100"))
    
    @staticmethod
    def min_life_span_random():
        dt = SSetting.load_data()
        return float(dt["env"].get("MIN_LIFESPAN_RND", "15"))
    
    @staticmethod
    def max_life_span_random():
        dt = SSetting.load_data()
        return float(dt["env"].get("MAX_LIFESPAN_RND", "100"))
    
    @staticmethod
    def male_gender_probability():
        dt = SSetting.load_data()
        return float(dt["env"].get("MALE_GENDER_PROB", "0.5"))
    
    @staticmethod
    def hit_wall_damage():
        dt = SSetting.load_data()
        return float(dt["env"].get("HIT_WALL_DAMAGE", "1"))
    
    @staticmethod
    def walking_hunger():
        dt = SSetting.load_data()
        return float(dt["env"].get("WALKING_HUNGER", "1"))
    
    @staticmethod
    def mate_distance():
        dt = SSetting.load_data()
        return float(dt["env"].get("MATE_DISTANCE", "2"))
    
    @staticmethod
    def kill_end_lifespan_threshold():
        dt = SSetting.load_data()
        return float(dt["env"].get("KILL_END_LIFE_THRESH", "0.1"))
    
    @staticmethod
    def eldery_damage():
        dt = SSetting.load_data()
        return float(dt["env"].get("ELD_DAMAGE", "1"))
    
    @staticmethod
    def unhealthy_hunger():
        dt = SSetting.load_data()
        return float(dt["env"].get("UNHEALTHY_HUNGER", "30"))
    
    @staticmethod
    def unhealthy_hunger_damage():
        dt = SSetting.load_data()
        return float(dt["env"].get("UNHEALTHY_HUNGER_DAMAGE", "0.1"))
    
    @staticmethod
    def good_diet_heal_health_less():
        dt = SSetting.load_data()
        return float(dt["env"].get("GOOD_DIET_HEAL_HEALTH_LESS", "90"))
    
    @staticmethod
    def good_diet_heal_hunger_more():
        dt = SSetting.load_data()
        return float(dt["env"].get("GOOD_DIET_HEAL_HUNGER_MORE", "90"))
    
    @staticmethod
    def good_diet_heal_amount():
        dt = SSetting.load_data()
        return float(dt["env"].get("GOOD_DIET_HEAL_AMOUNT", "5"))
    
    @staticmethod
    def good_diet_heal_hunger_amount():
        dt = SSetting.load_data()
        return float(dt["env"].get("GOOD_DIET_HEAL_HUNGRY_AMOUNT", "5"))
    
    @staticmethod
    def sex_horny_hunger():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_HORNY_HUNGER", "30"))
    
    @staticmethod
    def sex_horny_hunger_horny():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_HORNY_HUNGER_HORNY", "0.7"))
    
    @staticmethod
    def sex_horniness():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_HORNINESS", "0.5"))
    
    @staticmethod
    def sex_min_health():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_MIN_HEALTH", "60"))
    
    @staticmethod
    def sex_norm_hunger():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_NORM_HUNGRY", "2"))
    
    @staticmethod
    def sex_female_damage():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_FEMALE_DAMAGE", "3"))
    
    @staticmethod
    def sex_mast_hunger():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_MASTR_HUNGER", "2"))
    
    @staticmethod
    def sex_halt_steps():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_HALT_STEPS", "5"))

    @staticmethod
    def sex_good_parent_health_sum():
        dt = SSetting.load_data()
        return int(dt["sex"].get("SEX_PARENT_HEALTH_SUM", "90"))
    
    @staticmethod
    def sex_good_parent_hunger_sum():
        dt = SSetting.load_data()
        return int(dt["sex"].get("SEX_PARENT_HUNGER_SUM", "90"))
    
    @staticmethod
    def sex_good_parent_min_baby():
        dt = SSetting.load_data()
        return int(dt["sex"].get("SEX_PARENT_HEALTHY_BABY_MIN", "1"))
    
    @staticmethod
    def sex_good_parent_max_baby():
        dt = SSetting.load_data()
        return int(dt["sex"].get("SEX_PARENT_HEALTHY_BABY_MAX", "3"))
    
    @staticmethod
    def sex_bad_parent_died_baby():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_PARENT_UNHEALTHY_DIED_BABY", "3"))
    
    @staticmethod
    def min_vision():
        dt = SSetting.load_data()
        return float(dt["env"].get("MIN_VISION", "1"))
    
    @staticmethod
    def max_vision():
        dt = SSetting.load_data()
        return float(dt["env"].get("MAX_VISION", "10"))
    
    @staticmethod
    def heal_after_food():
        dt = SSetting.load_data()
        return float(dt["env"].get("HEAL_AFTER_EAT", "5"))
    
    @staticmethod
    def eat_after_food():
        dt = SSetting.load_data()
        return float(dt["env"].get("HUNGER_AFTER_FOOD", "5"))
    
    @staticmethod
    def init_pop():
        dt = SSetting.load_data()
        return int(dt["env"].get("INIT_POPULATION", "10"))

    @staticmethod
    def food_gen():
        dt = SSetting.load_data()
        return float(dt["env"].get("FOOD_GENERATE", "0.5"))
    
    @staticmethod
    def food_min():
        dt = SSetting.load_data()
        return int(dt["env"].get("FOOD_MIN", "1"))

    @staticmethod
    def food_max():
        dt = SSetting.load_data()
        return int(dt["env"].get("FOOD_MAX", "3"))
    
    @staticmethod
    def normal_parent_baby_dead():
        dt = SSetting.load_data()
        return float(dt["sex"].get("SEX_NORMAL_BABY_DEAD", "0.1"))