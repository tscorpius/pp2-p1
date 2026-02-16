import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

nums = list(map(int, input().split()))
primes = list(filter(lambda x: is_prime(x), nums))

if primes:
    print(*primes)
else:
    print("No primes")
