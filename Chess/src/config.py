import pygame
import os

from sound import Sound

class Config:

    def __init__(self):
        self.moveSound= Sound(os.path.join('assets/sounds/move.wav'))
        self.captureSound = Sound(os.path.join('assets/sounds/capture.wav'))



