from const import *
from square import Square
from piece import *
from move import Move

import copy
import random

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.lastMove = None
        self._create()
        self._addPieces('white')
        self._addPieces('black')


    def move(self,piece,move, testing=False):
        initial = move.initial
        final = move.final


        #board move update(console)
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece 
        
        # pawn promotion
        if isinstance(piece,Pawn):
            self.checkPromotion(piece,final)

        # castling
        if isinstance(piece,King):
            if self.castling(initial,final) and not testing:
                diff = final.col - initial.col
                rook = piece.leftRook if (diff < 0) else piece.rightRook
                self.move(rook,rook.moves[-1])

        #move
        piece.moved = True
        #remove valid moves
        piece.clearMoves()

        #hold last move
        self.lastMove = move

    def validAllMove(self,piece,row,col):
        return [row,col] in piece.allMoves

    def validMove(self,piece,move):
        return move in piece.moves

    def checkPromotion(self,piece,final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
            

    def castling(self,inital,final):
        return abs(inital.col - final.col) == 2


    def inCheck(self,piece,move):
        tempPiece = copy.deepcopy(piece)
        tempBoard = copy.deepcopy(self)
        tempBoard.move(tempPiece,move, testing = True)

        for row in range(ROWS):
            for col in range(COLS):
                if tempBoard.squares[row][col].hasEnemyPiece(piece.color):
                    p = tempBoard.squares[row][col].piece
                    tempBoard.calcMoves(p,row,col,bool = False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def  calcMoves(self,piece,row,col,bool = True):
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
                        
                        #see if move gets put in check
                        if bool:

                            if not self.inCheck(piece,move):
                                #adds move
                                piece.add_move(move)
                                piece.add_allMoves(possibleMoveRow,col)
                        else:
                            piece.add_move(move)
                            piece.add_allMoves(possibleMoveRow,col)

                    #piece is blocking pawns movement
                    else:break
                        
                else:break
            #Diangle move (taking opponents piece)          
            possibleMoveRow = row + piece.dir
            possibleMoveCols = [col-1,col+1]
            for possibleMoveCol in possibleMoveCols:
                if Square.inRange(possibleMoveRow,possibleMoveCol):
                    if self.squares[possibleMoveRow][possibleMoveCol].hasEnemyPiece(piece.color):
                        #create square for move
                        initial = Square(row,col)
                        finalPiece = self.squares[possibleMoveRow][possibleMoveCol].piece
                        final = Square(possibleMoveRow,possibleMoveCol,finalPiece)
                        #display move on board
                        move = Move(initial,final)
                        
                        #see if move gets put in check
                        if bool:

                            if not self.inCheck(piece,move):
                                #adds move
                                piece.add_move(move)
                                piece.add_allMoves(possibleMoveRow,possibleMoveCol)
                        else:
                            piece.add_move(move)
                            piece.add_allMoves(possibleMoveRow,possibleMoveCol)
                       

            
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
                        finalPiece = self.squares[possibleMoveRow][possibleMoveCol].piece
                        final = Square(possibleMoveRow,possibleMoveCol,finalPiece)
                        
                        #creates move
                        move = Move(initial,final)
                        
                        #see if move gets put in check
                        if bool:

                            if not self.inCheck(piece,move):
                                #adds move
                                piece.add_move(move)
                                piece.add_allMoves(possibleMoveRow,possibleMoveCol)
                            else: break
                        else:
                            piece.add_move(move)
                            piece.add_allMoves(possibleMoveRow,possibleMoveCol)

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
                        finalPiece = self.squares[possibleMoveRow][possibleMoveCol].piece
                        final = Square(possibleMoveRow,possibleMoveCol,finalPiece)

                        move = Move(initial,final)

                        if self.squares[possibleMoveRow][possibleMoveCol].isEmpty():
                            #see if move gets put in check
                            if bool:

                                if not self.inCheck(piece,move):
                                    #adds move
                                    piece.add_move(move)
                                    piece.add_allMoves(possibleMoveRow,possibleMoveCol)
                            else:
                                piece.add_move(move)
                                piece.add_allMoves(possibleMoveRow,possibleMoveCol)

                        #Enemy piece at current square
                        elif self.squares[possibleMoveRow][possibleMoveCol].hasEnemyPiece(piece.color):
                                                    #see if move gets put in check
                            if bool:

                                if not self.inCheck(piece,move):
                                    #adds move
                                    piece.add_move(move)
                                    piece.add_allMoves(possibleMoveRow,possibleMoveCol)
                            else:
                                piece.add_move(move)
                                piece.add_allMoves(possibleMoveRow,possibleMoveCol)
                            running = False
                            
                        #team piece at the current square
                        elif self.squares[possibleMoveRow][possibleMoveCol].hasTeamPiece(piece.color):
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
            for move in possibleMoves:
                possibleMoveRow = move[0]
                possibleMoveCol = move[1]
                if Square.inRange(possibleMoveRow,possibleMoveCol):
                    if self.squares[possibleMoveRow][possibleMoveCol].isEmptyOrEnemy(piece.color):
                        if not self.squares[possibleMoveRow][possibleMoveCol].hasTeamPiece(piece.color):
                            #create square for move
                            initial = Square(row,col)
                            final = Square(possibleMoveRow,possibleMoveCol)
                            #creates move
                            move = Move(initial,final) 
                            
                            #see if move gets put in check
                            if bool:
                                if  not self.inCheck(piece,move):
                                    #adds move
                                    piece.add_move(move)
                                    piece.add_allMoves(possibleMoveRow,possibleMoveCol)
                                   
                            else:
                                piece.add_move(move)
                                piece.add_allMoves(possibleMoveRow,possibleMoveCol)

                #Castling 
                if not piece.moved:
                        #queen side castle
                        leftRook = self.squares[row][0].piece
                        if isinstance(leftRook, Rook):
                            if not leftRook.moved:
                                for i in range(1,4): #checking if columns are empty between rook and queen
                                    if self.squares[row][i].hasPiece():
                                        break
                                    if i == 3:
                                        #adds left rook to king
                                        piece.leftRook = leftRook

                                        #create rook move
                                        initial = Square(row,0)
                                        final = Square(row,3)
                                        moveRook = Move(initial,final)

                                        #create king move
                                        initial = Square(row,col)
                                        final = Square(row,2)
                                        moveKing = Move(initial,final)

                                        if bool:
                                            if not self.inCheck(piece,moveKing) and not self.inCheck(leftRook,moveRook):
                                                #adds move to King
                                                piece.add_move(moveKing)
                                                piece.add_allMoves(row,2)
                                                #adds move to Rook
                                                leftRook.add_move(moveRook)
                                                leftRook.add_allMoves(row,3)
                                            
                                        else:
                                            #adds move to King
                                            piece.add_move(moveKing)
                                            piece.add_allMoves(row,2)
                                            #adds move to Rook
                                            leftRook.add_move(moveRook)
                                            leftRook.add_allMoves(row,3)
                                        
                        
                        #King side castle
                        rightRook = self.squares[row][7].piece
                        if isinstance(rightRook, Rook):
                            if not rightRook.moved:
                                for i in range(5,7): #checking if columns are empty between rook and queen
                                    if self.squares[row][i].hasPiece():
                                        break
                                    if i == 6:
                                        #adds right rook to king
                                        piece.rightRook = rightRook

                                        #create rook move
                                        initial = Square(row,7)
                                        final = Square(row,5)
                                        moveRook = Move(initial,final)

                                        #create king move
                                        initial = Square(row,col)
                                        final = Square(row,6)
                                        moveKing = Move(initial,final)

                                        if bool:
                                            if not self.inCheck(piece,moveKing) and not self.inCheck(rightRook,moveRook):
                                                #adds move to King
                                                piece.add_move(moveKing)
                                                piece.add_allMoves(row,6)
                                                #adds move to Rook
                                                rightRook.add_move(moveRook)
                                                rightRook.add_allMoves(row,5)
                                            
                                        else:
                                            #adds move to King
                                            piece.add_move(moveKing)
                                            piece.add_allMoves(row,6)
                                            #adds move to Rook
                                            rightRook.add_move(moveRook)
                                            rightRook.add_allMoves(row,5)




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
