import copy
import itertools


class Evaluation:
    def __init__(self, player0, player1, player2, player3, trump, logger):
        # Saving highest win score for best moves
        self.offense_win = 0
        self.defence_win = 0
        self.player0 = player0
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.players = [self.player1, self.player2, self.player3, self.player0]
        self.trump = trump[0]
        self.trump_flipped = trump
        self.logger = logger
        self.cards = {
            "H9": 1, "H1": 2, "HJ": 3, "HQ": 4, "HK": 5, "HA": 6,
            "D9": 1, "D1": 2, "DJ": 3, "DQ": 4, "DK": 5, "DA": 6,
            "S9": 1, "S1": 2, "SJ": 3, "SQ": 4, "SK": 5, "SA": 6,
            "C9": 1, "C1": 2, "CJ": 3, "CQ": 4, "CK": 5, "CA": 6}

    def initiate(self):
        save = []

        setups = self.valid_setups()

        for i, setup in enumerate(setups):
            output_file = f"BestGames - {setup[0]} {setup[1]} {i}.txt"
            sum_score = [0, 0]
            count_score = 0
            if setup[0] == 'O':
                print("Simulating")
                offense0 = False
                offense1 = False

                cards = self.set_trump(setup[1])
                # Initiate recursive simulator
                self.simulate([self.player1, self.player2, self.player3, setup[2]], 1, [], 0, [0, 0], cards)

                # MinMax Tree to get best move set
                print("\n\n*********** MinMax Tree ***********\n\n")
                games = self.logger.minmax_trees()

                # Getting make options for score orientation
                if self.valid_pick_up(0):
                    offense0 = True
                elif self.valid_pick_up(2):
                    offense0 = True
                if self.valid_pick_up(3):
                    offense1 = True
                # Orientated score
                if offense0 and offense1:
                    score = "Both Offence and Defence -> Equivalent Games"
                elif offense0:
                    score = "Defence, Offence"
                elif offense1:
                    score = "Offence, Defence"

                for j, game in enumerate(games):
                    print(f"\n\n*********** Best Game for Tree: {j} | Score = [{score}] ***********\n\n")
                    print(game)
                    for trick in game:
                        save.append(trick.cards)
                    save.append(game[4].score)
                    sum_score[0] += game[4].score[0]
                    sum_score[1] += game[4].score[1]
                    count_score += 1

                with open(output_file, "w") as file:
                    file.write(f"*********** Best Game's | Score = [{score}] ***********\n\n")
                    for j, s in enumerate(save, 1):
                        file.write(f"{s}")
                        if j % 6 == 0 and j != 0:
                            file.write("\n")
                        else:
                            file.write(", ")
                    file.write(f"\n\n*********** Average Score = [{score} = {sum_score[0] / count_score}, {sum_score[1] / count_score}] ***********\n\n")
                file.close()

            elif setup[0] == 'M':
                print("Simulating")
                cards = self.set_trump(setup[1])
                self.simulate([self.player1, self.player2, self.player3, self.player0], 1, [], 0, [0, 0], cards)

                # MinMax Tree to get best move set
                print("\n\n*********** MinMax Tree ***********\n\n")
                games = self.logger.minmax_trees()

                # Getting score orientation
                if setup[2] == 0:
                    score = "Offence, Defense"
                else:
                    score = "Defence, Offence"

                # Printing games
                for j, game in enumerate(games):
                    print(f"\n\n*********** Best Game for Tree: {j} | Score = [{score}] ***********\n\n")
                    print(game)
                    for trick in game:
                        save.append(trick.cards)
                    save.append(game[4].score)
                    sum_score[0] += game[4].score[0]
                    sum_score[1] += game[4].score[1]
                    count_score += 1

                with open(output_file, "w") as file:
                    file.write(f"*********** Best Game's | Score = [{score}] ***********\n\n")
                    for j, s in enumerate(save, 1):
                        file.write(f"{s}")
                        if j % 6 == 0 and j != 0:
                            file.write("\n")
                        else:
                            file.write(", ")
                    file.write(f"\n\n*********** Average Score = [{score} = {sum_score[0] / count_score}, {sum_score[1] / count_score}] ***********\n\n")
                file.close()
            else:
                print("Error: Invalid setup")
            self.reset_ranks()



        print("Completed all setup options")


    def valid_setups(self):
        # List of valid setups
        setup = []
        # Part of hand evaluation, not implemented
        score = 0

        # Only need to consider one of these as they all result in the same setup
        # If player1 orders up player0
        if self.valid_order_up(0):
            # Check which cards to get rid of
            hand0 = self.discard()
            setup.append(('O', self.trump, hand0))
        # Elif player3 orders up player0
        elif self.valid_order_up(2):
            # Check which cards to get rid of
            hand0 = self.discard()
            setup.append(('O', self.trump, hand0))
        # Elif player0 picks up the flipped card
        elif self.valid_pick_up(3):
            # Check which cards to get rid of
            hand0 = self.discard()
            setup.append(('0', self.trump, hand0))

        # If trump was turned down, go in a circle deciding trump
        for i in range(4):
            options = self.make_trump(i)
            if options:
                for option in options:
                    setup.append(('M', option, i % 2))
        return setup


    def simulate(self, hands, lead, history, trick, score, cards):
        player_legal_moves = [[], [], [], []]
        to_follow_legal_moves = [[], [], []]
        in_play = []

        # Copy hands
        new_hands = copy.deepcopy(hands)
        new_history = copy.deepcopy(history)
        new_score = copy.deepcopy(score)
        new_lead = copy.deepcopy(lead)

        # Check if hand is over
        if sum(score) >= 5:
            # Finish game and check if it should be logged
            self.win_hand(new_score, new_history)
            return

        # Get lead player's legal moves
        lead_legal_moves = self.legal_moves(hands[lead], '')

        for i, move in enumerate(lead_legal_moves):
            new_hands = copy.deepcopy(hands)
            new_lead = copy.deepcopy(lead)
            in_play.clear()
            in_play.append(move)

            zero_index = 0
            # Determine legal moves of remaining players
            for k in range(new_lead + 1, new_lead + 4):
                index = k % 4
                player_legal_moves[index] = self.legal_moves(hands[index], move)
                # For combination generation
                to_follow_legal_moves[zero_index] = player_legal_moves[index]
                zero_index += 1

            # Generate all possible combinations of plays
            combinations = itertools.product(*[range(len(m)) for m in to_follow_legal_moves])
            for combination in combinations:
                new_hands = copy.deepcopy(hands)
                new_lead = copy.deepcopy(lead)
                new_player_legal_moves = copy.deepcopy(player_legal_moves)

                zero_index = 0
                # Iterate through remaining plays to get all combinations of tricks
                for j in range(new_lead + 1, new_lead + 4):
                    index = j % 4
                    player_move = new_player_legal_moves[index][combination[zero_index]]
                    in_play.append(player_move)
                    zero_index += 1

                for k, card in enumerate(in_play):
                    new_hands[(k + new_lead) % 4].remove(card)

                # Update card ranks based on card led
                new_cards = self.update_ranks(in_play[0])
                # Evaluate the winner
                winner = self.win_play(in_play)

                # Count win
                if (winner + new_lead) % 2 == 0:
                    score0 = new_score[0] + 1
                    score1 = new_score[1]
                else:
                    score0 = new_score[0]
                    score1 = new_score[1] + 1

                # Record round
                current_history = [[in_play[0], new_lead], [in_play[1], new_lead + 1], [in_play[2], new_lead + 2], [in_play[3], new_lead + 3]]
                # Check if hand is over
                if sum(score) + 1 >= 5:
                    # Finish game and check if it should be logged
                    self.win_hand([score0, score1], new_history + [current_history])
                    return
                # Update leader
                new_lead = (winner + lead) % 4
                # Clear Play
                for k in range(3):
                    in_play.pop(1)

                self.simulate(copy.deepcopy(new_hands), copy.deepcopy(new_lead), copy.deepcopy(new_history + [current_history]), copy.deepcopy(trick) + 1, copy.deepcopy([score0, score1]), copy.deepcopy(new_cards))


    def valid_order_up(self, index):
        count = 0
        for card in self.players[index]:
            if card[0][0] == self.trump:
                count += 1
                if count == 2:
                    return True
        return False


    def valid_pick_up(self, index):
        for card in self.players[index]:
            if card[0][0] == self.trump:
                return True
        return False


    def make_trump(self, index):
        hand = [[[], 0], [[], 0], [[], 0], [[], 0]]
        options = []
        makes = list({'H', 'D', 'S', 'C'} - {self.trump})

        # Sorting hand by suit with trump suit last
        for card in self.players[index]:
            if card[0] == makes[0]:
                hand[0][0].append(card)
            elif card[0] == makes[1]:
                hand[1][0].append(card)
            elif card[0] == makes[2]:
                hand[2][0].append(card)
            else:
                hand[3][0].append(card)

        # Summing the scores of each suit
        for i, suit in enumerate(hand):
            for card in suit[0]:
                if card[1] == 'A':
                    hand[i][1] += 18
                elif card[1] == 'K':
                    hand[i][1] += 17
                elif card[1] == 'Q':
                    hand[i][1] += 16
                elif card[1] == 'J':
                    hand[i][1] += 20
                    # Check for matching jack
                    for jack in self.players[index]:
                        if jack[0] != card[0] and jack[1] == 'J':
                            if jack[0] == 'H' and card[0] == 'D':
                                hand[i][1] += 19
                            elif jack[0] == 'D' and card[0] == 'H':
                                hand[i][1] += 19
                            elif jack[0] == 'S' and card[0] == 'C':
                                hand[i][1] += 19
                            elif jack[0] == 'C' and card[0] == 'S':
                                hand[i][1] += 19
                elif card[1] == '1':
                    hand[i][1] += 14
                else:
                    hand[i][1] += 13

        # Checking for the best hand makes (Excluding proposed trump suit)
        # Skipping for now (Reduce value threshold to 60 if implementation is wanted)
        for value in hand:
            if value[1] >= 200 and value[0] != hand[3]:
                options.append(value[0][0][0])

        return options


    def discard(self):
        hand = [[], [], [], []]
        ranks = [["9", 1], ["1", 2], ["J", 3], ["Q", 4], ["K", 5], ["A", 6]]
        makes = list({"H", "D", "S", "C"} - {self.trump})
        low_one_suit = ["", 10]
        low = ["", 10]
        low_trump = ["", 10]

        for card in self.players[3]:
            if card[0] != self.trump:
                if card[0] == makes[0]:
                    hand[0].append(card)
                elif card[0] == makes[1]:
                    hand[1].append(card)
                elif card[0] == makes[2]:
                    hand[2].append(card)
            else:
                hand[3].append(card)

        for suit in hand:
            # If there is exactly one card of a suit
            if len(suit) == 1:
                for value in ranks:
                    if value[0] == suit[0][1]:
                        #print("Saved lowest one suit: ", suit[0])
                        low_one_suit = [suit[0], value[1]]
            # If there exists cards in suit
            elif len(suit) != 0:
                for card in suit:
                    # Iterate through card ranks to match card
                    for value in ranks:
                        if value[0] == card[1]:
                            if value[1] < low[1]:
                                if suit != hand[3]:
                                    low = [card, value[1]]
                                else:
                                    low_trump = [card, value[1]]

        if low_one_suit[1] <= 4:
            new_hand = list(self.players[3])
            new_hand.append(self.trump_flipped)
            new_hand.remove(str(low_one_suit[0]))
            return new_hand
        elif low[1] < 8:
            new_hand = list(self.players[3])
            new_hand.append(self.trump_flipped)
            new_hand.remove(str(low[0]))
            return new_hand
        else:
            new_hand = list(self.players[3])
            new_hand.append(self.trump_flipped)
            new_hand.remove(str(low_trump[0]))
            return new_hand


    def legal_moves(self, hand, trump):
        if trump == '':
            return hand

        # Determine the left bower based on the trump suit
        left_bower = self.get_left_bower(self.trump)

        if trump == left_bower:
            trump = self.trump
        else:
            trump = trump[0]

        legal_moves = []
        if trump == self.trump:
            for card in hand:
                if card[0] == trump or card == left_bower:
                    legal_moves.append(card)
        else:
            for card in hand:
                if card[0] == trump and card != left_bower:
                    legal_moves.append(card)

        if len(legal_moves) == 0:
            legal_moves = hand

        return legal_moves


    def get_left_bower(self, trump):
        # Hearts: Left bower is Jack of Diamonds
        if trump == 'H':
            return 'DJ'
        # Diamonds: Left bower is Jack of Hearts
        elif trump == 'D':
            return 'HJ'
        # Spades: Left bower is Jack of Clubs
        elif trump == 'S':
            return 'CJ'
        # Clubs: Left bower is Jack of Spades
        elif trump == 'C':
            return 'SJ'
        return None


    # Converts all hand's trump into the highest rank
    def set_trump(self, trump):
        trump = trump[0]
        self.trump = trump
        self.reset_ranks()

        for card in self.cards.keys():
            if card[0] == trump:
                self.cards[card] += 12

        # Setting jacks to bowers
        if trump == "H":
            self.cards["HJ"] += 5
            self.cards["DJ"] += 16
        if trump == "D":
            self.cards["DJ"] += 5
            self.cards["HJ"] += 16
        if trump == "S":
            self.cards["SJ"] += 5
            self.cards["CJ"] += 16
        if trump == "C":
            self.cards["CJ"] += 5
            self.cards["SJ"] += 16

        return self.cards


    # Updates the ranks of the cards based on the card led
    def update_ranks(self, suit):
        led = suit[0]
        # If card is trump, no update needed
        if led == self.trump:
            return
        # Update ranks based on card led
        for card in self.cards.keys():
            # If suit is not already boosted
            if self.cards[card] > 7 and card[0] == led:
                continue
            elif self.cards[card] < 7 and card[0] == led:
                self.cards[card] += 6
            # Devaluing past suits
            elif self.cards[card] > 6 and card[0] != self.trump and self.cards[card] != 19:
                self.cards[card] -= 6

        return self.cards


    def reset_ranks(self):
        self.cards = {
            "H9": 1, "H1": 2, "HJ": 3, "HQ": 4, "HK": 5, "HA": 6,
            "D9": 1, "D1": 2, "DJ": 3, "DQ": 4, "DK": 5, "DA": 6,
            "S9": 1, "S1": 2, "SJ": 3, "SQ": 4, "SK": 5, "SA": 6,
            "C9": 1, "C1": 2, "CJ": 3, "CQ": 4, "CK": 5, "CA": 6}


    def win_play(self, in_play):
        values = [0, 0, 0, 0]
        for i, card in enumerate(in_play):
            for value in self.cards.keys():
                if card == value:
                    values[i] = self.cards[value]
        return values.index(max(values))


    def win_hand(self, score, history):
        # Checking if hand is won
        if score[0] >= 3 and score[1] > 0:
            # Log it
            self.logger.log_hand(self.trump, 0, score, history)
        elif score[0] == 5:
            # Log it
            self.logger.log_hand(self.trump, 0, score, history)
        elif score[1] >= 3:
            # Log it
            self.logger.log_hand(self.trump, 1, score, history)

