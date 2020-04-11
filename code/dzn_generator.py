import numpy as np
import random
from dzn_formatter import array2str
from dzn_formatter import list2enum_str
from dzn_formatter import array2array2d
from dzn_export import export
from dzn_export import create_file


class Scenario:

    def __init__(self, seed):
        random.seed(seed)

    def generate_scenario(self, name, n_periods, n_venues, n_teams, n_coaches, n_teams_per_division):
        self.name = name

        scenario = {
            "NB_PERIODS" : n_periods,
            "NB_VENUES" : n_venues,
            "NB_GAMES" : self.get_total_number_of_games(n_teams_per_division),
            "NB_TEAMS" : n_teams,
            "NB_DIVISIONS" : len(n_teams_per_division),
            "NB_TEAMS_PER_DIVISION" : n_teams_per_division,
            "VENUE_AVAILABILITIES" : self.generate_venues_avaliability(n_venues, n_periods),
            "GAMES_TO_SCHEDULE" :  self.generate_games_to_schedule(n_teams_per_division),
            "TEAM_NAMES" : self.generate_team_names(n_teams_per_division),
            "TEAMS_TIME_PREFERENCES" : self.generate_teams_time_preferences(n_teams, n_periods),
            "COACH_NAMES" : self.generate_coach_names(n_coaches),
            "COACHES_BY_TEAM" : self.generate_coaches_by_team(n_coaches, n_teams)
        }

        return scenario

    def generate_team_names(self, n_teams_per_division):
        team_names = []
        for div_number, n_teams in enumerate(n_teams_per_division, 1):
            for team_number in range(1, n_teams+1):
                team_names.append(f"div_{div_number}_team_{team_number}")

        return list2enum_str(team_names)


    def generate_venues_avaliability(self, n_venues, n_periods):
        venues_availability = []

        for _ in range(n_venues):
            a = np.random.randint(2, size=n_periods)
            venues_availability.append(a.astype(bool))

        return array2str(venues_availability)


    def generate_games_to_schedule(self, n_teams_per_division):
        total_n_games = self.get_total_number_of_games(n_teams_per_division)
        games_to_schedule = np.chararray((total_n_games, 2), 14)
        i = 0
        for div_number, n_teams in enumerate(n_teams_per_division, 1):
            for team_1 in range(1, n_teams):
                for team_2 in range(team_1 + 1, n_teams + 1):
                    games_to_schedule[i, 0] = f"div_{div_number}_team_{team_1}"
                    games_to_schedule[i, 1] = f"div_{div_number}_team_{team_2}"
                    i += 1
        return array2str(games_to_schedule)


    def generate_teams_time_preferences(self, n_teams, n_periods, no_cost_proportion=0.8):
        teams_time_preferences = np.full((n_teams, n_periods), 0)
        for t in range(n_teams):
            for p in range(n_periods):
                if random.random() > no_cost_proportion:
                    teams_time_preferences[t, p] = random.randint(1, 5)
        return array2array2d(teams_time_preferences)


    def get_total_number_of_games(self, n_teams_per_division):
        total_n_games = 0
        for n_teams in n_teams_per_division:
            total_n_games += n_teams * (n_teams - 1)/2
        return int(total_n_games)


    def generate_coach_names(self, n_coaches):
        coach_names = []
        for coach_number in range(1, n_coaches + 1):
            coach_names.append(f"Coach_{coach_number}")
        return list2enum_str(coach_names)


    def generate_coaches_by_team(self, n_coaches, n_teams):
        coaches_list = []
        for i in range(n_teams):
            if i < n_coaches:
                coaches_list.append(f"Coach_{i+1}")
            else:
                sampled_coach = random.randint(1, n_coaches)
                coaches_list.append(f"Coach_{sampled_coach}")
        coaches_list = str(coaches_list).replace("'", "")
        return f"array1d(TEAM_NAMES, {coaches_list})"


    def generate_dfa(self, break_duration):
        b = np.zeros((break_duration+2, 2), dtype=int)
        b[0,:] = [break_duration+2, 2]
        b[break_duration+1,:] = [break_duration+2, 2]
        for i in range(1, break_duration+1):
            b[i,:] = [i+2, 0]

        return array2str(b)


#if __name__ == "__main__":
#
#    scenarios = [
#        {
#            "name" : "toy",
#            "n_periods" : 40,
#            "n_venues" : 6,
#            "n_teams": 20,
#            "n_coaches": 25,
#            "n_teams_per_division" : [5, 5, 5, 5],
#            "break_duration" : 4
#        }]
#
#    scenario = Scenario(seed=456)
#
#    for s in scenarios:
#
#        n = s["name"]
#        p = s["n_periods"]
#        v = s["n_venues"]
#        t = s["n_teams"]
#        c = s["n_coaches"]
#        d = s["n_teams_per_division"]
#        b = s["break_duration"]
#
#        random_scenario = scenario.generate_scenario(n, p, v, t, c, d)
#       # export(n + ".dzn", random_scenario)
#        export("../models/bruno.dzn", random_scenario)
#
#        s1 = f"Q = {b+2} and replace the DFA for:\n"
#        s1 += scenario.generate_dfa(b)
#        create_file("dfa.mzn", s1)


if __name__ == "__main__":
    gen = Scenario(seed=456)
    for team_number in [50, 55]:
        name = "Sam_runs"
        n_periods =  2*team_number
        n_venues =  4
        n_coaches = team_number
        n_teams = team_number
        n_teams_per_division = [5] * (team_number // 5)
        break_duration = 1
        random_scenario = gen.generate_scenario(name, n_periods, n_venues, n_teams,
                                                n_coaches, n_teams_per_division)
        export(f"../models/{name}_{n_periods}_{n_venues}_{n_coaches}_{n_teams}.dzn", random_scenario)



