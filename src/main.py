from world import World
from agent import Agent
from utils import Pos, SSetting
import random
from flask import Flask, send_from_directory
import threading



app = Flask(__name__)


world = None

world = World("./data/maps/map2.json")

for i in range(0, 50):
    world.add_food(world.get_free_pos())

def world_runner():
    global world
    while 1:
        world.update()
        if world.terminated():
            world.reset()

@app.route("/data")
def data():
    data = world.get_state()[-30:]
    steps = [d["step"] for d in data]
    pop = [d["pop"] for d in data]
    pop_health = [d["pop_health"] for d in data]
    pop_hunger = [d["pop_hunger"] for d in data]
    food_count = [d["food_count"] for d in data]
    male_count = [d["male_count"] for d in data]
    female_count = [d["female_count"] for d in data]
    dead_born = [d["dead_born"] for d in data]
    total_dead = [d["total_dead"] for d in data]
    birth = [d["birth"] for d in data]
    res = {
        "steps":steps, 
        "pop":pop, 
        "pop_health": pop_health, 
        "pop_hunger":pop_hunger, 
        "food_count":food_count,
        "male_count":male_count,
        "female_count":female_count,
        "dead_born":dead_born,
        "total_dead":total_dead,
        "birth":birth,
        }
    return res

@app.route("/")
def index():
    return send_from_directory("./html", "index.html")

def server():
    app.run(SSetting.http_host(), SSetting.http_port())

if __name__ == "__main__":
    th_world = threading.Thread(target=world_runner)
    th_server = threading.Thread(target=server)
    th_world.start()
    th_server.start()
    th_world.join()
    th_server.join()
