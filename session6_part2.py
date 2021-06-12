from functools import reduce, partial
import math
from swear_list import master_swear_list
from random import randint, choice

def fib_to(n):
	fibs = [0, 1]
	for i in range(2, n+1):
		fibs.append(fibs[-1] + fibs[-2])
	return fibs

# functions
def is_fibonacci(num):
	fib_numbers = fib_to(25)
	res = list(filter(lambda x: x == num, fib_numbers))
	return bool(res)

add_2_iterables_even_odd = lambda a,b: [i + j for i, j in zip(filter(lambda x: x%2 == 0, a), filter(lambda x: x%2 == 1, b))]
strip_vowels = lambda string: ''.join([x for x in string if x not in ('a', 'e', 'i', 'o', 'u')])
sigmoid = lambda l: reduce(lambda x,y: x+y, [1 / (1 + math.exp(-x)) for x in l])/len(l)
shift_chars_by_n = lambda string, n: ''.join([chr(97 + (ord(c) - 97 + n) % 26) for c in string])

filter_profanities = lambda para: ' '.join(['*'*len(word) if word.lower().replace(',', '').replace('.', '').replace('!', '').replace('.', '').replace('"', '') in [x.lower() for x in master_swear_list] else word for word in para.split(' ')])

add_evens = lambda l: reduce(lambda x,y: x+y if y%2==0 else x, [0] + l)
biggest_char = lambda string: reduce(lambda a, b: a if ord(a) > ord(b) else b, string)
add_every_third = lambda l: reduce(lambda a,b: (0, a[1]+b[1]) if b[0] % 3 == 0 else (0, a[1]), enumerate([0] + l))[1]

generate_number_plates_using_rand = lambda: ['KA' + str(randint(10,99)) + ''.join([choice([chr(i) for i in range(65, 91)]) for i in range(2)]) + str(randint(1000,9999)) for i in range(15)]

generate_number_plates_state_ranges = lambda state, range_start, range_end: [state + str(randint(10,99)) + ''.join([choice([chr(i) for i in range(65, 91)]) for i in range(2)]) + str(randint(range_start,range_end)) for i in range(15)]

generate_number_plates_partial_ka_1000_9999 = partial(generate_number_plates_state_ranges, 'KA', 1000, 9999)


