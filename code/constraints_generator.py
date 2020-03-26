#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 19:18:11 2020

@author: Samuel_Levesque
"""
import datetime
import random
import pandas

class ConstraintsGenerator:
    """ Class that generates random fictive scenarios for sports tournaments. """
    def __init__(self, seed):
        random.seed(seed)

    def generate_scenario(self, divisions_size,
                          n_shared_coaches, game_length,
                          venue_n_courts, date_start):
        self.game_length = game_length
        self.divisions_size = divisions_size
        self.number_of_games = self._calculate_n_games(divisions_size)

        self.teams = self._generate_teams(divisions_size, n_shared_coaches)
        self.court_availabilities = self._generate_court_availabilities(
                venue_n_courts,
                date_start,
                game_length,
                self.number_of_games)

    def _calculate_n_games(self, divisions_size):
        n_games = 0
        for div_size in divisions_size:
            n_games += div_size*(div_size-1)/2
        return n_games

    def _share_coaches(self, teams_table, n_shared_coaches):
        """
        Randomly takes n_shared_coaches and also assigns him/her to a team in another division
        """
        for _ in range(n_shared_coaches):
            chosen_index = random.choice(teams_table.index)
            busy_coach = teams_table.loc[chosen_index, "Coach Name"]
            division = teams_table.loc[chosen_index, "Division Name"]
            other_index = random.choice(teams_table[teams_table["Division Name"] != division].index)
            teams_table.loc[other_index, "Coach Name"] = busy_coach
        return teams_table

    def _generate_teams(self, divisions_sizes, n_shared_coaches=0):
        """ Generates a table containing all teams with their division + coach """
        teams_table = pandas.DataFrame(columns=["Team Name", "Division Name", "Coach Name"])
        index = 0
        for division_number, division_size in enumerate(divisions_sizes):
            for team_number in range(division_size):
                teams_table.loc[index, "Team Name"] = f"Div{division_number} Team {team_number}"
                teams_table.loc[index, "Division Name"] = f"Division {division_number}"
                teams_table.loc[index, "Coach Name"] = f"Coach {index}"
                index += 1
        teams_table = self._share_coaches(teams_table, n_shared_coaches)

        return teams_table

    def _generate_available_venues(self, venue_n_courts):
        available_venues = pandas.DataFrame(columns=["Venue", "Court"])
        index = 0
        for venue_number, n_courts in enumerate(venue_n_courts):
            for court_number in range(n_courts):
                available_venues.loc[index, "Venue"] = f"Venue {venue_number}"
                available_venues.loc[index, "Court"] = f"Court {court_number}"
                index += 1
        return available_venues

    def _generate_court_availabilities(self, venue_n_courts, date_start, game_length, n_games):
        available_game_spots = 0
        available_venues = self._generate_available_venues(venue_n_courts)
        availabilities = pandas.DataFrame(columns=["Venue", "Court", "Date", "Time Start", "Time End"])
        date = date_start
        index = 0
        while available_game_spots < n_games:
            for _, available_venue in available_venues.iterrows():
                bod = date.replace(hour=8, minute=0)
                eod = date.replace(hour=23, minute=0)
                last_start = bod
                latest_start = eod - datetime.timedelta(minutes=game_length)
                last_end = last_start
                while last_start < latest_start and last_end < latest_start:
                    last_start = random_between_two_times(
                            last_start,
                            latest_start,
                            rounding_method="floor")
                    last_end = random_between_two_times(
                            last_start + datetime.timedelta(minutes=game_length),
                            eod,
                            rounding_method="ceiling")
                    index += 1
                    availabilities.loc[index, "Venue"] = available_venue["Venue"]
                    availabilities.loc[index, "Court"] = available_venue["Court"]
                    availabilities.loc[index, "Date"] = date.strftime("%Y-%m-%d")
                    availabilities.loc[index, "Time Start"] = last_start.strftime("%Hh%M")
                    availabilities.loc[index, "Time End"] = last_end.strftime("%Hh%M")
                    available_game_spots += ((last_end - last_start).seconds/60.0) // game_length
                    if available_game_spots >= n_games:
                        break
                if available_game_spots >= n_games:
                    break

            date += datetime.timedelta(days=1)
        return availabilities

def random_between_two_times(time_start, time_end, rounding_method="floor"):
    time_diff = time_end - time_start
    random_time = time_start + datetime.timedelta(seconds=random.randint(0, time_diff.seconds))
    if rounding_method == "floor":
        random_time = random_time - datetime.timedelta(
                minutes=random_time.minute % 5,
                seconds=random_time.second,
                microseconds=random_time.microsecond)
    elif rounding_method == "ceiling":
        random_time = random_time - datetime.timedelta(
                minutes=random_time.minute % 5 + 5,
                seconds=random_time.second,
                microseconds=random_time.microsecond)
    return random_time


if __name__ == "__main__":
    seed = 123
    game_length = 60  # minutes
    teams_per_division = [6, 6, 6, 6]
    shared_coaches = 3
    venue_n_courts = [1, 2]
    date_start = datetime.datetime(2020, 3, 25)
    constraints_generator = ConstraintsGenerator(seed)

    constraints_generator.generate_scenario(teams_per_division,
                          shared_coaches, game_length,
                          venue_n_courts, date_start)

    print(constraints_generator.court_availabilities)


