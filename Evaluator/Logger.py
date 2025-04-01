from Evaluator.MinMaxTree import Tree


class Logger:
    def __init__(self, filename="game_log.txt"):
        self.tree = Tree()  # MinMaxTree to manage game states

    # Create log
    def log_hand(self, trump, winner, score, history):
        """
        Add a trick to the current setup and feed the logs to the tree for dynamic updates.

        Args:
            trump (str): The current trump suit (e.g., "D", "H").
            winner (int): The ID of the team/player who won this setup.
            score (list): Scores for both teams, e.g., [2, 3].
            history (list): List of tuples representing cards played (e.g., [("SQ", 0), ("DJ", 1)]).
        """
        log = {
            "trump": trump,
            "winner": winner,
            "score": score,
            "history": history,
        }
        self.tree.ingest_log(log)  # Send log to tree
        #print(f"Logged trick: {log}")


    def view_tree(self, file_path):
        """
        Displays the current structure of the game tree.
        """
        self.tree.print_tree(file_path)


    def minmax(self):
        """
        Finds the best next step for the given team based on the MinMax algorithm.

        Args:
            maximizing_team (bool): True for maximizing player/team, False for minimizing.

        Returns:
            dict: The best move (or game state node) found by MinMax.
        """
        print(f"Calculating best moves for each team...")
        return self.tree.minmax_roots()