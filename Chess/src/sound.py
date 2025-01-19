import pygame

class Sound:

    def __init__(self,path):
         self.path = path
         self.sound = pygame.mixer.Sound(path)
         pass
    
    def play(self):
         '''
         Plays sound effect for piece moving
         '''
         pygame.mixer.Sound.play(self.sound)
         pass