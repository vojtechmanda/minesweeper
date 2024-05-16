import random

def generate_board(rows, columns, num_mines):
    """
    Creates a game board with hidden mines and neighbor counts.

    Args:
        rows: Number of rows in the board.
        columns: Number of columns in the board.
        num_mines: Number of mines to place on the board.

    Returns:
        A tuple containing two lists:
            - hidden_board: A list of lists representing the actual board with 'M' for mines and numbers for neighbor counts.
            - visible_board: A list of lists representing the player's view of the board with '-' for hidden squares and numbers/flags.
    """
    hidden_board = [[" " for _ in range(columns)] for _ in range(rows)]
    visible_board = [["-" for _ in range(columns)] for _ in range(rows)]

    # Place mines randomly
    for _ in range(num_mines):
        while True:
            row = random.randint(0, rows - 1)
            col = random.randint(0, columns - 1)
            if hidden_board[row][col] != "M":
                hidden_board[row][col] = "M"
                break

    # Calculate neighbor counts for each cell (excluding mines)
    for row in range(rows):
        for col in range(columns):
            if hidden_board[row][col] != "M":
                neighbor_mines = 0
                for i in range(row - 1, row + 2):
                    for j in range(col - 1, col + 2):
                        if 0 <= i < rows and 0 <= j < columns and hidden_board[i][j] == "M":
                            neighbor_mines += 1
                hidden_board[row][col] = str(neighbor_mines)

    return hidden_board, visible_board

def print_board(visible_board):
    """
    Prints the current state of the visible board to the console.
    """
    # Print column numbers
    print("  ", end="")
    for col in range(len(visible_board[0])):
        print(col, end=" ")
    print("")

    # Print separator line
    print("-" * (len(visible_board[0]) * 2 + 2))

    for row in range(len(visible_board)):
        print(row, "|", sep="", end="")
        for col in range(len(visible_board[0])):
            print(visible_board[row][col], end=" ")
        print("|")

def reveal_cell(row, col, hidden_board, visible_board):
    """
    Reveals the cell at the specified row and column on the visible board.

    Args:
        row: Row index of the cell.
        col: Column index of the cell.
        hidden_board: The hidden board containing mine locations and neighbor counts.
        visible_board: The visible board representing the player's view.
    """
    if visible_board[row][col] != "-":
        print("This cell is already revealed.")
        return

    if hidden_board[row][col] == "M":
        visible_board[row][col] = "M"
        print_board(visible_board)
        print("Game Over! You hit a mine!")
        return

    visible_board[row][col] = hidden_board[row][col]
    if hidden_board[row][col] == "0":
        # If the revealed cell has no neighboring mines, recursively reveal neighboring cells
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < len(visible_board) and 0 <= j < len(visible_board[0]):
                    reveal_cell(i, j, hidden_board, visible_board)

def play_game(rows, columns, num_mines):
    hidden_board, visible_board = generate_board(rows, columns, num_mines)
    game_over = False
    flags_planted = 0

    while not game_over:
        print_board(visible_board)

        # Get user input inside the loop
        action = input("Enter action (reveal: row col, flag: f row col, quit: q): ").lower().split()
        if len(action) < 2 or len(action) > 3:
            print("Invalid input. Please enter a valid action.")
            continue

        if action[0] == 'q':
            break

        try:
            row = int(action[1])
            col = int(action[2])
            if row < 0 or row >= rows or col < 0 or col >= columns:
                print("Invalid coordinates. Please enter values within board limits.")
                continue
        except ValueError:
            print("Invalid coordinates. Please enter integer values.")
            continue

        # Move reveal logic based on action type
        if action[0] == 'f':
            # Plant a flag
            if visible_board[row][col] == "-":
                visible_board[row][col] = "F"
                flags_planted += 1
            else:
                print("You can only plant flags on hidden squares.")
        else:
            # Reveal logic (action[0] == 'r')
            reveal_cell(row, col, hidden_board, visible_board)
            # Check for win condition after reveal
            win = True
            for row in range(rows):
                for col in range(columns):
                    if visible_board[row][col] != "F" and visible_board[row][col] != hidden_board[row][col]:
                        win = False
                        break
            if win:
                print("Congratulations! You win!")
                game_over = True
            for row in range(rows):
                for col in range(columns):
                    if visible_board[row][col] == "M":
                        game_over = True
                        break
# Example usage:
play_game(5, 5, 5)  # 5x5 board with 5 mines