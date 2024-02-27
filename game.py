import screen_updates
import player
import random
import numpy


class Game:
    def __init__(self, config, field):
        BASE_PLAYERS = 10
        PLAYERS_PER_SP = 2
        BASE_SPEED = 0.5
        SPEED_PER_SP = 0.05
        BASE_HUNT_RANGE = 500
        HUNT_RANGE_PER_SP = 30
        BASE_HUNT_WEIGHT = 0.1
        HUNT_WEIGHT_PER_SP = 0.01
        BASE_AVOID_RANGE = 10
        AVOID_RANGE_PER_SP = 1.5
        BASE_AVOID_WEIGHT = -0.1
        AVOID_WEIGHT_PER_SP = -0.01
        BASE_ESCAPE_RANGE = 50
        ESCAPE_RANGE_PER_SP = 10
        BASE_ESCAPE_WEIGHT = -0.3
        ESCAPE_WEIGHT_PER_SP = -0.02
        BASE_CONQUER_RANGE = 7.5
        CONQUER_RANGE_PER_SP = 1.25

        self.num_factions = int(config.get('rules', 'factions'))
        self.faction_stats = []
        self.field = field
        self.highlight_player = False
        self.highlight_id = 0
        self.winner = 0
        self.reload_config = False
        if config.get('tournament', 'tournament_mode') == 'True':
            self.tournament_mode = True
        if config.get('rules', 'teams_equal') == 'True':
            if config.get('rules', 'start_random') == 'True':
                num_players = random.randint(7, 14)
                speed = random.randint(7, 14)
                hunt_range = random.randint(7, 14)
                avoid_range = random.randint(7, 14)
                escape_range = random.randint(7, 14)
                conquer_range = random.randint(7, 14)
                hunt_weight = random.randint(7, 14)
                avoid_weight = random.randint(7, 14)
                escape_weight = random.randint(7, 14)
            else:
                num_players = int(config.get('team_default', 'players'))
                speed = float(config.get('team_default', 'speed'))
                hunt_range = float(config.get('team_default', 'hunt_range'))
                avoid_range = float(config.get('team_default', 'avoid_range'))
                escape_range = float(config.get('team_default', 'escape_range'))
                conquer_range = float(config.get('team_default', 'conquer_range'))
                hunt_weight = float(config.get('team_default', 'hunt_weight'))
                avoid_weight = float(config.get('team_default', 'avoid_weight'))
                escape_weight = float(config.get('team_default', 'escape_weight'))
            self.num_players_faction = [int(BASE_PLAYERS + PLAYERS_PER_SP * num_players)
                                        for _ in range(self.num_factions)]
            self.faction_stats.extend([[BASE_SPEED + SPEED_PER_SP * speed,
                                        BASE_HUNT_RANGE + HUNT_RANGE_PER_SP * hunt_range,
                                        BASE_AVOID_RANGE + AVOID_RANGE_PER_SP * avoid_range,
                                        BASE_ESCAPE_RANGE + ESCAPE_RANGE_PER_SP * escape_range,
                                        BASE_CONQUER_RANGE + CONQUER_RANGE_PER_SP * conquer_range,
                                        BASE_HUNT_WEIGHT + HUNT_WEIGHT_PER_SP * hunt_weight,
                                        BASE_AVOID_WEIGHT + AVOID_WEIGHT_PER_SP * avoid_weight,
                                        BASE_ESCAPE_WEIGHT + ESCAPE_WEIGHT_PER_SP * escape_weight]
                                       for _ in range(self.num_factions)])
        else:
            self.num_players_faction = []
            for i in range(self.num_factions):
                if config.get('rules', 'start_random') == 'True':
                    num_players = random.randint(7, 14)
                    speed = random.randint(7, 14)
                    hunt_range = random.randint(7, 14)
                    avoid_range = random.randint(7, 14)
                    escape_range = random.randint(7, 14)
                    conquer_range = random.randint(7, 14)
                    hunt_weight = random.randint(7, 14)
                    avoid_weight = random.randint(7, 14)
                    escape_weight = random.randint(7, 14)
                else:
                    num_players = int(config.get('faction'+str(i + 1), 'players'))
                    speed = float(config.get('faction'+str(i + 1), 'speed'))
                    hunt_range = float(config.get('faction'+str(i + 1), 'hunt_range'))
                    avoid_range = float(config.get('faction'+str(i + 1), 'avoid_range'))
                    escape_range = float(config.get('faction'+str(i + 1), 'escape_range'))
                    conquer_range = float(config.get('faction'+str(i + 1), 'conquer_range'))
                    hunt_weight = float(config.get('faction'+str(i + 1), 'hunt_weight'))
                    avoid_weight = float(config.get('faction'+str(i + 1), 'avoid_weight'))
                    escape_weight = float(config.get('faction'+str(i + 1), 'escape_weight'))
                self.num_players_faction.append(int(BASE_PLAYERS + PLAYERS_PER_SP * num_players))
                self.faction_stats.append([BASE_SPEED + SPEED_PER_SP * speed,
                                           BASE_HUNT_RANGE + HUNT_RANGE_PER_SP * hunt_range,
                                           BASE_AVOID_RANGE + AVOID_RANGE_PER_SP * avoid_range,
                                           BASE_ESCAPE_RANGE + ESCAPE_RANGE_PER_SP * escape_range,
                                           BASE_CONQUER_RANGE + CONQUER_RANGE_PER_SP * conquer_range,
                                           BASE_HUNT_WEIGHT + HUNT_WEIGHT_PER_SP * hunt_weight,
                                           BASE_AVOID_WEIGHT + AVOID_WEIGHT_PER_SP * avoid_weight,
                                           BASE_ESCAPE_WEIGHT + ESCAPE_WEIGHT_PER_SP * escape_weight])
        self.num_players_faction_current = []
        self.players = self.new_players()
        self.distances = [[(0, 0, 0) for _ in range(len(self.players))] for _ in range(len(self.players))]
        self.conquer_table = [[0 for _ in range(self.num_factions)] for _ in range(self.num_factions)]
        for i in range(self.num_factions):
            conquer_list = list(map(int, str(config.get('faction'+str(i + 1), 'beats')).split(',')))
            for j in conquer_list:
                self.conquer_table[i][j - 1] = 1

    def new_players(self):
        players = []
        for i in range(self.num_factions):
            for j in range(self.num_players_faction[i]):
                players.append(player.Player(len(players), (random.randint(10, self.field[0] - 10),
                                             random.randint(10, self.field[0] - 10)), self.faction_stats[i][0],
                                             self.faction_stats[i][1], self.faction_stats[i][2],
                                             self.faction_stats[i][3], self.faction_stats[i][4],
                                             self.faction_stats[i][5], self.faction_stats[i][6],
                                             self.faction_stats[i][7], i))
        self.winner = 0
        self.num_players_faction_current = [self.num_players_faction]
        return players

    def in_range(self, p, max_dist, factions):
        return [n for n in self.players if
                (self.distances[p.id][n.id][2] < max_dist and p.id != n.id and n.faction in factions)]

    def calc_distances(self):
        for p in self.players:
            for n in self.players:
                if p.id < n.id:
                    dist_x = n.pos[0] - p.pos[0]
                    dist_y = n.pos[1] - p.pos[1]
                    self.distances[p.id][n.id] = (dist_x, dist_y, numpy.sqrt(dist_x ** 2 + dist_y ** 2))
                    self.distances[n.id][p.id] = (-dist_x, -dist_y, self.distances[p.id][n.id][2])

    def count_players(self):
        self.num_players_faction_current.append([[p.faction for p in self.players].count(i)
                                                 for i in range(self.num_factions)])

    def check_winner(self):
        for idf, players in enumerate(self.num_players_faction_current[-1]):
            if not players:
                self.winner = [self.conquer_table[i][idf] for i in range(self.num_factions)]

    def step(self):
        random.shuffle(self.players)
        self.calc_distances()
        for p in self.players:
            p.move(self)
        for p in self.players:
            p.conquer(self)
        self.count_players()
        self.check_winner()
