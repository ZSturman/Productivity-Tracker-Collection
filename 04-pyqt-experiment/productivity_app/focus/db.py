import time
import datetime

def number_letter_alternation():
    sequence = "1a2b3c4d5e"
    start_time = time.time()

    for char in sequence:
        guess = input(f"Enter the next character (hint: it's {char}): ")
        if guess.lower() != char:
            print("Incorrect, try again.")
            return

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Congratulations, you completed the task in {time_taken} seconds.")

    # Log the score
    with open("scores.txt", "a") as file:
        file.write(f"{datetime.datetime.now()}: Number-Letter Alternation task completed in {time_taken} seconds\n")

number_letter_alternation()
