from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
print("")

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


class Discovery():
    def __init__(self):
        self.graph = {}
        self.stack = []
        self.the_way = []
        self.the_rooms = set()
        self.moves = 0

    def addstack(self, value):
        self.stack.append(value)

    def remstack(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

    def start_graph(self, room_graph):
        room_model = {'n':"?", 'e':"?", 's':"?", 'w':"?"}
        for room in room_graph:
            self.graph[room] = room_model



# A function that finds possible paths
def possible_path():
    disco = Discovery()
    disco.start_graph(room_graph)

    directions = disco.find_directions(0)

    player.current_room.get_exits()
    player.travel("n")
    player.current_room.get_exits()



    print('directions: ', directions, player.current_room.id)

    # room_details = room_graph[player.current_room.id]
    # disco.addstack(room_details)

    # # Stop on empty stack
    # # Explore
    # # Store the connected paths in the_way
    # # Reach the end of a path, then back track it?
    # # Don't go over same path again and again
    while disco.size() > 0:
        path = disco.remstack()
        print(path)

    # while len(self.stack) > 0:
    #     path = self.stack.pop()
    #     pathend = path[-1]
    #     # coords = pathend[0]
    #     poss_direct = pathend[1]

    #     print('poss_direct: ', poss_direct)

    #     for connected_room in poss_direct:
    #         self.the_way.append(connected_room)
    #         path_copy = list(path)
    #         path_copy.append(self.graph[poss_direct[connected_room]])
            
    #         print('  >>> print : ', path_copy, "\n", connected_room, self.the_way, "\n", self.graph[poss_direct[connected_room]])
    #         self.moves += 1
    #         if self.moves > 10:
    #             break
    #         self.stack.append(path_copy)
            
    #         print('self.the_way: ', self.the_way)
    print('\nWhat to do, Mandalorian? ', disco.the_way)

possible_path()



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

print("")
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

