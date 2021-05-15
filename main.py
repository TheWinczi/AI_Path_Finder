from world.world import World
from agent.agent import Agent


def main():
    world_height, world_width = 20, 20
    world = World(world_width, world_height)
    agent = Agent(world)
    world.place_agent(agent)

    start_agent_x, start_agent_y = agent.get_position()
    while True:
        print(world)
        agent.go_to_destination()
        agent.learn_new_strategy()
        print(world)
        print(agent.get_strategy_bucket())
        input("Press enter:")

        agent.set_position(start_agent_x, start_agent_y)


if __name__ == '__main__':
    main()
