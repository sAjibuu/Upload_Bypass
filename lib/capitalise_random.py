#!/usr/bin/env python3

import random


# Function to return a string with a random capitalization
def capitalise_random(string):
	characters = list(string)
	length = len(characters)
	index_to_capitalize = random.randint(0, length - 1)
	at_least_one_capitalized = False
	for i in range(length):
		if characters[i].isalpha():
			characters[i] = characters[i].upper() if i == index_to_capitalize or not at_least_one_capitalized else characters[i].lower()
			at_least_one_capitalized = True
	return ''.join(characters)
