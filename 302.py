super_n = int(input())

def isUsual(n):
	for prime in [2, 3, 5]:
		while n % prime == 0:
			n /= prime

	return n == 1


if isUsual(super_n):
	print("Yes")
else:
	print("No")