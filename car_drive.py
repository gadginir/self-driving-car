import pygame
import random
import math
import pymunk
from PIL import Image
from skimage.io import imread
import numpy as np

pygame.init()

display_width = 700
display_height = 450

black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)

screen = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

carImage = pygame.image.load('car_red.png')

pi = 3.141592653

stages = [
            (100, 250),
            (175, 175),
            (250, 100), 
            (325, 175),
            (350, 250),
            (425, 325),
            (500, 400),
            (575, 325),
            (650, 250),
            (650, 250)
        ]

class GameState:
    def __init__(self):

        self.done = False
        self.count = 0

        self.total_rewards = 0
        self.stage_reward = 100      # Reward after crossing particular stage
        self.action_reward = 0      # Reward for per action
        self.stage = -1

        self.car_x_loc = 125
        self.car_y_loc = 225 

        self.x_first_stage = 400
        self.y_first_stage = 250

        screen.fill(black)
        
        

    def car(self, x, y):
        screen.blit(carImage, (x, y))
        #inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        #self.car_body = pymunk.Body(1, inertia)
        #self.car_body.position = x, y

    def hasCarCrashed(self, eclipse, car_x_loc, car_y_loc, size, x_distance, y_distance, limit, operation):
        
        x = car_x_loc - x_distance
        y = car_y_loc - y_distance

        calc = ((x * x) + (y * y))/(size * size)
        #print(eclipse, ": ", calc)

        if operation == 0:

            if calc > limit:
                print(eclipse + " Car Crashed =", calc)
                return True
            else:
                return False
        else:
            if calc < limit:
                print(eclipse + " Car Crashed =", calc)
                return True
            else:
                return False

    
    def create_track(self):
        #arc(Surface, color, Rect, start_angle, stop_angle, width=1)
        pygame.draw.arc(screen, white, [100,100,300,300], 0, pi, 5)
        pygame.draw.arc(screen, white, [150,150,200,200], 0, pi, 5)

        pygame.draw.arc(screen, white, [400-5,150,200,200], pi, 2*pi, 5)
        pygame.draw.arc(screen, white, [350-5,100,300,300], pi, 2*pi, 5)

        #line(Surface, color, start_pos, end_pos, width=1)
        pygame.draw.line(screen, white, (600-5, 250), (650-10,250), 5)
    
    def frame_step(self, action):
        pygame.event.get()
        self.create_track()

        x_change = 0
        y_change = 0

        self.action_reward = -5
        
        if action == 0:     # K_LEFT
            x_change = -1
        elif action == 1:   # K_RIGHT
            x_change = 1
        elif action == 2:   # K_UP
            y_change = -1
        elif action == 3:   # K_DOWN
            y_change = 1

        #Car object
        #pygame.draw.circle(screen, white, [car_x_loc, car_y_loc], 5, 5)
        self.car_x_loc += x_change
        self.car_y_loc += y_change

        
        #Check Stage and Assing Reward
        if self.stage <= 7:
            current_stage = stages[self.stage+1]
            next_stage = stages[self.stage+2]

            if self.car_x_loc in range(stages[self.stage][0], stages[self.stage+1][0]) and (self.car_y_loc in range(stages[self.stage][1], stages[self.stage+1][1])) or self.car_y_loc in list(range(stages[self.stage+1][1], stages[self.stage][1])):
                self.action_reward = 0

                '''print("X", current_stage[0] , self.car_x_loc , next_stage[0])
                print("Y", current_stage[1] , self.car_y_loc , next_stage[1])'''

        if self.stage == 7 and 600 < self.car_x_loc and self.car_y_loc == 250:
            self.total_rewards = self.total_rewards + 500
            stage = self.stage + 1
            print(stage, " | ", self.total_rewards)
            self.action_reward = 500
            self.done = True
            print('Car reached the destination')
            #pygame.quit()
            #quit()
            #return self.action_reward, self.done
        elif current_stage[0] < self.car_x_loc < next_stage[0]:
            if current_stage[1] < next_stage[1]:
                if current_stage[1] < self.car_y_loc < next_stage[1]:
                    #self.total_rewards = self.total_rewards + ((self.stage +1) * self.stage_reward)
                    self.action_reward =  ((self.stage +1) * self.stage_reward)
                    self.stage = self.stage + 1
                    if self.count <= 100:       
                        self.action_reward = 200
                    self.count = 0
            elif current_stage[1] > next_stage[1]:
                if current_stage[1] > self.car_y_loc > next_stage[1]:
                    #self.total_rewards = self.total_rewards + ((self.stage + 1) * self.stage_reward)
                    self.action_reward =  ((self.stage +1) * self.stage_reward)
                    self.stage = self.stage + 1
                    if self.count <= 100:       
                        self.action_reward = 200
                    self.count = 0

        #print(self.stage, " | ", self.total_rewards)

        #Check car crash
        #hasCarCrashed(eclipse, car_x_loc, car_y_loc, size, x_distance, y_distance, limit, operation)
        if self.car_x_loc < self.x_first_stage and self.car_y_loc < self.y_first_stage:
            if self.hasCarCrashed("Outer 1", self.car_x_loc, self.car_y_loc, 150, 250, 250, 0.9, 0):
                self.total_rewards = self.total_rewards - 200
                self.action_reward = -200
                self.done = True
            if self.hasCarCrashed("Inner 1", self.car_x_loc, self.car_y_loc, 105, 250, 250, 1.1, 1):
                self.total_rewards = self.total_rewards - 200
                self.action_reward = -200
                self.done = True
        else:
            if self.hasCarCrashed("Outer 2", self.car_x_loc, self.car_y_loc, 150, 500, 250, 0.9, 0):
                self.total_rewards = self.total_rewards - 200
                self.action_reward = -200
                self.done = True
            if self.hasCarCrashed("Inner 2", self.car_x_loc, self.car_y_loc, 105, 500, 250, 1.0, 1):
                self.total_rewards = self.total_rewards - 200
                self.action_reward = -200
                self.done = True

        '''If Agent moving in the same region for more than 200 steps, then assign him -ve point
        If agent crosses the region in less than 100 steps then assign him 200 points'''
        if self.count > 200:
            self.action_reward = 0

        self.car(self.car_x_loc, self.car_y_loc)

        pygame.display.flip()
        #pygame.display.update()

        rect = pygame.Rect(98, 98, 554, 304)
        sub = screen.subsurface(rect)

        #image_path = 'images/screenshot_' + str(self.count) +'.jpg'
        image_path = 'screenshot.jpg'

        pygame.image.save(sub, image_path)


        img = Image.open(image_path)
        
        basewidth = 120
        
        '''wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))'''
        hsize = 65
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img.save('sompic.jpg')
        im = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
        
        im = im.sum(axis=2) # to greyscale
        #img[img==mspacman_color] = 0 # Improve contrast
        im = (im // 3 - 128).astype(np.int8) # normalize from -128 to 127
        
        state =  im.reshape(65, 120, 1)

        clock.tick(3)
        screen.fill((0,0,0))

        print('action_reward=',self.action_reward)
        self.count = self.count + 1
        return self.action_reward, state, self.done 


if __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step((random.randint(0, 4)))
