from p5 import *
from world import World
from agent import Agent
from utils import Pos
import random

world = None

def setup():
    global world
    world = World("./data/maps/map2.json")
    
    for i in range(0, 10):
        world.add_food(world.get_free_pos())

    for i in range(0, 10):
        agent_x = Agent(world.get_free_pos(), world)
        world.add_agent(agent_x)

def draw():
    global world

    for i in range(0, 10):
        world.update()
        print("Step: ", i)
    world.render()

if __name__ == "__main__":
    run()
