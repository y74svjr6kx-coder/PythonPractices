# 1
def squares(n):
    for i in range(n + 1):
        yield i * i

n = int(input())

for x in squares(n):
    print(x)


# 2
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input())

print(",".join(str(x) for x in even_numbers(n)))


# 3
def divisible(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())

for x in divisible(n):
    print(x)


# 4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

a = int(input())
b = int(input())

for x in squares(a, b):
    print(x)


# 5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input())

for x in countdown(n):
    print(x)
