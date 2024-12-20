import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def mainLoop(self):
        '''
        Responsible for calling all other classes
        '''
       
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

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

                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.updateMouse(event.pos)

                    clickedRow = dragger.mouseY // SQSIZE
                    clickedCol = dragger.mouseX // SQSIZE
                    #checks if thw clicked square has a piece
                    if board.squares[clickedRow][clickedCol].hasPiece():
                        piece = board.squares[clickedRow][clickedCol].piece
                        #check if valid piece(color)
                        if piece.color == game.nextPlayer:
                            board.calcMoves(piece,clickedRow,clickedCol)
                            dragger.saveInitial(event.pos)
                            dragger.dragePiece(piece)
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
                            board.move(dragger.piece,move)
                            #display methods.functions
                            game.showBackground(screen)
                            game.showLastMove(screen)
                            game.showPieces(screen)
                            game.nextTurn()
                            
                            
                    dragger.undragPiece()


                    

                #Quit
                elif event.type == pygame.QUIT: # checks if we close the window
                    pygame.quit()
                    sys.exit()

            






            pygame.display.update()



        pass


main = Main()
main.mainLoop()