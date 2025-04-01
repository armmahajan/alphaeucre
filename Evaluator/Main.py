from Evaluation import Evaluation
from Logger import Logger

class Main:
    def __init__(self):
        self.logger = None
        self.evaluation = None
        self.games = [[]]

    def simulate(self, games):
        logger = Logger("euchre_log.txt")
        print("Start Simulation")
        evaluator = Evaluation(games[0][0], games[0][1], games[0][2], games[0][3], games[1], logger)
        evaluator.initiate()

    def run_auto(self, games):
        main_instance = Main()
        main_instance.simulate(games)


if __name__ == "__main__":
    player1 = ["HJ", "H1", "CA", "S9", "SK"]
    player2 = ["SQ", "H9", "CJ", "SA", "D1"]
    player3 = ["HA", "SJ", "S1", "D9", "HK"]
    player0 = ["DJ", "C9", "CQ", "DA", "DQ"]
    trump = 'DK'
    main_obj = Main()
    main_obj.run_auto([[player1, player2, player3, player0], trump])