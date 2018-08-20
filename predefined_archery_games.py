"""
This file contains ArcheryGames objects - for archery games with fixed
ends and scoring and functions for creating predefined archery games
that can be influenced by the user.
"""
from typing import List
from archery_game import GameEnd, ArcheryGame


class LigaEnd(GameEnd):
    def __init__(self, end_number: int, distance: str, archer_position: str,
                 target: str, arrows_number=6, max_scoring_per_arrow=5):
        """
        GameEnd modified for 'liga'. Fixed arrows number and scoring system.
        Added properties for archer position and target.

        :param end_number: int representing end's number
        :param distance: str representing distance from archer to target
        (eg.'15 m')
        :param archer_position: str representing body position of the archer
        :param target: str representing position of face target
        :param arrows_number: int representing number of arrows shot
        at one target during one end -> default 6
        :param max_scoring_per_arrow: int representing number of points
        for hitting most awarded target zone -> default 5

        Inherited end_scoring_list property method.
        """
        super().__init__(end_number, distance, arrows_number,
                         max_scoring_per_arrow)
        self.archer_position = archer_position
        self.target = target


LIGA = ArcheryGame([LigaEnd(1, '15 m', 'tradycyjna', 'górna'),
                    LigaEnd(2, '20 m', 'tradycyjna', 'górna'),
                    LigaEnd(3, '25 m', 'tradycyjna', 'górna'),
                    LigaEnd(4, '15 m', 'klęcząc', 'górna'),
                    LigaEnd(5, '20 m', 'tradycyjna', 'dolna'),
                    LigaEnd(6, '25 m', 'tradycyjna', 'dolna'),
                    LigaEnd(7, '15 m', 'tyłem', 'górna'),
                    LigaEnd(8, '20 m', 'tyłem', 'górna'),
                    LigaEnd(9, '15 m', 'tradycyjna', 'dolna'),
                    LigaEnd(10, '20 m', 'klęcząc', 'górna')])


class SciezkaEnd(GameEnd):
    def __init__(self, end_number: int, distance: List, arrows_number: int,
                 max_scoring_per_arrow: int):
        '''
        Constituent of ArcheryGame, modified for `ścieżka łucznicza`.

        :param end_number: int representing end's number
        :param distance: list of str representing positions of marker
         for archer for the end's target
        :param arrows_number: int representing number of arrows shot
        from each marker to target during one end
        :param max_scoring_per_arrow: int representing number of points
        for hitting most awarded target zone
        '''
        super().__init__(end_number, distance, arrows_number,
                         max_scoring_per_arrow)

    @property
    def end_scoring_list(self) -> List:
        """
        :return: list of all possible scores for the end
        taking into consideration the distances (markers).
        """
        max_score_per_end = self.arrows_number * self.max_scoring_per_arrow \
                            * len(self.distance)
        return [score for score in range(max_score_per_end, -1, -1)]


def create_sciezka(distances: List, arrows_number: int,
                   max_scoring_per_arrow: int) -> ArcheryGame:
    """
    :return: ArcheryGame for `ścieżka łucznicza` of 14 different targets along.
    Distances, arrows number and scoring system are chosen by the user.
    """
    sciezka = ArcheryGame([
        SciezkaEnd(x, distances, arrows_number, max_scoring_per_arrow)
        for x in range(1, 15)
        ])
    return sciezka