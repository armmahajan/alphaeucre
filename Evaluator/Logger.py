from Evaluator.MinMaxTree import Tree


class Logger:
    def __init__(self, filename="game_log.txt"):
        #self.tree = Tree()
        self.filename = filename
        self.logs = []

    # Create log
    def log_hand(self, trump, history, winner, score, trick):
        print("Saving Hand")
        self.logs.append({
            "trump": trump,
            "history": history,
            "winner": winner,
            "score": score,
            "trick": trick
        })

    # Write to JSON
    def save_logs(self):
        print("Writing Logs")

        #for log in enumerate(self.logs):
            #tree.ingest(log)



        # Write to JSON file
        with open(self.filename, "w") as f:
            # Print logs in a readable format
            f.write("\n=== Trick History ===\n")
            for i, log in enumerate(self.logs):
                f.write(f"\nTrick {i + 1} (Trump: {log['trump']}, Winner: {log['winner']}, Score: {log['score']}, Trick: {log['trick']})\n")
                for play in log["history"]:
                    trick_str = " | ".join([f"{card} (P{player % 4})" for card, player in play])
                    trick_str += '\n'
                    f.writelines(trick_str)
                f.write("\n" + "-" * 50)  # Separator between tricks


    # Clears log
    # Runs if hand is obsolete
    def clear_logs(self):
        self.logs = []