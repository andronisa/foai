import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from sys import stdout
from solver import Solver


def print_search_result(result):
    moves_count = result.moves_count
    if result.is_successful:
        outcome = "Successful"
    else:
        if moves_count > 900000:
            outcome = "Unsuccesful - Infinite loop"
        else:
            outcome = "Unsuccesful"

    outputs = [
        ("     Result", outcome),
        ("     Total time", result.total_time),
        ("     Total moves number to goal", "{} moves".format(moves_count)),
        ("     Total iterations", result.total_iters),
        ("     Queue size at the end", result.queue_size)
    ]

    print("")

    for output in outputs:
        output_key = output[0]
        output_value = output[1]

        print(output_key + " - " + str(output_value))
    print("")


def get_seconds(total_time):
    time = total_time
    time_arr = str(time).split(":")
    minutes = time_arr[1][1]
    seconds_array = time_arr[2].split(".")
    seconds = seconds_array[0][1] if seconds_array[0][0] == 0 else seconds_array[0]
    seconds += "." + seconds_array[1][0]

    total_seconds = float(minutes) * 60 + float(str(seconds))

    return total_seconds


def bar_plot(result, title):
    OX = [
        'MinMax',
        'Alpha Beta',
        'Tie'
    ]

    mm = result['mm_wins']
    ab = result['ab_wins']
    ties = result['ties']

    OY = [mm, ab, ties]

    fig = plt.figure()

    width = .20
    ind = np.arange(len(OY))
    barlist = plt.bar(ind, OY, align='center')
    plt.xticks(ind + width / 2, OX)

    barlist[0].set_color('r')
    barlist[1].set_color('b')
    barlist[2].set_color('g')
    plt.legend((barlist[0], barlist[1], barlist[2]),
               ('MinMax Wins: ' + str(mm), 'AlphaBeta Wins: ' + str(ab), 'Ties: ' + str(ties)))

    plt.xlabel('Result')
    plt.ylabel('Wins Count')
    plt.title(title)
    plt.show()


def plot_times(result, limit=None, title=None):
    bfs = result['bfs']
    id_dfs = result['id_dfs']
    a_star = result['a_star']

    bfs_average = sum(bfs) / len(bfs)
    id_dfs_average = sum(id_dfs) / len(id_dfs)
    a_star_average = sum(a_star) / len(a_star)

    lines = plt.plot(bfs, 'xr-', id_dfs, 'xb-', a_star, 'xg-', linewidth=3)

    plt.legend((lines[0], lines[1], lines[2]),
               ('BFS: ' + str(bfs_average) + " seconds",
                'IDDFS: ' + str(id_dfs_average) + " seconds",
                'A*: ' + str(a_star_average) + " seconds"),
               loc=1)

    plt.xlabel('Time(seconds)')
    plt.ylabel('Times tried')
    if title:
        plt.title(title)

    if limit:
        x1, x2, y1, y2 = plt.axis()

        plt.axis((x1, x2, 0, limit))

    plt.show()


def plot_iterations(result, limit=None, title=None):
    bfs = result['bfs']
    id_dfs = result['id_dfs']
    a_star = result['a_star']

    bfs_average = sum(bfs) / len(bfs)
    id_dfs_average = sum(id_dfs) / len(id_dfs)
    a_star_average = sum(a_star) / len(a_star)

    lines = plt.plot(bfs, 'xr-', id_dfs, 'xb-', a_star, 'xg-', linewidth=3)

    plt.legend((lines[0], lines[1], lines[2]),
               ('BFS: ' + str(bfs_average) + " iterations",
                'IDDFS: ' + str(id_dfs_average) + " iterations",
                'A*: ' + str(a_star_average) + " iterations"),
               loc=1)

    plt.xlabel('Iterations')
    plt.ylabel('Times tried')
    if title:
        plt.title(title)

    if limit:
        x1, x2, y1, y2 = plt.axis()

        plt.axis((x1, x2, 0, limit))

    plt.show()


def plot_queue_sizes(result, limit=None, title=None):
    bfs = result['bfs']
    id_dfs = result['id_dfs']
    a_star = result['a_star']

    bfs_average = sum(bfs) / len(bfs)
    id_dfs_average = sum(id_dfs) / len(id_dfs)
    a_star_average = sum(a_star) / len(a_star)

    lines = plt.plot(bfs, 'xr-', id_dfs, 'xb-', a_star, 'xg-', linewidth=3)

    plt.legend((lines[0], lines[1], lines[2]),
               ('Avg BFS queue: ' + str(bfs_average),
                'Avg IDDFS queue: ' + str(id_dfs_average),
                'Avg A* queue: ' + str(a_star_average)),
               loc=1)

    plt.xlabel('Time(seconds)')
    plt.ylabel('Times tried')
    if title:
        plt.title(title)

    if limit:
        x1, x2, y1, y2 = plt.axis()

        plt.axis((x1, x2, 0, limit))

    plt.show()


def plot_moves(result, limit=None, title=None):
    OX = [
        'BFS',
        'IDDFS',
        'Tie'
    ]

    bfs = result['bfs']
    id_dfs = result['id_dfs']
    a_star = result['a_star']

    bfs_average = sum(bfs) / len(bfs)
    id_dfs_average = sum(id_dfs) / len(id_dfs)
    a_star_average = sum(a_star) / len(a_star)

    OY = [bfs_average, id_dfs_average, a_star_average]

    fig = plt.figure()

    width = .20
    ind = np.arange(len(OY))
    barlist = plt.bar(ind, OY, align='center')
    plt.xticks(ind + width / 2, OX)

    barlist[0].set_color('r')
    barlist[1].set_color('b')
    barlist[2].set_color('g')
    plt.legend((barlist[0], barlist[1], barlist[2]),
               ('Avg BFS moves: ' + str(bfs_average),
                'Avg IDDFS moves: ' + str(id_dfs_average),
                'Avg A* moves: ' + str(a_star_average)))

    plt.xlabel('Algorithm')
    plt.ylabel('Moves')
    plt.title(title)
    plt.show()


def solve_blocksword_puzzle():
    solver = Solver()

    algorithms = [
        ('bfs', 'BFS'),
        # ('dfs', 'DFS'),
        ('id_dfs', 'Iterative Deepening DFS'),
        ('a_star', 'A* (Heuristic: Sum of Manhattan distances)'),
    ]

    total_results = {
        'bfs': {
            'times': [],
            'iterations': [],
            'moves': [],
            'queue_size': []
        },
        'dfs': {
            'times': [],
            'iterations': [],
            'moves': [],
            'queue_size': []
        },
        'id_dfs': {
            'times': [],
            'iterations': [],
            'moves': [],
            'queue_size': []
        },
        'a_star': {
            'times': [],
            'iterations': [],
            'moves': [],
            'queue_size': []
        }
    }

    for i in range(10):
        print("")
        print(i)
        for algorithm, output_text in algorithms:
            stdout.write(output_text)
            result = solver.search(algorithm)

            total_seconds = get_seconds(result.total_time)

            total_results[algorithm]['times'].append(total_seconds)
            total_results[algorithm]['iterations'].append(result.total_iters)
            total_results[algorithm]['moves'].append(result.moves_count)
            total_results[algorithm]['queue_size'].append(result.queue_size)

            print_search_result(result)

    plot_times({
        'bfs': total_results['bfs']['times'],
        'id_dfs': total_results['id_dfs']['times'],
        'a_star': total_results['a_star']['times']
    }, 85, 'Search Algorithms Execution Times')

    plot_iterations({
        'bfs': total_results['bfs']['iterations'],
        'id_dfs': total_results['id_dfs']['iterations'],
        'a_star': total_results['a_star']['iterations']
    }, 1600000, title='Search Algorithms Total Iterations')

    plot_queue_sizes({
        'bfs': total_results['bfs']['queue_size'],
        'id_dfs': total_results['id_dfs']['queue_size'],
        'a_star': total_results['a_star']['queue_size']
    }, 100000, title='Search Algorithms Queue Size at execution end')

    plot_moves({
        'bfs': total_results['bfs']['moves'],
        'id_dfs': total_results['id_dfs']['moves'],
        'a_star': total_results['a_star']['moves']
    }, title='Search Algorithms Total Moves')


# Execute solver only when running this module
if __name__ == "__main__":
    solve_blocksword_puzzle()
