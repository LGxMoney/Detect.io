from Player import *
from Game import *
# from Species import *
import math

class Evolution():

   #construct the population
    def __init__(self,size, screen):
        self.games = []
        self.bestScore = 0
        self.innovationHistory = []

        #change based on number of champs
        self.champions = []

        self.gen = 0
        self.screen = screen
        self.averageFitness = 0
        self.fitnessHistory = []

        #Create the initial games
        for i in range(size):
            self.games.append(Game(screen))
            # generate their brains
            self.games[i].player.brain.generateNetwork()
            # mutate their brains
            self.games[i].player.brain.mutate(self.innovationHistory)

    # this function is called when all the players in the population are dead and a new generation needs to be made
    def naturalSelection(self):
        """ 
        Here we calculate our fitness of our last generation and create
        a new generation from (most) of their ashes. 
            - 5% of the best players stick around (champs)
            - 25% of the best players get mutated (mutants)
            - 70% of the players are babies from the top 50%
        """

        self.calculateFitness() # calculate the fitness of each player
        self.merge_sort(self.games) # sort the species to be ranked in fitness order, best first
        self.updateAverageFitness() # just book keeping


        #Begin creating the next generation of players
        children = [] #the next generation

        #carry over the best 5% of players --> accounts for 5% of new generation
        self.updateChampions() # saves the top 5 players per generation
        children.extend(self.champions)
        
        # Create children from the old generation
        for i in range(len(self.games) - len(self.champions)): #get the calculated amount of children from this species
            children.append(self.giveMeBaby(self.innovationHistory))
            # create a new child

        while len(children) < len(self.games): #if not enough babies (due to flooring the number of children to get a whole int) 
            children.append(self.giveMeBaby(self.innovationHistory)) #get babies from the best species

        # clear all of the games
        self.games.clear()

        for child in children: #set the children as the current population
            self.games.append(Game(self.screen, child))

        self.resetFitness()
        self.gen += 1

        # for game in self.games: # generate networks for each of the children
        #     game.player.brain.generateNetwork()
        #sets the best player globally and for this gen

    def updateChampions(self):
        tempChamps = []
        for i in range(0, math.ceil(len(self.games)* .05)):
            tempChamps.append(games[i])
        self.champions = tempChamps

    #calculates the fitness of all of the players 
    def calculateFitness(self):
        for game in self.games:
            game.player.calculateFitness()

  # gets baby from the players in the generation
    def giveMeBaby(self, innovationHistory):
        baby = None
        if random.uniform(0,1) < 0.25: # 25% of the time there is no crossover and the child is simply a clone of a random(ish) player
            baby = self.selectPlayer().clone()
        else: # 75% of the time do crossover 
            # get 2 random(ish) parents 
            parent1 = self.selectPlayer()
            parent2 = self.selectPlayer()
            
            #the crossover function expects the highest fitness parent to be the object and the lowest as the argument
            if parent1.fitness < parent2.fitness:
                baby = parent2.crossover(parent1)
            else:
                baby =  parent1.crossover(parent2)
        baby.brain.mutate(innovationHistory) # mutate the baby brain
        return baby

    def selectPlayer(self):
        fitnessSum = 0.0
        for game in self.games:
            fitnessSum += abs(game.player.fitness)
        
        rand = random.uniform(0,fitnessSum)
        runningSum = 0.0

        for i in range(len(self.games)):
            runningSum += abs(self.games[i].player.fitness)
            if runningSum > rand:
                return self.games[i].players

        # unreachable code to make the parser happy
        #print("Oops - something went wrong. This species has", str(len(self.players)), "players but it should have more.")
        return self.games[0].player

    # returns the sum of each species average fitness
    def getAvgFitnessSum(self):
        averageSum = 0
        for game in self.games:
            averageSum += game.player.fitness
        averageSum = float( averageSum  / len(self.games))
        self.fitnessHistory.append(averageSum)
        return averageSum

    def draw(self, showNothing, showIndex):
        if not showNothing:
            if showIndex == -1: #showAll
                self.games[0].level.drawBG(self.games[0])
                self.games[0].player.brain.draw(self.screen, self.gen)
                for game in self.games:
                    game.level.draw(game) #draw elements
            else: #use index - show only that game
                self.games[showIndex].level.drawBG(self.games[showIndex])
                self.games[showIndex].level.draw(self.games[showIndex])
                self.games[showIndex].player.brain.draw(self.screen, self.gen)

    def resetFitness(self):
        for game in self.games:
            game.player.resetFitness()

    # merge sort algorithm
    #https://medium.com/@george.seif94/a-tour-of-the-top-5-sorting-algorithms-with-python-code-43ea9aa02889
    def merge_sort(self, arr):
        # The last array split
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        # Perform merge_sort recursively on both halves
        left, right = self.merge_sort(arr[:mid]), self.merge_sort(arr[mid:])
        # Merge each side together
        return self.merge(left, right, arr.copy())


    def merge(self, left, right, merged):
        left_cursor, right_cursor = 0, 0
        while left_cursor < len(left) and right_cursor < len(right):
        
            # Sort each one and place into the result
            if left[left_cursor].bestFitness >= right[right_cursor].bestFitness:
                merged[left_cursor+right_cursor]=left[left_cursor]
                left_cursor += 1
            else:
                merged[left_cursor + right_cursor] = right[right_cursor]
                right_cursor += 1
                
        for left_cursor in range(left_cursor, len(left)):
            merged[left_cursor + right_cursor] = left[left_cursor]
            
        for right_cursor in range(right_cursor, len(right)):
            merged[left_cursor + right_cursor] = right[right_cursor]

        return merged