n = int(input())
numbers = [input().strip() for _ in range(n)]
freq = {}
for num in numbers:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1

count_three = 0
for v in freq.values():
    if v == 3:
        count_three += 1

print(count_three)

