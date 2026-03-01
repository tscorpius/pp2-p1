import re

line = input()
pattern = r"Name: (.+), Age: (.+)"
match = re.match(pattern, line)

if match:
    name, age = match.groups()
    print(name, age)