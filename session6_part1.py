import collections
from itertools import combinations

class Card:
	def __init__(self, name):
		self.name = name
		self.value = 'ace'
		self.suit = 'spades'
		self.rank = 13
		self.initialize_card_details()

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
		if not isinstance(name, str):
			raise TypeError("The card name must be a string")
		elif ' of ' not in name:
			raise ValueError("The card name must be of the format '2 of clubs'")
		else:
			self._name = name
	
	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		possible_vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
		if value not in possible_vals:
			raise ValueError("The value is incorrect. Should lie in {0}".format(possible_vals))
		else:
			self._value = value

	@property
	def suit(self):
		return self._suit

	@suit.setter
	def suit(self, suit):
		possible_suits = ['spades', 'clubs', 'hearts', 'diamonds']
		if suit not in possible_suits:
			raise ValueError("The suit is incorrect. Allowed values : {0}".format(possible_suits))
		else:
			self._suit = suit

	def initialize_card_details(self):
		self.value = self.name.split(' of ')[0]
		self.suit = self.name.split(' of ')[1]
		card_ranking = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'jack': 10, 'queen': 11, 'king': 12, 'ace': 13}
		self.rank = card_ranking[self.value]

	def __eq__(self, other):
		return self.rank == other.rank

	def __gt__(self, other):
		return self.rank > other.rank

	def __lt__(self, other):
		return self.rank < other.rank

	def __ge__(self, other):
		return self.rank >= other.rank

	def __le__(self, other):
		return self.rank <= other.rank

	def __ne__(self, other):
		return not self.__eq__(other)

	def __repr__(self):
		return f"Card({self.value, self.suit})"

	def __str__(self):
		return f"Your card is the {self.value} of {self.suit}"

	def __hash__(self):
		return (self.value, self.suit)

	def is_exact_match(self, other):
		return self.suit == other.suit and self.value == other.value 

class Hand:

	def __init__(self, card_list):
		self.hand_priority = {'High Card' : 1, 'One Pair' : 2, 'Two Pair' : 3, 'Three of a Kind' : 4, 'Straight' : 5, 'Flush' : 6, 'Full House' : 7, 'Four of a Kind' : 8, 'Straight Flush' : 9}
		self.cards = card_list
		self.hand_name = str()
		self.sorting_key = []
		self.pairs = []
		self.threes = []
		self.fours = []
		self.straight = False
		self.flush = False
		self.classify()
		self.hand_rank = self.hand_priority[self.hand_name]

	@property
	def cards(self):
		return self._cards
	
	@cards.setter
	def cards(self, cards):
		if len(cards) > 5 or len(cards) < 3:
			raise ValueError("Invalid number of cards")
		if not isinstance(cards, list):
			raise ValueError("Hand expects a list of cards")
		for card in cards:
			if not isinstance(card, Card):
				raise ValueError(f"The {card} element is not of type Card in the Hand. Please send a list of Card objects")
		sorted_cards = sorted(cards, key = lambda x: x.rank, reverse = True)
		for card1, card2 in zip(sorted_cards[:-1], sorted_cards[1:]):
			if card1.is_exact_match(card2):
				raise ValueError("{0} is repeated, only 1 deck is present. Please check again".format(card1.__repr__()))
		self._cards = sorted_cards

	def get_pairs(self, pair_length = 2, already_paired_indices = []):
		pair_list = []
		paired_indices = []
		card_ranks = [(index, card.rank) for index, card in enumerate(self.cards) if index not in already_paired_indices]
		card_combinations = combinations(card_ranks, pair_length)
		for selected_cards in card_combinations:
			selected_card_indices = [card[0] for card in selected_cards]
			selected_card_ranks = [card[1] for card in selected_cards]
			if len(set(selected_card_ranks)) == 1:
				pair_list.append(tuple([(index, self.cards[index]) for index in selected_card_indices]))
				paired_indices += selected_card_indices
		return pair_list, paired_indices + already_paired_indices

	def is_straight(self):
		card_ranks = [card.rank for card in self.cards]
		differences = [x - y for x,y in zip(card_ranks[:-1], card_ranks[1:])]
		return set(differences) == {1}

	def is_flush(self):
		suits = [card.suit for card in self.cards]
		return len(set(suits)) == 1

	def classify(self):
		paired_indices = []
		fours, paired_indices = self.get_pairs(pair_length = 4, already_paired_indices = paired_indices)
		threes, paired_indices = self.get_pairs(pair_length = 3, already_paired_indices = paired_indices)
		pairs, paired_indices = self.get_pairs(pair_length = 2, already_paired_indices = paired_indices)
		self.pairs = [] or pairs
		self.threes = [] or threes
		self.fours = [] or fours
		self.straight = self.is_straight()
		self.flush = self.is_flush()

		if self.straight and self.flush:
			self.hand_name = 'Straight Flush'

		elif self.straight:
			self.hand_name = 'Straight'

		elif self.flush:
			self.hand_name = 'Flush'

		elif self.fours:
			self.hand_name = 'Four of a Kind'

		elif self.threes and self.pairs:
			self.hand_name = 'Full House'

		elif self.threes:
			self.hand_name = 'Three of a Kind'

		elif len(self.pairs) > 1:
			self.hand_name = 'Two Pair'

		elif self.pairs:
			self.hand_name = 'One Pair'

		else:
			self.hand_name = 'High Card'

		self.sorting_key = self.form_sorting_keys()

	def form_sorting_keys(self):
		key = []
		selected_card_indices = []
		remaining_card_indices = [i for i in range(len(self.cards))]
		for group in [self.fours, self.threes, self.pairs]:
			if group:
				selected_group_indices = [x[0] for pair in group for x in pair]
				selected_card_indices += selected_group_indices
				remaining_card_indices = [x for x in remaining_card_indices if x not in selected_group_indices]
				selected_card_ranks = [self.cards[index].rank for index in selected_group_indices]
				unique_ranks = list(set(selected_card_ranks))
				key += sorted(unique_ranks, reverse = True)
		remaining_card_ranks = [self.cards[index].rank for index in remaining_card_indices]
		key += sorted(remaining_card_ranks, reverse = True)
		return key

	def __gt__(self, other):
		if len(self.cards) != len(other.cards):
			raise AssertionError("Are you comparing Teen patti hands with poker ones? Number of cards in hands need to be equal!!")
		if self.hand_rank != other.hand_rank:
			return self.hand_rank > other.hand_rank
		else:
			return self.sorting_key > other.sorting_key

	def __lt__(self, other):
		if len(self.cards) != len(other.cards):
			raise AssertionError("Are you comparing Teen patti hands with poker ones? Number of cards in hands need to be equal!!")
		if self.hand_rank != other.hand_rank:
			return self.hand_rank < other.hand_rank
		else:
			return self.sorting_key < other.sorting_key

	def __ge__(self, other):
		if len(self.cards) != len(other.cards):
			raise AssertionError("Are you comparing Teen patti hands with poker ones? Number of cards in hands need to be equal!!")
		if self.hand_rank != other.hand_rank:
			return self.hand_rank >= other.hand_rank
		else:
			return self.sorting_key >= other.sorting_key

	def __le__(self, other):
		if len(self.cards) != len(other.cards):
			raise AssertionError("Are you comparing Teen patti hands with poker ones? Number of cards in hands need to be equal!!")
		if self.hand_rank != other.hand_rank:
			return self.hand_rank <= other.hand_rank
		else:
			return self.sorting_key <= other.sorting_key

	def __eq__(self, other):
		if len(self.cards) != len(other.cards):
			raise AssertionError("Are you comparing Teen patti hands with poker ones? Number of cards in hands need to be equal!!")
		return self.hand_rank == other.hand_rank and self.sorting_key == other.sorting_key

	def __ne__(self, other):
		return not self.__eq__(other)

	def __repr__(self):
		card_repr = [(card.value, card.suit) for card in self.cards]
		return f"{self.hand_name} Hand{card_repr}"

	def __str__(self):
		card_str = [card.value + " of " + card.suit for card in self.cards]
		return f"You have a {self.hand_name} with Hand{card_str}"

vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
suits = ['spades', 'clubs', 'hearts', 'diamonds']

# single expression using map lambda and zip to create deck of cards
deck_of_cards = list(map(lambda x: Card(x[0] + ' of ' + x[1]), zip(vals*len(suits), suits*len(vals))))

def create_deck_of_cards_without_using_map_lambda_zip():
	'''single function to create a deck of cards using list comprehension'''
	deck = [Card(x + ' of ' + y) for x in vals for y in suits]
	return deck

def get_winning_hand(*hands: 'hand objects of the class Hand') -> 'winning hand(s)':
	'''
	Function finds the winning hand among a set of hands
	'''
	if len(hands) < 2:
		raise ValueError("More than one hand needs to be passed to obtain winner")
	winning_hands = []
	enumerated_hands = list(enumerate(hands)) # each element has (index, hand)
	sorted_hands = sorted(enumerated_hands, key = lambda x: x[1].hand_rank, reverse = True)
	for i in range(len(sorted_hands)):
		winning_hands.append({'index' : sorted_hands[i][0], 'hand' : sorted_hands[i][1]})
		if i != len(sorted_hands) - 1 and sorted_hands[i][1] != sorted_hands[i+1][1]: # if the next best hand is not a winner
			break

	if len(winning_hands) == 1: # single winner
		print(f"Winner is hand {winning_hands[0]['index'] + 1}")
		return winning_hands[0]['hand']
	else: # multiple winners due to ties
		print(f"The pot is split between these hands : {[x['index'] + 1 for x in winning_hands]}")
		return [x['hand'] for x in winning_hands]