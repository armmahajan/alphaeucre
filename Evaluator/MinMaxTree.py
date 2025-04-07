import copy
from importlib.metadata import distribution


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
        self.win_count = 0
        self.end_states = 0

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


    def evaluate(self, child, team, path):
        self.win_count = 0
        self.end_states = 0

        #print(f"Evaluating {child} with path {path}")

        root_node = path[0]
        imm_control = 0
        future_control = 0
        if root_node.child_has_child():
            for child in root_node.children:
                grand_child = child.get_child()[0]
                if int(grand_child.cards[0][5]) % 2 == int(child.cards[0][5]) % 2:
                    if int(child.cards[0][5]) % 2 == 0:
                        imm_control += 1
                    else:
                        imm_control -= 1
                for grand_grandchild in grand_child.children:
                    if int(grand_grandchild.cards[0][5]) % 2 == int(grand_child.cards[0][5]) % 2:
                        if int(grand_grandchild.cards[0][5]) % 2 == 0:
                            future_control += 1
                        else:
                            future_control -= 1
            imm_control /= len(root_node.children)
            future_control /= sum(len(child.children) for child in root_node.children)

            imm_control *= 1.2
            future_control *= 0.8
        else:
            imm_control = 0.9
            future_control = 0.5

        # Get win ratio and dispersion metrics
        self._get_win_ratio(root_node)
        win_ratio = self.win_count / self.end_states
        #dispersion_penalty = self._get_win_dispersion(root_node)

        # Dynamic weighting
        depth_weight = max(0.45, 1 - len(path) / 7)
        control_weight = 1 - depth_weight

        # Final evaluation
        score_component = (child.score[0] - child.score[1]) * win_ratio * depth_weight
        control_component = (imm_control + future_control) * control_weight

        #print(f"Score Calculated: {score_component + control_component}")

        return score_component + control_component


    def _get_win_ratio(self, node):
        #print(f"Getting win ratio for {node}")
        if not node.children:
            self.win_count += node.score[0] - node.score[1]
            self.end_states += 1
            return

        for child in node.children:
            self._get_win_ratio(child)


    def minmax_roots(self):
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
        #print(f"Finding best game for {node} with path {path}")
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
                    score = self.evaluate(child, team, path + [node])
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