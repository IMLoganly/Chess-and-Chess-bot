import pygame
import sys
import random

from const import *
from game import Game
from square import Square
from move import Move
from piece import Piece

from chess_bot import chessBot

verseBot = True #play against bot or player (true = Bot, false = player)


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()
        self.bot = chessBot()



    def mainLoop(self):
        '''
        Responsible for calling all other classes
        '''
       
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        bot = self.bot
        #console board creation

        firstMoveWhite = True
        firstMoveBlack = True
 
        while True:
            #display methods/functions
            game.showBackground(screen)
            game.showLastMove(screen)
            game.showMoves(screen)
            game.showPieces(screen)
            game.showHover(screen)

            if dragger.dragging:
                dragger.updateBlit(screen)

            for event in pygame.event.get():
                
                if game.nextPlayer == "white" or not verseBot: #player move
                    

                    #click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.updateMouse(event.pos)

                        clickedRow = dragger.mouseY // SQSIZE
                        clickedCol = dragger.mouseX // SQSIZE

                        #checks if the clicked square has a piece
                        if board.squares[clickedRow][clickedCol].hasPiece():
                            piece = board.squares[clickedRow][clickedCol].piece
                            #check if valid piece(color)
                            if piece.color == game.nextPlayer:
                                piece.clearMoves()
                                piece.clearAllMoves()
                                board.calcMoves(piece,clickedRow,clickedCol, bool = True)
                                dragger.saveInitial(event.pos)
                                dragger.dragPiece(piece)
                                #show method
                                game.showBackground(screen)
                                game.showLastMove(screen)
                                game.showMoves(screen)
                                game.showPieces(screen)     

                            
                    #location of mouse
                    elif event.type == pygame.MOUSEMOTION:
                        motionRow = event.pos[1] //SQSIZE
                        motionCol = event.pos[0] //SQSIZE
                        
                        if motionRow > 7:
                            motionRow = 7
                        elif motionRow < 0:
                            motionRow = 0
                        if motionCol > 7:
                            motionCol = 7
                        elif motionCol < 0:
                            motionCol = 0   
                        game.setHover(motionRow,motionCol)

                        if dragger.dragging:
                            dragger.updateMouse(event.pos)
                            #display methods/functions
                            game.showBackground(screen)
                            game.showLastMove(screen)
                            game.showMoves(screen)
                            game.showPieces(screen)
                            game.showHover(screen)
                            dragger.updateBlit(screen)


                    #release click
                    elif event.type== pygame.MOUSEBUTTONUP:

                        if dragger.dragging:
                            dragger.updateMouse(event.pos)
                            releaseRow = dragger.mouseY // SQSIZE
                            releaseCol = dragger.mouseX // SQSIZE

                            #creates the possible move 
                            initial = Square(dragger.initialRow,dragger.initialCol)
                            final = Square(releaseRow,releaseCol)
                            move = Move(initial,final)
                            #checks if created move is valid
                            if board.validMove(dragger.piece,move):
                                captured = board.squares[releaseRow][releaseCol].hasPiece()
                                board.move(dragger.piece,move)
                                #sound plays
                                game.soundEffect(captured)
                                #display methods.functions
                                game.showBackground(screen)
                                game.showLastMove(screen)
                                game.showPieces(screen)
                                if game.nextPlayer != "white":
                                    firstMoveBlack = False
                                else:
                                    firstMoveWhite = False

                                #checks if checkmate occurs
                                kingRow,kingCol = board.findKing(game,board)
                                kingPiece = board.squares[kingRow][kingCol].piece
                                kingPiece.clearMoves()
                                kingPiece.clearAllMoves()
                                board.calcMoves(kingPiece,kingRow,kingCol,True)
                                if kingPiece.numberOfMoves() == 0 and (board.kingCheck(kingPiece,kingRow,kingCol,game.currentPlayer)) and not(firstMoveWhite or firstMoveBlack):
                                    print(f"Player {game.nextPlayer} wins")
                                    pygame.quit()
                                    sys.exit()  
                                game.nextTurn()
                                
                            dragger.undragPiece()


                    #key pressed
                    elif event.type == pygame.KEYDOWN:
                        
                        #restart game
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                   


                    #Quit
                    elif event.type == pygame.QUIT: # checks if we close the window
                        pygame.quit()
                        sys.exit()

                #moves for bot
                else:
                    #checks if checkmate occurs
                    kingRow,kingCol = board.findKing(game,board)

                    kingPiece = board.squares[kingRow][kingCol].piece
                    kingPiece.clearMoves()
                    kingPiece.clearAllMoves()
                    board.calcMoves(kingPiece,kingRow,kingCol,True)
                    
                    if kingPiece.numberOfMoves() == 0 and (board.kingCheck(kingPiece,kingRow,kingCol,game.currentPlayer)) and not(firstMoveWhite or firstMoveBlack):
                        print(f"Player {game.nextPlayer} wins")
                        pygame.quit()
                        sys.exit()        
                    print("test")
                    intRow, intCol = bot.checkSquare(board)
                    finalRow,finalCol = None,None
                    piece = board.squares[intRow][intCol].piece
                    piece.clearMoves()
                    piece.clearAllMoves()
                    board.calcMoves(piece, intRow, intCol, bool = True)
                    initial = Square(intRow, intCol)
                    valid_moves = piece.allMoves

                    
                    if len(valid_moves) :
                        notChecked = False
                        while not notChecked:
                            finalRow, finalCol = random.choice(valid_moves)
                            final = Square(finalRow,finalCol)
                            moveBot = Move(initial, final)
                            if not board.inCheck(piece,move):
                                notChecked = True
                    else:
                        print(intRow,intCol)
                        print(finalRow,finalCol)

                    captured = board.squares[finalRow][finalCol].hasPiece()
                    board.move(piece, moveBot)
                    game.soundEffect(captured)
                    game.showBackground(screen)
                    game.showLastMove(screen)
                    game.showPieces(screen)
                    firstMoveBlack = False
                    game.nextTurn()                   





                    if event.type == pygame.QUIT: # checks if we close the window
                        pygame.quit()
                        sys.exit()


            pygame.display.update()




main = Main()
main.mainLoop()