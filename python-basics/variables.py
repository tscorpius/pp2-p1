# ex 1
x = 5
y = "John"
print(x)
print(y)

# ex 2
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

# ex 3
x = "John"
# is the same as
x = 'John'

# ex 4
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

# ex 5
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)