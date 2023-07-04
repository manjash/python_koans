#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from random import choice
from string import ascii_lowercase

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

from runner.koan import *
from koans.about_dice_project import DiceSet
from koans.about_scoring_project import score


class Player:
    def __init__(self):
        self.accumulated_score = 0
        self.turn_accumulated_score = 0
        self.can_accumulate = False
        self.name = ''.join(choice(ascii_lowercase) for i in range(6))


class Game:
    def __init__(self, n):
        self.n_players = n
        self.players = [Player() for p in range(n)]

    @staticmethod
    def non_scoring_dice(roll_values):
        stats = defaultdict(int)
        count = 0
        for v in roll_values:
            stats[v] += 1
        for k, v in stats.items():
            if k in [2, 3, 4, 6] and v < 3:
                count += v
        if count == 0:
            count = 5
        return count

    def ordinary_round(self):
        dice = DiceSet()
        for player in self.players:
            # initial roll per turn
            dice_left = 5
            what_next = "roll"
            turn_accumulated_score = 0
            while dice_left > 0 and what_next == "roll":
                dice.roll(dice_left)
                roll_score = score(dice.values)
                dice_left = self.non_scoring_dice(dice.values)
                # print(player.name,
                #       f"{dice.values}",
                #       f"dice left: {dice_left},",
                #       f"can_accumulate: {player.can_accumulate},",
                #       f"roll_score: {roll_score},",
                #       f"accum_score: {player.accumulated_score},",
                #       f"turn_accum_score: {turn_accumulated_score}",
                #       )
                if not player.can_accumulate and roll_score >= 300:
                    player.can_accumulate = True
                if player.can_accumulate:
                    if roll_score > 0:
                        turn_accumulated_score += roll_score

                        what_next = input(f"--> Want to roll or pass? You have {dice_left} dice left\n")
                        if what_next == "roll":
                            continue
                        elif what_next == "pass":
                            player.accumulated_score += turn_accumulated_score
                            # print("Turn res for",
                            #       player.name,
                            #       f"dice left: {dice_left},",
                            #       f"can_accumulate: {player.can_accumulate},",
                            #       f"roll_score: {roll_score},",
                            #       f"accum_score: {player.accumulated_score},",
                            #       f"turn_accum_score: {turn_accumulated_score}\n",
                            #       )
                            if player.accumulated_score >= 3000:
                                return self.final_round()
                    else:
                        break
                else:
                    break
        self.ordinary_round()

    def final_round(self):
        dice = DiceSet()
        max_score = 0
        winner = ""
        for player in self.players:
            dice.roll(5)
            player.accumulated_score += score(dice.values)
            if max_score < player.accumulated_score:
                max_score, winner = player.accumulated_score, player.name
        # res = ''
        # for p in self.players:
        #     res += f"{p.name}: {p.accumulated_score}, "
        # print(f"All: {res[:-2]}")
        # print(winner, max_score)
        return winner, max_score


class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py

    def test_non_scoring_dice(self):
        game = Game(3)
        self.assertEqual(game.non_scoring_dice([1, 1, 1, 2, 3]), 2)
        self.assertEqual(game.non_scoring_dice([1, 1, 5, 2, 3]), 2)
        self.assertEqual(game.non_scoring_dice([1, 6, 5, 2, 3]), 3)
        self.assertEqual(game.non_scoring_dice([3, 6, 5, 2, 3]), 4)
        self.assertEqual(game.non_scoring_dice([3, 3, 3, 1, 5]), 5)
        self.assertEqual(game.non_scoring_dice([2, 3, 4, 3, 6]), 5)

    def test_extra_credit_task(self):
        pass
        # game = Game(3)
        # print(game.ordinary_round())
