from world.world import World
from agent.agent import Agent
from gui_app.application import Application


def main2():
    world_height, world_width = 15, 15
    world = World(world_width, world_height)
    agent = Agent(world)
    world.place_agent(agent)

    app = Application(world, agent)
    app.start()


if __name__ == '__main__':
    main2()
