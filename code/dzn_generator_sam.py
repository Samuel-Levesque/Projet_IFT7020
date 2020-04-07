import numpy
import random
from code.dzn_formatter import array2str
from code.dzn_formatter import list2enum_str
from code.dzn_formatter import array2array2d


def generate_team_names(n_teams_per_division):
    team_names = []
    for div_number, n_teams in enumerate(n_teams_per_division, 1):
        for team_number in range(1, n_teams+1):
            team_names.append(f"Div_{div_number}_Team_{team_number}")

    return list2enum_str(team_names)


def generate_games_to_schedule(n_teams_per_division):
    total_n_games = get_total_number_of_games(n_teams_per_division)
    games_to_schedule = numpy.chararray((total_n_games, 2), 14)
    i = 0
    for div_number, n_teams in enumerate(n_teams_per_division, 1):
        for team_1 in range(1, n_teams):
            for team_2 in range(team_1 + 1, n_teams + 1):
                games_to_schedule[i, 0] = f"Div_{div_number}_Team_{team_1}"
                games_to_schedule[i, 1] = f"Div_{div_number}_Team_{team_2}"
                i += 1
    return array2str(games_to_schedule)


def generate_teams_time_preferences(n_teams, n_periods, no_cost_proportion=0.8):
    teams_time_preferences = numpy.full((n_teams, n_periods), 0)
    for t in range(n_teams):
        for p in range(n_periods):
            if random.random() > no_cost_proportion:
                teams_time_preferences[t, p] = random.randint(1, 5)
    return array2array2d(teams_time_preferences)


def get_total_number_of_games(n_teams_per_division):
    total_n_games = 0
    for n_teams in n_teams_per_division:
        total_n_games += n_teams * (n_teams - 1)/2
    return int(total_n_games)


def generate_coach_names(n_coaches):
    coach_names = []
    for coach_number in range(1, n_coaches + 1):
        coach_names.append(f"Coach_{coach_number}")
    return list2enum_str(coach_names)


def generate_coaches_by_team(n_coaches, n_teams):
    coaches_list = []
    for i in range(n_teams):
        if i < n_coaches:
            coaches_list.append(f"Coach_{i+1}")
        else:
            sampled_coach = random.randint(1, n_coaches)
            coaches_list.append(f"Coach_{sampled_coach}")
    coaches_list = str(coaches_list).replace("'", "")
    return f"array1d(TEAM_NAMES, {coaches_list})"


if __name__ == "__main__":
    random.seed(456)
    n_teams = 6
    n_periods = 4
    n_coaches = 4
    n_teams_per_division = [3, 3]
    games_to_schedule = generate_games_to_schedule(n_teams_per_division)
    print(games_to_schedule)
    team_names = generate_team_names(n_teams_per_division)
    print(team_names)
    team_time_preferences = generate_teams_time_preferences(n_teams, n_periods)
    print(team_time_preferences)
    coach_names = generate_coach_names(n_coaches)
    print(coach_names)
    coaches_by_team = generate_coaches_by_team(n_coaches, n_teams)
    print(coaches_by_team)
