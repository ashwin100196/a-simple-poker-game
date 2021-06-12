import random
import pytest
import inspect
import re
import os
import session6_part1 as s6
import math

README_CONTENT_CHECK_FOR = [
    'Card',
    'Hand',
    'get_winning_hand',
    'create_deck_of_cards_without_using_map_lambda_zip',
    'Usage',
    'Test Cases',
    'notebook_part1'
]

# generic tests

# 1
def test_readme_exists():
	assert os.path.isfile('README.md'), "Put a README file, man!!"

# 2
def test_readme_contents():
	readme_words = [word for line in open('README.md', 'r') for word in line]
	assert len(readme_words) >= 500, "Say more in the README. please....."

# 3
def test_readme_proper_description():
	README_LOOKS_GOOD = True
	with open('README.md', 'r') as f:
		content = f.read()
	for mandatory_word in README_CONTENT_CHECK_FOR:
		README_LOOKS_GOOD = README_LOOKS_GOOD and (mandatory_word in content)

	assert README_LOOKS_GOOD == True, "Cover all concepts, no half baked README alloweed"

# 4
def test_readme_file_for_formatting():
    f = open("README.md", "r")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

# 5
def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(s6)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines" 

# 6
def test_function_name_had_cap_letter():
    functions = inspect.getmembers(s6, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

#7 - test docstrings present
def test_function_has_docstrings():
    functions = inspect.getmembers(s6, inspect.isfunction)
    for func_name, function in functions:
        assert function.__doc__ is not None, "You have to implement docstring for every function"

#8 - test annotations present
def test_function_has_annotations():
    functions = inspect.getmembers(s6, inspect.isfunction)
    for func_name, function in functions:
        assert function.__annotations__ is not {}, "You have to implement docstring for every function"

# module specific test cases
# correct deck of cards
vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
suits = ['spades', 'clubs', 'hearts', 'diamonds']

test_deck_of_cards = [s6.Card(x + ' of ' + y) for x in vals for y in suits]

#9 - test single expression that creates deck of cards
def test_single_expression_deck_of_cards():
    for card in s6.deck_of_cards:
        assert card in test_deck_of_cards, "Incorrect card has been created"
    for card in test_deck_of_cards:
        assert card in s6.deck_of_cards, "Some cards have not been created"

#10 - test function that creates deck of cards
def test_function_deck_of_cards():
    created_deck = s6.create_deck_of_cards_without_using_map_lambda_zip()
    for card in created_deck:
        assert card in test_deck_of_cards, "Incorrect card has been created"
    for card in test_deck_of_cards:
        assert card in created_deck, "Some cards have not been created"

#11 - test invalid length of hands
def test_invalid_hand_length():
    with pytest.raises(ValueError):
        s6.Hand([s6.Card('2 of spades'), s6.Card('3 of hearts')])
    with pytest.raises(ValueError):
        s6.Hand([s6.Card('2 of spades'), s6.Card('3 of hearts'),s6.Card('4 of diamonds'), s6.Card('ace of hearts'),s6.Card('2 of clubs'), s6.Card('king of diamonds')])

#12 - test length mismatch of hands
def test_mismatched_hand_length():
    h1 = s6.Hand([s6.Card('2 of spades'), s6.Card('3 of hearts'), s6.Card('4 of diamonds')])
    h2 = s6.Hand([s6.Card('2 of spades'), s6.Card('3 of hearts'), s6.Card('4 of diamonds'), s6.Card('5 of spades')])
    with pytest.raises(AssertionError):
        winner = s6.get_winning_hand(h1,h2)

#13 - test invalid cards
def test_invalid_cards():
    with pytest.raises(ValueError):
        c1 = s6.Card('2 of apples')
    with pytest.raises(ValueError):
        c2 = s6.Card('11 of spades')

#14 - test repetition of cards in hand (due to 1 deck constraint)
def test_repeated_cards_in_hand():
    with pytest.raises(ValueError):
        h = s6.Hand([s6.Card('2 of spades'), s6.Card('3 of hearts'), s6.Card('4 of diamonds'), s6.Card('2 of spades')])

#15 - test invalid data type of card - expected string
def test_invalid_card_type():
    with pytest.raises(TypeError):
        c1 = s6.Card((2,'spades'))
    with pytest.raises(ValueError):
        c2 = s6.Card('10, hears')

#16 - test classify hand functionality
def test_hand_classification_functionality():
    h = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of hearts'), s6.Card('3 of hearts'), s6.Card('king of hearts'), s6.Card('ace of hearts')])
    assert h.hand_name == 'Flush'
    assert h.hand_rank == 6

    h = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of hearts'), s6.Card('6 of hearts'), s6.Card('8 of hearts'), s6.Card('9 of hearts')])
    assert h.hand_name == 'Straight Flush'
    assert h.hand_rank == 9

    h = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of clubs'), s6.Card('6 of spades'), s6.Card('8 of clubs'), s6.Card('9 of hearts')])
    assert h.hand_name == 'Straight'
    assert h.hand_rank == 5

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('ace of spades'), s6.Card('ace of diamonds'), s6.Card('9 of hearts')])
    assert h.hand_name == 'Four of a Kind'
    assert h.hand_rank == 8

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('ace of spades'), s6.Card('king of diamonds'), s6.Card('king of hearts')])
    assert h.hand_name == 'Full House'
    assert h.hand_rank == 7

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('ace of spades'), s6.Card('3 of diamonds'), s6.Card('9 of hearts')])
    assert h.hand_name == 'Three of a Kind'
    assert h.hand_rank == 4

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('jack of spades'), s6.Card('9 of diamonds'), s6.Card('9 of hearts')])
    assert h.hand_name == 'Two Pair'
    assert h.hand_rank == 3

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('7 of spades'), s6.Card('2 of diamonds'), s6.Card('9 of hearts')])
    assert h.hand_name == 'One Pair'
    assert h.hand_rank == 2

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('king of clubs'), s6.Card('2 of spades'), s6.Card('10 of diamonds'), s6.Card('9 of hearts')])
    assert h.hand_name == 'High Card'
    assert h.hand_rank == 1

#17 - test highcards sorting key functionality
def test_hand_sorting_key():
    h = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of hearts'), s6.Card('3 of hearts'), s6.Card('king of hearts'), s6.Card('ace of hearts')])
    assert h.sorting_key == [13,12,6,4,2]

    h = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of hearts'), s6.Card('6 of hearts'), s6.Card('8 of hearts'), s6.Card('9 of hearts')])
    assert h.sorting_key == [8,7,6,5,4]

    h = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of clubs'), s6.Card('6 of spades'), s6.Card('8 of clubs'), s6.Card('9 of hearts')])
    assert h.sorting_key == [8,7,6,5,4]

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('ace of spades'), s6.Card('ace of diamonds'), s6.Card('9 of hearts')])
    assert h.sorting_key == [13,8]

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('ace of spades'), s6.Card('king of diamonds'), s6.Card('king of hearts')])
    assert h.sorting_key == [13,12]

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('ace of spades'), s6.Card('3 of diamonds'), s6.Card('9 of hearts')])
    assert h.sorting_key == [13,8,2]

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('jack of spades'), s6.Card('9 of diamonds'), s6.Card('9 of hearts')])
    assert h.sorting_key == [13,8,10]

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('7 of spades'), s6.Card('2 of diamonds'), s6.Card('9 of hearts')])
    assert h.sorting_key == [13,8,6,1]

    h = s6.Hand([s6.Card('ace of hearts'), s6.Card('king of clubs'), s6.Card('2 of spades'), s6.Card('10 of diamonds'), s6.Card('9 of hearts')])
    assert h.sorting_key == [13,12,9,8,1]

#18 - test get_winning_hand functionality(20+ combinations)
def test_get_winning_hand_functionality():
    flush1 = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of hearts'), s6.Card('3 of hearts'), s6.Card('king of hearts'), s6.Card('ace of hearts')])
    flush2 = s6.Hand([s6.Card('5 of spades'), s6.Card('7 of spades'), s6.Card('3 of spades'), s6.Card('king of spades'), s6.Card('queen of spades')])
    straight_flush = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of hearts'), s6.Card('6 of hearts'), s6.Card('8 of hearts'), s6.Card('9 of hearts')])
    royal_flush = s6.Hand([s6.Card('10 of hearts'), s6.Card('jack of hearts'), s6.Card('king of hearts'), s6.Card('queen of hearts'), s6.Card('ace of hearts')])
    straight = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of clubs'), s6.Card('6 of spades'), s6.Card('8 of clubs'), s6.Card('9 of hearts')])
    four_kind = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('ace of spades'), s6.Card('ace of diamonds'), s6.Card('9 of hearts')])
    full_house = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('ace of spades'), s6.Card('king of diamonds'), s6.Card('king of hearts')])
    three_kind = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('ace of spades'), s6.Card('3 of diamonds'), s6.Card('9 of hearts')])
    two_pair = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('jack of spades'), s6.Card('9 of diamonds'), s6.Card('9 of hearts')])
    one_pair = s6.Hand([s6.Card('ace of hearts'), s6.Card('ace of clubs'), s6.Card('7 of spades'), s6.Card('2 of diamonds'), s6.Card('9 of hearts')])
    high_card1 = s6.Hand([s6.Card('ace of hearts'), s6.Card('king of clubs'), s6.Card('2 of spades'), s6.Card('10 of diamonds'), s6.Card('9 of hearts')])
    high_card2 = s6.Hand([s6.Card('3 of hearts'), s6.Card('king of clubs'), s6.Card('2 of spades'), s6.Card('10 of diamonds'), s6.Card('9 of hearts')])

    assert s6.get_winning_hand(flush1, flush2) == flush1
    assert s6.get_winning_hand(straight_flush, flush2) == straight_flush
    assert s6.get_winning_hand(royal_flush, straight_flush) == royal_flush
    assert s6.get_winning_hand(flush1, straight) == flush1
    assert s6.get_winning_hand(flush2, straight) == flush2
    assert s6.get_winning_hand(straight, four_kind) == four_kind
    assert s6.get_winning_hand(full_house, four_kind) == four_kind
    assert s6.get_winning_hand(full_house, flush1) == full_house
    assert s6.get_winning_hand(straight, three_kind) == straight
    assert s6.get_winning_hand(two_pair, three_kind) == three_kind
    assert s6.get_winning_hand(two_pair, one_pair) == two_pair
    assert s6.get_winning_hand(high_card1, one_pair) == one_pair
    assert s6.get_winning_hand(high_card1, high_card2) == high_card1
    assert s6.get_winning_hand(high_card1, high_card1) == [high_card1, high_card1] # both should be winning hands

#19 - test str of card and hand
def test_str_card_hand():
    c1 = s6.Card('5 of hearts')
    h1 = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of hearts'), s6.Card('3 of hearts'), s6.Card('king of hearts'), s6.Card('ace of hearts')])
    assert 'Your card is the' in c1.__str__()
    assert 'You have' in h1.__str__()

#20 - test repr of card and hand classes
def test_repr_card_hand():
    c1 = s6.Card('5 of hearts')
    h1 = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of hearts'), s6.Card('3 of hearts'), s6.Card('king of hearts'), s6.Card('ace of hearts')])
    assert 'object at' not in c1.__repr__()
    assert 'object at' not in h1.__repr__()

#21 - test get_winning_hand invalid number of hands : must be atleast two hands
def test_get_winning_hand_invalid_number_of_hands():
    with pytest.raises(ValueError):
        flush1 = s6.Hand([s6.Card('5 of hearts'), s6.Card('7 of hearts'), s6.Card('3 of hearts'), s6.Card('king of hearts'), s6.Card('ace of hearts')])
        winner = s6.get_winning_hand(flush1)