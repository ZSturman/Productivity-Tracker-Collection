import random
import time

def digit_span_task(trials=5, min_digits=4, max_digits=8):
    for _ in range(trials):
        digits = [random.randint(0, 9) for _ in range(random.randint(min_digits, max_digits))]
        print("Remember these numbers:")
        print(digits)

        time.sleep(5)  # Wait for 5 seconds

        for _ in range(50):  # Clear the screen
            print("\n")

        guess = input("Enter the numbers you remembered, separated by spaces: ")

        if [int(num) for num in guess.split()] == digits:
            print("Correct!\n")
        else:
            print(f"Sorry, the correct sequence was {digits}\n")

digit_span_task()
