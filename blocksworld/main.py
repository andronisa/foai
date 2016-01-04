from sys import stdout
from solver import Solver


def print_search_result(result):
    result_moves = result.moves

    moves = ""
    if result_moves is []:
        moves = "Too many moves"
    for move in result_moves:
        moves += ", " + move

    outputs = [
        ("     Result", "Successful" if result.is_successful else "Unsuccesful"),
        ("     Total time", result.total_time),
        ("     Total moves number to goal", "{} moves".format(result.moves_count)),
        ("     Total moves", moves),
        ("     Total iterations", result.total_iters),
        ("     Queue size at the end", result.queue_size)
    ]

    print("")

    for output in outputs:
        output_key = output[0]
        output_value = output[1]

        print(output_key + " - " + str(output_value))
    print("")


def solve_blocksword_puzzle():
    solver = Solver()

    stdout.write("BFS")
    print_search_result(solver.search('bfs'))

    stdout.write("DFS")
    print_search_result(solver.search('dfs'))

    stdout.write("Iterative Deepening DFS")
    print_search_result(solver.search('id_dfs'))

    stdout.write("A* (Heuristic: Sum of Manhattan distances)")
    print_search_result(solver.search('a_star'))


# Execute solver only when running this module
if __name__ == "__main__":
    solve_blocksword_puzzle()
