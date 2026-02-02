n = int(input())
arr = list(map(int, input().split()))
freq = {}
for x in arr:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

max_count = max(freq.values())
most_freq = min(k for k, v in freq.items() if v == max_count)
print(most_freq)

