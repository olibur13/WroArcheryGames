"""
Archery game consisting defined number of ends (rounds),
each defined with distance, arrows number and scoring system.
"""
from typing import List


class GameEnd:
    def __init__(self, end_number, distance, arrows_number: int,
                 max_scoring_per_arrow: int):
        """
        Constituent of ArcheryGame, representing one end (round) of the game.

        :param end_number: int representing end's number
        :param distance: str representing distance from archer to target
        (eg.'15 m')
        :param arrows_number: int representing number of arrows shot
        at one target during one end
        :param max_scoring_per_arrow: int representing number of points
        for hitting most awarded target zone
        """
        self.end_number = end_number
        self.distance = distance
        self.arrows_number = arrows_number
        self.max_scoring_per_arrow = max_scoring_per_arrow

    @property
    def end_scoring_list(self) -> List:
        """
        :return: list of all possible scores for the end
        """
        max_score_per_end = self.arrows_number * self.max_scoring_per_arrow
        return [score for score in range(max_score_per_end, -1, -1)]


class ArcheryGame:
    """
    Archery game consisting defined number of ends (rounds),
    each defined with distance, arrows number and scoring system.
    :param ends: list of game ends (GameEnd objects)
    """
    def __init__(self, ends: List[GameEnd]):

        self.ends = ends