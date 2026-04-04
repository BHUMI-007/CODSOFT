from game import create_board, print_board, make_move, check_winner, is_draw
from minimax import best_move

def human_turn(board):
    while True:
        try:
            print("Enter your move:")
            row = int(input("Row (0, 1, 2): "))
            col = int(input("Col (0, 1, 2): "))
            if row in range(3) and col in range(3):
                if make_move(board, row, col, "X"):
                    break
                else:
                    print("❌ Cell already taken! Try again.")
            else:
                print("❌ Invalid input! Enter 0, 1, or 2 only.")
        except ValueError:
            print("❌ Please enter a number!")

def ai_turn(board):
    print("🤖 AI is thinking...")
    move = best_move(board)
    if move:
        make_move(board, move[0], move[1], "O")
        print(f"AI played at row {move[0]}, col {move[1]}")

def play_game():
    board = create_board()
    print("=" * 30)
    print("   Welcome to Tic-Tac-Toe!")
    print("   You = X  |  AI = O")
    print("=" * 30)
    print_board(board)

    while True:
        # Human turn
        human_turn(board)
        print_board(board)

        if check_winner(board, "X"):
            print("🎉 Congratulations! You won!")
            break
        if is_draw(board):
            print("🤝 It's a draw!")
            break

        # AI turn
        ai_turn(board)
        print_board(board)

        if check_winner(board, "O"):
            print("🤖 AI wins! Better luck next time.")
            break
        if is_draw(board):
            print("🤝 It's a draw!")
            break

    print("\nThanks for playing! 👋")
    play_again = input("Play again? (yes/no): ")
    if play_again.lower() in ["yes", "y"]:
        play_game()

if __name__ == "__main__":
    play_game()