class Account:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient Funds"
        else:
            self.balance -= amount
            return self.balance

balance, withdrawal = map(int, input().split())
acc = Account(balance)
result = acc.withdraw(withdrawal)
print(result)
