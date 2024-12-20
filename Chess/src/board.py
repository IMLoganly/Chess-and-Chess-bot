from const import *
from square import Square
from piece import *
from move import Move


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.lastMove = None
        self._create()
        self._addPieces('white')
        self._addPieces('black')


    def move(self,piece,move):
        initial = move.initial
        final = move.final

        #board move update(console)
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece 
        #move
        piece.moved = True
        #remove valid moves
        piece.clearMoves()

        #hold last move
        self.lastMove = move

    def validMove(self,piece,move):
        return move in piece.moves

    def  calcMoves(self,piece,row,col):
        '''
        Takes a given piece and gets all the valid moves for
        a piece on a spacific position on the board
        '''
        def pawnMoves():
            steps = 1 if piece.moved else 2

            #Vertical moves (up:white down:black)
            start = row+piece.dir
            end = row + (piece.dir *(1+steps))
            for possibleMoveRow in range(start,end,piece.dir):
                if Square.inRange(possibleMoveRow):
                    if self.squares[possibleMoveRow][col].isEmpty():
                        #create square for move
                        initial = Square(row,col)
                        final = Square(possibleMoveRow,col)

                        move = Move(initial,final)
                        piece.add_move(move)

                    #piece is blocking pawns movement
                    else:break
                        
                else:break
            #Diangle move (taking opponents piece)          
            possibleMoveRow = row + piece.dir
            possibleMoveCols = [col-1,col+1]
            for possMoveCol in possibleMoveCols:
                if Square.inRange(possibleMoveRow,possMoveCol):
                    if self.squares[possibleMoveRow][possMoveCol].hasEnemyPiece(piece.color):
                        #create square for move
                        initial = Square(row,col)
                        final = Square(possibleMoveRow,possMoveCol)
                        #display move on board
                        move = Move(initial,final)
                        piece.add_move(move)

            
        def knightMoves():
            #8 possible moves
            possibleMoves = [ 
                (row-2,col+1),
                (row-1,col+2),
                (row+1,col+2),
                (row+2,col+1),
                (row+2,col-1),
                (row+1,col-2),
                (row-1,col-2),
                (row-2,col-1)
            ]
            for posMove in possibleMoves:
                possibleMoveRow,possibleMoveCol = posMove
                if Square.inRange(possibleMoveRow,possibleMoveCol):
                    if self.squares[possibleMoveRow][possibleMoveCol].isEmptyOrEnemy(piece.color):
                        #create square for move
                        initial = Square(row,col)
                        final = Square(possibleMoveRow,possibleMoveCol)

                        #creates move
                        move = Move(initial,final)

                        #append vaild move 
                        piece.add_move(move)

        def straightLineMoves(incrs):
            for incr in incrs:
                rowIncr, colIncr = incr
                possibleMoveRow = row + rowIncr
                possibleMoveCol = col + colIncr
                running = True
                while running:
                    if Square.inRange(possibleMoveRow,possibleMoveCol):
                        #create square for move
                        initial = Square(row,col)
                        final = Square(possibleMoveRow,possibleMoveCol)

                        move = Move(initial,final)

                        if self.squares[possibleMoveRow][possibleMoveCol].isEmpty():
                            piece.add_move(move)

                        #Enemy piece at current square
                        if self.squares[possibleMoveRow][possibleMoveCol].hasEnemyPiece(piece.color):
                            piece.add_move(move)
                            running = False
                        #team piece at the current square
                        if self.squares[possibleMoveRow][possibleMoveCol].hasTeamPiece(piece.color):
                            running = False

                    else:running = False
                        
                    #Increments    
                    possibleMoveRow = possibleMoveRow + rowIncr
                    possibleMoveCol = possibleMoveCol + colIncr
                        
        def kingMoves():
            possibleMoves = [
                (row-1,col+0), #up
                (row-1,col+1), #up-right
                (row+0,col+1), #right
                (row+1,col+1), #down-right
                (row+1,col+0), #down
                (row+1,col-1), #down-left
                (row+0,col-1), #left
                (row-1,col-1)] #up-left
            #normal moves
            for possibleMove in possibleMoves:
                possibleMoveRow, possibleMoveCol = possibleMove
                if Square.inRange(possibleMoveRow,possibleMoveCol):
                    if self.squares[possibleMoveRow][possibleMoveCol].isEmptyOrEnemy(piece.color):
                        #create square for move
                        initial = Square(row,col)
                        final = Square(possibleMoveRow,possibleMoveCol)
                        #creates move
                        move = Move(initial,final)
                        #append vaild move 
                        piece.add_move(move)
            #Castling (king or queen)

        if isinstance(piece,Pawn):
            pawnMoves()
        elif isinstance(piece,Knight):
            knightMoves()
            
        elif isinstance(piece,Bishop):
            straightLineMoves([
                (-1,1),  #up-right
                (-1,-1), #up-left
                (1,-1),  #down-left
                (1,1)    #down-right
            ])

        elif isinstance(piece,Rook):
            straightLineMoves([
                (-1,0), #up
                (0,1),  #right
                (1,0),  #down
                (0,-1)  #left
            ])

        elif isinstance(piece,Queen):
            straightLineMoves([
                (-1,1),  #up-right
                (-1,-1), #up-left
                (1,-1),  #down-left
                (1,1),   #down-right
                (-1,0), #up
                (0,1),  #right
                (1,0),  #down
                (0,-1)  #left
            ])

        elif isinstance(piece,King):
            kingMoves()



    def _create(self):
        '''
        adds a Sqaure() class to each square on the board
        '''
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)

    def _addPieces(self,color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)

        #pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        
        #knights
        self.squares[row_other][1] = Square(row_other,1,Knight(color)) 
        self.squares[row_other][6] = Square(row_other,6,Knight(color))

        #bishops
        self.squares[row_other][2] = Square(row_other,2,Bishop(color)) 
        self.squares[row_other][5] = Square(row_other,5,Bishop(color))

        
        #Rooks
        self.squares[row_other][0] = Square(row_other,0,Rook(color)) 
        self.squares[row_other][7] = Square(row_other,7,Rook(color)) 

        #Queen
        self.squares[row_other][3] = Square(row_other,3,Queen(color))    

        #King
        self.squares[row_other][4] = Square(row_other,4,King(color))    
