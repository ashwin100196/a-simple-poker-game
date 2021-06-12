import session6_part1
from session6_part1 import Card, Hand

# create hands
# h : Straight Flush
# h2 : One Pair of 8 with high card 7
# h3 : One Pair of 7 with high card 8
# h4 : One Pair of 7 with high card 9
# h5 : incorrect card in hand - 7 of harts**

cards = [Card('5 of spades'), Card('6 of spades'), Card('7 of spades'), Card('8 of spades'), Card('9 of spades')]
h = Hand(cards)

print(h.hand_name)
print(h.sorting_key)

cards = [Card('5 of spades'), Card('6 of spades'), Card('7 of spades'), Card('8 of spades'), Card('8 of hearts')]
h2 = Hand(cards)

print(h2.hand_name)
print(h2.sorting_key)

cards = [Card('5 of spades'), Card('6 of spades'), Card('7 of spades'), Card('8 of spades'), Card('7 of hearts')]
h3 = Hand(cards)

print(h3.hand_name)
print(h3.sorting_key)

cards = [Card('5 of spades'), Card('6 of spades'), Card('7 of spades'), Card('9 of spades'), Card('7 of hearts')]
h4 = Hand(cards)

print(h4.hand_name)
print(h4.sorting_key)

# compare hands

print("first hand better than second?", h > h2)
print("second hand better than third?", h2 > h3)
print("third hand better than fourth?", h3 > h4)

# errors out
try:
	cards = [Card('5 of spades'), Card('6 of spades'), Card('7 of spades'), Card('9 of spades'), Card('7 of harts')]
	h5 = Hand(cards)

	print(h5.hand_name)
	print(h5.sorting_key)
except Exception as e:
	print(e)

# get the winning hand from a selection of hands
winner = session6.get_winning_hand(h2, h3, h4)
print(winner)