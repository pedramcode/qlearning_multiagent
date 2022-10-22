import math


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