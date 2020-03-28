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
                          venue_n_courts, date_start,
                          n_time_restrictions, n_venue_restrictions):
        self.game_length = game_length
        self.divisions_size = divisions_size
        self.number_of_games = self._calculate_n_games(divisions_size)

        self.teams = self._generate_teams(divisions_size, n_shared_coaches)
        self.court_availabilities = self._generate_court_availabilities(
                venue_n_courts,
                date_start,
                game_length,
                self.number_of_games)

        self.teams_time_restrictions = self._generate_time_restrictions(n_time_restrictions)
        self.teams_venue_restrictions = self._generate_venue_restrictions(n_venue_restrictions)

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
                            last_end,
                            latest_start,
                            rounding_method="floor")
                    last_end = random_between_two_times(
                            last_start + datetime.timedelta(minutes=game_length+5),
                            eod,
                            rounding_method="ceiling")
                    index += 1
                    availabilities.loc[index, "Venue"] = available_venue["Venue"]
                    availabilities.loc[index, "Court"] = available_venue["Court"]
                    availabilities.loc[index, "Date"] = date#.strftime("%Y-%m-%d")
                    availabilities.loc[index, "Time Start"] = last_start#.strftime("%Hh%M")
                    availabilities.loc[index, "Time End"] = last_end#.strftime("%Hh%M")
                    available_game_spots += ((last_end - last_start).seconds/60.0) // game_length
                    if available_game_spots >= n_games:
                        break
                if available_game_spots >= n_games:
                    break

            date += datetime.timedelta(days=1)
        return availabilities

    def _generate_time_restrictions(self, n_restrictions):
        """
        Restrictions are defined using the following format:
            Team: Team name for which we want to apply constraint
            Date: Date for which we want to apply the constraint
            Constraint Type: Before/After. If before, the team prefers NOT to play before
                specified time. If after, the team preferes NOT to play after specified time
            Constraint Time: Time threshold used to define the constraint.
        """
        time_restrictions = pandas.DataFrame(columns=["Team", "Date", "Constraint Type", "Constraint Time"])
        teams = self.teams["Team Name"].unique().tolist()
        dates = self.court_availabilities["Date"].unique().tolist()
#        dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]
        applied_constraints = {}
        n_applied_constraints = 0
        while n_applied_constraints < n_restrictions:
            chosen_team = random.choice(teams)
            chosen_date = random.choice(dates)
            lookup_key = (chosen_team, chosen_date)
            earliest_time = chosen_date.replace(hour=8, minute=0)
            latest_time = chosen_date.replace(hour=23, minute=0)
            # Look if constraint was already applied on this team/date
            if lookup_key in applied_constraints:
                previous_constraints = applied_constraints[(chosen_team, chosen_date)]
                if len(previous_constraints) > 1:
                    # No more than 2 constraints per team/date
                    continue
                if previous_constraints[0][0] == "before":
                    constraint_type = ["after"]
                    constraint_time = random_between_two_times(
                            earliest_time,
                            previous_constraints[0][1],
                            rounding_method="ceiling")
                elif previous_constraints[0][0] == "after":
                    constraint_type = ["before"]
                    constraint_time = random_between_two_times(
                            previous_constraints[0][1],
                            latest_time,
                            rounding_method="floor")
            else:
                constraint_type = random.choice(["before", "after"])
                if constraint_type == "before":
                    constraint_time = random_between_two_times(
                            earliest_time,
                            latest_time,
                            "ceiling")
                elif constraint_type == "after":
                    constraint_time = random_between_two_times(
                            earliest_time,
                            latest_time,
                            "floor")

            time_restrictions.loc[n_applied_constraints, "Team"] = chosen_team
            time_restrictions.loc[n_applied_constraints, "Date"] = chosen_date
            time_restrictions.loc[n_applied_constraints, "Constraint Type"] = constraint_type
            time_restrictions.loc[n_applied_constraints, "Constraint Time"] = constraint_time

            # Updating applied_constraints dict
            if lookup_key in applied_constraints:
                applied_constraints[lookup_key].append((constraint_type, constraint_time))
            else:
                applied_constraints[lookup_key] = [(constraint_type, constraint_time)]

            n_applied_constraints += 1

        return time_restrictions

    def _generate_venue_restrictions(self, n_restrictions):
        pass

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
    n_time_constraints = 10
    n_venue_constraints = 5

    constraints_generator = ConstraintsGenerator(seed)

    constraints_generator.generate_scenario(teams_per_division,
                          shared_coaches, game_length,
                          venue_n_courts, date_start,
                          n_time_constraints, n_venue_constraints)

    print(constraints_generator.court_availabilities)
    print(constraints_generator.teams_time_restrictions)

