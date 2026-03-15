import random
import time

COLORS = ['red', 'green', 'blue', 'yellow']
simon_sequence = []

def simon_says(rounds=5):
    for _ in range(rounds):
        simon_sequence.append(random.choice(COLORS))
        print(f"Simon says: {', '.join(simon_sequence)}")
        time.sleep(2)

        for _ in range(50):  # Clear the screen
            print("\n")

        player_sequence = input("What did Simon say? Enter the colors separated by a space: ").split()

        if player_sequence != simon_sequence:
            print("Incorrect, game over.")
            return
        else:
            print("Correct!\n")

    print("Congratulations, you won Simon Says!")

simon_says()
