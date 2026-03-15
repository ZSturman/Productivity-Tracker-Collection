import random

def print_board(board, revealed):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if revealed[i][j]:
                print(board[i][j], end=' ')
            else:
                print('_', end=' ')
        print()

def card_matching_game():
    cards = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cards *= 2  # We need pairs of each card
    random.shuffle(cards)

    # Initialize game board
    board = [[0]*4 for _ in range(4)]
    revealed = [[False]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            board[i][j] = cards[i*4 + j]

    # Game loop
    while not all(val for sublist in revealed for val in sublist):
        print_board(board, revealed)
        x1, y1 = map(int, input("Enter coordinates of the first card to flip (x, y): ").split())
        x2, y2 = map(int, input("Enter coordinates of the second card to flip (x, y): ").split())
        if board[x1][y1] == board[x2][y2]:
            revealed[x1][y1] = revealed[x2][y2] = True
            print("Match found!")
        else:
            print("Not a match, try again.")
    print("Congratulations, you found all pairs!")

card_matching_game()
