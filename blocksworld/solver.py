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

        result = SearchResult(
                search_outcome,
                self.total_iters,
                len(self.queue),
                self.puzzle_state.moves if self.puzzle_state else None,
                end - start
        )

        return result

    def log_state(self):
        if self.total_iters % 20000 == 0:
            stdout.write(".")
            stdout.flush()

    def reset_puzzle(self, method):
        self.total_iters = 0
        self.puzzle_state = BlocksworldPuzzle(setup.starting_tiles())
        self.visited = set()

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
            self.heuristic = lambda b: b.total_manhattan_distance()

    # Breadth-first search.
    # FIFO queue -- Double Ended Queue(DEQUEUE)
    # POP - left | ADD - right.
    def bfs(self):
        while len(self.queue) > 0:
            self.total_iters += 1
            self.log_state()

            self.puzzle_state = self.queue.popleft()  # Get shallowest state.
            self.visited.add(self.puzzle_state.puzzle_hash())  # Mark current state as visited.

            if self.puzzle_state.is_goal_state():
                return True

            # Add not visited valid moves to the right of the queue.
            self.queue.extend(
                    filter(
                            lambda state: state.puzzle_hash() not in self.visited,
                            self.puzzle_state.get_children()))
        # Loop did not find result: search space exhaustion, no goal found.
        return False

    def dfs(self, limit=None):
        start_state = self.puzzle_state
        # Depth goes from 0 to infinity. We start at 0 to ensure optimality: we must check
        # that the initial state is not a goal state before generating its children.
        if limit:
            depth_limit = limit
        else:
            depth_limit = itertools.count()
        for depth in depth_limit:
            # Visited is a dictionary with state hash as key and state depth as value. We need
            # to track depth as in DFS we may encounter visited states later at shallower depth.
            self.queue = [start_state]
            self.visited = {}

            while len(self.queue) > 0:
                self.total_iters += 1
                self.log_state()

                self.puzzle_state = self.queue.pop()  # Get deepest state.

                current_state_hashcode = self.puzzle_state.puzzle_hash()
                self.visited[current_state_hashcode] = self.puzzle_state.moves  # Mark current state as visited.

                if self.puzzle_state.is_goal_state():
                    return True

                if self.puzzle_state.moves < depth:
                    self.queue.extend(
                            filter(
                                    lambda child:
                                    child.puzzle_hash() not in self.visited or
                                    self.visited[current_state_hashcode] > child.moves,
                                    self.puzzle_state.get_children()))

        # Loop did not return result -> search space exhaustion, no goal found.
        return False

    # 1b) Iterative deepening depth-first search. Should find the optimal solution like
    # BFS but use less memory. On the other hand the time cost is larger because self.puzzle_states
    # above the goal depth are recomputed over and over again. No depth limit is set so
    # this implementation will not terminate if the search space is infinite. Fringe is a
    # LIFO queue. Here we use an ordinary python list with O(1) append and pop (both are
    # done from the right).

    def id_dfs(self, ):
        for limit in itertools.count():
            result = self.dfs(limit)
            if result is True:
                return result

    # A* search. Should find the result much faster than BFS and IDDFS.
    # Fringe is a priority queue ordered by a cost estimate function.
    # This is a general implementation that is parameterized to receive any heuristic.
    # States sharing same priority are in no special order -> traversal order
    # is not fully deterministic.
    def a_star(self):
        # Cost estimate = accumulated cost so far + heuristic estimate of future cost.
        def estimate_cost(puzzle_state):
            return puzzle_state.moves + self.heuristic(self.puzzle_state)

        def queue_entry(puzzle_state):
            return estimate_cost(puzzle_state), puzzle_state

        def unvisited_children(puzzle_state, visited):
            return filter(
                    lambda child: child.puzzle_hash() not in visited,
                    puzzle_state.get_children())

        while not self.queue.empty():
            self.total_iters += 1
            self.log_state()

            self.puzzle_state = self.queue.get()[1]  # get self.puzzle_state with highest priority
            self.visited.add(self.puzzle_state.puzzle_hash())  # Mark current state as visited

            if self.puzzle_state.is_goal_state():
                self.queue = self.queue.queue
                return True

            for entry in map(queue_entry, unvisited_children(self.puzzle_state, self.visited)):
                self.queue.put(entry)

        # Loop did not return result -> search space exhaustion, no goal found.
        self.queue = self.queue.queue
        return False


class SearchResult:
    def __init__(self, is_succesful, total_iters, queue_size, total_moves, time_elapsed):
        self.__is_succesful = is_succesful
        self.__total_iters = total_iters
        self.__queue_size = queue_size
        self.__total_moves = total_moves
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
    def total_moves(self):
        return self.__total_moves

    @property
    def total_time(self):
        return self.__time_elapsed
