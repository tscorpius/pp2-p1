n = int(input())
arr = list(map(int, input().split()))

mx = arr[0]
for x in arr:
    if x > mx:
        mx = x

print(mx)
