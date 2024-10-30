# read version from installed package
from importlib.metadata import version
__version__ = version("tictactoe_hc3448")

from .tictactoe_hc3448 import initialize_board, make_move, check_winner, reset_game