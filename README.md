# Poker it

A python implementation to determine the winner(s) at a table of poker. For the dummies among us :P

### Usage

Using this to determine the winner at a table is extremely easy, and has been illustrated in an example in notebook_part1.ipynb.
Cards are created as objects using the class Card like:

```python
c = Card('king of clubs')
```

A hand object is then created of the Class Hand, which is nothing but a set of cards dealt to each player. Takes input of a list of Card objects

```python
h = Hand([Card('2 of spades'), Card('ace of diamonds'), Card('10 of hearts')])
```
Each hand object internally uses methods upon initialization to classify the type of Hand and a key is assigned to it to sort against multiple hands. For example,

```python
h = Hand([Card('2 of spades'), Card('ace of diamonds'), Card('10 of hearts')])

print(h.hand_name)
print(h.sorting_key)
```
This returns:
> High Card</br>
> [13, 9, 1]</br>

Cool right?

### Features

Some quality of life functionalities of this module includes:

- supports any number of players: will find the best hand from even hundreds of hands
- supports Teen patti (3 card poker), texas hold-em poker(5 cards), and even if we were to come up with some weird version with 4 cards in each Hand, this module will work
- simplifies the process of comparing hands. A simple ```hand1 > hand2``` comparison can be used to determine the better hand
- many hands, say at a poker table, can be sorted and even the max and min functions can be used to get the best and worst hands
- a utility function has been included named get_winning_hands(\*hands). This takes any number of hands as positional arguments to return the best hand(s)
- Handles tie scenarios in cases where multiple winners are present too!
- various validations have been carried out to ensure accurate Cards and Hands are created accurately. For example, 
```python
c = Card('5 of apples')
```
will definitely error out with ```ValueError: The suit is incorrect. Allowed values : ['spades', 'clubs', 'hearts', 'diamonds']```. Things like
```python
h = Hand([Card('5 of spades'), Card('5 of spades'), Card('5 of spades')])
```
will also error out with ```ValueError: Card(('5', 'spades')) is repeated, only 1 deck is present. Please check again```

All these are implemented using the classes below

### Classes

1. __Card__ - Represents a card from a deck

    > Attributes</br>
    > name - the full name of the card; 'queen of clubs'</br>
    > value - the number/symbol of the card; 'ace'</br>
    > suit - the suit name</br>
    > rank - a numerical rank to decide priority of cards</br>

    > Methods</br>
    > __init__ : initializes the Card object</br>
    > __repr__ : Provides the representation of the Card object</br>
    > __eq__, __gt__, __lt__, __ge__, __le__, __ne__ : methods to help compare objects by rank</br>
    > __hash__ : returns value, suit pair to act as a hash value for the object</br>
    > __is_exact_match__ : checks if a card is exactly the same as another card</br>

2. __Hand__ - Represents a Hand which is simply a list of cards. It is initialized with a list of objects of the Card class

    > Attributes</br>
    > cards - list of cards that make up the hand</br>
    > hand_name - a computed name of the type of hand; eg: Flust, Straight, Four of a kind etc. used to determine the better hand</br>
    > sorting_key - a combination of ranks of pairs and the ranks of single cards that form the hand. also used to determine the better hand</br>
    > pairs - number of combinations of 2 cards with the same value</br>
    > threes - number of combinations of 3 cards with the same value</br>
    > fours - number of combinations of 4 cards with the same value</br>
    > straight - boolean set to True when the cards are in sequence</br>
    > flush - boolean set to True when cards are of the same suit</br>
    > hand_rank - a numerical rank to decide priority of hands</br>

    > Methods</br>
    > __init__ : initializes the Hand object with list of cards</br>
    > __repr__ : Provides the representation of the Hand object</br>
    > __str__ : Provides the details of the Hand object</br>
    > __get_pairs__ : initialization method to calculate set of cards with same value</br>
    > __classify__ : initialization method to calculate the hand name, rank, sorting key etc</br>
    > __eq__, __gt__, __lt__, __ge__, __le__, __ne__ : methods to help compare objects by rank</br>

### Functions

1. __create_deck_of_cards_without_using_map_lambda_zip__ - Create a list of Card objects using list comprehension

    > Arguments</br>
    > None</br>
    
    > Returns</br>
    > deck - list of 52 Card objects representing the 52 cards</br>

With the help of the Card and Hand classes, the get_winning_hand function has been implemented.

2. __get_winning_hand__ - Identifies the winning hand among the hands sent as positional arguments and returns it. In cases where multiple hands are tied for the winning position, the appropriate hands are identified and returns them.

    > Arguments</br>
    > *hands - the number of hands to be considered to identify winner</br>
    
    > Returns</br>
    > winning hand - the hand that has won. In case multiple winners, a list of hand objects is returned</br>
    
    > Usage</br>
    > get_winning_hand(hand1, hand2,  hand3)</br>
    > Winner is hand 2</br>
    > You have a Straight Flush with Hand['7 of hearts', '6 of hearts', '5 of hearts']</br>

**Note:** The function also prints out the index of the winning hand

### Test Cases Summary and Results

| Sl.No | Test Name | Description |
|-----|-------------|--------------|
|1|test_readme_exists| README.md must exist|
|2|test_readme_contents| README must be greater than 500 words|
|3|test_readme_proper_description|Keywords must be present in README|
|4|test_readme_file_for_formatting|More than 10 # must be used in README|
|5|test_indentations|Code must be indented according to PEP8 conventions|
|6|test_function_name_had_cap_letter|Function names must not contain capital letters|
|7|test_function_has_docstrings|Functions must contain docstrings|
|8|test_function_has_annotations|Functions must contain annotations|
|9|test_single_expression_deck_of_cards|Must create a correct deck of cards using map, lambda and zip|
|10|test_function_deck_of_cards|Function using list comprehension must return correct deck of cards|
|11|test_invalid_hand_length|Must raise ValueError exception for hands with cards < 3 or > 5|
|12|test_mismatched_hand_length|Must raise ValueError when hands of unequal length are compared|
|13|test_invalid_cards| Must raise ValueError when invalid cards are created|
|14|test_repeated_cards_in_hand|Must raise ValueError when two cards in a Hand are exactly the same|
|15|test_invalid_card_type|Must raise exception when cards are created improperly|
|16|test_hand_classification_functionality|Must assign correct hand names for different card combinations|
|17|test_hand_sorting_key|Must assign correct sorting key for different card combinations|
|18|test_get_winning_hand_functionality|Must return the winner correctly for different hand combinations|
|19|test_str_card_hand|Card and Hand must contain appropriate representation method|
|20|test_repr_card_hand|Card and Hand must contain appropriate str method|
|21|test_get_winning_hand_invalid_number_of_hands|Must raise ValueError exception when get_winning_hand method is called with hands <= 1|

The test cases have all passed as shown below.
![TestCases](/test_case_results.png)