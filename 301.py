def is_all_even(n):
    for symbol in n:
        if int(symbol) % 2 != 0:
            return False
    return True


n = input()

if is_all_even(n):
    print("Valid")
else:
    print("Not valid")
