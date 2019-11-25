from sys import argv
import random as rn
import math
from scipy.stats import t

filename = argv

# creating global lists that will be used
deck = []
your_hand = []
community = []
opponent_hand = []

# (re)creates a the deck in a list and shuffles it
def shuffle_deck():
    for suit in ["hearts", "diamonds", "spades", "clubs"]:
        for x in range(1, 14):
            if x < 11:
                deck.append(f"{x} of {suit}")
            elif x == 11:
                deck.append(f"jack of {suit}")
            elif x == 12:
                deck.append(f"queen of {suit}")
            elif x == 13:
                deck.append(f"king of {suit}")

            rn.shuffle(deck)


# prints out lists
def iterate(a_list):
    for index in range(len(a_list)):
        print(a_list[index])

def faces_to_nums(hand):
    num = []
    for card in hand:
        # replaces face values with numbers for sorting
        if "j" in card:
            num.append(card.replace("j", "11"))
        elif "q" in card:
            num.append(card.replace("q", "12"))
        elif "k" in card:
            num.append(card.replace("k", "13"))
        else:
            num.append(card)
    return num

def nums_to_faces(hand):
    faces = []
    for card in hand:
        # replaces face values with numbers for sorting
        if "11" in card:
            faces.append(card.replace("11", "j"))
        elif "12" in card:
            faces.append(card.replace("12", "q"))
        elif "13" in card:
            faces.append(card.replace("13", "k"))
        else:
            faces.append(card)
    return faces
# takes cards from the "deck" list, and adds them to another list (the "hand")
def draw(number_of_cards, hand):
    for n in range(int(number_of_cards)):
        hand.append(deck.pop())

# takes a hand that's in word form (e.g. "king of hearts") and changes it to
# simplified form (e.g. "kh")
def simplify_cards(hand):
    # creating list for simplified hand
    simp_hand = []
    for card in hand:
        # if card isn't a face card, strips all the letters and spaces and adds
        # one letter for the suit
        if not card.startswith(("king", "queen", "jack")):
            if "hearts" in card:
                simp_hand.append(f"{card.strip('abcdefghijklmnopqrstuvwxyz ')}h")
            elif "diamonds" in card:
                simp_hand.append(f"{card.strip('abcdefghijklmnopqrstuvwxyz ')}d")
            elif "clubs" in card:
                simp_hand.append(f"{card.strip('abcdefghijklmnopqrstuvwxyz ')}c")
            elif "spades" in card:
                simp_hand.append(f"{card.strip('abcdefghijklmnopqrstuvwxyz ')}s")
        # if card is a face card, instead replaces it with first letter of card
        # (e.g. "j" for "jack") and adds one letter for the suit
        else:
            if "hearts" in card:
                simp_hand.append(f"{card[0]}h")
            elif "diamonds" in card:
                simp_hand.append(f"{card[0]}d")
            elif "clubs" in card:
                simp_hand.append(f"{card[0]}c")
            elif "spades" in card:
                simp_hand.append(f"{card[0]}s")
    # returns simplified hand
    return simp_hand

# does the opposite of simplify_cards(), takes the simplified form and converts
# it back to word form for display
def complex_cards(hand):
    comp_hand = []
    for card in hand:
        # as 10s don't play well with the way I wrote this (they turn into 1s),
        # they get their own special case
        if card.startswith("10"):
            if card.endswith("h"):
                comp_hand.append(f"10 of hearts")
            elif card.endswith("d"):
                comp_hand.append(f"10 of diamonds")
            elif card.endswith("c"):
                comp_hand.append(f"10 of clubs")
            elif card.endswith("s"):
                comp_hand.append(f"10 of spades")
        # fairly self explanatory, expands non-face cards
        elif not card.startswith(("k", "q", "j")):
            if card.endswith("h"):
                comp_hand.append(f"{card[0]} of hearts")
            elif card.endswith("d"):
                comp_hand.append(f"{card[0]} of diamonds")
            elif card.endswith("c"):
                comp_hand.append(f"{card[0]} of clubs")
            elif card.endswith("s"):
                comp_hand.append(f"{card[0]} of spades")
        # same as above for face cards
        else:
            for word in ["king", "queen", "jack"]:
                if card.startswith(word[0]):
                    if card.endswith("h"):
                        comp_hand.append(f"{word} of hearts")
                    elif card.endswith("d"):
                        comp_hand.append(f"{word} of diamonds")
                    elif card.endswith("c"):
                        comp_hand.append(f"{word} of clubs")
                    elif card.endswith("s"):
                        comp_hand.append(f"{word} of spades")
    return comp_hand

# checks if set of cards has a flush in it
def flush_check(hand):
    hearts_count = 0
    diamonds_count = 0
    clubs_count = 0
    spades_count = 0
    for card in hand:
        # checks last letter for suit, then adds one to the respective counter
        if card[-1] == "h":
            hearts_count += 1
        elif card[-1] == "d":
            diamonds_count += 1
        elif card[-1] == "c":
            clubs_count += 1
        elif card[-1] == "s":
            spades_count += 1
    suit_count = [hearts_count, diamonds_count, clubs_count, spades_count]
    # checks if any suit has five or more cards
    for suit in suit_count:
        if suit >= 5:
            return True
        else:
            pass
    else:
        return False

# checks for matches (pairs, etc.)
def match_check(hand):
    match_count = 0
    numbers = []
    matches = []
    for card in hand:
        # if it's a 10, just slaps on a 10, same for face cards
        if card.startswith("10"):
            numbers.append(10)
        elif card.startswith("j"):
            numbers.append(11)
        elif card.startswith("q"):
            numbers.append(12)
        elif card.startswith("k"):
            numbers.append(13)
        # otherwise just throws in the 1st character
        else:
            numbers.append(int(card[0]))
    # checks every value of card
    for value in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
        # if there's more than 1, adds tuple with value of card and number of
        # appearances to list of matches (side note, as the cards are checked
        # in ascending value, matches are always in order of card value)
        if numbers.count(value) > 1:
            matches.append((numbers.count(value), value))
        else:
            pass
    if matches == []:
        return False
    else:
        # sorts them so trips and quads come last
        quads = []
        trips = []
        pairs = []
        for match in matches:
            if match[0] == 4:
                quads.append(match)
            if match[0] == 3:
                trips.append(match)
            if match[0] == 2:
                pairs.append(match)
        pairs.sort()
        trips.sort()
        quads.sort()
        pairs.reverse()
        trips.reverse()
        quads.reverse()
        matches = pairs + trips + quads
        return matches

# checks for straights
def straight_check(hand):
    straight_types = []
    unstripped_num = []
    numbers = []
    straights_in_hand = []
    # iteratively makes a list of lists conatining all possible straights
    # (I know I should just type out the list so it runs a little faster, but I
    # really can't be bothered to at the moment, I'll probably revise it later)
    for n in range(1, 11):
        if n < 7:
            straight_types.append([n, n+1, n+2, n+3, n+4])
        elif n == 7:
            straight_types.append([n, n+1, n+2, n+3, 11])
        elif n == 8:
            straight_types.append([n, n+1, n+2, 11, 12])
        elif n == 9:
            straight_types.append([n, n+1, 11, 12, 13])
        elif n == 10:
            straight_types.append([n, 11, 12, 13, 1])
    for card in hand:
        # replaces face values with numbers for sorting
        if "j" in card:
            unstripped_num.append(card.replace("j", "11"))
        elif "q" in card:
            unstripped_num.append(card.replace("q", "12"))
        elif "k" in card:
            unstripped_num.append(card.replace("k", "13"))
        else:
            unstripped_num.append(card)
    for card in unstripped_num:
        # strips all letters and spaces, and makes them into ints for sorting
        # (it took me a while to realizei had to make them ints, as "12" goes
        # before "5" when sorting strs lol)
        numbers.append(int(card.strip('abcdefghilmnoprstuvwxyz ')))
    # sorts cards
    numbers.sort()
    # as ace can be low or high, puts on on end if there's one in there
    if numbers[0] == 1:
        numbers.append(1)
    # checks for each straight individually
    for straight in straight_types:
        is_in = False
        # checks if all the numbers in the straight are in the hand
        for n in straight:
            # if ANY number in the straight isnt in the hand, sets is_in to
            # False and breaks loop
            if n not in numbers:
                is_in = False
                break
            else:
                is_in = True
        # if all the cards were there, adds that straight to a list of
        # straights that are in the hand
        if is_in == True:
            straights_in_hand.append(straight)
    # if there are no straights returns False
    if straights_in_hand == []:
        return False
    else:
        # as the straights are tested in order of "height", the best one will
        # always be the last one
        large_straight = straights_in_hand[-1]
        final_straight = []
        # changes back to str for the output
        for n in large_straight:
            final_straight.append(str(n))
        for card in final_straight:
            if n == "11":
                n = "j"
            elif n == "12":
                n = "q"
            elif n == "13":
                n = "k"
            else:
                pass
        return final_straight

def straight_flush_check(hand):
    if straight_check(hand) == ["10", "11", "12", "13", "1"] and flush_check(hand) == True:
        straight = straight_check(hand)
        cards_in_straight = []
        # makes sure cards in straight are the ones in the flush
        for card in hand:
            # gets rid of suit to check if it's in the straight
            if (card.strip(card[-1])) in straight:
                # if it is, puts original card in new list
                cards_in_straight.append(card)
        # checks new list for a flush, and if found, it's a royal flush
        if flush_check(cards_in_straight) == True:
            return "Royal Flush"
        else:
            pass
    if straight_check(hand) != False and flush_check(hand) == True:
        straight = straight_check(hand)
        cards_in_straight = []
        for card in hand:
            if (card.strip(card[1])) in straight:
                cards_in_straight.append(card)
        if flush_check(cards_in_straight) == True:
            for n in [["11", "j"], ["12", "q"], ["13", "k"]]:
                if straight[-1] == n[0]:
                    return n[1] + " high straight flush"
                else:
                    pass
            else:
                # puts highest card in straight in the str
                return str(straight[-1]) + " high straight flush"
        else:
            return False
    else:
        return False
# really complicated lol. This takes a hand and returns the best set that can
# be made from it
def hand_rank(hand):
    # concatenates the given hand and the "community cards" taht anyone can use
    full_hand = hand + community
    # gets any matches from the hand
    matches = match_check(full_hand)
    # this is just a placeholder tuple, basically "False", but plays nice with
    # code made for tuples
    big_match = (0, 0)
    if matches != False:
        # big_match is the last match, so it'll be the biggest
        big_match = matches[0]
        # if there's more than one match, makes a second match variable (three
        # pair isn't a thing so we don't have to worry about a third match)
        if len(matches) > 1:
            small_match = matches[1]
        else:
            small_match = (0, 0)
    else:
        small_match = (0, 0)
    # checks for royal flush
    if straight_flush_check(full_hand) == "Royal Flush":
        return "Royal Flush"
    # checks for straight flush (see Royal Flush for explanation)
    elif straight_flush_check(full_hand) != False:
        return straight_flush_check(full_hand)
    # checks for 4 of a kind
    elif big_match[0] == 4:
        # if 4 of a kind, there wont be any other matches to worry about
        for n in [[11, "j"], [12, "q"], [13, "k"]]:
            if big_match[1] == n[0]:
                return "four of a kind " + n[1] + "s"
        else:
            return "four of a kind " + str(big_match[1]) + "s"
    # checks for full house if there's a trip and a pair (remember, matches are
    # sorted by number of cards in them, so big_match will always be the trip in
    # this case)
    elif big_match[0] == 3 and small_match[0] == 2:
        # checks if card number is 11, 12, or 13, and if it is, checks the other
        # one too, and replaces any with
        for n in [[11, "j"], [12, "q"], [13, "k"]]:
            if big_match[1] == n[0]:
                for x in [[11, "j"], [12, "q"], [13, "k"]]:
                    if small_match == x[0]:
                        return "full house " + n[1] + "s and " + x[1] + "s"
                    else:
                        pass
                else:
                    return "full house " + n[1] + "s and " + str(small_match[1]) + "s"
            elif small_match[1] == n[0]:
                return "full house " + str(big_match[1]) + "s and " + n[1] + "s"
        else:
            return "full house " + str(big_match[1]) + "s and " + str(small_match[1]) + "s"
    # checks for flush
    elif flush_check(full_hand) == True:
        # needed a bit more detail to make the high card always be part of the
        # flush, I'll clean this up later
        hearts_count = 0
        diamonds_count = 0
        clubs_count = 0
        spades_count = 0
        for card in full_hand:
            # checks last letter for suit, then adds one to the respective counter
            if card[-1] == "h":
                hearts_count += 1
            elif card[-1] == "d":
                diamonds_count += 1
            elif card[-1] == "c":
                clubs_count += 1
            elif card[-1] == "s":
                spades_count += 1
        suit_count = [[hearts_count, "h"], [diamonds_count, "d"], [clubs_count, "c"], [spades_count, "s"]]
        # checks if any suit has five or more cards
        for suit in suit_count:
            if suit[0] >= 5:
                card_suit = suit[1]
            else:
                pass
        # this bit finds high cards (I'll probably make this it's own function
        # at some point)
        flush_hand = []
        for card in full_hand:
            if card[1] == card_suit:
                flush_hand.append(card)
        #-----------------------------------------------------------------------
        num_hand_unstripped = []
        num_hand = []
        # replaces faces with numbers for sorting
        for card in flush_hand:
            if "j" in card:
                num_hand_unstripped.append(card.replace("j", "11"))
            elif "q" in card:
                num_hand_unstripped.append(card.replace("q", "12"))
            elif "k" in card:
                num_hand_unstripped.append(card.replace("k", "13"))
            else:
                num_hand_unstripped.append(card)
        # strips suits
        for card in num_hand_unstripped:
            num_hand.append(int(card.strip('abcdefghijklmnopqrstuvwxyz ')))
        # sorts cards
        num_hand.sort()
        # if ace is in there, make that high card
        if num_hand[0] == 1:
            num_hand.append(1)
        # gets higest card (the last one)
        high_card = num_hand[-1]
        # turns numbers back into faces
        if high_card == 11:
            high_card = "j"
        elif high_card == 12:
            high_card = "q"
        elif high_card == 13:
            high_card = "k"
        else:
            pass
        #-----------------------------------------------------------------------
        return str(high_card) + " high flush"
    # checks for straight
    elif straight_check(full_hand) != False:
        straight = straight_check(full_hand)
        # takes highest value in straight
        return str(straight[-1]) + " high straight"
    # checks for trips
    elif big_match[0] == 3:
        for n in [[11, "j"], [12, "q"], [13, "k"]]:
            if big_match[1] == n[0]:
                return "three of a kind " + n[1] + "s"
        else:
            return "three of a kind " + str(big_match[1]) + "s"
    # checks for 2 pair
    elif big_match[0] == 2 and small_match[0] == 2:
        # see explanation in full house
        for n in [[11, "j"], [12, "q"], [13, "k"]]:
            if big_match[1] == n[0]:
                for x in [[11, "j"], [12, "q"], [13, "k"]]:
                    if small_match == x[0]:
                        return "two pair " + n[1] + "s and " + x[1] + "s"
                    else:
                        pass
                else:
                    return "two pair " + n[1] + "s and " + str(small_match[1]) + "s"
            elif small_match[1] == n[0]:
                return "two pair " + str(big_match[1]) + "s and " + n[1] + "s"
        else:
            return "two pair " + str(big_match[1]) + "s and " + str(small_match[1]) + "s"
    # checks for pair
    elif big_match[0] == 2:
        for n in [[11, "j"], [12, "q"], [13, "k"]]:
            if big_match[1] == n[0]:
                return "pair of " + n[1] + "s"
        else:
            return "pair of " + str(big_match[1]) + "s"
    # just looks for high card, as hand fits no other rank (see flush for
    # explanation)
    else:
        num_hand_unstripped = []
        num_hand = []
        for card in full_hand:
            if "j" in card:
                num_hand_unstripped.append(card.replace("j", "11"))
            elif "q" in card:
                num_hand_unstripped.append(card.replace("q", "12"))
            elif "k" in card:
                num_hand_unstripped.append(card.replace("k", "13"))
            else:
                num_hand_unstripped.append(card)
        for card in num_hand_unstripped:
            num_hand.append(int(card.strip('abcdefghijklmnopqrstuvwxyz ')))
        num_hand.sort()
        if num_hand[0] == 1:
            num_hand.append(1)
        high_card = num_hand[-1]
        if high_card == 11:
            high_card = "j"
        elif high_card == 12:
            high_card = "q"
        elif high_card == 13:
            high_card = "k"
        else:
            pass
        return str(high_card) + " high"

# makes tuple of hand power: (hand rank, high card, high card 2)
# note: (when making comparison function, don't forget to consider kickers as
# well)
def hand_tuple(hand_rank):
    # makes tuple based off of hand type and card values
    if not "10" in hand_rank:
        if hand_rank == "Royal Flush":
            tuple = (0, 0, 0)
        elif hand_rank.endswith("straight flush"):
            tuple = (1, hand_rank[0], 0)
        elif hand_rank.startswith("four of a kind"):
            tuple = (2, hand_rank[-2], 0)
        elif hand_rank.startswith("full house"):
            tuple = (3, hand_rank[11], hand_rank[-2])
        elif hand_rank.endswith("high flush"):
            tuple = (4, hand_rank[0], 0)
        elif hand_rank.endswith("high straight"):
            tuple = (5, hand_rank[0], 0)
        elif hand_rank.startswith("three of a kind"):
            tuple = (6, hand_rank[-2], 0)
        elif hand_rank.startswith("two pair"):
            tuple = (7, hand_rank[9], hand_rank[-2])
        elif hand_rank.startswith("pair of"):
            tuple = (8, hand_rank[-2], 0)
        elif hand_rank.endswith("high"):
            tuple = (9, hand_rank[0], 0)
    # as 10, being 2 digits, messes stuff, up, made special accomodations for it
    else:
        if hand_rank == "Royal Flush":
            tuple = (0, 0, 0)
        elif hand_rank.endswith("straight flush"):
            tuple = (1, hand_rank[0:2], 0)
        elif hand_rank.startswith("four of a kind"):
            tuple = (2, hand_rank[15:17], 0)
        elif hand_rank.endswith("high flush"):
            tuple = (4, hand_rank[0:2], 0)
        elif hand_rank.endswith("high straight"):
            tuple = (5, hand_rank[0:2], 0)
        elif hand_rank.startswith("three of a kind"):
            tuple = (6, hand_rank[16:18], 0)
        elif hand_rank.startswith("pair of"):
            tuple = (8, hand_rank[8:10], 0)
        elif hand_rank.endswith("high"):
            tuple = (9, hand_rank[0:2], 0)
        elif hand_rank.startswith("two pair"):
            if hand_rank.find("10") == 9:
                tuple = (7, hand_rank[9:11], hand_rank[-2])
            elif hand_rank.find("10") == 16:
                tuple = (7, hand_rank[9], hand_rank[16:18])
        elif hand_rank.startswith("full house"):
            if hand_rank.find("10") == 11:
                tuple = (3, hand_rank[11:13], hand_rank[-2])
            elif hand_rank.find("10") == 18:
                tuple = (3, hand_rank[11], hand_rank[18:20])
    # converts faces to numbers, as it's easier to compare numbers
    list_to_tuple = []
    for n in range(3):
        if tuple[n] == "j":
            list_to_tuple.append(11)
        elif tuple[n] == "q":
            list_to_tuple.append(12)
        elif tuple[n] == "k":
            list_to_tuple.append(13)
        else:
            list_to_tuple.append(int(tuple[n]))
    val_1, val_2, val_3 = list_to_tuple
    return (val_1, val_2, val_3)

# sees which of 2 hands is stronger, 0 if hand1, 1 if hand 2, 2 if tie
def showdown(hand1, hand2):
    # checks values of hands and makes tuple
    hand_val_1 = hand_rank(hand1)
    hand_val_2 = hand_rank(hand2)
    hand_tuple_1 = hand_tuple(hand_val_1)
    hand_tuple_2 = hand_tuple(hand_val_2)
    # if 1st number is smaller, its a stronger hand
    if hand_tuple_1[0] < hand_tuple_2[0]:
        return 0
    elif hand_tuple_2[0] < hand_tuple_1[0]:
        return 1
    # if they're tied, checks second and third numbers (card values)
    elif hand_tuple_1[0] == hand_tuple_2[0]:
        if hand_tuple_1[1] > hand_tuple_2[1]:
            return 0
        elif hand_tuple_2[1] > hand_tuple_1[1]:
            return 1
        elif hand_tuple_1[1] == hand_tuple_2[1]:
            if hand_tuple_1[2] > hand_tuple_2[2]:
                return 0
            elif hand_tuple_2[2] > hand_tuple_1[2]:
                return 1
            elif hand_tuple_1[2] == hand_tuple_2[2]:
                # if tuples are identical,
                hand1 = hand1 + community
                hand2 = hand2 + community
                hand1 = faces_to_nums(hand1)
                hand2 = faces_to_nums(hand2)
                hand1.sort()
                hand2.sort()
                hand1_sorted = []
                hand2_sorted = []
                for card in hand1:
                    hand1_sorted.append(card.strip("hdcs"))
                for card in hand2:
                    hand2_sorted.append(card.strip("hdcs"))
                if hand_tuple_1[0] == 2:
                    for x in range(4):
                        hand1_sorted.remove(str(hand_tuple_1[1]))
                        hand2_sorted.remove(str(hand_tuple_2[1]))
                    for card in hand1_sorted:
                        hand1.append(card)
                    for card in hand2_sorted:
                        hand2.append(card)
                    if hand1[-1] > hand2[-1]:
                        return 0
                    elif hand2[-1] > hand1[-1]:
                        return 1
                    elif hand1[-1] == hand2[-1]:
                        return 2
                if hand_tuple_1[0] == 4:
                    # going to condense this to a function later
                    #-----------------------------------------------------------
                    hearts_count = 0
                    diamonds_count = 0
                    clubs_count = 0
                    spades_count = 0
                    for card in hand1:
                        # checks last letter for suit, then adds one to the respective counter
                        if card[-1] == "h":
                            hearts_count += 1
                        elif card[-1] == "d":
                            diamonds_count += 1
                        elif card[-1] == "c":
                            clubs_count += 1
                        elif card[-1] == "s":
                            spades_count += 1
                    suit_count = [[hearts_count, "h"], [diamonds_count, "d"], [clubs_count, "c"], [spades_count, "s"]]
                    # checks if any suit has five or more cards
                    for suit in suit_count:
                        if suit[0] >= 5:
                            card_suit = suit[1]
                        else:
                            pass
                    # this bit finds high cards (I'll probably make this it's own function
                    # at some point)
                    flush_hand1 = []
                    for card in hand1:
                        if card[1] == card_suit:
                            flush_hand1.append(card)
                    #-----------------------------------------------------------
                    hearts_count = 0
                    diamonds_count = 0
                    clubs_count = 0
                    spades_count = 0
                    for card in hand2:
                        # checks last letter for suit, then adds one to the respective counter
                        if card[-1] == "h":
                            hearts_count += 1
                        elif card[-1] == "d":
                            diamonds_count += 1
                        elif card[-1] == "c":
                            clubs_count += 1
                        elif card[-1] == "s":
                            spades_count += 1
                    suit_count = [[hearts_count, "h"], [diamonds_count, "d"], [clubs_count, "c"], [spades_count, "s"]]
                    # checks if any suit has five or more cards
                    for suit in suit_count:
                        if suit[0] >= 5:
                            card_suit = suit[1]
                        else:
                            pass
                    # this bit finds high cards (I'll probably make this it's own function
                    # at some point)
                    flush_hand2 = []
                    for card in hand2:
                        if card[1] == card_suit:
                            flush_hand2.append(card)
                    #-----------------------------------------------------------
                    for n in range(5):
                        if flush_hand1[-n] > flush_hand2[-n]:
                            return 0
                        elif flush_hand2[-n] > flush_hand1[-n]:
                            return 1
                        else:
                            pass
                    else:
                        return 2
                if hand_tuple_1[0] == 6:
                    for x in range(3):
                        hand1_sorted.remove(str(hand_tuple_1[1]))
                        hand2_sorted.remove(str(hand_tuple_2[1]))
                    for card in hand1_sorted:
                        hand1.append(card)
                    for card in hand2_sorted:
                        hand2.append(card)
                    if hand1[-1] > hand2[-1]:
                        return 0
                    elif hand2[-1] > hand1[-1]:
                        return 1
                    elif hand1[-1] == hand2[-1]:
                        if hand1[-2] > hand2[-2]:
                            return 0
                        elif hand2[-2] > hand1[-2]:
                            return 1
                        elif hand1[-1] == hand2[-1]:
                            return 2
                if hand_tuple_1[0] == 7:
                    for x in range(2):
                        hand1_sorted.remove(str(hand_tuple_1[1]))
                        hand1_sorted.remove(str(hand_tuple_1[2]))
                        hand2_sorted.remove(str(hand_tuple_2[1]))
                        hand2_sorted.remove(str(hand_tuple_2[2]))
                    for card in hand1_sorted:
                        hand1.append(card)
                    for card in hand2_sorted:
                        hand2.append(card)
                    if hand1[-1] > hand2[-1]:
                        return 0
                    elif hand2[-1] > hand1[-1]:
                        return 1
                    elif hand1[-1] == hand2[-1]:
                        return 2
                if hand_tuple_1[0] == 8:
                    for x in range(2):
                        hand1_sorted.remove(str(hand_tuple_1[1]))
                        hand2_sorted.remove(str(hand_tuple_2[1]))
                    for card in hand1_sorted:
                        hand1.append(card)
                    for card in hand2_sorted:
                        hand2.append(card)
                    if hand1[-1] > hand2[-1]:
                        return 0
                    elif hand2[-1] > hand1[-1]:
                        return 1
                    elif hand1[-1] == hand2[-1]:
                        if hand1[-2] > hand2[-2]:
                            return 0
                        elif hand2[-2] > hand1[-2]:
                            return 1
                        elif hand1[-2] == hand2[-2]:
                            if hand1[-3] > hand2[-3]:
                                return 0
                            elif hand2[-3] > hand1[-3]:
                                return 1
                            elif hand1[-3] == hand2[-3]:
                                return 2
                if hand_tuple_1[0] == 9:
                    for n in range(5):
                        if hand1_sorted[-n] > hand2_sorted[-n]:
                            return 0
                        elif hand2_sorted[-n] > hand1_sorted[-n]:
                            return 1
                        else:
                            pass
                    else:
                        return 2


#for i in [100, 500, 1000, 2000, 3000, 4000, 5000, 20000, 30000, 40000, 50000]:
i = 10000
undone = True
while (undone):

    list_of_hands = [0,0,0,0,0,0,0,0,0,0]

    for n in range(i): # make deck

        for suit in ["hearts", "diamonds", "spades", "clubs"]:
            for x in range(1, 14):
                if x < 11:
                    deck.append(f"{x} of {suit}")
                elif x == 11:
                    deck.append(f"jack of {suit}")
                elif x == 12:
                    deck.append(f"queen of {suit}")
                elif x == 13:
                    deck.append(f"king of {suit}")


        for num in [5,6,18]: ### edit these numbers to change starting cards ###

            your_hand.append(deck.pop(num))



        rn.shuffle(deck) # shuffles deck

        draw(5-len(your_hand), your_hand) # draw up to 5 cards

        your_hand = simplify_cards(your_hand)

        list_of_hands[hand_tuple(hand_rank(your_hand))[0]] += 1 # add 1 to respective counter

        your_hand = [] # reset hand
        deck = [] # reset deck

    print(f"{i}: {list_of_hands}")

    one_ct = 0
    zero_ct = 0
    neg_ct = 0

    for j in range(10): # for each rank of hand
        if (j < 8): # if better than a pair
            one_ct += list_of_hands[j]
        elif (j == 8): # if a pair
            zero_ct += list_of_hands[j]
        elif (j > 8): # if worse than a pair
            neg_ct += list_of_hands[j]

    s_mean = (one_ct - neg_ct) / i # find sample mean

    print(f"{i} mean: {s_mean}")

    var_sum = 0

    var_sum += one_ct * ((1 - s_mean) ** 2) # sumn the squares of the differences
    var_sum += zero_ct * ((0 - s_mean) ** 2)
    var_sum += one_ct * ((-1 - s_mean) ** 2)

    s_var = var_sum / (i-1) # divide by degrees of freedom

    print(f"{i} var: {s_var}")

    nf_int = 2 * 1.96 * (s_var / math.sqrt(i)) # used 1.96 because n >> 30

    print(f"{i} 95% confidence interval: centered on {s_mean}, width = {nf_int}\n")

    if (nf_int < .01): # if width is under .01, exit
        undone = False
    else: # otherwise, increment n by 10 000
        i += 10000

print("done") # signify completion
