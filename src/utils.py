import math
import os


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
        self.__width = height


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
    def http_port():
        return int(os.environ.get("HTTP_PORT", "8080"))

    @staticmethod
    def http_host():
        return os.environ.get("HTTP_HOST", "127.0.0.1")

    @staticmethod
    def max_health():
        return float(os.environ.get("MAX_HEALTH", "100"))

    @staticmethod
    def max_hunger():
        return float(os.environ.get("MAX_HUNGER", "100"))
    
    @staticmethod
    def min_life_span_random():
        return float(os.environ.get("MIN_LIFESPAN_RND", "15"))
    
    @staticmethod
    def max_life_span_random():
        return float(os.environ.get("MAX_LIFESPAN_RND", "100"))
    
    @staticmethod
    def male_gender_probability():
        return float(os.environ.get("MALE_GENDER_PROB", "0.5"))
    
    @staticmethod
    def hit_wall_damage():
        return float(os.environ.get("HIT_WALL_DAMAGE", "1"))
    
    @staticmethod
    def walking_hunger():
        return float(os.environ.get("WALKING_HUNGER", "1"))
    
    @staticmethod
    def mate_distance():
        return float(os.environ.get("MATE_DISTANCE", "2"))
    
    @staticmethod
    def kill_end_lifespan_threshold():
        return float(os.environ.get("KILL_END_LIFE_THRESH", "0.1"))
    
    @staticmethod
    def eldery_damage():
        return float(os.environ.get("ELD_DAMAGE", "1"))
    
    @staticmethod
    def unhealthy_hunger():
        return float(os.environ.get("UNHEALTHY_HUNGER", "30"))
    
    @staticmethod
    def unhealthy_hunger_damage():
        return float(os.environ.get("UNHEALTHY_HUNGER_DAMAGE", "0.1"))
    
    @staticmethod
    def good_diet_heal_health_less():
        return float(os.environ.get("GOOD_DIET_HEAL_HEALTH_LESS", "90"))
    
    @staticmethod
    def good_diet_heal_hunger_more():
        return float(os.environ.get("GOOD_DIET_HEAL_HUNGER_MORE", "90"))
    
    @staticmethod
    def good_diet_heal_amount():
        return float(os.environ.get("GOOD_DIET_HEAL_AMOUNT", "5"))
    
    @staticmethod
    def good_diet_heal_hunger_amount():
        return float(os.environ.get("GOOD_DIET_HEAL_HUNGRY_AMOUNT", "5"))
    
    @staticmethod
    def sex_horny_hunger():
        return float(os.environ.get("SEX_HORNY_HUNGER", "30"))
    
    @staticmethod
    def sex_horny_hunger_horny():
        return float(os.environ.get("SEX_HORNY_HUNGER_HORNY", "0.7"))
    
    @staticmethod
    def sex_horniness():
        return float(os.environ.get("SEX_HORNINESS", "0.5"))
    
    @staticmethod
    def sex_min_health():
        return float(os.environ.get("SEX_MIN_HEALTH", "60"))
    
    @staticmethod
    def sex_norm_hunger():
        return float(os.environ.get("SEX_NORM_HUNGRY", "2"))
    
    @staticmethod
    def sex_female_damage():
        return float(os.environ.get("SEX_FEMALE_DAMAGE", "3"))
    
    @staticmethod
    def sex_mast_hunger():
        return float(os.environ.get("SEX_MASTR_HUNGER", "2"))
    
    @staticmethod
    def sex_halt_steps():
        return float(os.environ.get("SEX_HALT_STEPS", "5"))

    @staticmethod
    def sex_good_parent_health_sum():
        return int(os.environ.get("SEX_PARENT_HEALTH_SUM", "90"))
    
    @staticmethod
    def sex_good_parent_hunger_sum():
        return int(os.environ.get("SEX_PARENT_HUNGER_SUM", "90"))
    
    @staticmethod
    def sex_good_parent_min_baby():
        return int(os.environ.get("SEX_PARENT_HEALTHY_BABY_MIN", "1"))
    
    @staticmethod
    def sex_good_parent_max_baby():
        return int(os.environ.get("SEX_PARENT_HEALTHY_BABY_MAX", "3"))
    
    @staticmethod
    def sex_bad_parent_died_baby():
        return float(os.environ.get("SEX_PARENT_UNHEALTHY_DIED_BABY", "3"))
    
    @staticmethod
    def eps_greed():
        return float(os.environ.get("EPS_GREED", "0.2"))
    
    @staticmethod
    def min_vision():
        return float(os.environ.get("MIN_VISION", "1"))
    
    @staticmethod
    def max_vision():
        return float(os.environ.get("MAX_VISION", "10"))
    
    @staticmethod
    def heal_after_food():
        return float(os.environ.get("HEAL_AFTER_EAT", "5"))
    
    @staticmethod
    def eat_after_food():
        return float(os.environ.get("HUNGER_AFTER_FOOD", "5"))
    
    @staticmethod
    def init_pop():
        return int(os.environ.get("INIT_POPULATION", "10"))

    @staticmethod
    def food_gen():
        return float(os.environ.get("FOOD_GENERATE", "0.5"))
    
    @staticmethod
    def food_min():
        return int(os.environ.get("FOOD_MIN", "1"))

    @staticmethod
    def food_max():
        return int(os.environ.get("FOOD_MAX", "3"))