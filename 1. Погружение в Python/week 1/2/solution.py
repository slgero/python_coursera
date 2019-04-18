import sys
if len(sys.argv) == 2:
    my_str = sys.argv[1]
    if my_str.isdigit():
        my_sum = 0
        for i in my_str:
            my_sum += int(i)
        print(my_sum)
