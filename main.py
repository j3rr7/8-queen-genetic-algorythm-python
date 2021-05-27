from dearpygui.core import *
from dearpygui.simple import *
import threading
from .Solver import *

# DPG COUNTER FOR TABLE
frame_target = 4
frame_counter = 0

#list_thread = []
list_queens = []
list_solver = []
best_solution_found = False
custom_click_table = False
custom_click_table_data = []
coords_queen = [
    [[40, 40], [100, 40], [160, 40], [220, 40], [280, 40], [340, 40], [400, 40], [460, 40]],
    [[40, 100], [100, 100], [160, 100], [220, 100], [280, 100], [340, 100], [400, 100], [460, 100]],
    [[40, 160], [100, 160], [160, 160],[220, 160], [280, 160], [340, 160], [400, 160], [460, 160]],
    [[40, 220], [100, 220], [160, 220], [220, 220],[280, 220], [340, 220], [400, 220], [460, 220]],
    [[40, 280], [100, 280], [160, 280], [220, 280], [280, 280],[340, 280], [400, 280], [460, 280]],
    [[40, 340], [100, 340], [160, 340], [220, 340], [280, 340], [340, 340],[400, 340], [460, 340]],
    [[40, 400], [100, 400], [160, 400], [220, 400], [280, 400], [340, 400], [400, 400],[460, 400]],
    [[40, 460], [100, 460], [160, 460], [220, 460], [280, 460], [340, 460], [400, 460], [460, 460]]
]


def thread_2():
    pass


def thread_1(pop_: int, gen_: int, cros_: float, mut_: float):
    global list_queens, list_solver, best_solution_found

    # generate random
    init_array = GeneticAlgorythm.generate_random_data(pop_)
    init_fitness = [GeneticAlgorythm.calculate_fitness(array) for array in init_array]
    #log_debug(f"Size of init_array = {len(init_array)}")

    for index, array in enumerate(init_array):
        list_queens.append(QUEEN(array, init_fitness[index]))
    #log_debug(f"Size of list_queens = {len(list_queens)}")

    tmp_solver = GeneticAlgorythm.run_genetic_algorithm(list_queens, gen_, cros_, mut_, False)
    tmp_solver.sort(key=lambda x: x.fitness, reverse=True)
    list_solver = tmp_solver
    #log_debug(f"Size of list_solver = {len(list_solver)}")
    best_solution_found = True

    #y = threading.Thread(target=thread_2, args=(), daemon=True)
    #y.start()
    #y.join()


def on_window_close(sender, data):
    delete_item(sender)
    # log_debug("window was deleted")


def start_(sender, data):
    global list_queens, best_solution_found, custom_click_table
    custom_click_table = False
    best_solution_found = False
    list_queens.clear()

    population = get_value("Population")
    generation = get_value("Generation")
    cross_prob = get_value("Crossover Probability")
    mut_prob = get_value("Mutation Probability")
    run_thread = threading.Thread(target=thread_1, args=(population, generation, cross_prob, mut_prob,), daemon=False)
    #list_thread.append(run_thread)
    run_thread.start()


def show_settings(sender, data):
    if does_item_exist("Settings"):
        # log_debug("window already exists")
        pass
    else:
        with window("Settings", on_close=on_window_close, width=600, height=150, no_collapse=False, no_resize=True):
            add_input_int("Population", min_value=1, max_value=1000000, tip="population", default_value=1)
            add_input_int("Generation", min_value=1, max_value=1000000, tip="generation", default_value=1)
            add_slider_float("Crossover Probability", min_value=0.0, max_value=1.0, clamped=True,
                             tip="Ctrl + click to edit")
            add_slider_float("Mutation Probability", min_value=0.0, max_value=1.0, clamped=True,
                             tip="Ctrl + click to edit")
            add_dummy(height=3)
            add_button("Run", width=150, callback=start_)


def click_logger_(sender, data):
    global custom_click_table, custom_click_table_data
    coord_list = get_table_selections("table_logger")
    #log_debug(f"Selected Cells (coordinates): {coord_list}")
    #data = []
    for coordinates in coord_list:
        #data.append(get_table_item("table_logger", coordinates[0], coordinates[1]))
        if coordinates[1] != 1:
            custom_click_table = True
            data = get_table_item("table_logger", coordinates[0], coordinates[1])
            # convert string to list
            import ast
            data = ast.literal_eval(data)
            custom_click_table_data = data
    #log_info(data)


def callback_renderer():
    global frame_counter, frame_target, list_solver, custom_click_table, custom_click_table_data
    if frame_counter == frame_target:
        clear_table("table_logger")
        for i in list_solver:
            add_row("table_logger", [i.arrays, i.fitness])
        clear_drawing("canvas")
        draw_image("canvas", "chessboard.png", [0, 0], pmax=[500, 500])
        if len(list_solver) > 0 and not custom_click_table:
            for index, value in enumerate(list_solver[0].arrays):
                draw_circle("canvas", coords_queen[value][index], 15, [255, 0, 255, 255], fill=[255, 100, 0],
                            tag=f"circle{index}##dynamic{value}")
                # draw_circle("canvas", coords_queen[index][value], 15, [255, 0, 255, 255], fill=[255, 100, 0],
                #             tag=f"circle{index}##dynamic{value}")
        if custom_click_table:
            for index, value in enumerate(custom_click_table_data):
                draw_circle("canvas", coords_queen[value][index], 15, [255, 0, 255, 255], fill=[255, 100, 0],
                            tag=f"circle{index}##dynamic{value}")
        frame_counter = 0
    else:
        frame_counter += 1


with window("Main Chess Board"):
    with menu_bar("##top_menu"):
        with menu("Views"):
            add_menu_item("Show Logger", callback=show_logger)
            add_menu_item("Show Settings", callback=show_settings)
    clear_drawing("canvas")
    add_drawing("canvas", width=500, height=500)
    #draw_image("canvas", "chessboard.png", [0, 0], pmax=[500, 500])
    #draw_circle("canvas", coords_queen[0][7], 15, [255, 0, 255, 255], fill=[255, 100, 0], tag=f"circle{0}##dynamic{0}")
    add_same_line()
    with group("##group1"):
        with child("##child", width=450, height=500):
            add_text("Logger Place")
            add_separator()
            add_table("table_logger", ["Arrays", "Fitness"], height=450, callback=click_logger_)

# Main script
if __name__ == '__main__':
    set_main_window_title("8 Queen Chessboard")
    set_theme("Red")
    set_primary_window("Main Chess Board", True)
    set_main_window_size(1000, 600)
    set_main_window_resizable(False)
    set_render_callback(callback_renderer)
    start_dearpygui()
