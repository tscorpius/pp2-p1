import re

s = input()
def repeat_digit(match):
    return match.group() * 2

result = re.sub(r'\d', repeat_digit, s)
print(result)