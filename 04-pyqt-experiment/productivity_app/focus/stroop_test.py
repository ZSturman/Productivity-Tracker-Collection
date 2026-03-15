import time
import random

COLORS = ['red', 'blue', 'green', 'yellow', 'black', 'white']
WORDS = ['RED', 'BLUE', 'GREEN', 'YELLOW', 'BLACK', 'WHITE']

def stroop_test(trials=10):
    correct = 0
    start = time.time()
    
    for _ in range(trials):
        word, color = random.choice(WORDS), random.choice(COLORS)
        print(f'\033[38;5;{color}m {word} \033[0m')
        
        answer = input('What is the color? ')
        
        if answer.lower() == color:
            correct += 1
            
    end = time.time()
    print(f'\nYou got {correct} out of {trials} correct.')
    print(f'Time taken: {end - start} seconds')

stroop_test()
