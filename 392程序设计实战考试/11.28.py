import random
class Card:
    def __init__(self,flower,number):
        self.number = number
        self.flower = flower

    def get_score(self):

        if self.number in ['J', 'Q', 'K']:
            return 10
        elif self.number=='A':
            return 11
        return int(self.number)


class Cards:
    def __init__(self):
        flowers = ['Spade','Hearts','Diamond','Plum blossom']
        numbers = ['A','J','Q','K','2','3','4','5','6','7','8','9','10']
        self.cards = [Card(f,n) for f in flowers for n in numbers]
        random.shuffle(self.cards)

    def select_card(self):
        return self.cards.pop(0)


class player:
    def __init__(self,name):
        self.name = name
        self.hand_cards = []
        self.score = 0

    def get_card(self,card):
        self.hand_cards.append(card)
        self.cal_score()

    def cal_score(self):
        self.score = sum(card.value() for card in self.hand)
        aces = sum(1 for card in self.hand_cards if card.rank == 'A')

        while self.score > 21 and aces > 0:
            self.score -= 10
            aces -= 1


    def show_hand(self, hide_first=False):
        if hide_first:
            return f"[?] " + " ".join(str(card) for card in self.hand_cards[1:])
        return " ".join(str(card) for card in self.hand_cards)


    def __str__(self):
        return f"{self.name}: {self.show_hand()} ({self.score})"


class BlackjackGame:
    def __init__(self):
        self.deck = Cards()
        self.player = player("Player")
        self.dealer = player("Dealer")

    def deal_initial(self):
        for _ in range(2):
            self.player.get_card(self.deck.select_card())
            self.dealer.get_card(self.deck.select_card())

    def player_turn(self):
        while self.player.score < 21:
            print(f"\nDealer: {self.dealer.show_hand(hide_first=True)}")
            print(f"You: {self.player}")

            action = input("Hit or Stand? (h/s): ").lower()
            if action == 'h':
                self.player.get_card(self.deck.select_card())
            else:
                break

    def dealer_turn(self):
        while self.dealer.score < 17:
            self.dealer.get_card(self.deck.select_card())

    def determine_winner(self):
        p, d = self.player.score, self.dealer.score

        print(f"\n{'=' * 30}")
        print(f"Dealer: {self.dealer}")
        print(f"You: {self.player}")

        if p > 21:
            print("You bust! Dealer wins.")
        elif d > 21:
            print("Dealer busts! You win!")
        elif p > d:
            print("You win!")
        elif d > p:
            print("Dealer wins.")
        else:
            print("Push (Tie).")

    def play(self):
        print("=" * 30)
        print("BLACKJACK")
        print("=" * 30)

        self.deal_initial()
        self.player_turn()

        if self.player.score <= 21:
            self.dealer_turn()

        self.determine_winner()