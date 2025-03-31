import copy


class Node:
    # Node Class to implement a tree structure
    def __init__(self, trump, winner, score, cards):
        self.trump = trump
        self.winner = winner
        self.score = score
        self.cards = cards  # Cards played in the trick
        self.children = []  # Possible next game states

    # Add child to node
    def add_child(self, child_node):
        self.children.append(child_node)

    # Remove child from node
    def remove_child(self, child_node):
        self.children.remove(child_node)

    # Get Child from node
    def get_child(self):
        return self.children

    # Check if nodes child has child
    def child_has_child(self):
        for child in self.children:
            if child.children:
                return True
            else:
                return False

    def __repr__(self):
        return (f"Trump: {self.trump}, Winner: {self.winner}, "
                f"Score: {self.score}, Cards: {self.cards}")


class Tree:
    # Tree for minmax
    def __init__(self):
        self.roots = []  # Stores all root nodes (one root per starting trick)
        self.best_path = []
        self.best_score = 0
        self.suboptimal_path = []

    # Take a log, create a node and add to the tree
    def ingest_log(self, log):
        # Checking if log is root
        previous_node = None
        first_trick = [f"{card} (P{player % 4})" for card, player in log["history"][0]]

        # If root is matched, continue from child
        for root in self.roots:
            if first_trick == root.cards:
                previous_node = root
                log["history"].pop(0)
                break

        # Process each trick in the log's history
        for trick in log["history"]:
            update = True
            # Create a node for the current trick
            node = Node(
                trump=log["trump"],
                winner=log["winner"],
                score=log["score"],
                cards=[f"{card} (P{player % 4})" for card, player in trick]
            )
            # Creating new root
            if previous_node is None:
                # First trick (starting trick) -> new root
                self.roots.append(node)
                previous_node = node
                continue
            # If child is matched, continue from child
            for child in previous_node.children:
                if node.cards == child.cards:
                    previous_node = child
                    update = False
                    break
            # Adding child to node if child does not yet exist
            if update:
                previous_node.add_child(node)
                # Update the previous node pointer
                previous_node = node


    def evaluate(self, node):
        # Could evaluate on hand control as well
        #   Immediate and future hand control
        # Additionally could include leaf win dispersion ratio -> would be in _find_best()
        return node.score[0] - node.score[1]  # Difference between the teams


    def minmax_roots(self, max_depth=5):
        best_game_paths = []

        # Iterate through all possible roots
        for root in copy.deepcopy(self.roots):
            # Start recursion
            paths = self._minmax(root, [root])
            best_game_paths += [paths]

        # Return best path for each root
        return best_game_paths


    def _minmax(self, node, path):
        # Base case: Max depth reached or no children
        if not node.children:
            return path

        # Finding last tricks winner
        winner = int(node.children[0].cards[0][5])

        # Recursively explore children through minmax
        paths = []
        update_node = node
        # For each player
        for i in range(0, 4):
            self.best_score = 0
            self.best_path = []
            # Find the best final game state
            self._find_best(update_node, (winner + i) % 2, [])
            # If only remaining option is suboptimal for a team
            if not self.best_path:
                self.best_path = self.suboptimal_path

            # Iterate through nodes children and eliminate non-prospects
            for child in update_node.children[:]:
                if child.cards[i][:2] != self.best_path[1].cards[i][:2]:
                    update_node.remove_child(child)

        # Ensure only one child remains
        if len(update_node.get_child()) == 1:
            new_node = update_node.get_child()[0]
        elif len(update_node.get_child()) == 0:
            print("Error: No children left")
            exit(0)
        else:
            print("Error: More than one child left")
            exit(0)

        # Return node and path to node in recursive call
        return self._minmax(new_node, path + [new_node])


    def _find_best(self, node, team, path):
        # If node has children
        if node.children:
            # If nodes children are not the leafs
            if node.child_has_child():
                # Iterate through all children recursively
                for child in node.children:
                    self._find_best(child, team, path + [node])
            # Else nodes children are leafs
            else:
                # Iterate through all children and evaluate their game state
                for child in node.children:
                    score = self.evaluate(child)
                    # If team 0 maximizing and score beats best score
                    if team == 0:
                        if score > self.best_score:
                            self.best_score = score
                            self.best_path = path + [node] + [child]
                        self.suboptimal_path = path + [node] + [child]
                    # If team 1 maximizing and score beats best score
                    else:
                        if score < self.best_score:
                            self.best_score = score
                            self.best_path = path + [node] + [child]
                        self.suboptimal_path = path + [node] + [child]


    def print_tree(self, file_path):
        # Open file for writing
        with open(file_path, "w") as file:
            file.write("Game Tree:\n")
            # For root print tree
            for idx, root in enumerate(self.roots, start=1):
                file.write(f"Root {idx}: {root}\n")  # Write root info
                self._print_children(root, file, level=1)

            file.close()

    def _print_children(self, node, file, level):
        # For child, print child
        for child1 in node.children:
            file.write(f"{' ' * (2 * level)}-> {child1}\n")
        # For child, find all children
        for child2 in copy.deepcopy(node.children):
            file.write(f"{' ' * (2 * level)}-> Exploring: {child2}\n")
            self._print_children(child2, file, level + 1)



