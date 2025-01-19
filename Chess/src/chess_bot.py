import random

from piece import *
from board import Board
from square import Square

class chessBot:

    def checkSquare(self,board):
        validSquare = False
        while not validSquare:
            intRow = random.randint(0,7)
            intCol = random.randint(0,7)
            if board.squares[intRow][intCol].hasPiece():
                piece = board.squares[intRow][intCol].piece
                if piece.color == "black":
                    board.calcMoves(piece,intRow,intCol,bool = True)
                    if piece.numberOfMoves() > 0:
                        validSquare = True
                else:
                    intRow = random.randint(0,8)
                    intCol = random.randint(0,8)   
            else:
                intRow = random.randint(0,8)
                intCol = random.randint(0,8)
            
        return intRow , intCol





