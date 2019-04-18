import sys

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])

# find the discriminant
d = b * b - 4 * a * c

# if a == 0, we have linear equation: bx + c = 0
if a == 0:
    # bx = -c => x = -c / b
    if b != 0:
        print(-c // b)
    # if b == 0, we have no roots
elif d == 0:
    # if D == 0, we have only one root
    print(-b // (2 * a))
else:  # if D > 0 we have two roots
    r1 = (-b + d ** 0.5) / (2 * a)
    r2 = (-b - d ** 0.5) / (2 * a)
    print(int(r1))
    print(int(r2))
