import screen_updates
import player
import random
import numpy


class Game:
    def __init__(self, config, field):
        self.factions = int(config.get('rules', 'factions'))
        self.field = field
        self.highlight_player = False
        self.highlight_id = 0
        self.reload_config = False
        if config.get('rules', 'teams_equal'):
            self.nRock = self.nPaper = self.nScissors = int(config.get('team_default', 'players'))
            self.speed = float(config.get('team_default', 'speed'))
            self.hunt_range = float(config.get('team_default', 'hunt_range'))
            self.avoid_range = float(config.get('team_default', 'avoid_range'))
            self.escape_range = float(config.get('team_default', 'escape_range'))
            self.conquer_range = float(config.get('team_default', 'conquer_range'))
        self.players = self.new_players()
        self.distances = [[(0, 0, 0) for _ in range(len(self.players))] for _ in range(len(self.players))]

    def new_players(self):
        players = []
        for i in range(self.factions):
            for j in range(self.nRock):
                players.append(player.Player(len(players), self.random_location(self.field), self.speed,
                                             self.hunt_range, self.avoid_range, self.escape_range, i))
        return players

    @staticmethod
    def random_location(field):
        return random.randint(10, field[0] - 10), random.randint(10, field[0] - 10)

    def in_range(self, p, max_dist, faction):
        return [n for n in self.players if
                (self.distances[p.id][n.id][2] < max_dist and p.id != n.id and n.faction == faction)]

    def calc_distances(self):
        for p in self.players:
            for n in self.players:
                if p.id < n.id:
                    dist_x = n.pos[0] - p.pos[0]
                    dist_y = n.pos[1] - p.pos[1]
                    self.distances[p.id][n.id] = (dist_x, dist_y, numpy.sqrt(dist_x ** 2 + dist_y ** 2))
                    self.distances[n.id][p.id] = (-dist_x, -dist_y, self.distances[p.id][n.id][2])

    def step(self, screen, font, times):
        random.shuffle(self.players)
        self.calc_distances()
        for p in self.players:
            p.move(self)
        for p in self.players:
            p.conquer(self)

    def highlight(self, screen, font, times):
        self.highlight_player = True
        screen_updates.game_screen(self, screen, font, times)
        self.highlight_player = False
