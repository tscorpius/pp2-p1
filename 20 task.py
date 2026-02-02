'''n = int(input())
document = {}

for _ in range(n):
    parts = input().split()
    cmd = parts[0]
    if cmd == "set":
        key = parts[1]
        value = parts[2]
        document[key] = value  
    elif cmd == "get":
        key = parts[1]
        if key in document:
            print(document[key])
        else:
            print(f"KE: no key {key} found in the document")
            


n = int(input())
db = {}

for _ in range(n):
    command = input().split()

    if command[0] == "set":
        key = command[1]
        value = command[2]
        db[key] = value

    else:  
        key = command[1]
        if key in db:
            print(db[key])
        else:
            print(f"KE: no key {key} found in the document")
'''


import sys
read = sys.stdin.readline
write = sys.stdout.write
n = int(read())
db = {}
for _ in range(n):
    line = read().split()
    if line[0] == "set":
        db[line[1]] = line[2]
    else:  
        key = line[1]
        if key in db:
            write(db[key] + '\n')
        else:
            write(f"KE: no key {key} found in the document\n")

