from tkinter import *
from constants.constants import *
from world.world import World
from agent.agent import Agent
from time import time
import matplotlib.pyplot as plt


class GUI(Frame):

    def __init__(self, master, world: World, agent: Agent):
        super(GUI, self).__init__(master)

        self.__world_width = world.get_width()
        self.__world_height = world.get_height()
        self.__agent = agent
        self.__world = world
        self.__master = master
        self.__canvas_width = self.__world_width * FIELD_WIDTH
        self.__canvas_height = self.__world_height * FIELD_HEIGHT
        self.__create_widgets()
        self.pack()
        self.__draw_world()

    def __create_widgets(self):
        self.__create_canvas()
        self.__create_world_widgets()
        self.__create_learning_widgets()
        self.__create_other_settings_widgets()
        self.__create_start_button()
        self.__create_text_fields()

    def __create_canvas(self):
        self.__canvas = Canvas(self, width=self.__canvas_width, height=self.__canvas_height)
        self.__canvas.grid(row=0, column=0, columnspan=self.__world_width, rowspan=self.__canvas_height,
                           padx=10, pady=10, sticky=N+S+E+W)

    def __create_empty_column(self, column: int):
        empty_label = Label(self, height=1, width=1)
        empty_label.grid(row=0, column=column)

    def __create_world_widgets(self):
        world_label = Label(self, text="World settings", font=('Arial', 10, 'bold underline'))
        world_label.grid(row=0, column=self.__world_width + 1, columnspan=4, pady=10)

        self.__create_width_entry()
        self.__create_height_entry()
        self.__create_obstacles_entry()

        world_bttn = Button(self, text="Generate World", command=self.__reload_world, bg=BUTTON_COLOR)
        world_bttn.grid(row=1, column=self.__world_width + 4, rowspan=3, padx=10, sticky=N+S+E+W)

    def __create_width_entry(self):
        width_label = Label(self, text="width", pady=2)
        width_label.grid(row=1, column=self.__world_width + 1, sticky=N+S+E+W)
        self.__width_entry = Entry(self, justify=CENTER, bd=5)
        self.__width_entry.insert(0, str(self.__world_width))
        self.__width_entry.grid(row=1, column=self.__world_width + 2, columnspan=2, sticky=N+S+E+W)

    def __create_height_entry(self):
        height_label = Label(self, text="height", pady=2)
        height_label.grid(row=2, column=self.__world_width + 1, sticky=N+S+E+W)
        self.__height_entry = Entry(self, justify=CENTER, bd=5)
        self.__height_entry.insert(0, str(self.__world_height))
        self.__height_entry.grid(row=2, column=self.__world_width + 2, columnspan=2, sticky=N+S+E+W)

    def __create_obstacles_entry(self):
        obstacles_label = Label(self, text="obstacles", pady=2)
        obstacles_label.grid(row=3, column=self.__world_width + 1, sticky=N+S+E+W)
        self.__obstacles_entry = Entry(self, justify=CENTER, bd=5)
        self.__obstacles_entry.insert(0, str(self.__world.get_obstacles_count()))
        self.__obstacles_entry.grid(row=3, column=self.__world_width + 2, columnspan=2, sticky=N+S+E+W)

    def __create_learning_widgets(self):
        world_label = Label(self, text="Strategy settings", font=('Arial', 10, 'bold underline'))
        world_label.grid(row=4, column=self.__world_width+3, columnspan=2, pady=10)

        self.__clear_strategy_bttn = Button(self, text="Clear", command=self.__clear_strategy, bg=BUTTON_COLOR)
        self.__clear_strategy_bttn.grid(row=5, column=self.__world_width+3, padx=15, pady=2, columnspan=2, sticky=N+S+E+W)

        self.__print_strategy_bttn = Button(self, text="Print", command=self.__print_strategy, bg=BUTTON_COLOR)
        self.__print_strategy_bttn.grid(row=6, column=self.__world_width+3, padx=15, pady=2, columnspan=2, sticky=N+S+E+W)

    def __create_other_settings_widgets(self):
        world_label = Label(self, text="Other settings", font=('Arial', 10, 'bold underline'))
        world_label.grid(row=4, column=self.__world_width + 1, columnspan=2, pady=10)

        self.__diagrams_cb_var = IntVar()
        self.__diagrams_cb = Checkbutton(self, text="Create diagrams", onvalue=1, offvalue=0, variable=self.__diagrams_cb_var)
        self.__diagrams_cb.grid(row=5, column=self.__world_width+1, columnspan=2, sticky=N+S+E+W)

        self.__path_animation_cb_var = IntVar()
        self.__path_animation_cb = Checkbutton(self, text="Animate paths", onvalue=1, offvalue=0, variable=self.__path_animation_cb_var)
        self.__path_animation_cb.grid(row=6, column=self.__world_width+1, columnspan=2, sticky=N+S+E+W)
        self.__path_animation_cb.select()

        self.__show_statistics_cb_var = IntVar()
        self.__show_statistics_cb = Checkbutton(self, text="Show statistics", onvalue=1, offvalue=0, variable=self.__show_statistics_cb_var)
        self.__show_statistics_cb.grid(row=7, column=self.__world_width+1, columnspan=2, sticky=N+S+E+W)
        self.__show_statistics_cb.select()

    def __create_empty_row(self, row: int):
        empty_label = Label(self, height=1)
        empty_label.grid(row=row, column=self.__world_width, columnspan=4)

    def __create_start_button(self):
        self.__start_bttn = Button(self, text="START", command=self.__lunch_agent, bg=START_BUTTON_COLOR, font=('Arial', 10, 'bold'))
        self.__start_bttn.grid(row=8, column=self.__world_width + 1, columnspan=4, padx=10, pady=20, sticky=N+S+E+W)

    def __create_text_fields(self):
        self.__text_field = Text(self, width=40, height=max(self.__world_height-15, 4), wrap=WORD)
        self.__text_field.grid(row=9, column=self.__world_width + 1, pady=10, padx=10, columnspan=4, sticky=N+S+E+W)

    def __draw_world(self):
        world = self.__world.get_world_copy()
        for i, row in enumerate(world):
            for j, field in enumerate(row):
                color = self.__get_field_color(world[i][j])
                self.__canvas.create_rectangle(j * FIELD_WIDTH, i * FIELD_HEIGHT, (j + 1) * FIELD_WIDTH,
                                               (i + 1) * FIELD_HEIGHT, fill=color, tags="area")

    def __lunch_agent(self):
        self.__agent.reset()
        start_agent_x, start_agent_y = self.__agent.get_position()
        dx, dy = self.__agent.get_destination()
        fail_counter = 0

        self.__start_bttn["state"] = DISABLED

        self.__paths_history = []
        self.__iterations_history = []
        self.__statistics = {}
        shortest_path = -1

        learning_count = 1
        start = time()
        for i in range(learning_count):
            while True:
                current_exploration_rate = self.__agent.get_exploration_rate()

                if current_exploration_rate < 0.01:
                    optimal_path, optimal_path_size = self.__agent.get_optimal_path()
                    self.print_optimal_path(optimal_path)
                    self.__statistics["time"] = time() - start
                    self.__statistics["learning_shortest_path"] = shortest_path
                    self.__statistics["optimal_path"] = optimal_path_size
                    self.__statistics["strategies_learned"] = len(self.__agent.get_strategy_bucket().get_strategies_list())
                    self.__start_bttn["state"] = ACTIVE
                    self.__check_checkbuttons()
                    break

                status = self.__agent.go_to_destination()
                if status == 0:
                    fail_counter += 1
                if status == 1:
                    fail_counter -= 9999999
                if fail_counter > 200:
                    raise Exception("bad world")

                if shortest_path > len(self.__agent.get_history()) or shortest_path == -1:
                    self.__paths_history.append(len(self.__agent.get_history()))
                    shortest_path = len(self.__agent.get_history())
                    if self.__path_animation_cb_var.get():
                        self.__draw_shortest_path()
                self.__iterations_history.append(len(self.__agent.get_history()))

                self.__agent.learn_new_strategy()
                self.__agent.set_position(start_agent_x, start_agent_y)
                self.__world.place_destination_on_map(dx, dy)


    def __get_field_color(self, field_value: int):
        if field_value == EMPTY_FIELD_COLOR:
            return EMPTY_FIELD_COLOR
        elif field_value == OBSTACLE_VALUE:
            return OBSTACLE_COLOR
        elif field_value == DESTINATION_VALUE:
            return DESTINATION_COLOR
        elif field_value == AGENT_VALUE:
            return AGENT_COLOR
        elif field_value == PATH_VALUE:
            return PATH_COLOR
        else:
            return "white"

    def print_optimal_path(self, optimal_path: list):
        world_copy = self.__world.get_world_copy()
        self.__world.set_world_array(optimal_path)
        self.__draw_world()
        self.__world.set_world_array(world_copy)

    def __clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def __reload_world(self):
        new_world_width = int(self.__width_entry.get())
        new_world_height = int(self.__height_entry.get())
        new_obstacles_count = int(self.__obstacles_entry.get())

        self.__world.set_width(new_world_width)
        self.__world.set_height(new_world_height)
        self.__world.set_obstacles_count(new_obstacles_count)
        self.__world.clear_world()
        self.__world.generate_world()
        self.__world.place_agent(self.__agent)

        self.__world_width = self.__world.get_width()
        self.__world_height = self.__world.get_height()
        self.__canvas_width = self.__world_width * FIELD_WIDTH
        self.__canvas_height = self.__world_height * FIELD_HEIGHT

        self.__clear_frame()
        self.__create_widgets()
        self.pack()
        self.__draw_world()

    def __clear_strategy(self):
        self.__agent.reset_strategy_bucket()
        self.__text_field.delete(0.0, END)
        self.__text_field.insert(0.0, "Strategies have been cleaned")

    def __print_strategy(self):
        print("Actual strategies list:\n".upper())
        strategies = self.__agent.get_strategy_bucket().get_strategies_list()
        for strategy in strategies:
            print(self.__world.get_world_row_as_string(strategy.environment[0]))
            print(self.__world.get_world_row_as_string(strategy.environment[1]), f"=> {strategy.direction}, rating = {strategy.rating}")
            print(self.__world.get_world_row_as_string(strategy.environment[2]))
            print()

    def __check_checkbuttons(self):
        if self.__show_statistics_cb_var.get():
            self.__show_statistics()
        else:
            self.__text_field.delete(0.0, END)
            self.__text_field.insert(0.0, "END")

        if self.__diagrams_cb_var.get():
            self.__show_diagrams()


    def __show_diagrams(self):
        fig = plt.figure()
        xs = range(len(self.__paths_history))
        plt.plot(xs, self.__paths_history)
        plt.title("Shortest path length in subsequent iterations")
        plt.xlabel("subsequent iterations")
        plt.ylabel("Shortest path length")
        plt.show()

        fig = plt.figure()
        xs = range(len(self.__iterations_history))
        plt.scatter(xs, self.__iterations_history)
        plt.title("Number of iterations in successive paths")
        plt.xlabel("Number of path")
        plt.ylabel("Number of iterations")
        plt.show()

    def __show_statistics(self):
        message = "learning took " + str(self.__statistics["time"]) + "\n"
        message += "shortest learning path length = " + str(self.__statistics["learning_shortest_path"]) + "\n"
        message += "strategies learned = " + str(self.__statistics["strategies_learned"]) + "\n"
        message += "optimal path length = " + str(self.__statistics["optimal_path"]) + "\n"

        self.__text_field.delete(0.0, END)
        self.__text_field.insert(0.0, message)

    def __draw_shortest_path(self):
        for y, world_row in enumerate(self.__world.get_world_copy()):
            for x, field in enumerate(world_row):
                if field == EMPTY_FIELD_VALUE:
                    self.__canvas.create_rectangle(x * FIELD_WIDTH, y * FIELD_HEIGHT, (x+1) * FIELD_WIDTH, (y+1) * FIELD_HEIGHT, fill=EMPTY_FIELD_COLOR)

        for i, coord in enumerate(self.__agent.get_coords_history()):
            x, y = coord[0], coord[1]
            self.__canvas.create_rectangle(x * FIELD_WIDTH, y * FIELD_HEIGHT, (x+1) * FIELD_WIDTH, (y+1) * FIELD_HEIGHT, fill=PATH_COLOR)

        x, y = self.__agent.get_destination()
        self.__canvas.create_rectangle(x*FIELD_WIDTH, y*FIELD_HEIGHT, (x+1)*FIELD_WIDTH, (y+1)*FIELD_HEIGHT, fill=DESTINATION_COLOR)
        x, y = self.__agent.get_start_position()
        self.__canvas.create_rectangle(x * FIELD_WIDTH, y * FIELD_HEIGHT, (x + 1) * FIELD_WIDTH, (y + 1) * FIELD_HEIGHT, fill=AGENT_COLOR)
        self.__canvas.update()
