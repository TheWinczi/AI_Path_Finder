from tkinter import *
from constants.constants import *
from world.world import World
from agent.agent import Agent


class GUI(Frame):

    def __init__(self, master, world: World, agent: Agent):
        super(GUI, self).__init__(master)

        self.__world_width = world.get_width()
        self.__world_height = world.get_height()
        self.__agent = agent
        self.__world = world
        self.__master = master
        self.__canvas_width = self.__world_width * FIELD_WIDTH + 1
        self.__canvas_height = self.__world_height * FIELD_HEIGHT + 1

        self.__create_widgets()
        self.pack()
        self.__draw_world()

    def __create_widgets(self):
        self.__create_canvas()
        self.__create_empty_column(self.__world_width)
        self.__create_world_widgets()
        self.__create_empty_row(4)
        self.__create_buttons()
        self.__create_empty_row(6)
        self.__create_text_fields()
        self.__create_empty_column(self.__world_width + 5)
        self.__create_empty_row(self.__world_height)

    def __create_canvas(self):
        self.__canvas = Canvas(self, width=self.__canvas_width, height=self.__canvas_height, bg="black")
        self.__canvas.grid(row=0, column=0, columnspan=self.__world_width, rowspan=self.__canvas_height,
                           sticky=N + S + E + W)

    def __create_empty_column(self, column: int):
        empty_label = Label(self, height=1, width=1)
        empty_label.grid(row=0, column=column)

    def __create_world_widgets(self):
        world_label = Label(self, text="Choose what size world has to have")
        world_label.grid(row=0, column=self.__world_width + 1, columnspan=4)

        width_label = Label(self, text="Width")
        width_label.grid(row=1, column=self.__world_width + 1, columnspan=2, sticky=N+S+E+W)
        self.__width_entry = Entry(self, justify=CENTER)
        self.__width_entry.insert(0, str(self.__world_width))
        self.__width_entry.grid(row=2, column=self.__world_width + 1, columnspan=2, sticky=N+S+E+W)

        height_label = Label(self, text="Height")
        height_label.grid(row=1, column=self.__world_width + 3, columnspan=2, sticky=N+S+E+W)
        self.__height_entry = Entry(self, justify=CENTER)
        self.__height_entry.insert(0, str(self.__world_height))
        self.__height_entry.grid(row=2, column=self.__world_width + 3, columnspan=2, sticky=N+S+E+W)

        world_bttn = Button(self, text="Generate World", command=self.__reload_world)
        world_bttn.grid(row=3, column=self.__world_width + 2, columnspan=2, sticky=N+S+E+W)

    def __create_empty_row(self, row: int):
        empty_label = Label(self, height=1)
        empty_label.grid(row=row, column=self.__world_width, columnspan=4)

    def __create_buttons(self):
        start_bttn = Button(self, text="START", command=self.__lunch_agent)
        start_bttn.grid(row=5, column=self.__world_width + 2, columnspan=2, sticky=N+S+E+W)

    def __create_text_fields(self):
        text_field = Text(self, width=30, height=self.__world_height - 8)
        text_field.grid(row=7, column=self.__world_width + 1, columnspan=4)

    def __draw_world(self):
        world = self.__world.get_world_copy()
        for i, row in enumerate(world):
            for j, field in enumerate(row):
                color = self.__get_field_color(world[i][j])
                self.__canvas.create_rectangle(j * FIELD_WIDTH, i * FIELD_HEIGHT, (j + 1) * FIELD_WIDTH,
                                               (i + 1) * FIELD_HEIGHT, fill=color, tags="area")

    def __lunch_agent(self):
        start_agent_x, start_agent_y = self.__agent.get_position()
        dx, dy = self.__agent.get_destination()
        fail_counter = 0

        learning_count = 1
        for i in range(learning_count):
            while True:
                current_exploration_rate = self.__agent.get_exploration_rate()

                if current_exploration_rate < 0.01:
                    optimal_path, path_size = self.__agent.get_optimal_path()
                    self.print_optimal_path(optimal_path, path_size)
                    self.__agent.reset()
                    break

                status = self.__agent.go_to_destination()
                if status == 0:
                    fail_counter += 1
                if status == 1:
                    fail_counter -= 9999999
                if fail_counter > 100:
                    raise Exception("bad world")

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

    def print_optimal_path(self, optimal_path: list, path_length: int):
        self.__world.set_world_array(optimal_path)
        self.__draw_world()

    def __clear_canvas(self):
        self.__canvas.delete("all")

    def clear_frame(self):
        for widgets in self.__master.winfo_children():
            widgets.destroy()

    def __reload_world(self):
        new_world_width = int(self.__width_entry.get())
        new_world_height = int(self.__height_entry.get())
        self.pack_forget()
        self.grid_forget()
        agent = self.__world.get_agent()
        self.__world = World(new_world_width, new_world_height)
        self.__world.place_agent(agent)

        self.__world_width = self.__world.get_width()
        self.__world_height = self.__world.get_height()
        self.__canvas_width = self.__world_width * FIELD_WIDTH + 1
        self.__canvas_height = self.__world_height * FIELD_HEIGHT + 1

        self.__create_widgets()
        self.pack()
        self.__draw_world()
