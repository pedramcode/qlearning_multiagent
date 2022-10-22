from utils import Size


class WorldSettings(object):
    """
        World settings
    """

    __name: str = None
    __size: Size = None
    __grid: Size = None


    def __init__(self, name: str, world_width: int, world_height: int, world_grid_width: int, world_grid_height: int):
        self.__name = name
        self.__size = Size(world_width, world_height)
        self.__grid = Size(world_grid_width, world_grid_height)

    def get_size(self) -> Size:
        return self.__size
    
    def get_grid(self) -> Size:
        return self.__grid
    
    def __str__(self):
        return self.__name