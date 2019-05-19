from Player import *
from Enemy import *
from Level import *
import random
import pygame

#Sets up a game between the AI and non-AI
class Game():
    def __init__(self, screen, player=None):
        """ Creates a game that contains two players and a level """
        self.screen = screen
        if player != None:
            self.player = player
        else:
            self.player = None
        self.level = None
        self.entities = []
        self.intializeGame() #set up each game

    #Add the players to the environment
    def intializeGame(self):
        #Add the AI
        if self.player == None:
            self.player = Player(self.screen, (0,450))
        self.player.rect.x = 0 # x-position
        self.player.rect.y =  450 # y-position
        self.level = Level_01(self.player, self.screen)
        self.player.level = self.level

        #Add the players to the player list for the game
        self.level.player_list.add(self.player)
        self.entities.append(self.player)

