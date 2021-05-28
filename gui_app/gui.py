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
        self.__create_start_buttons()
        self.__create_text_fields()

    def __create_canvas(self):
        self.__canvas = Canvas(self, width=self.__canvas_width, height=self.__canvas_height)
        self.__canvas.grid(row=0, column=0, columnspan=self.__world_width, rowspan=self.__canvas_height,
                           padx=10, pady=10, sticky=N+S+E+W)

    def __create_world_widgets(self):
        world_label = Label(self, text="World settings", font=('Arial', 10, 'bold underline'))
        world_label.grid(row=0, column=self.__world_width + 1, columnspan=4, pady=10)

        self.__create_width_entry()
        self.__create_height_entry()
        self.__create_obstacles_entry()

        world_bttn = Button(self, text="Generate World", command=self.__reload_world, bg=BUTTON_COLOR)
        world_bttn.grid(row=1, column=self.__world_width + 4, rowspan=2, padx=10, sticky=N+S+E+W)

        world_bttn = Button(self, text="Clear World", command=self.__clear_world, bg=BUTTON_COLOR)
        world_bttn.grid(row=3, column=self.__world_width + 4, padx=10, sticky=N+S+E+W)

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

    def __create_start_buttons(self):
        self.__start_bttn = Button(self, text="START", command=self.__start, bg=START_BUTTON_COLOR, font=('Arial', 10, 'bold'))
        self.__start_bttn.grid(row=8, column=self.__world_width + 1, columnspan=2, padx=10, pady=20, sticky=N+S+E+W)

        self.__start_learning_bttn = Button(self, text="START LEARNING", command=self.__start_learning, bg=START_BUTTON_COLOR, font=('Arial', 10, 'bold'))
        self.__start_learning_bttn.grid(row=8, column=self.__world_width + 3, columnspan=10, padx=5, pady=20, sticky=N+S+E+W)

    def __create_text_fields(self):
        self.__text_field = Text(self, width=40, height=max(self.__world_height-15, 4), wrap=WORD)
        self.__text_field.grid(row=9, column=self.__world_width + 1, pady=10, padx=10, columnspan=4, sticky=N+S+E+W)

    def __draw_world(self):
        world = self.__world.get_world_copy()
        for i, row in enumerate(world):
            for j, field in enumerate(row):
                color = self.__get_field_color(world[i][j])
                self.__canvas.create_rectangle(j * FIELD_WIDTH, i * FIELD_HEIGHT, (j + 1) * FIELD_WIDTH,
                                               (i + 1) * FIELD_HEIGHT, fill=color)

    def __lunch_agent(self):
        dx, dy = self.__agent.get_destination()
        self.__paths_history = []
        self.__iterations_history = []
        self.__statistics = {}
        self.__shortest_path_length = -1
        self.__shortest_path_coords = []
        self.__time = 0
        self.__fails_counter = 0
        is_ever_rich_destination = False

        start = time()
        while True:
            current_exploration_rate = self.__agent.get_exploration_rate()
            if current_exploration_rate < 0.01:
                optimal_path_map = self.__agent.get_optimal_path()
                optimal_path_coords = self.__agent.get_coords_history()
                self.__time = time() - start
                self.__draw_new_path(optimal_path_coords, self.__shortest_path_coords)
                self.__check_statistics()
                self.__check_diagrams()
                break

            status = self.__agent.go_to_destination()
            if status == 0:
                    self.__fails_counter += 1
                    is_ever_rich_destination = True
            if self.__fails_counter > MAX_FAILS_COUNT and not is_ever_rich_destination:
                    raise Exception("bad world")

            if self.__shortest_path_length > len(self.__agent.get_history()) or self.__shortest_path_length == -1:
                self.__check_path_drawing(self.__shortest_path_coords)
                self.__shortest_path_coords = self.__agent.get_coords_history().copy()
                self.__shortest_path_length = len(self.__shortest_path_coords)
                self.__paths_history.append(len(self.__agent.get_history()))

            self.__iterations_history.append(len(self.__agent.get_history()))

            self.__agent.learn_new_strategy()
            self.__agent.go_to_start()
            self.__world.place_destination_on_map(dx, dy)

    def __set_statistics(self):
        self.__statistics["time"] = self.__time
        self.__statistics["learning_shortest_path"] = self.__shortest_path_length
        self.__statistics["optimal_path"] = len(self.__agent.get_coords_history())
        self.__statistics["strategies_learned"] = len(self.__agent.get_strategy_bucket().get_strategies_list())
        self.__statistics["fails"] = self.__fails_counter

    def __start(self):
        self.__agent.go_to_start()
        self.__agent.clear_history()
        dest_x, dest_y = self.__agent.get_destination()
        self.__world.place_destination_on_map(dest_x, dest_y)
        self.__draw_world()
        self.__agent.set_exploration_rate(0)
        self.__lunch_agent()

    def __start_learning(self):
        self.__agent.reset()
        self.__draw_world()
        self.__lunch_agent()

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
        self.__set_text_field_data("Strategies have been cleaned")

    def __print_strategy(self):
        print("Actual strategies list:\n".upper())
        strategies = self.__agent.get_strategy_bucket().get_strategies_list()
        for strategy in strategies:
            print(self.__world.get_world_row_as_string(strategy.environment[0]))
            print(self.__world.get_world_row_as_string(strategy.environment[1]), f"=> {strategy.direction}, rating = {strategy.rating}")
            print(self.__world.get_world_row_as_string(strategy.environment[2]), "\n")

    def __check_statistics(self):
        if self.__show_statistics_cb_var.get():
            self.__set_statistics()
            self.__show_statistics()
        else:
            self.__set_text_field_data("END")

    def __set_text_field_data(self, message: str):
        self.__text_field.delete(0.0, END)
        self.__text_field.insert(0.0, message)

    def __check_diagrams(self):
        if self.__diagrams_cb_var.get():
            self.__show_diagrams()

    def __show_diagrams(self):
        self.__show_iterations_diagram()
        self.__show_paths_history_diagram()

    def __show_paths_history_diagram(self):
        fig = plt.figure()
        xs = range(len(self.__paths_history))
        plt.plot(xs, self.__paths_history)
        plt.title("Shortest path length in subsequent iterations")
        plt.xlabel("subsequent iterations")
        plt.ylabel("Shortest path length")
        plt.show()

    def __show_iterations_diagram(self):
        fig = plt.figure()
        xs = range(len(self.__iterations_history))
        plt.plot(xs, self.__iterations_history)
        plt.title("Number of iterations in successive paths")
        plt.xlabel("Number of path")
        plt.ylabel("Number of iterations")
        plt.show()

    def __clear_world(self):
        self.__agent.go_to_start()
        dx, dy = self.__agent.get_destination()
        self.__world.place_destination_on_map(dx, dy)
        self.__draw_world()

    def __show_statistics(self):
        message = "learning took " + str(self.__statistics["time"]) + "\n"
        message += "shortest learning path length = " + str(self.__statistics["learning_shortest_path"]) + "\n"
        message += "strategies learned = " + str(self.__statistics["strategies_learned"]) + "\n"
        message += "optimal path length = " + str(self.__statistics["optimal_path"]) + "\n"
        self.__set_text_field_data(message)

    def __check_path_drawing(self, prev_path_coords: list):
        if self.__path_animation_cb_var.get():
            self.__draw_new_path(self.__agent.get_coords_history(), prev_path_coords)

    def __clear_path(self, coords: list):
        for coord in set(coords):
            x, y = coord[0], coord[1]
            self.__canvas.create_rectangle(x * FIELD_WIDTH, y * FIELD_HEIGHT, (x + 1) * FIELD_WIDTH,
                                           (y + 1) * FIELD_HEIGHT, fill=EMPTY_FIELD_COLOR)

    def __draw_new_path(self, new_coords: list, prev_coords: list):
        self.__clear_path(prev_coords)
        self.__draw_path(new_coords)
        self.__draw_agent_and_destination()
        self.__canvas.update()

    def __draw_path(self, coords: list):
        for coord in set(coords):
            x, y = coord[0], coord[1]
            self.__canvas.create_rectangle(x * FIELD_WIDTH, y * FIELD_HEIGHT, (x + 1) * FIELD_WIDTH,
                                           (y + 1) * FIELD_HEIGHT, fill=PATH_COLOR)

    def __draw_agent_and_destination(self):
        self.__draw_agent()
        self.__draw_destination()

    def __draw_agent(self):
        x, y = self.__agent.get_start_position()
        self.__canvas.create_rectangle(x * FIELD_WIDTH, y * FIELD_HEIGHT, (x + 1) * FIELD_WIDTH, (y + 1) * FIELD_HEIGHT,
                                       fill=AGENT_COLOR)

    def __draw_destination(self):
        x, y = self.__agent.get_destination()
        self.__canvas.create_rectangle(x * FIELD_WIDTH, y * FIELD_HEIGHT, (x + 1) * FIELD_WIDTH, (y + 1) * FIELD_HEIGHT,
                                       fill=DESTINATION_COLOR)
