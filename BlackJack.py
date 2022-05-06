#Welcome to my game of Blackjack. 
import random

suits = ("Hearts","Clubs","Spades","Diamonds")
ranks = ("Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace")
values = {"Two":2,"Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9,"Ten":10,
         "Jack":10,"Queen":10,"King":10,"Ace":11}

class Card():
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck():
    def __init__(self):
        self.deck=[]
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                
    def __str__(self):
        deck_comp=""
        for card in self.deck:
            deck_comp += "\n "+card.__str__()
        return "The deck has the following cards: "+ deck_comp
    
    def shuffle(self):
        return random.shuffle(self.deck)
    
    def deal(self):
        return self.deck.pop()

class Hand():
    def __init__(self):
        self.cards=[]
        self.value=0
        self.aces=0
        
    def add_card(self,card):
        self.cards.append(card)
        self.value+=values[card.rank]
        if card.rank == "Ace":
            self.aces+=1
        
    def adjust_aces(self):
        if self.value > 21 and self.aces:
            self.value-=10
            self.aces-=1

class Chips:
	def __init__(self):
		self.total=100
		self.bet=0
        
	def win_bet(self):
		self.total+=self.bet
        
	def lose_bet(self):
		self.total-=self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet=int(input("How much would you like to bet?  "))
        except ValueError:
            print("Please input an integer.")
            continue
        else:
            if chips.bet > chips.total:
                print("Your bet amount exceeds your holdings.")
                continue
            elif chips.bet == 0:
                print("You must enter a number greater tan zero")
                continue
            else:
                break

def show_some(player,dealer):
    print("---------------")
    print("| Dealer Hand |")
    print("---------------")
    print("| <unknown card> |")
    print("|",dealer.cards[1],"|")
    print("                  ")
    print("                  ")
    print("---------------")
    print("| Player Hand |")
    print("---------------")
    print(*player.cards, sep="\n")
    print("--> Hand Value:",player.value)

def show_all(player,dealer):
    print("---------------")
    print("| Dealer Hand |")
    print("---------------")
    print(*dealer.cards, sep="\n")
    print("---> Hand Value:",dealer.value)
    print("                  ")
    print("                  ")
    print("---------------")
    print("| Player Hand |")
    print("---------------")
    print(*player.cards, sep="\n")
    print("--> Hand Value:",player.value)

#Function for taking hits
def hit(hand,deck):
    new_card=deck.deal()
    hand.add_card(new_card)
    if hand.value > 21 and hand.aces:
        hand.adjust_aces()

def hit_or_stand(player,deck):
    global hitting
    while True:
        play=(input("\nWould you like to hit? Y or N: ")).upper()
        if play not in ("Y","N"):
            print("Please select either Y or N.")
            continue
        else:
            if play == "Y":
                print("You've chosen to hit. Fortune favours the brave.\n")
                hit(player,deck)
                return True
                break
            else:
                print("You've chosen to stand.\n")
                hitting=False
                return False
                break

def player_busts(chips):
    chips.lose_bet()
    print("\n| Player has bust |")
    
def player_wins(chips):
    chips.win_bet()
    print("\n| Player wins |")
    
def dealer_bust(chips):
    chips.win_bet()
    print("\n| Dealer has bust |")

def dealer_wins(chips):
    chips.lose_bet()
    print("\n| Dealer has won |")
    
def push():
    print("\n| It's a tie. Game is pushed. |")


def play_again():
    while True:
        again=(input("Would you like to play again? Y or N: ")).upper()
        if again not in ("Y","N"):
            print("Please choose either Y or N.")
            continue
        else:
            break
    if again == "Y":
        return True
    else:
        print("Thank you for playing.")
        return False




#Setting game here
while True:
    print("Welcome to Blackjack")
    chips=Chips()
    print(f"\nYou have {chips.total} chips to play with")
    
    playing=True
    while playing:
        #Setting the deck and establishing empty player hands
        deck=Deck()
        deck.shuffle()
        player=Hand()
        dealer=Hand()
        
        #Allow player to input qty to bet
        take_bet(chips)
        
        #Round 1 of deal
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
        
        #Round 2 of deal
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
        
        #Check for Aces
        player.adjust_aces()
        dealer.adjust_aces()
        
        #Printing round number per hand displayed
        print("\nRound 1")
        show_some(player,dealer)
        
        #Setting place variables
        hitting=True
        game_num=1
        
        while hitting:
            game_num+=1
            
            if hit_or_stand(player,deck):
                print(f"\nRound {game_num}")
                show_some(player,dealer)
            
            if player.value > 21:
                player_busts(chips)
                playing=False
                break
            else:
                continue
        
        #Hitting dealer hand until value > 17
        if player.value <=21 and player.value > dealer.value:
            while dealer.value < 17:
                hit(dealer,deck)
                game_num+=1
                print(f"\nRound {game_num}")
                show_all(player,dealer)
        else:
            if playing == True:
            	show_all(player,dealer)
            
        #Winning and losing scenarios
        if dealer.value>21:
            dealer_bust(chips)
        elif dealer.value <= 21 and dealer.value > player.value:
            dealer_wins(chips)
        elif player.value <= 21 and dealer.value < player.value:
            player_wins(chips)
        elif player.value == dealer.value:
            push()
        
        #Provide chip total after game
        print("-------------")
        print(f"Chips Total: {chips.total}")
        #Do you want to play again?
        if chips.total > 0:
            playing = play_again()
        else:
            playing = False
            print("--------")
            print("You have no chips left.\nThank you for playing.")
            break
        
    break