import sys
if len(sys.argv) == 2:
    if sys.argv[1].isnumeric():
        var = int(sys.argv[1])
        for i in range(var + 1):
            print(" " * (var - i), "#" * i, sep="")
