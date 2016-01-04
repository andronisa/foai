import itertools
from collections import deque
from Queue import PriorityQueue
import datetime as dt
from sys import stdout
from config import setup
from puzzle import BlocksworldPuzzle


class Solver:
    def __init__(self):
        self.total_iters = 0
        self.queue = None
        self.visited = None
        self.visited_directions = None
        self.puzzle_state = None
        self.heuristic = None
        self.method = None
        self.methods = {
            'bfs': self.bfs,
            'dfs': self.dfs,
            'id_dfs': self.id_dfs,
            'a_star': self.a_star
        }

    def search(self, method):
        self.reset_puzzle(method)

        start = dt.datetime.now()
        search_outcome = self.methods[method]()
        end = dt.datetime.now()

        if self.puzzle_state:
            moves = self.puzzle_state.moves
            print("")
            print(len(self.puzzle_state.directions))

            directions = self.puzzle_state.directions if len(self.puzzle_state.directions) < 50 else []
            print(directions)
        else:
            moves = None
            directions = None

        result = SearchResult(
                search_outcome,
                self.total_iters,
                len(self.queue),
                moves,
                directions,
                end - start
        )

        return result

    def log_state(self):
        if self.total_iters % 20000 == 0:
            stdout.write(".")
            stdout.flush()

    def reset_puzzle(self, method):
        self.total_iters = 0
        self.puzzle_state = BlocksworldPuzzle(setup.generate_puzzle())
        self.visited = set()
        self.visited_directions = {}

        if method == 'bfs':
            self.queue = deque([self.puzzle_state])
        elif method == 'dfs':
            self.queue = [self.puzzle_state]
            self.visited = {}
        elif method == 'id_dfs':
            self.queue = [self.puzzle_state]
            self.visited = {}
        elif method == 'a_star':
            self.queue = PriorityQueue()
            self.queue.put((0, self.puzzle_state))
            self.heuristic = lambda heur: heur.total_manhattan_distance()

    # Breadth-first search.
    # FIFO queue -- Double Ended Queue(DEQUEUE)
    # GET - left | ADD - right.
    def bfs(self):
        while len(self.queue) > 0:
            self.total_iters += 1
            self.log_state()
            self.visited_directions = {}

            # Get nearest(more shallow state.
            self.puzzle_state = self.queue.popleft()
            # Add current state to visited ones
            self.visited.add(self.puzzle_state.puzzle_hash())
            self.visited_directions[self.puzzle_state.puzzle_hash()] = self.puzzle_state.directions

            if self.puzzle_state.is_goal_state():
                return True

            def is_visited(state, visited):
                return state.puzzle_hash() in visited

            # Queue extend with not visited
            valid_children = []
            for child_state in self.puzzle_state.get_children():
                if not is_visited(child_state, self.visited):
                    valid_children.append(child_state)
            self.queue.extend(valid_children)

        # No result.
        return False

    # Depth First Search.
    # Not optimal solution.
    # It can go on infinitely.
    # LIFO Queue --> python list()
    def dfs(self):
        self.queue = [self.puzzle_state]
        # Visited : {state_hash:state_depth}
        self.visited = {}

        while len(self.queue) > 0:
            # Stopping in 2000000 iterations in case of infinite loop
            if self.total_iters > 2000000:
                return False
            self.total_iters += 1
            self.log_state()

            # Get the state that is deepest
            self.puzzle_state = self.queue.pop()  # Get deepest state.
            # Add current state in visited.
            self.visited[self.puzzle_state.puzzle_hash()] = self.puzzle_state.moves
            self.visited_directions[self.puzzle_state.puzzle_hash()] = self.puzzle_state.directions

            if self.puzzle_state.is_goal_state():
                return True

            def is_visited(child, visited):
                return child.puzzle_hash() in visited

            valid_children = []
            for child_state in self.puzzle_state.get_children():
                if not is_visited(child_state, self.visited) \
                        or self.visited[child_state.puzzle_hash()] > child_state.moves:
                    valid_children.append(child_state)
            self.queue.extend(valid_children)

        # No result
        return False

    # Iterative deepening depth-first search.
    # The solution is more optimal than DFS.
    # It is faster than BFS
    # It can go on infinitely, like DFS.
    # LIFO Queue --> python list()
    def id_dfs(self):
        start_state = self.puzzle_state

        for depth in itertools.count():
            self.queue = [start_state]
            self.visited = {}

            while len(self.queue) > 0:
                self.total_iters += 1
                self.log_state()

                # Get the state that is the deepest.
                self.puzzle_state = self.queue.pop()
                # Add current state to visited ones.
                self.visited[self.puzzle_state.puzzle_hash()] = self.puzzle_state.moves
                self.visited_directions[self.puzzle_state.puzzle_hash()] = self.puzzle_state.directions

                if self.puzzle_state.is_goal_state():
                    return True

                def is_visited(child, visited):
                    return child.puzzle_hash() in visited

                if self.puzzle_state.moves < depth:
                    valid_children = []
                    for child_state in self.puzzle_state.get_children():
                        if not is_visited(child_state, self.visited) \
                                or self.visited[child_state.puzzle_hash()] > child_state.moves:
                            valid_children.append(child_state)
                    self.queue.extend(valid_children)

        return False

    # A* search.
    # Most optimal solution time-wise.
    # QUEUE: PRIORITY QUEUE(when _get() is used, it gets the item with the minimum value first)
    # ORDER: Heuristic(Total Manhattan Distance + number of state moves)
    def a_star(self):
        # Total_moves = total so far + total to be made
        def total_moves(puzzle_state, heuristic):
            return puzzle_state.moves + heuristic(self.puzzle_state)

        def state_cost_tuple(puzzle_state, heuristic):
            return total_moves(puzzle_state, heuristic), puzzle_state

        def valid_children(puzzle_state, visited):
            children = []
            for child_state in puzzle_state.get_children():
                if child_state.puzzle_hash() not in visited:
                    children.append(child_state)
            return children

        while not self.queue.empty():
            self.total_iters += 1
            self.log_state()

            # Get state with lowest value(moves left)
            self.puzzle_state = self.queue.get()[1]
            # Add state to visited
            self.visited.add(self.puzzle_state.puzzle_hash())
            self.visited_directions[self.puzzle_state.puzzle_hash()] = self.puzzle_state.directions

            if self.puzzle_state.is_goal_state():
                self.queue = self.queue.queue
                return True

            for valid_child in valid_children(self.puzzle_state, self.visited):
                self.queue.put(state_cost_tuple(valid_child, self.heuristic))

        # No result
        self.queue = self.queue.queue
        return False


class SearchResult:
    def __init__(self, is_succesful, total_iters, queue_size, moves_count, total_moves, time_elapsed):
        self.__is_succesful = is_succesful
        self.__total_iters = total_iters
        self.__queue_size = queue_size
        self.__moves_count = moves_count
        self.__moves = total_moves
        self.__time_elapsed = time_elapsed

    @property
    def is_successful(self):
        return self.__is_succesful

    @property
    def total_iters(self):
        return self.__total_iters

    @property
    def queue_size(self):
        return self.__queue_size

    @property
    def moves_count(self):
        return self.__moves_count

    @property
    def moves(self):
        return self.__moves

    @property
    def total_time(self):
        return self.__time_elapsed
