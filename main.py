from model import Game

game = Game(ai_player=2)

while True:
    if game.is_ai_turn():
        game.play_turn()
    else:
        try:
            col = int(input("Enter column (1-9): "))
            game.play_turn(col)
        except ValueError:
            print("Please enter a number between 1 and 9.")
            continue

    winner = game.check_winner()
    if winner:
        print(f"Player {winner} wins!")
        break
