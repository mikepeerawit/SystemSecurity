import hashlib
import itertools
import json
import time
from concurrent.futures import ThreadPoolExecutor
import os

def get_combination_character(letter):
    characters = [letter.upper(), letter.lower()]
    if letter in 'il':
       characters.append('1') 
       return characters
    elif letter in 'o':
        characters.append('0')
        return characters
    else:
        return characters

def create_rainbow_table_part(words):
    rainbow_table = {}
    for word in words:
        # Create a copy of the word to make modifications
        modified_word = word
        # Create all possible combinations of characters and number substitutions
        all_combinations = [''.join(combo) for combo in itertools.product(*((get_combination_character(c)) for c in modified_word))]
        for c in all_combinations:
            # Hash the combination
            hashed_word = hashlib.sha1(c.encode()).hexdigest()
            # Add the combination and its hash to the dictionary
            rainbow_table[hashed_word] = c
    return rainbow_table

def create_rainbow_table(dictionary_file):
    rainbow_table = {}
    with open(dictionary_file) as f:
        words = f.read().splitlines()
    with ThreadPoolExecutor() as executor:
        # Divide the words into chunks and submit each chunk to a separate process
        chunks = [words[i:i+10] for i in range(0, len(words), 10)]
        results = [executor.submit(create_rainbow_table_part, chunk) for chunk in chunks]
        for future in results:
            rainbow_table.update(future.result())
    print(f'The tablesize is {len(rainbow_table)}.')
    return rainbow_table

def write_to_file(rainbow_table, filename):
    with open(filename, 'w') as f:
        json.dump(rainbow_table, f)

def find_original_value(hash_value, rainbow_table_file):
    with open(rainbow_table_file) as f:
        rainbow_table = json.load(f)
    return rainbow_table.get(hash_value)

def get_size(file_path, unit='bytes'):
    file_size = os.path.getsize(file_path)
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)

# Example Usage
start_time = time.time()
rainbow_table = create_rainbow_table('dictionary.txt')
with ThreadPoolExecutor() as executor:
    executor.submit(write_to_file, rainbow_table, 'rainbow_table.json')

hash_value = 'd54cc1fe76f5186380a0939d2fc1723c44e8a5f7'
original_value = find_original_value(hash_value, 'rainbow_table.json')
end_time = time.time()

if original_value:
    print(f'The original value is: {original_value}')
else:
    print('The original value could not be found in the rainbow table.')
print(f'The runtime is {end_time - start_time} seconds.')
filePath = './rainbow_table.json'
fileSize = get_size(filePath, 'mb')
print(f'The file size is {fileSize} MB')