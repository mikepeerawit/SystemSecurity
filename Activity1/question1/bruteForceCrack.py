import hashlib
import itertools
import time

def brute_force_attack(dictionary_file, target_hash):
    with open(dictionary_file) as f:
        words = f.read().splitlines()
    for word in words:
        # Create all possible combinations of characters and number substitutions
        all_combinations = [''.join(combo) for combo in itertools.product(*((c.upper(), c.lower(), '0' if c == 'o' else '1' if c in 'il' else c) for c in word))]
        for c in all_combinations:
            # Hash the combination
            hashed_word = hashlib.sha1(c.encode()).hexdigest()
            # Compare the resulting hash value with the target hash value
            if hashed_word == target_hash:
                return c
    return None

# Example usage
start_time = time.time()
target_hash = 'd54cc1fe76f5186380a0939d2fc1723c44e8a5f7'
original_value = brute_force_attack('dictionary.txt', target_hash)
end_time = time.time()

if original_value:
    print(f'The original value is: {original_value}')
else:
    print('The original value could not be found in the dictionary.')
print(f'The runtime is {end_time - start_time} seconds.')
