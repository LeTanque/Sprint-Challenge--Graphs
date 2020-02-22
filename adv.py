from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# Why does this keep happening
# 148: {'n': 163, 's': 121, 'e': 178},
# 178: {'w': 178, 'e': 178}}
# curr_exits:  {'w': 178, 'e': 178}

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()
# print("")

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


class Discovery():
    def __init__(self):
        self.queue = []
        self.stack = []
        self.the_way = []
        self.moves = 0
        self.graph = {}

    def addq(self, value):
        self.queue.append(value)

    def remq(self):
        if self.size() > 0:
            return self.queue.pop()
        else:
            return None

    def size(self):
        return len(self.queue)

# Find the way back
def backtracker(player, discovery):
    new_disco = Discovery()
    visited = set()
    # print('discovery graph when we hit a dead end: ', discovery.graph)
    new_disco.addq([player.current_room.id])
    while new_disco.size() > 0:
        path = new_disco.remq()
        last_room = path[-1]
        if last_room not in visited:
            # print('last_room, path: ', last_room, path)
            visited.add(last_room)
            for exit in discovery.graph[last_room]:
                if discovery.graph[last_room][exit] == "?":
                    return path
                else:
                    # Copy the path, append the room, keep looking
                    # print('discovery.graph: ', discovery.graph)
                    # print('discovery.graph[last_room][exit]: ', discovery.graph[last_room][exit])
                    # print('exit: ', exit)
                    path_copy = list(path)
                    path_copy.append(discovery.graph[last_room][exit])
                    new_disco.addq(path_copy)

    # print('visited: ', visited, discovery.queue)
    return []

# Function to find directions at given room
# Takes player and discovery queue
def direction_exploration(mando, disco_queue):
    curr_exits = disco_queue.graph[mando.current_room.id]
    other_ways = []
    print('current room: curr_exits: ', mando.current_room.id, curr_exits)   # This is the problem

    # print("actual current exits", mando.current_room.id, room_graph[mando.current_room.id][1])
    for direction in curr_exits:
        if curr_exits[direction] == "?":
            other_ways.append(direction)


    # print('other_ways: ', other_ways)

    if len(other_ways) == 0:
        path_to_unexplored = backtracker(mando, disco_queue)
        print('path_to_unexplored: ', path_to_unexplored)
        room_on_path = mando.current_room.id
        for next_room in path_to_unexplored:
            for direction in disco_queue.graph[room_on_path]:
                if disco_queue.graph[room_on_path][direction] == next_room:
                    disco_queue.addq(direction)
                    room_on_path = next_room
                    break
    else:
        disco_queue.addq(other_ways[random.randint(0, len(other_ways) - 1)])


# A function that finds possible paths
def possible_path():
    mando = Player(world.starting_room)
    disco = Discovery()
    exit_rooms = {}
    exits = mando.current_room.get_exits()
    moves = []
    the_way = []
    shortest_length = 5000000

    # # Stop on empty stack
    # # Explore
    # Adds the ? for each poss room at room
    for poss_direct in exits:
        exit_rooms[poss_direct] = "?"

    # Starts the disco graph with empty ? rooms
    disco.graph[world.starting_room.id] = exit_rooms

    direction_exploration(mando, disco)
    inverse = {"n": "s", "s": "n", "e": "w", "w": "e"}
    
    # # Store the moves in moves
    # # if queue, trigger direction_exploration 
    # # Don't go over same path again and again
    while len(disco.queue) > 0:
        start = mando.current_room.id
        next_room = disco.remq()
        mando.travel(next_room)
        moves.append(next_room)
        end = mando.current_room.id

        disco.graph[start][next_room] = end
        # print('disco.graph[start][next_room] : ', disco.graph[start][next_room] , end)


        if end not in disco.graph:
            disco.graph[end] = {}
            for exit in mando.current_room.get_exits():
                disco.graph[end][exit] = "?"

        disco.graph[end][inverse[next_room]] = start

        if len(disco.queue) == 0:
            direction_exploration(mando, disco)

    # Disco queue is empty
    # Check to see if moves are less than shortest length
    # Check if moves are at least greater than max rooms
    # if len(moves) < shortest_length and len(moves) >= len(room_graph):
    if len(moves) < shortest_length:
        the_way = moves
        shortest_length = len(moves)
    # print('\nWhat to do, Mando? ', the_way)
    # print('Mando moves, shortest length: ', the_way, "\n", shortest_length, len(room_graph))
    return the_way


# # Test loop
# traversal_path = ['w', 'w', 's', 's', 'e', 'e', 'n', 'n', 'e', 'e', 'w', 'w', 'n', 'n']
# # Test loop bigger
# traversal_path =  ['w', 'w', 's', 's', 'e', 'e', 'n', 'n', 'e', 'e', 'w', 'w', 'n', 'w', 'w', 'n', 'e', 'e', 's', 'e', 'e', 'n', 's', 'e', 'e', 'n']
traversal_path = []

solution_found = False

if len(traversal_path) > 0:
    solution_found = True


while solution_found is False:
    traversal_path = possible_path()
    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)
    solution_found = True
    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)
    if len(visited_rooms) == len(room_graph):
        print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
        solution_found = True
        break

print('traversal_path receipt: ', traversal_path)
print("")

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)


# world.print_rooms()
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


