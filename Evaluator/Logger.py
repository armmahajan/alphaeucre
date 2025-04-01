from Evaluator.MinMaxTree import Tree


class Logger:
    def __init__(self, filename="game_log.txt"):
        self.tree = Tree()  # MinMaxTree to manage game states

    # Create log
    def log_hand(self, trump, winner, score, history):
        log = {
            "trump": trump,
            "winner": winner,
            "score": score,
            "history": history,
        }
        self.tree.ingest_log(log)
        #print(f"Logged trick: {log}")


    def minmax_trees(self):
        print(f"Getting best move path for each root...")
        return self.tree.minmax_roots()