import random as r
import discord

class Card:

    def __init__(self, suit, val):
        self.suit = suit
        if isinstance(val, int):
            self.val = val

        elif isinstance(val, str):
            self.val = val
   
    def info(self):
        print("{} of {}".format(self.val, self.suit))
    
    def is_str(self):
        return isinstance(self.val, str)

    def set_val(self, int : int):
        self.val == int

    def get_card_str(self):
        return "{} of {}".format(self.val, self.suit)

    def get_val(self):
        return self.val

    def get_suit(self):
        return self.suit


class Deck:

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for i in ['Spades', 'Diamonds', 'Hearts', "Clubs"]:
            for n in range(1, 14):
                if n == 1:
                    self.cards.append(Card(i, 'Ace'))
                if n == 11:
                    self.cards.append(Card(i, 'King'))
                if n == 12:
                    self.cards.append(Card(i, 'Queen'))
                if n == 13:
                    self.cards.append(Card(i, 'Jack'))
                elif n < 11 and n != 1:
                    self.cards.append(Card(i, n))

    def printDeck(self):
        for c in self.cards:
            c.info()

    def shuffle(self):
        for n in range(len(self.cards) -1, 0, -1):
            rand = r.randint(0, n)
            self.cards[n], self.cards[rand] = self.cards[rand], self.cards[n]

    def draw(self):
        c = self.cards.pop()
        return c
    
class BlackJackDisc:

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.p_total = 0
        self.d_total = 0
        self.p_hand = []
        self.d_hand = []
        self.hole_val_holder = 0
        self.hit_hand = []
        self.hit_counter = 0
        self.embed = discord.Embed(title="Blackjack", 
        type='rich', description="Outcome:")
        
    def create_embed(self, bool):

        if len(self.deck.cards) == 0:
            print(len(self.deck.cards))
            self.deck = Deck()
            self.deck.shuffle()

        if bool: 
            #Draws cards 
            p1 = self.deck.draw()
            d1 = self.deck.draw()
            p2 = self.deck.draw()

            hit_0 = self.deck.draw()
            hit_1 = self.deck.draw()
            hit_2 = self.deck.draw()
            hit_3 = self.deck.draw()
            hit_4 = self.deck.draw()
            hit_5 = self.deck.draw()
        
            #Sanitizes cards
            p1 = self.adjust_card(p1)
            d1 = self.adjust_card(d1)
            p2 = self.adjust_card(p2)

            hit_0 = self.adjust_card(hit_0)
            hit_1 = self.adjust_card(hit_1)
            hit_2 = self.adjust_card(hit_2)
            hit_3 = self.adjust_card(hit_3)
            hit_4 = self.adjust_card(hit_4)
            hit_5 = self.adjust_card(hit_5)

            self.hit_hand.append(hit_0.get_val())
            self.hit_hand.append(hit_1.get_val())
            self.hit_hand.append(hit_2.get_val())
            self.hit_hand.append(hit_3.get_val())
            self.hit_hand.append(hit_4.get_val())
            self.hit_hand.append(hit_5.get_val())

            self.p_hand.append(p1.get_val())
            self.p_hand.append(p2.get_val())
            
            self.d_hand.append(d1.get_val())

            hole = self.deck.draw()
            hole = self.adjust_card(hole)
            self.hole_val_holder = hole.get_val()
            self.p_total = p1.get_val() + p2.get_val()
            
            self.d_total = d1.get_val()
        
            self.embed.add_field(name='Your cards:', value=f'{self.p_hand}', inline=True)
            self.embed.add_field(name="Dealer cards:", value=f'{self.d_hand}', inline=True)
            self.embed.add_field(name='Would you like to hit or stand?', value='Outcome:', inline=False)

            if self.p_total == 21:
                self.embed.set_field_at(2, name="Blackjack you won!", value="Play again by sending r and bet amount", inline=False)
        
        #temporary when replayed resets everything until have more time in resetting everything right, except embed breaks
        elif bool == False:
            self.embed.clear_fields()
            self.deck = Deck()
            self.deck.shuffle()
            self.p_total = 0
            self.d_total = 0
            self.p_hand = []
            self.d_hand = []
            self.hole_val_holder = 0
            self.hit_hand = []
            self.hit_counter = 0
            self.create_embed(True)
        
    
    def play_game(self, ipt):
        
        if self.p_total > 21:
            self.embed.set_field_at(0, name="Your Cards:", value=f'{self.p_hand[0:5]}', inline=True)
            self.embed.set_field_at(2, name="Outcome:", value="You Lost!", inline=False)
                
                
        if self.d_total > 21:
            self.embed.set_field_at(1, name="Dealer Cards:", value=f'{self.d_hand}', inline=True)
            self.embed.set_field_at(2, name="Outcome:", value="You Won!", inline=False)

        if ipt == 'hit':

            self.hand_append(self.hit_hand[self.hit_counter])
            self.p_total = self.p_total + self.hit_hand[self.hit_counter]
            self.hit_counter = self.hit_counter + 1
            print(self.hit_hand)
            if self.p_total > 21:
                self.embed.set_field_at(0, name="Your Cards:", value=f'{self.p_hand[0:5]}', inline=True)
                self.embed.set_field_at(2, name='Outcome:', value='You Lost', inline=False)
            else: 
                self.embed.set_field_at(0, name="Your Cards:", value=f'{self.p_hand[0:5]}', inline=True)


        elif ipt == 'stand':
                
            self.d_total = self.d_total + self.hole_val_holder
            print(self.hole_val_holder)
            self.d_hand.append(self.hole_val_holder)
            self.embed.set_field_at(1, name='Dealer cards:', value=f'{self.d_hand}', inline=True)

            if self.d_total == 21: 
                self.embed.set_field_at(2, name="Outcome:", value="You Lost! Dealer got blackjack!", inline=False)
                    
            elif self.d_total > 21:  
                self.embed.set_field_at(2, name="Outcome:", value="You Won!", inline=False)
                
            elif self.d_total > self.p_total:
                self.embed.set_field_at(2, name="Outcome:", value="You Lost!", inline=False)
            
            elif self.d_total < self.p_total and self.d_total > 21:
                self.embed.set_field_at(2, name="Outcome:", value="You Won!", inline=False)
            
            elif self.d_total == 17 and self.d_total > self.p_total:
                self.embed.set_field_at(2, name="Outcome:", value="You Lost!", inline=False)

            elif self.d_total == 17 and self.d_total < self.p_total:
                self.embed.set_field_at(2, name="Outcome:", value="You Won!", inline=False)
                
            else:
                self.dealer_hit()
                self.embed.set_field_at(1, name='Dealer cards:', value=f'{self.d_hand}', inline=True)

        return         
        
        


                

    def hand_append(self, n):
        self.p_hand.append(n)
    

    def adjust_card(self, n):
        if n.is_str() and n.get_val() == 'King':
            return Card(n.get_suit(), 10)
        if n.is_str() and n.get_val() == 'Queen':
            return Card(n.get_suit(), 10)
        if n.is_str() and n.get_val() == 'Jack':
            return Card(n.get_suit(), 10)
        elif n.is_str() and n.get_val() == 'Ace':
            if self.p_total < 11:
                return Card(n.get_suit(), 11)
            else: 
                n.set_val(1)
                return Card(n.get_suit(), 1)
        else: 
            return n


    def hit(self):

        h = self.deck.draw()
        h = self.adjust_card(h)
        hit_card = h.get_val()
        self.p_total = hit_card + self.p_total
        return h


    def dealer_hit(self):
        while self.d_total < 18:
            print(self.d_total)
            d_draw = self.deck.draw()
            d_draw = self.adjust_card(d_draw)
                    
            d_draw_val = d_draw.get_val()
            self.d_hand.append(d_draw_val)
            self.d_total = self.d_total + d_draw_val
        
        if self.d_total == self.p_total:
            self.embed.set_field_at(2, name="Outcome:", value="Pushback!", inline=False)

        if self.d_total < 22 and self.d_total > self.p_total:            
            self.embed.set_field_at(2, name="Outcome:", value="You Lost!", inline=False)
        elif self.d_total < 22 and self.d_total < self.p_total:
            self.embed.set_field_at(2, name="Outcome:", value="You Win!", inline=False)
        elif self.d_total == 21:
            self.embed.set_field_at(2, name="Outcome:", value="You Lost! Dealer got 21", inline=False)
        elif self.d_total > 21:
            self.embed.set_field_at(2, name="Outcome:", value="You Win! Dealer went bust!", inline=False)
        return print('broke here')

    def dealer_count(self, count):
        if count < 17:
            return 1 
        elif count == 17:
            return 2
        elif count < 22 and count > 17:
            return 3
        else: 
            return 0
