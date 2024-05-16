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
    print("   ", end="")
    for col in range(len(visible_board[0])):
        print(col if col > 9 else f"{col} ", end=" ")  # Add space for col >= 10
    print("")

    # Print separator line
    print("-" * ((len(visible_board[0]) * 3) + 3))
    for row in range(len(visible_board)):
        print(row if row > 9 else f"{row} ", "|", sep="", end="")
        for col in range(len(visible_board[0])):
            print(visible_board[row][col] if col==len(visible_board[0])-1 else f"{visible_board[row][col]} ", end=" ")
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
        if action[0] == 'p' and len(action) < 2 or len(action) > 3 or action[0] == 'f' and len(action) < 2 or len(action) > 3:
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

def play_random_game(rows, columns, num_mines):
  hidden_board, visible_board = generate_board(rows, columns, num_mines)
  tries = 0
  while tries < MAX_TRIES:
    # Analyze revealed cells for guaranteed safe/mine neighbors
    safe_cells, flagged_cells = analyze_revealed_cells(visible_board)
    # Reveal safe cells and update visible board
    for row, col in safe_cells:
      reveal_cell(row, col, hidden_board, visible_board)
    # Check win condition after revealing safe cells
    if check_win(visible_board, hidden_board):
      return tries
    # If no guaranteed safe cells, prioritize low-risk guesses
    if not safe_cells:
      guess = choose_low_risk_guess(visible_board)
      reveal_cell(guess[0], guess[1], hidden_board, visible_board)
      if visible_board[guess[0]][guess[1]] == "M":
        break
    tries += 1
  return -1  # Loss if no win within MAX_TRIES

def check_win(visible_board, hidden_board):
  """
  Checks if the player has won the game.

  Args:
      visible_board: A list of lists representing the player's view of the board.

  Returns:
      True if the player has won, False otherwise.
  """
  for row in range(len(visible_board)):
    for col in range(len(visible_board[0])):
      # Check if any non-flagged safe cell remains hidden
      if visible_board[row][col] != "F" and visible_board[row][col] != hidden_board[row][col]:
        return False
  return True

def analyze_revealed_cells(visible_board):
  safe_cells = []
  flagged_cells = []
  for row in range(len(visible_board)):
    for col in range(len(visible_board[0])):
      if visible_board[row][col].isdigit():
        num_mines = int(visible_board[row][col])
        # Count revealed neighbors (excluding flags)
        revealed_neighbors = 0
        for i in range(row - 1, row + 2):
          for j in range(col - 1, col + 2):
            if 0 <= i < len(visible_board) and 0 <= j < len(visible_board[0]) and visible_board[i][j] != "-":
              revealed_neighbors += 1
        # Check for guaranteed safe/mine neighbors based on revealed info
        hidden_neighbors = num_mines - revealed_neighbors
        if hidden_neighbors == 1:
          for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
              if 0 <= i < len(visible_board) and 0 <= j < len(visible_board[0]) and visible_board[i][j] == "-":
                safe_cells.append((i, j))
        elif hidden_neighbors == 0:
          flagged_cells.append((row, col))
  return safe_cells, flagged_cells

def choose_low_risk_guess(visible_board):
  """
  Selects a cell with a lower probability of being a mine.

  Args:
      visible_board: A list of lists representing the player's view of the board.

  Returns:
      A tuple (row, col) representing the chosen cell coordinates.
  """
  # Priority 1: Unrevealed cells next to revealed cells with numbers
  # These cells have a higher chance of being safe if the revealed number
  # of neighboring mines matches the number of revealed neighboring cells.
  priority_cells = []
  for row in range(len(visible_board)):
    for col in range(len(visible_board[0])):
      if visible_board[row][col].isdigit():
        num_mines = int(visible_board[row][col])
        revealed_neighbors = 0
        for i in range(row - 1, row + 2):
          for j in range(col - 1, col + 2):
            if 0 <= i < len(visible_board) and 0 <= j < len(visible_board[0]) and visible_board[i][j] != "-":
              revealed_neighbors += 1
        if revealed_neighbors == num_mines:
          for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
              if 0 <= i < len(visible_board) and 0 <= j < len(visible_board[0]) and visible_board[i][j] == "-":
                priority_cells.append((i, j))

  # If priority cells exist, choose one randomly (all have equal probability)
  if priority_cells:
    return random.choice(priority_cells)

  # Priority 2: Unrevealed cells with more revealed empty neighbors
  # These cells are surrounded by more revealed safe cells, suggesting a lower chance of being a mine.
  candidate_cells = []
  for row in range(len(visible_board)):
    for col in range(len(visible_board[0])):
      if visible_board[row][col] == "-":
        revealed_empty_neighbors = 0
        for i in range(row - 1, row + 2):
          for j in range(col - 1, col + 2):
            if 0 <= i < len(visible_board) and 0 <= j < len(visible_board[0]) and visible_board[i][j] == " ":
              revealed_empty_neighbors += 1
        candidate_cells.append((row, col, revealed_empty_neighbors))

  # Sort cells by the number of revealed empty neighbors (descending order)
  candidate_cells.sort(key=lambda x: x[2], reverse=True)

  # If multiple cells have the same number of empty neighbors, choose one randomly
  # (all with the same number have equal probability)
  max_empty_neighbors = candidate_cells[0][2]
  filtered_candidates = [cell for cell in candidate_cells if cell[2] == max_empty_neighbors]
  return random.choice(filtered_candidates)


MAX_TRIES = 100  # Adjust this value as needed

def main():
  rows = 5
  columns = 5
  num_mines = 5
  total_tries = 0
  while total_tries == 0:
    tries = play_random_game(rows, columns, num_mines)
    if tries > -1:
      total_tries = tries
  print(f"It took {total_tries} tries to win!")
main()
# Example usage:
#play_game(5, 5, 3)  # 5x5 board with 5 mines
