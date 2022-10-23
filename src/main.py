from world import World
from agent import Agent
from utils import Pos
import random
from flask import Flask, send_from_directory
import threading

app = Flask(__name__)


world = None

world = World("./data/maps/map2.json")

for i in range(0, 50):
    world.add_food(world.get_free_pos())

for i in range(0, 30):
    agent_x = Agent(world.get_free_pos(), world)
    world.add_agent(agent_x)

def world_runner():
    global world
    while 1:
        world.update()

@app.route("/data")
def data():
    data = world.get_state()
    steps = [d["step"] for d in data]
    pop = [d["pop"] for d in data]
    pop_health = [d["pop_health"] for d in data]
    pop_hunger = [d["pop_hunger"] for d in data]
    food_count = [d["food_count"] for d in data]
    return {"steps":steps, "pop":pop, "pop_health": pop_health, "pop_hunger":pop_hunger, "food_count":food_count}

@app.route("/")
def index():
    return send_from_directory("./html", "index.html")

def server():
    app.run("127.0.0.1", 8080)

if __name__ == "__main__":
    th_server = threading.Thread(target=server)
    th_world = threading.Thread(target=world_runner)
    th_server.start()
    th_world.start()
    th_server.join()
    th_world.join()
