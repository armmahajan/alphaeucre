from Evaluation import Evaluation
from Logger import Logger

class Main:
    def __init__(self):
        self.logger = None
        self.evaluation = None
        self.games = [[]]

    def simulate(self, games):
        logger = Logger()
        print("Start Simulation")
        evaluator = Evaluation(games[0][0], games[0][1], games[0][2], games[0][3], games[1], logger)
        evaluator.initiate()

    def run_auto(self, games):
        main_instance = Main()
        main_instance.simulate(games)


if __name__ == "__main__":
    # OG Test -> runs one simulation
    player1 = ["HJ", "H1", "CA", "S9", "SK"]
    player2 = ["SQ", "H9", "CJ", "SA", "D1"]
    player3 = ["HA", "SJ", "S1", "D9", "HK"]
    player0 = ["DJ", "C9", "CQ", "DA", "DQ"]
    trump = 'DK'


    # Evaluation Test -> even hands
    '''player1 = ["SA", "S1", "HA", "DQ", "CK"]
    player2 = ["SJ", "HQ", "DK", "C1", "CA"]
    player3 = ["S9", "DA", "DJ", "C9", "CQ"]
    player0 = ["SQ", "CJ", "H9", "HK", "D1"]
    trump = 'SK'
    '''

    # Evaluation Test -> infinite recursion while searching for the 7th root's best path
    '''player1 = ["H9", "S1", "HA", "DQ", "CK"]
    player2 = ["SA", "HQ", "DK", "C1", "CA"]
    player3 = ["S9", "DA", "DJ", "C9", "CQ"]
    player0 = ["SQ", "CJ", "SJ", "HK", "D1"]
    trump = 'SK'
    '''
    main_obj = Main()
    main_obj.run_auto([[player0, player1, player2, player3], trump])