def binom(n, k):
    """    
    Parameters:
        n - Number of elements of the entire set
        k - Number of elements in the subset
    It should hold that 0 <= k <= n
    Returns - The binomial coefficient n choose k that represents the number of ways of picking k unordered outcomes from n possibilities
    """
    answer = 1
    for i in range(1, min(k, n - k) + 1):
        answer = answer * (n + 1 - i) / i
    return int(answer)

def multivariate_hypgeom(deck, needed):
    """    
    Parameters:
        deck - A dictionary of cardname : number of copies
        needed - A dictionary of cardname : number of copies
    It should hold that the cardname keys of deck and needed are identical
    Returns - the multivariate hypergeometric probability of drawing exactly the cards in 'needed' from 'deck' when drawing without replacement 
    """
    answer = 1
    sum_deck = 0
    sum_needed = 0
    for card in deck.keys():
        answer *= binom(deck[card], needed[card])
        sum_deck += deck[card]
        sum_needed += needed[card]
    return answer / binom(sum_deck, sum_needed)

#I will assume that we want to cast a Commandeer without paying its mana cost on our opponent’s third turn.
#There are no mulligans. So then we have seen 9 cards.
handsize = 9

print("Probability of holding a Pitcher or another Commandeer, conditional on holding Commandeer")

for Commandeer_deck in range(1,5):
    print("=====")
    #Consider decks with 1 to 4 Commandeers
    for Pitcher_deck in range(35):
        #Consider decks with 0-34 pitchers (cards of the same color that you can 'pitch' to cast a Commandeer)
        #Total number of cards in the deck is 60
        deck = {
            'Commandeer': Commandeer_deck,
            'Pitcher': Pitcher_deck,
            'Other': 60-Commandeer_deck-Pitcher_deck
        }
        #Combo_Success_prob will sum up the probabilities for all combinations with >=1 Commandeer and either >=2 Commandeer or >=1 pitcher
        Combo_Success_prob = 0
        #Commandeer_prob will sum up the probabilities for all combinations with >=1 Commandeer
        Commandeer_prob = 0
        for Commandeer in range(1, Commandeer_deck +1):
            #So if, e.g., we have Commandeer_deck = 2 Commandeers in our deck, then this range is the set [1, 2]
            #Hence, the presence of at least one Commandeer is guaranteed
            for Pitcher in range(Pitcher_deck +1):
                #So if, e.g., we have Pitcher_deck = 4 Pitchers in our deck, then this range is the set [0, 1, 2, 3, 4]
                if Commandeer + Pitcher <= handsize:
                    #We can't consider combinations with, say, 10 Pitchers as those would exceed the number of cards drawn
                    needed = {}
                    needed['Commandeer'] = Commandeer
                    needed['Pitcher'] = Pitcher
                    needed['Other'] = handsize - Commandeer - Pitcher
                    probability = multivariate_hypgeom(deck, needed)
                    if Pitcher >= 2 or Commandeer >= 3 or (Pitcher >=1 and Commandeer >=2):
                        #We have either a Pitcher or another Commandeer to pay for the alternative cost
                        Combo_Success_prob += probability
                    #In any case, this was a combination of cards with at least one Commandeer
                    Commandeer_prob += probability

        print(f'Deck with {Commandeer_deck} Commandeers and {Pitcher_deck} pitchers; probability : {(Combo_Success_prob/Commandeer_prob)* 100:.1f}%.')