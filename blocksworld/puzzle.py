import numpy as np
import scipy.spatial as spatial
import collections
import hashlib

from config import setup

_key = 0


def _get_new_key():
    global _key
    _key += 1
    return _key


attributes = collections.defaultdict(_get_new_key)


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


class BlocksworldPuzzle:
    def __init__(self, tiles, moves=0):
        self.tiles = np.array(tiles, dtype=np.int)
        self.moves = moves
        self.height = None
        self.width = None
        self.agent = 0

    def get_tile(self, tile):
        tiles_matched = np.where(self.tiles == tile)
        coords = Coords(
                tiles_matched[0].item(0),
                tiles_matched[1].item(0),
                self.get_height(),
                self.get_height()
        )
        return coords

    def find_agent(self):
        return self.get_tile(self.agent)

    def is_goal_state(self):
        return np.count_nonzero(self.tiles != setup.goal_state()) == 0

    def get_width(self):
        if not self.width:
            self.width = self.tiles.shape[1]
        return self.width

    def get_height(self):
        if not self.height:
            self.height = self.tiles.shape[0]
        return self.height

    # Returns a new BlocksworldPuzzle with the agent on the new position.
    def move_agent(self, target_coords):
        previous_agent_position = self.find_agent()

        new_tiles = np.copy(self.tiles)

        target_tile = self.tiles[target_coords.x_axis][target_coords.y_axis]

        # Replace agent with target.
        new_tiles[previous_agent_position.x_axis][previous_agent_position.y_axis] = target_tile

        # Replace target with agent.
        new_tiles[target_coords.x_axis][target_coords.y_axis] = self.agent

        return BlocksworldPuzzle(new_tiles, self.moves + 1)

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

        north = (0, 1)
        east = (1, 0)
        south = (0, -1)
        west = (-1, 0)

        possible_directions = [north, east, south, west]
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

    # create big hash of all the tiles of the puzzle, useful for comparing
    def puzzle_hash(self):
        global attributes
        return attributes[hashlib.md5(self.tiles.tostring()).digest()]

    # Manhattan distance for tile.
    def manhattan_to_goal(self, tile):
        tile_coords = self.get_tile(tile)
        return spatial.distance.cityblock(setup.get_goal_coordinates(tile), (tile_coords.x_axis, tile_coords.y_axis))

    # Manhattan distances total.
    def total_manhattan_distance(self):
        tiles = np.nditer(self.tiles)
        distance_sum = 0

        for tile in tiles:
            distance_sum += self.manhattan_to_goal(tile)
        return distance_sum
