import reversi
from boardserver import server

board = reversi.Board()
api = server.Server(board)
api.run()
