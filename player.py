import numpy


class Player:

    def __init__(self, id, pos, speed, hunt_range, avoid_range, escape_range, conquer_range, hunt_weight, avoid_weight,
                 escape_weight, faction):
        self.id = id
        self.pos = pos
        self.speed = speed
        self.hunt_range = hunt_range
        self.hunt_weight = hunt_weight
        self.avoid_range = avoid_range
        self.avoid_weight = avoid_weight
        self.escape_range = escape_range
        self.escape_weight = escape_weight
        self.conquer_range = conquer_range
        self.faction = faction
        self.dirs = [(0, 0), (0, 0), (0, 0)]

    def move(self, game):
        self.dirs = [(0, 0), (0, 0), (0, 0)]

        # hunting
        neighbors = game.in_range(self, self.hunt_range, [x for x in range(len(game.conquer_table[self.faction]))
                                                          if game.conquer_table[self.faction][x] == 1])
        if neighbors:
            hunt_targets = [(n.id, game.distances[self.id][n.id][2]) for n in neighbors]
            hunt_id = min(hunt_targets, key=lambda x: x[1])[0]
            self.dirs[0] = tuple(self.hunt_weight * x for x in game.distances[self.id][hunt_id][:2])

        # avoiding
        neighbors = game.in_range(self, self.avoid_range, [x for x in range(len(game.conquer_table[self.faction]))
                                                           if game.conquer_table[self.faction][x] == 0])
        for n in neighbors:
            self.dirs[1] = tuple(self.avoid_weight * x + self.dirs[1][i]
                                 for i, x in enumerate(game.distances[self.id][n.id][:2]))

        # escaping
        neighbors = game.in_range(self, self.escape_range, [x for x in range(len(game.conquer_table[self.faction]))
                                                            if game.conquer_table[x][self.faction] == 1])
        for n in neighbors:
            self.dirs[2] = tuple(self.escape_weight * x + self.dirs[1][i]
                                 for i, x in enumerate(game.distances[self.id][n.id][:2]))

        total_x = sum([xy[0] for xy in self.dirs])
        total_y = sum([xy[1] for xy in self.dirs])
        length = numpy.sqrt(total_x ** 2 + total_y ** 2) if total_x or total_y else 1
        total_x = total_x / length * self.speed
        total_y = total_y / length * self.speed
        new_x = self.pos[0] + total_x
        new_y = self.pos[1] + total_y
        if new_x < 0:
            new_x = game.field[0] - 10
        if new_y < 0:
            new_y = game.field[1] - 10
        if new_x > game.field[0] - 10:
            new_x = 0
        if new_y > game.field[1] - 10:
            new_y = 0
        self.pos = new_x, new_y

    def conquer(self, game):
        neighbors = game.in_range(self, self.conquer_range, [x for x in range(len(game.conquer_table[self.faction]))
                                                             if game.conquer_table[self.faction][x] == 1])
        for n in neighbors:
            n.faction = self.faction
            n.speed = self.speed
            n.hunt_range = self.hunt_range
            n.avoid_range = self.avoid_range
            n.escape_range = self.escape_range
            n.conquer_range = self.conquer_range
