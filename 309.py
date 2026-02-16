class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        p = 3.14159
        return p * self.radius * self.radius

r = int(input())
c = Circle(r)
print(f"{c.area():.2f}")
