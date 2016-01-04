import numpy as np
import scipy.spatial as spatial
import hashlib

from config import setup


class Coords:
    def __init__(self, x, y, height, width):
        self.x_axis = x
        self.y_axis = y
        self.height = height
        self.width = width

    def is_valid(self):
        return self.x_axis_valid() and self.y_axis_valid()

    def x_axis_valid(self):
        return 0 <= self.x_axis < self.width

    def y_axis_valid(self):
        return 0 <= self.y_axis < self.height

    @staticmethod
    def coordinates():
        return {
            'north': (0, 1),
            'east': (1, 0),
            'south': (0, -1),
            'west': (-1, 0)
        }

    @staticmethod
    def coordinates_by_value():
        return {v: k for k, v in Coords.coordinates().items()}


class BlocksworldPuzzle:
    def __init__(self, blocks, moves=0, directions=list()):
        self.blocks = np.array(blocks, dtype=np.int)
        self.moves = moves
        self.directions = directions
        self.height = None
        self.width = None
        self.agent = 0
        self.goal_state = setup.goal_state()

    def get_block(self, block):
        blocks_matched = np.where(self.blocks == block)
        coords = Coords(
                blocks_matched[0].item(0),
                blocks_matched[1].item(0),
                self.get_height(),
                self.get_height()
        )
        return coords

    def find_agent(self):
        return self.get_block(self.agent)

    def is_goal_state(self):
        return np.count_nonzero(self.blocks != self.goal_state) == 0

    def get_width(self):
        if not self.width:
            self.width = self.blocks.shape[1]
        return self.width

    def get_height(self):
        if not self.height:
            self.height = self.blocks.shape[0]
        return self.height

    # Returns a new BlocksworldPuzzle with the agent on the new position.
    def move_agent(self, target_coords):
        previous_agent_position = self.find_agent()
        agent_x = previous_agent_position.x_axis
        agent_y = previous_agent_position.y_axis

        new_puzzle = np.copy(self.blocks)

        target_block = self.blocks[target_coords.x_axis][target_coords.y_axis]
        target_block_x = target_coords.x_axis
        target_block_y = target_coords.y_axis

        movement = (agent_x - target_block_x, agent_y - target_block_y)
        direction = Coords.coordinates_by_value()[movement]
        self.directions.append(direction)

        # Replace agent with target block.
        new_puzzle[agent_x][agent_y] = target_block

        # Replace target block with agent.
        new_puzzle[target_block_x][target_block_y] = self.agent

        return BlocksworldPuzzle(new_puzzle, self.moves + 1, self.directions)

    def neighbor_states(self, agent_coord):
        def move_towards(direction):
            x_axis_move = direction[0]
            y_axis_move = direction[1]

            return Coords(
                    agent_coord.x_axis + x_axis_move,
                    agent_coord.y_axis + y_axis_move,
                    self.get_height(),
                    self.get_width()
            )

        coordinates = Coords.coordinates()

        possible_directions = [coordinates['north'], coordinates['east'], coordinates['south'], coordinates['west']]
        direction_coords = set()

        for possible_dir in possible_directions:
            coordinate = move_towards(possible_dir)
            if coordinate.is_valid():
                direction_coords.add(coordinate)
        return direction_coords

    def valid_moves(self):
        return self.neighbor_states(self.find_agent())

    # Generator of children moves.
    def get_children(self):
        children = []
        for valid_move in self.valid_moves():
            children.append(self.move_agent(valid_move))
        return children

    # Manhattan distance for block.
    def manhattan_to_goal(self, block):
        block_coords = self.get_block(block)
        return spatial.distance.cityblock(self.get_goal_coordinates(block), (block_coords.x_axis, block_coords.y_axis))

    # Manhattan distances total.
    def total_manhattan_distance(self):
        blocks = np.nditer(self.blocks)
        distance_sum = 0

        for block in blocks:
            distance_sum += self.manhattan_to_goal(block)
        return distance_sum

    # create big hash of all the blocks of the puzzle, useful for comparing
    def puzzle_hash(self):
        sha_one_blocks = hashlib.sha1(self.blocks)
        return sha_one_blocks.hexdigest()

    # Goal coordinates for a single block.
    def get_goal_coordinates(self, block):
        goal_coordinates = np.where(self.goal_state == block)
        matched = np.array([
            goal_coordinates[0].item(0),
            goal_coordinates[1].item(0)
        ])

        return matched
