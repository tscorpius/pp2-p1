n = int(input()) 
surnames = [input().strip() for _ in range(n)]
unique_surnames = set(surnames)  
print(len(unique_surnames))
