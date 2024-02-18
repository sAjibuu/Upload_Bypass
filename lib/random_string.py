#!/usr/bin/env python3

import random
import string


# Generate a random string based on a given length
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
