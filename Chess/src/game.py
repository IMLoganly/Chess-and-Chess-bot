import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config

class Game:
    def __init__(self):
        self.currentPlayer = 'black'
        self.nextPlayer = 'white'
        self.hoveredSQ = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    def showBackground(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row+col)%2 == 0:
                    color =  (209, 209, 157)#white
                else:
                    color = (86, 163, 103)#green
                rect = (col*SQSIZE,row*SQSIZE,SQSIZE,SQSIZE)
                pygame.draw.rect(surface,color,rect)
        
    def showPieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                #Check if piece is on a square
                if self.board.squares[row][col].hasPiece():
                    piece = self.board.squares[row][col].piece

                    #all piece execpt held piece (dragger piece)
                    if piece is not self.dragger.piece:
                        piece.set_images(size=80)
                    #creates img on board
                        img = pygame.image.load(piece.texture)
                        imgCenter = col*SQSIZE+SQSIZE//2, row*SQSIZE + SQSIZE//2
                        piece.texture_rect = img.get_rect(center = imgCenter)

                        surface.blit(img,piece.texture_rect)

    def showMoves(self,surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                #color
                color = '#746875' if (move.final.row + move.final.col) % 2 == 0 else '#4c484d'

                rect = (move.final.col * SQSIZE,move.final.row * SQSIZE, SQSIZE,SQSIZE)
                pygame.draw.rect(surface,color,rect)
    
    def showLastMove(self,surface):
        if self.board.lastMove:
            initial = self.board.lastMove.initial
            final = self.board.lastMove.final

            for pos in [initial,final]:
                #color
                color = (244,247,116) if (pos.row + pos.col)% 2 == 0 else (172,195,51)
                rect = (pos.col*SQSIZE,pos.row*SQSIZE,SQSIZE,SQSIZE)
                pygame.draw.rect(surface,color,rect)

    def showHover(self,surface):
        if self.hoveredSQ:
            color = (180,180,180)
            rect = (self.hoveredSQ.col*SQSIZE,self.hoveredSQ.row*SQSIZE,SQSIZE,SQSIZE)
            pygame.draw.rect(surface,color,rect,width = 5)
            
    def nextTurn(self):
        self.nextPlayer = 'white' if self.nextPlayer == 'black' else 'black'

        self.currentPlayer = 'black' if self.currentPlayer == 'white' else 'white'
    
    def setHover(self,row,col):
        self.hoveredSQ = self.board.squares[row][col]

    def soundEffect(self, capture = False):

        if capture:
            self.config.captureSound.play()
        else:
            self.config.moveSound.play()

    


    def reset(self):
        self.__init__()


    