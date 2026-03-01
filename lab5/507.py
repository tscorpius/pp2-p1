import re

s = input()
pattern = input()
replacement = input()

result = re.sub(re.escape(pattern), replacement, s)

print(result)