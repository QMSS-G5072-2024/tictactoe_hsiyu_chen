import pytest
from tictactoe_hc3448 import tictactoe_hc3448
from typing import Literal

#  verifies the initialize_board function creates an empty 3x3 board.
def test_initialize_board():
    board = tictactoe_hc3448.initialize_board()
    # check the board if it has 3 rows
    assert len(board) == 3, "Expect 3 rows"
    # check the board if it has 3 columns
    assert all(len(row) == 3 for row in board), "Expect 3 columns in all rows"
    # check if it is empty
    assert all(cell == ' ' for row in board for cell in row), "Cells are not all empty"
    
    print("test_initialize_board passed.")


#  checks whether make_move successfully places a player’s symbol on an empty cell. Test this for both players ‘X’ and ‘O’.
def test_make_move_valid():
    # Test for player 'X'
    board_x = tictactoe_hc3448.initialize_board()
    success_x = tictactoe_hc3448.make_move(board_x, 1, 1, 'X')  # Make a valid move for 'X'
    assert success_x == True, "The move should be successful."
    assert board_x[1][1] == 'X', "The cell (1,1) should contain 'X'."

    # Test for player 'O'
    board_o = tictactoe_hc3448.initialize_board()
    success_o = tictactoe_hc3448.make_move(board_o, 0, 0, 'O')  # Make a valid move for 'O'
    assert success_o == True, "The move should be successful."
    assert board_o[0][0] == 'O', "The cell (0,0) should contain 'O'."
    
    print("test_make_move_valid passed for both 'X' and 'O'.")
   
 
# ensure that it does not allow moves on already occupied cells and returns False. 
def test_make_move_invalid():
    # Initialize a board and place a move at (1, 1)
    board = tictactoe_hc3448.initialize_board()
    tictactoe_hc3448.make_move(board, 1, 1, 'X')  # Place 'X' at (1, 1)
    
    # Attempt to place 'O' at the same position (1, 1)
    success = tictactoe_hc3448.make_move(board, 1, 1, 'O')
    
    # Check that the move was not allowed
    assert success == False, "The move should be unsuccessful."
    assert board[1][1] == 'X', "The cell (1,1) should remain 'X'."

    print("test_make_move_invalid passed for occupied cells.")
    

# performs a series of operations: initializing the board, making multiple moves, checking for a winner, and resetting the game. After each operation, verify the state of the board and the game status (i.e. if there is a winner).
def test_game_integration():
    # 1: Initialize the board
    board = tictactoe_hc3448.initialize_board()
    assert board == [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], "The board should be initialized with empty spaces."
    
    # 2: Make multiple moves
    tictactoe_hc3448.make_move(board, 0, 0, 'X')  
    tictactoe_hc3448.make_move(board, 1, 1, 'O')  
    tictactoe_hc3448.make_move(board, 0, 1, 'X')  
    tictactoe_hc3448.make_move(board, 2, 1, 'O')  
    tictactoe_hc3448.make_move(board, 0, 2, 'X')  # winning move for 'X'
    
    # Verify board state after these moves
    expected_board = [
        ['X', 'X', 'X'], 
        [' ', 'O', ' '],
        [' ', 'O', ' ']
    ]
    assert board == expected_board, "The board state should match the expected board after the moves."
    
    # 3: Check for winner
    winner = tictactoe_hc3448.check_winner(board)
    assert winner == 'X', "Player 'X' should be the winner."
    
    # 4: Reset the game
    board = tictactoe_hc3448.reset_game()
    assert board == [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], "The board should be reset to an empty state."
    
    # Ensure no winner after reset
    winner_after_reset = tictactoe_hc3448.check_winner(board)
    assert winner_after_reset is None, "There should be no winner after the board is reset."

    print("test_game_integration passed.")



# Advanced Test

@pytest.mark.parametrize("initial_board, row, col, player, expected_success, expected_board, raises_error", [
    # Test Case 1: Valid move on an empty board
    ([[' ', ' ', ' '],
      [' ', ' ', ' '],
      [' ', ' ', ' ']], 0, 0, 'X', True, [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], None),
    
    # Test Case 2: Trying to move into an occupied cell
    ([['X', ' ', ' '],
      [' ', ' ', ' '],
      [' ', ' ', ' ']], 0, 0, 'O', False, [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], None),
    
    # Test Case 3: Valid move on a partially filled board
    ([['X', ' ', ' '],
      [' ', ' ', ' '],
      [' ', ' ', ' ']], 1, 1, 'O', True, [['X', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']], None),

    # Test Case 4: Out-of-bounds move (negative index)
    ([[' ', ' ', ' '],
      [' ', ' ', ' '],
      [' ', ' ', ' ']], -1, 0, 'X', None, None, IndexError),

    # Test Case 5: Out-of-bounds move (index greater than 2)
    ([[' ', ' ', ' '],
      [' ', ' ', ' '],
      [' ', ' ', ' ']], 3, 0, 'O', None, None, IndexError)
])

#Parameterized test for make_move function, checking multiple scenarios such as valid moves, invalid moves (occupied cell, out-of-bounds), and board updates.
def test_make_move(initial_board: list[list[str]], row: Literal[0] | Literal[1] | Literal[-1] | Literal[3], col: Literal[0] | Literal[1], player: Literal['X'] | Literal['O'], expected_success: None | bool, expected_board: list[list[str]] | None, raises_error: None | type[IndexError]):

    if raises_error:
        with pytest.raises(raises_error):
            tictactoe_hc3448.make_move(initial_board, row, col, player)
    else:
        success = tictactoe_hc3448.make_move(initial_board, row, col, player)
        assert success == expected_success, f"Expected {expected_success}, but got {success}."
        assert initial_board == expected_board, f"Expected board:\n{expected_board}\nBut got:\n{initial_board}"


@pytest.fixture
def fresh_board():
    return tictactoe_hc3448.initialize_board()

# test using the fresh_board fixture
@pytest.mark.parametrize("row, col, player, expected_success, expected_board", [
    # Test Case 1: Valid move on an empty board
    (0, 0, 'X', True, [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]),
    
    # Test Case 2: Valid move after the first move
    (1, 1, 'O', True, [[' ', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']]),

    # Test Case 3: Occupied cell (attempt to place a move in an already taken spot)
    (0, 0, 'O', False, [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']])
])
#Example 1: Test make_move using a fresh board initialized by the fresh_board fixture.
def test_make_move_freshboard(fresh_board, row, col, player, expected_success, expected_board):
    # Make an initial move for Test Case 3 to simulate the board state
    if row == 0 and col == 0 and player == 'O':
        tictactoe_hc3448.make_move(fresh_board, 0, 0, 'X')  # Initial move for 'X' to occupy (0,0)
    
    # Attempt to make the move for the test
    success = tictactoe_hc3448.make_move(fresh_board, row, col, player)
    # Assert whether the move was successful or not
    assert success == expected_success, f"Expected success: {expected_success}, but got: {success}."   
    # Assert the board state after the move
    assert fresh_board == expected_board, f"Expected board: {expected_board}, but got: {fresh_board}"

# Example 2: Test that the reset_game function properly resets the board to its initial state.
def test_reset_board(fresh_board):
    # Make a move on the fresh board
    tictactoe_hc3448.make_move(fresh_board, 1, 1, 'X')
    # Ensure the board has been updated
    assert fresh_board[1][1] == 'X', "The cell (1,1) should contain 'X' after the move."
    # Reset the board
    reset_board = tictactoe_hc3448.reset_game()
    # Ensure the board is reset to all empty spaces
    assert reset_board == [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], "The board should be reset to an empty state."