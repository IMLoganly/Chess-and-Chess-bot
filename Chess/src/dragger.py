import pygame
from const import *



class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initialRow = 0
        self.initialCol = 0

    #blit method
    def updateBlit(self,surface):
        #image path
        self.piece.set_images(size=128)
        texture = self.piece.texture

        #img
        img = pygame.image.load(texture)
        #rectangle for img
        imgCenter = (self.mouseX,self.mouseY)
        self.piece.texture_rect = img.get_rect(center = imgCenter)
        #places image on screen
        surface.blit(img,self.piece.texture_rect)

    # other methods
    #----------------
    def updateMouse(self,pos):
        self.mouseX, self.mouseY = pos #(Xcord,Ycord)
        if self.mouseX > WIDTH:
            self.mouseX = WIDTH
        if self.mouseY > HEIGHT:
            self.mouseY= HEIGHT

    def saveInitial(self,pos):
        self.initialRow = pos[1] // SQSIZE
        self.initialCol = pos[0] // SQSIZE

    def dragPiece(self,piece):
        self.piece = piece
        self.dragging = True

    def undragPiece(self):
        self.piece = None
        self.dragging = False

        