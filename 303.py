triplet_to_digit = {
    "ZER": "0", "ONE": "1", "TWO": "2",
    "THR": "3", "FOU": "4", "FIV": "5",
    "SIX": "6", "SEV": "7", "EIG": "8",
    "NIN": "9"
}

digit_to_triplet = {v: k for k, v in triplet_to_digit.items()}


s = input().strip()


for op in "+-*":
    if op in s:
        left, right = s.split(op)
        operator = op
        break


def convert(x):
    result = ""
    for i in range(0, len(x), 3):
        result += triplet_to_digit[x[i:i+3]]
    return int(result)


a = convert(left)
b = convert(right)

if operator == "+":
    res = a + b
elif operator == "-":
    res = a - b
else:
    res = a * b


answer = ""
for digit in str(res):
    answer += digit_to_triplet[digit]

print(answer)
