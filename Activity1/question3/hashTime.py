import hashlib
import time

password="password"
start_time = time.time()
hashed_password = hashlib.sha1(password.encode()).hexdigest()
end_time = time.time()

print(f'The runtime is {end_time - start_time} seconds.')