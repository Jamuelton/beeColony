import numpy as np
import math


def fitness(food,problem="sphere"):

    if(problem == "sphere"):
        resultado = 0
  
        for i in food:
            resultado += i**2
        
        return resultado
    
    if(problem == "rastrigin"):
        resultado = 0
  
        for i in food:
            numero = 2 * 3.1415 * i
            p = (numero/180) * math.pi
            resultado+= (i**2) - (10 * math.cos(p)) + 10
    
        return resultado
    
    if(problem == "rosenbrock"):
        resultado = 0
  
        for i in range(0,(len(food)-1)):
            resultado += 100*(food[i+1] - food[i]**2)**2 + (food[i] - 1)**2
    
        return 
    
def roulette(foodSolutions):
    
    fitnessValues = np.array([1.0 / (fs.fitness + 1e-6) for fs in foodSolutions])
    totalFitness = np.sum(fitnessValues)
    probabilities = fitnessValues / totalFitness 
    return probabilities

def bestSolution(foodSolutions):
    best = min(foodSolutions, key=lambda fs:fs.fitness)
    return best


# Initialization Phase 

class foodSolution:
    def __init__(self,position,fitness, abandonment = 0):
        self.position = position
        self.fitness = fitness
        self.abandonment = abandonment

def generateFoodSolution(foodSize,dimentions,minLimit, maxLimit):
    positons = np.random.uniform(minLimit,maxLimit,(foodSize,dimentions))

    food = [foodSolution(pos,fitness(pos)) for pos in positons]

    return food

def populationIniciation(populationSize, dimentions,minLimit, maxLimit):

    foodSolution = generateFoodSolution(populationSize//2,dimentions,minLimit, maxLimit)

    employedBee = foodSolution[:populationSize//2]

    onlookerBee = [None for _ in range(populationSize//2)]

    return foodSolution, employedBee, onlookerBee


#   Employed Bees Phase
def employedBeePhase(foodSolutions, minLimit, maxLimit):
    
    for i, foodSolution in enumerate(foodSolutions):
        beeCord = np.random.randint(0,len(foodSolution.position))

        foodCord = np.random.choice([fs for fs in range(len(foodSolutions)) if fs != i])

        
        newPosition = foodSolution.position.copy()
        phi = np.random.uniform(-1, 1)
        newPosition[beeCord] = foodSolution.position[beeCord] + phi * (foodSolution.position[beeCord] - foodSolutions[foodCord].position[beeCord])
        
        
        newPosition = np.clip(newPosition, minLimit, maxLimit)
        
        
        newFitness = fitness(newPosition)
        
        
        if newFitness < foodSolution.fitness:
           
            foodSolution.position = newPosition
            foodSolution.fitness = newFitness
            foodSolution.abandonment = 0 
        else:
            
            foodSolution.abandonment += 1

#   Onlooker Bees Phase
def onlookerBeePhase(foodSolutions, onlookerBee, minLimit, maxLimit):
    chance = roulette(foodSolutions)

    for onlooker in onlookerBee:
        foodIndex = np.random.choice(len(foodSolutions), p=chance)
        foodSelect = foodSolutions[foodIndex]

        beeCord = np.random.randint(0,len(foodSelect.position))

        foodCord = np.random.choice([fs for fs in range(len(foodSolutions)) if fs != foodIndex])

        newPosition = foodSelect.position.copy()
        phi = np.random.uniform(-1, 1)
        newPosition[beeCord] = foodSelect.position[beeCord] + phi * (foodSelect.position[beeCord] - foodSolutions[foodCord].position[beeCord])

        newPosition = np.clip(newPosition, minLimit, maxLimit)
        
        newFitness = fitness(newPosition)

        if newFitness < foodSelect.fitness:
           
            foodSelect.position = newPosition
            foodSelect.fitness = newFitness
            foodSelect.abandonment = 0 
        else:
            
            foodSelect.abandonment += 1

#   Scout Bees Phase
def scoutBeePhase(foodSolutions, minLimit, maxLimit, maxAbandonment):
    for foodSolution in foodSolutions:
        if(foodSolution.abandonment > maxAbandonment):
            newPosition = np.random.uniform(minLimit,maxLimit,len(foodSolution.position))
            newFitness = fitness(newPosition)

            foodSolution.position = newPosition
            foodSolution.fitness = newFitness
            foodSolution.abandonment = 0


def beeColony(populationSize, cicles, dimentions, minLimit, maxLimit, maxAbandonment):

    foodSolution, employedBee, onlookerBee = populationIniciation(populationSize,dimentions,minLimit, maxLimit)

    bestFood = bestSolution(foodSolution)
    print(f"Melhor fitnes inicial: {bestFood.fitness}")
    for cycle in range(cicles):
        employedBeePhase(employedBee,minLimit,maxLimit)

        onlookerBeePhase(foodSolution,onlookerBee,minLimit, maxLimit)

        scoutBeePhase(foodSolution,minLimit,maxLimit,maxAbandonment)

        bestCycle = bestSolution(foodSolution)

        if(bestCycle.fitness < bestFood.fitness):
            bestFood = bestCycle

        print(f"Melhor fitness no ciclo {cycle}: {bestFood.fitness}")

    for i, fs in enumerate(foodSolution):
        print(f"Fonte de Alimentação {i+1}: Posição = {fs.position}, Fitness = {fs.fitness}, Fator de Abandono = {fs.abandonment}")


    

beeColony(20,100,2,-10,10,5)

