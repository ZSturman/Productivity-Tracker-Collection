import random
import time

def trail_making_test_A(n=15):
    numbers = list(range(1, n+1))
    random.shuffle(numbers)

    print("Connect these numbers in ascending order:")
    print(numbers)

    start = time.time()

    for i in range(1, n+1):
        guess = int(input(f"Enter number {i}: "))
        if guess != i:
            print("Incorrect, please try again.")
            return
    end = time.time()

    print(f"\nCongratulations, you completed the test in {end - start} seconds.")

trail_making_test_A()
