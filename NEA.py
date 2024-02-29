import pygame
from boarder import boards
import math
import copy
pygame.init()

Width = 900
Height = 900

WINDOW = pygame.display.set_mode([Width,Height]) # basic display commands located in all Pygame to create the screen
Time = pygame.time.Clock()
Frames = 60 # later is set to initae by the pygame clock allows for real time to ococur which is essential
caption = pygame.display.set_caption("PACMAN BY RAUL!")
font = pygame.font.Font("freesansbold.ttf", 20) # only font i could find that works
Game_Board = copy.deepcopy(boards) # this is so when restart is pressed it gives the original board copy and allows for all points to be reoladed on to screen
Pallet_OF_BOARD = "red" # this is the colour feature that allows you to change the board colour it is a variable allowing for less repition with the draw feature 
PI = math.pi 
Player = []
image_paths = {
    "player": [f"player_images/{i}.png" for i in range(1, 5)],
    "red": "ghost_images/red.png",
    "pink": "ghost_images/pink.png",
    "blue": "ghost_images/blue.png",
    "orange": "ghost_images/orange.png",
    "powerup": "ghost_images/powerup.png",
    "dead": "ghost_images/dead.png"
} # this just loads the images and assigns to a dictionary value using an f string with a for loop to iterate through each one.

# Load images into a dictionary
images = {}
for key, path in image_paths.items():  # this for loop here then loads the images and scales them aswell 
    if isinstance(path, list):  # For multiple player images
        images[key] = [pygame.transform.scale(pygame.image.load(img_path), (45, 45)) for img_path in path]
    else:
        images[key] = pygame.transform.scale(pygame.image.load(path), (45, 45))


Player = images["player"] # now assiging them all formal names to use throught the code 
red_img = images["red"]
pin_img = images["pink"]
blue_img = images["blue"]
yellow_img = images["orange"]
spooked_img = images["powerup"]
dead_img = images["dead"]


X_Pos_Player = 426  # sets inital co-ordinates of Pacman move these around if you would like Pacman to start somehwere else
Y_Pos_Player = 618
Location_of_movement = 0

red_x = 427 # all of these variables can change to place ghosts into differnt start locations 
red_y = 43 # he starts outside the box in pacman games as found by reaserch so this places him outside box
red_Location_of_movement = 0

blue_x = 389
blue_y = 399
blue_Location_of_movement = 2

pin_x = 440
pin_y = 387
pin_Location_of_movement = 2

yellow_x = 400
yellow_y = 390
yellow_Location_of_movement = 2

Reverse_Eat = False  # initaisies all powerups and movement so logic can be preformed on varibles below.
power_v = False
Moves_possible = [False,False,False,False] #right,left,up,down
Pointer = 0
blink = False
Location_of_movement_command= 0 

EATEN_GHOST = [False,False,False,False]  # sets ghosts to dead = False this will alow for us to chnage each Ghost indivisually 
Player_Player_location = [(X_Pos_Player,Y_Pos_Player),(X_Pos_Player,Y_Pos_Player),(X_Pos_Player,Y_Pos_Player),(X_Pos_Player,Y_Pos_Player)] # sets Player_location to player location for each ghosts but manipulate this based on power up and eaten 
player_speed = 2 # allows for player speed to be change a request made by user 
Player_Score = 0
POWER_POINT_CHECK = 0


moving = False # sets moveemnt to false
ghost_speed = [2,2,2,2]  # here we can change ghost speed to make it easier or harder each run allowing for that difficulty and repetivness feature to be met and intervieww needs.
Inital_Location_of_movement = 0
lives = 5 # amount of lives assigned can be changed 
MATCH_LOST = False # sets inital game condions 
MATCH_WON = False
original_lives = lives # so when the game is restart the lives are realoded.

red_dead = False  # sets all of there inital states to alive we can manipulate these variables with the ID in the Ghosts and Collisons with powerups active.
blue_dead = False
pin_dead = False
yellow_dead = False
red_box = False
pin_box = False
yellow_box = False
blue_box = False



def ADDED_FEATURES():  # this is just a nice feature screen shown in lots of Pygame games linked with refernces we can just add things to the screen of a set condition
    if MATCH_LOST:
        draw_game_over_screen()
    elif MATCH_WON:
        draw_game_won_screen()
    
    draw_player_score()
    draw_player_lives()

def draw_game_over_screen():
    pygame.draw.rect(WINDOW, "red", [48, 190, 790, 290], 0, 9)  # this does as it says and grwas a game over screen if pacman loses using blit on to over the screen.
    pygame.draw.rect(WINDOW, "blue", [48, 215, 790, 255], 0, 9)
    gameover_text = font.render('Game Over! Press Spacebar To Restart ', True, "red")
    WINDOW.blit(gameover_text, (150, 290))

def draw_game_won_screen():
    pygame.draw.rect(WINDOW, "red", [48, 190, 790, 290], 0, 9)
    pygame.draw.rect(WINDOW, "blue", [48, 215, 790, 255], 0, 9)  # does the same as game over but insted is if Pacman/user wins and a differnt text is displayed 
    gameover_text = font.render('You won! : Congratulations, Press Spacebar To Restart', True, 'green')
    WINDOW.blit(gameover_text, (150, 290))

def draw_player_score():
    Player_Score_text = font.render(f"Points: {Player_Score}", True, 'green')  # gives a real time score counter update which i have placed out of bounds in a clear location
    WINDOW.blit(Player_Score_text, (410, 20))

def draw_player_lives():
    for health in range(lives):
        WINDOW.blit(pygame.transform.scale(Player[0], (26, 26)), (648 + health * 40, 14))  # draw the Pacmans lives using the original Pamcna dictionary image loaded at the start and bases the amount shown dependednt of the lives counter a loop to have real time updates.


class  Ghost:  # this is the instaniated ghost class i will be refering to lots of refernces as stated not much of the mathematics can change but i will change the orider of operations and partial mathematics to meet the interviewee and clients requests of the indivisul Ghosts requirements
    def __init__(self, x_coorinate, y_coordinate, Player_location, speed, img, direct, dead, box, id):
        self.xcord = x_coorinate
        self.ycord = y_coordinate  # this is just setting main and dveloping atrributes which will  be used throughout
        self.velocity = speed
        self.image = img
        self.Location_of_movement = direct
        self.Ghost_Dead = dead
        self.In_Main = box
        self.cenx = self.xcord + 22
        self.ceny = self.ycord + 22
        self.Player_location = Player_location
        self.Identification = id
        self.U_R_L_D, self.In_Main = self.Contact()
        self.rect = self.Create()

    def Create(self):   # this is the loading of the images, it bases of each condiotn such as if powerup is acitve or not and loads the speific image for each
        if (not Reverse_Eat and not self.Ghost_Dead) or (EATEN_GHOST[self.Identification] and Reverse_Eat and not self.Ghost_Dead): # saying the defult image if power up is not active and dead
            WINDOW.blit(self.image, (self.xcord, self.ycord))
        
        elif Reverse_Eat and not self.Ghost_Dead and not EATEN_GHOST[self.Identification]: # for Reverse_Eat
            WINDOW.blit(spooked_img, (self.xcord, self.ycord))# making either base image spooked image or dead iage
        else: # for dead as final condition 
            WINDOW.blit(dead_img, (self.xcord,self.ycord))

        ghost_rect = pygame.rect.Rect((self.cenx -17, self.ceny -17), (35,35)) # if you want the hit box to be smaller use smaller values for the minus
        return ghost_rect

    def Contact(self): # handles weather ghosts can turn at any point in the map checks with collsions with walls and everything
        Num_Of_Y = ((Height-50)//32)
        Num_Of_X = (Width//30)
        Colision_of_Walls = 15 # checks for collisions with walls is around half Width of sprites body
        self.U_R_L_D = [False,False,False,False]
        if 0 < self.cenx //30 <29:  # mkes them leave door and no errors of getting of the WINDOW.
            if Game_Board[(self.ceny - Colision_of_Walls)//Num_Of_Y][(self.cenx//Num_Of_X)] == 9:
                self.U_R_L_D[2] = True
            if Game_Board[self.ceny//Num_Of_Y][(self.cenx-Colision_of_Walls)//Num_Of_X] < 3 \
                or (Game_Board[self.ceny//Num_Of_Y][(self.cenx-Colision_of_Walls)//Num_Of_X] == 9 and (
                    self.In_Main or self.Ghost_Dead)): # basicalaly if they have a 2,1,0 then checks if can go left right up down for ghosts but consididering the door 
                    self.U_R_L_D[1] = True
            
            if Game_Board[self.ceny//Num_Of_Y][(self.cenx+Colision_of_Walls)//Num_Of_X] < 3 \
                or (Game_Board[self.ceny//Num_Of_Y][(self.cenx+Colision_of_Walls)//Num_Of_X] == 9 and (
                    self.In_Main or self.Ghost_Dead)): 
                    self.U_R_L_D[0] = True #left
            
            if Game_Board[(self.ceny +Colision_of_Walls) //Num_Of_Y][self.cenx//Num_Of_X] < 3 \
                or (Game_Board[(self.ceny +Colision_of_Walls) //Num_Of_Y][self.cenx//Num_Of_X] == 9 and (
                    self.In_Main or self.Ghost_Dead)): # down
                    self.U_R_L_D[3] = True
            
            if Game_Board[(self.ceny  - Colision_of_Walls) //Num_Of_Y][self.cenx//Num_Of_X] < 3 \
                or (Game_Board[(self.ceny  - Colision_of_Walls) //Num_Of_Y][self.cenx//Num_Of_X] == 9 and (
                    self.In_Main or self.Ghost_Dead)): # up
                    self.U_R_L_D[2] = True
                
            if self.Location_of_movement == 2 or self.Location_of_movement == 3: # checks up and down
                if 12 <= self.cenx % Num_Of_X <= 18: # checks x 
                    if Game_Board[(self.ceny + Colision_of_Walls)//Num_Of_Y][self.cenx//Num_Of_X] < 3 \
                        or (Game_Board[(self.ceny + Colision_of_Walls)//Num_Of_Y][self.cenx//Num_Of_X] == 9 and  (
                            self.In_Main or self.Ghost_Dead)):
                        self.U_R_L_D[3] = True # checks down
                    if Game_Board[(self.ceny - Colision_of_Walls)//Num_Of_Y][self.cenx//Num_Of_X] < 3 \
                        or (Game_Board[(self.ceny - Colision_of_Walls)//Num_Of_Y][self.cenx//Num_Of_X] == 9 and  (
                            self.In_Main or self.Ghost_Dead)):
                        self.U_R_L_D[2] = True # checks up

                if 12 <= self.ceny % Num_Of_Y <= 18: # checks for y
                    if Game_Board[self.ceny//Num_Of_Y][(self.cenx-Colision_of_Walls)//Num_Of_X] < 3 \
                        or (Game_Board[self.ceny//Num_Of_Y][(self.cenx - Colision_of_Walls)//Num_Of_X] == 9 and  (
                            self.In_Main or self.Ghost_Dead)):
                        self.U_R_L_D[1] = True # left
                    if Game_Board[self.ceny//Num_Of_Y][(self.cenx + Colision_of_Walls)//Num_Of_X] < 3 \
                        or (Game_Board[self.ceny//Num_Of_Y][(self.cenx + Colision_of_Walls)//Num_Of_X] == 9 and  (
                            self.In_Main or self.Ghost_Dead)):
                        self.U_R_L_D[0] = True # right
        else:
            self.U_R_L_D[0] = True
            self.U_R_L_D[1] = True
        if 350 < self.xcord < 550 and 370 < self.ycord < 480:
            self.In_Main = True
        else:
            self.In_Main = False  # this just chekcs if in the box based on board dimensions of x and y 
                
                
                
                


            
            


        return self.U_R_L_D, self.In_Main


    def move_yellow(self): # this is now moving the yellow ghost and has acess to all main init attributes 
        # right, left, up down U_R_L_D when he is at an advanage to turn in proper game function
        if self.Location_of_movement == 0:
            if self.Player_location[0] > self.xcord and self.U_R_L_D[0]:# co-ordinate of Player_location is grater than x position and can keep moviung right
                self.xcord += self.velocity
            elif not self.U_R_L_D[0]: # was going right and hit soemthing on the right
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: # for down 
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]: # left 
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.U_R_L_D[3]:  # if nothing is feasable then this and code below just makes them turn otherwise they would remain stationary this case it is moving down
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity  # we can move these around to fit for interivewee requests which will be trail and error for each pattern
                
                elif self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
            elif self.U_R_L_D[0]:
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: # now looks at best route U_R_L_D even if wall hasnt been hit to ensure for best patterns
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                if self.Player_location[1] < self.ycord and self.U_R_L_D[2]: 
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                else:
                    self.xcord += self.velocity

        
        elif self.Location_of_movement == 1: # now for left making sure loop isnt formed
            if self.Player_location[1] > self.ycord and self.U_R_L_D[3]:
                self.Location_of_movement = 3     
            
            
            
            elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:# co-ordinate of Player_location is grater than x position and can keep moviung right
                self.xcord -= self.velocity
            elif not self.U_R_L_D[1]: # was going right and hit soemthing on the right
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: 
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.U_R_L_D[3]:
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                
                elif self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
            elif self.U_R_L_D[1]:
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: 
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                if self.Player_location[1] < self.ycord and self.U_R_L_D[2]: 
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity  # again this can all be changed to differ order of patterns 
                else:
                    self.xcord -= self.velocity
        
        
        elif self.Location_of_movement == 2: # now for left making sure loop isnt formed
            if self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                self.Location_of_movement = 1
                self.xcord -= self.velocity
            
            
            
            elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:# co-ordinate of Player_location is grater than x position and can keep moviung right
                self.ycord -= self.velocity
            elif not self.U_R_L_D[2]: # was going right and hit soemthing on the right
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.Player_location[1] > self.ycord and self.U_R_L_D[3]: 
                    self.Location_of_movement = 3
                    self.xcord += self.velocity
                 
                elif self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                
                
                elif self.U_R_L_D[3]:
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
               
                
                elif self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
            elif self.U_R_L_D[2]:
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                else:
                    self.ycord -= self.velocity

        elif self.Location_of_movement == 3: # now for left making sure loop isnt formed
            
            if self.Player_location[1] > self.ycord and self.U_R_L_D[3]:
                self.ycord += self.velocity
            elif not self.U_R_L_D[3]:
            
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity   # the code is partcially the same for all Location_of_movements but just checking against x and y and reversing plus and = to on the co-ordinates depenedent of left right up and down 

            
            
            
        
            
            elif self.U_R_L_D[3]:  # on this now raul !!
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                else:
                    self.ycord += self.velocity
        if self.xcord < -30:
            self.xcord = 900
        elif self.xcord > 900:
            self.xcord -30
        return self.xcord, self.ycord, self.Location_of_movement
    
    def move_blue(self):  # does the same for yellow as rember interviewee wanted yellow and blue to be the same but partually differnt in terms of left and right so i will comment where i have made that change 
        # right, left, up down U_R_L_D when he is at an advanage to turn in proper game function
        if self.Location_of_movement == 0:
            if self.Player_location[0] > self.xcord and self.U_R_L_D[0]:# co-ordinate of Player_location is grater than x position and can keep moviung right
                self.xcord += self.velocity
            elif not self.U_R_L_D[0]: # was going right and hit soemthing on the right
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: # for down 
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]: # left 
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.U_R_L_D[3]:  # if nothing is feasable then this and code below just makes them turn otherwise they would remain stationary this case it is moving down
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                
                elif self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
            elif self.U_R_L_D[0]:
               
                
                self.xcord += self.velocity

        
        elif self.Location_of_movement == 1: # now for left making sure loop isnt formed
            if self.Player_location[1] > self.ycord and self.U_R_L_D[3]:
                self.Location_of_movement = 3     
            
            
            
            elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:# co-ordinate of Player_location is grater than x position and can keep moviung right
                self.xcord -= self.velocity
            elif not self.U_R_L_D[1]: # was going right and hit soemthing on the right
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: 
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.U_R_L_D[3]:
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                
                elif self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
            elif self.U_R_L_D[1]:
                
                self.xcord -= self.velocity
        
        
        elif self.Location_of_movement == 2: # now for left making sure loop isnt formed
            if self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                self.Location_of_movement = 1
                self.xcord -= self.velocity
            
            
            
            elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:# co-ordinate of Player_location is grater than x position and can keep moviung right
                self.ycord -= self.velocity
            elif not self.U_R_L_D[2]: # was going right and hit soemthing on the right
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.Player_location[1] > self.ycord and self.U_R_L_D[3]: 
                    self.Location_of_movement = 3
                    self.xcord += self.velocity
                 
                elif self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                
                
                elif self.U_R_L_D[3]:
                    self.Location_of_movement = 3  # here is the change made to make Yellow and blue differ from left and right partially and meet interviewee requests 
                    self.ycord += self.velocity
               
                
                elif self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
            elif self.U_R_L_D[2]:
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                else:
                    self.ycord -= self.velocity

        elif self.Location_of_movement == 3: # now for left making sure loop isnt formed
            
            if self.Player_location[1] > self.ycord and self.U_R_L_D[3]:
                self.ycord += self.velocity
            elif not self.U_R_L_D[3]:
            
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity   # the code is partcially the same for all Location_of_movements but just checking against x and y and reversing plus and = to on the co-ordinates depenedent of left right up and down 

            
            
            
        
            
            elif self.U_R_L_D[3]:  # on this now raul !!
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                else:
                    self.ycord += self.velocity
        if self.xcord < -30:
            self.xcord = 900
        elif self.xcord > 900:
            self.xcord -30
        return self.xcord, self.ycord, self.Location_of_movement
    
    def move_pin(self):
        # right, left, up down U_R_L_D when he is at an advanage to turn in proper game function
        if self.Location_of_movement == 0:
            if self.Player_location[0] > self.xcord and self.U_R_L_D[0]:# co-ordinate of Player_location is grater than x position and can keep moviung right
                self.xcord += self.velocity
            elif not self.U_R_L_D[0]: # was going right and hit soemthing on the right
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: # for down 
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]: # left 
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.U_R_L_D[3]:  # if nothing is feasable then this and code below just makes them turn otherwise they would remain stationary this case it is moving down
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                
                elif self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
            elif self.U_R_L_D[0]:
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: # now looks at best route U_R_L_D even if wall hasnt been hit
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                if self.Player_location[1] < self.ycord and self.U_R_L_D[2]: 
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                else:
                    self.xcord += self.velocity

        
        elif self.Location_of_movement == 1: # now for left making sure loop isnt formed
            if self.Player_location[1] > self.ycord and self.U_R_L_D[3]:
                self.Location_of_movement = 3     
            
            
            
            elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:# co-ordinate of Player_location is grater than x position and can keep moviung right
                self.xcord -= self.velocity
            elif not self.U_R_L_D[1]: # was going right and hit soemthing on the right
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: 
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.U_R_L_D[3]:
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                elif self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                
                elif self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
            elif self.U_R_L_D[1]:
                if self.Player_location[1] > self.ycord and self.U_R_L_D[3]: 
                    self.Location_of_movement = 3
                    self.ycord += self.velocity
                if self.Player_location[1] < self.ycord and self.U_R_L_D[2]: 
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                else:
                    self.xcord -= self.velocity
        
        
        elif self.Location_of_movement == 2: # now for left making sure loop isnt formed
            
            
            
            
            if self.Player_location[1] < self.ycord and self.U_R_L_D[2]:# co-ordinate of Player_location is grater than x position and can keep moviung right
                self.ycord -= self.velocity
            elif not self.U_R_L_D[2]: # was going right and hit soemthing on the right
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.Player_location[1] > self.ycord and self.U_R_L_D[3]: 
                    self.Location_of_movement = 3
                    self.xcord += self.velocity
                 
                elif self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                
                
                elif self.U_R_L_D[3]:
                    self.Location_of_movement = 3
                    self.ycord += self.velocity  # here again is to make left and right differ for interviewee requests 
               
                
                elif self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
            elif self.U_R_L_D[2]:
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                else:
                    self.ycord -= self.velocity

        elif self.Location_of_movement == 3: # now for left making sure loop isnt formed
            
            
            if not self.U_R_L_D[3]:
            
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.Player_location[1] < self.ycord and self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.U_R_L_D[2]:
                    self.Location_of_movement = 2
                    self.ycord -= self.velocity
                elif self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                elif self.U_R_L_D[0]:
                    self.Location_of_movement = 0
                    self.xcord += self.velocity   # the code is partcially the same for all Location_of_movements but just checking against x and y and reversing plus and = to on the co-ordinates depenedent of left right up and down 

            
            
            
        
            
            elif self.U_R_L_D[3]:  
                if self.Player_location[0] > self.xcord and self.U_R_L_D[0]: 
                    self.Location_of_movement = 0
                    self.xcord += self.velocity
                elif self.Player_location[0] < self.xcord and self.U_R_L_D[1]:
                    self.Location_of_movement = 1
                    self.xcord -= self.velocity
                else:
                    self.ycord += self.velocity
        if self.xcord < -30:
            self.xcord = 900
        elif self.xcord > 900:
            self.xcord -30
        return self.xcord, self.ycord, self.Location_of_movement         
    
                




        

def Contact(SCORE_OF_POINTS,POWER_REVERSE_EAT,POWER_TIME,EATEN_GHOSTS):  # this is collison with the points and powerups on the board based of game board array
    Num_Of_Y = (Height-48) // 32  # based of the board below
    Num_Of_X = (Width//30)  # based of the board below
    if 0 < X_Pos_Player < 870:
        if Game_Board[center_y // Num_Of_Y][center_x//Num_Of_X] == 1: # esentially ssaying where his center is is when he is eating over the dot
            Game_Board[center_y//Num_Of_Y][center_x//Num_Of_X] = 0 # saying the dot has been eaten
            SCORE_OF_POINTS += 10 # assigns points 

        if Game_Board[center_y//Num_Of_Y][center_x//Num_Of_X] == 2: # esentially ssaying where his center is is when he is eating over the dot
            Game_Board[center_y//Num_Of_Y][center_x//Num_Of_X] = 0 # saying the dot has been eaten
            SCORE_OF_POINTS += 20  # assigns points 
            POWER_REVERSE_EAT = True
            POWER_TIME = 0
            EATEN_GHOSTS = [False,False,False,False]
        
        if Game_Board[center_y//Num_Of_Y][center_x//Num_Of_X] == 0.5: # esentially ssaying where his center is is when he is eating over the dot
            Game_Board[center_y//Num_Of_Y][center_x//Num_Of_X] = 0
            SCORE_OF_POINTS += 20
            power_v = True
            POWER_TIME = 0
    
    return SCORE_OF_POINTS, POWER_REVERSE_EAT, POWER_TIME,EATEN_GHOSTS

def GAME_SPACE(Game_Board):  # this is drawing the main feature which everything is based of the board
    Num_Of_Y = ((Height-50)//32)  # these are spesific mathematics found with in depth reaseerch
    Num_Of_X = Width//30  # also spesific mathematics found 
    for WIDTH_OF_BOARD in range(len(Game_Board)):
        for HEIGHT_OF_BOARD in range(len(Game_Board[WIDTH_OF_BOARD])):
            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 1: # points 
                pygame.draw.circle(WINDOW, "purple", (HEIGHT_OF_BOARD*Num_Of_X+(0.5*Num_Of_X),WIDTH_OF_BOARD*Num_Of_Y+(Num_Of_Y*0.5)),4)  # not one of the mathematics can change here say i were to change the 0.5 to  fractionl 0.4 the game shapes would not look correct or smooth therfore these mathematics are univeral for an array baord drawn in pygame
            
            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 2 and not blink:  # blink feature added here with use of the Pygame clock detiled below # freeze/ radar powerup
                pygame.draw.circle(WINDOW, "yellow", (HEIGHT_OF_BOARD*Num_Of_X+(0.5*Num_Of_X),WIDTH_OF_BOARD*Num_Of_Y+(Num_Of_Y*0.5)),10)

            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 3: # vertical line
                pygame.draw.line(WINDOW, Pallet_OF_BOARD, (HEIGHT_OF_BOARD*Num_Of_X+(0.5*Num_Of_X),WIDTH_OF_BOARD*Num_Of_Y),
                                 (HEIGHT_OF_BOARD*Num_Of_X+(Num_Of_X*0.5),WIDTH_OF_BOARD*Num_Of_Y + Num_Of_Y),3)
            
            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 4: # horizontal line
                pygame.draw.line(WINDOW, Pallet_OF_BOARD, (HEIGHT_OF_BOARD * Num_Of_X, WIDTH_OF_BOARD * Num_Of_Y+(0.5*Num_Of_Y)),
                                 (HEIGHT_OF_BOARD * Num_Of_X + Num_Of_X, WIDTH_OF_BOARD * Num_Of_Y + (0.5*Num_Of_Y)), 3)
            
            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 5: # left up curve (parabolica)
                pygame.draw.arc(WINDOW, Pallet_OF_BOARD,
                                [(HEIGHT_OF_BOARD * Num_Of_X - (Num_Of_X * 0.4)) - 2, (WIDTH_OF_BOARD * Num_Of_Y + (0.5 * Num_Of_Y)), Num_Of_X, Num_Of_Y], 0, PI / 2,
                                3)
            
            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 6: #right up curve (parabolica)
                pygame.draw.arc(WINDOW, Pallet_OF_BOARD, [(HEIGHT_OF_BOARD * Num_Of_X + (Num_Of_X * 0.5)), (WIDTH_OF_BOARD * Num_Of_Y + (0.5 * Num_Of_Y)), Num_Of_X, Num_Of_Y],
                                PI / 2, PI, 3)
            
            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 7:  # right down curve (parabolica)
                pygame.draw.arc(WINDOW, Pallet_OF_BOARD, [(HEIGHT_OF_BOARD * Num_Of_X + (Num_Of_X * 0.5)), (WIDTH_OF_BOARD * Num_Of_Y - (0.4 * Num_Of_Y)), Num_Of_X, Num_Of_Y],
                                PI, 3 * PI / 2, 3)

            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 8: # left down curve (parabolica)
                pygame.draw.arc(WINDOW, Pallet_OF_BOARD,
                                [(HEIGHT_OF_BOARD * Num_Of_X - (Num_Of_X * 0.4)) - 2, (WIDTH_OF_BOARD * Num_Of_Y - (0.4 * Num_Of_Y)), Num_Of_X, Num_Of_Y],
                                3 * PI / 2, 2 * PI, 3)

            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 9:  # the ghost gate code was featured in the Ghost class which allows them to pass through 9 at any point and pacman cannot enter
                pygame.draw.line(WINDOW, "white", (HEIGHT_OF_BOARD * Num_Of_X, WIDTH_OF_BOARD * Num_Of_Y + (0.5 * Num_Of_Y)),
                                 (HEIGHT_OF_BOARD * Num_Of_X + Num_Of_X, WIDTH_OF_BOARD * Num_Of_Y + (0.5 * Num_Of_Y)), 3)
            
            
            if Game_Board[WIDTH_OF_BOARD][HEIGHT_OF_BOARD] == 0.5 and not blink:  # sets the velocty powerup on the board and makes it blink aswell
                pygame.draw.circle(WINDOW,"red",(HEIGHT_OF_BOARD*Num_Of_X+(0.5*Num_Of_X),WIDTH_OF_BOARD*Num_Of_Y+(Num_Of_Y*0.5)),10)

def INITALISE_PACMAN():  # this is acting as an aesteic feature so that when pacman turns he isnt just looking in the same direction but fully roates and flips to match direction of travel
    
    if Location_of_movement == 1:
        WINDOW.blit(pygame.transform.flip(Player[Pointer//5], True,False),  (X_Pos_Player,Y_Pos_Player))#left uses flip 
    elif Location_of_movement == 0:
        WINDOW.blit(Player[Pointer//5], (X_Pos_Player,Y_Pos_Player)) #right
    elif Location_of_movement == 3:
        WINDOW.blit(pygame.transform.rotate(Player[Pointer//5], 270), (X_Pos_Player,Y_Pos_Player)) #down uses roation
    elif Location_of_movement == 2:
        WINDOW.blit(pygame.transform.rotate(Player[Pointer//5], 90), (X_Pos_Player,Y_Pos_Player))# up
    
   

def Check_location_OF_POSITION(MID_X,MID_Y):  # indicates collion for walls for Pacman and the points where he can turn up down left or right
    U_R_L_D = [False,False,False,False]  # inital condion set which means that he cannot turn up down left or right at ny point this is to be manipulated
    Num_Of_Y = (Height-50)//32 # spesific board maths
    Num_Of_X = (Width//30)
    Colision_of_Walls = 13  # this is like a plus or minus factor we can chnage it ever so slightly but remebr board mathematics is very spesiic indiactes collions with walls at a point
    
    if MID_X//30 <29: #check collisions based on MID_X so the x middle co-ordinate and y of player +- a num 3 
        if Location_of_movement == 0: # if moving right
            if Game_Board[MID_Y//Num_Of_Y][(MID_X - Colision_of_Walls)//Num_Of_X ] < 3:
                U_R_L_D[1] = True  # if moving left and right is possible as no collison with wall then allow to move right 
        
        if Location_of_movement == 1: # if moving left
            if Game_Board[MID_Y//Num_Of_Y][(MID_X + Colision_of_Walls)//Num_Of_X ] < 3:
                U_R_L_D[0] = True  # if moving left right is possible as long s no collion with a walll
        
        if Location_of_movement == 2: # if moving up
            if Game_Board[(MID_Y + Colision_of_Walls)//Num_Of_Y][MID_X//Num_Of_X ] < 3: # co-ordinats up increses and oppsoite decreses
                U_R_L_D[3] = True # enstates the opposite so if moving up the down is possible as long as board collison dosnt block it
        
        if Location_of_movement == 3: # if moving down 
            if Game_Board[(MID_Y-Colision_of_Walls)//Num_Of_Y][MID_X//Num_Of_X ] < 3:
                U_R_L_D[2] = True # enstates if movement is down then up is possible based on if board allows it with factor of collisons
    

        if Location_of_movement == 2 or Location_of_movement == 3:
            if 12 <= MID_X % Num_Of_X <=18: # makes so it dosnt look like your travelling through pixels this makes it turn through when at midpoint 12-18 is a good middle after extensive testing.
                if Game_Board[(MID_Y + Colision_of_Walls) // Num_Of_Y][MID_X // Num_Of_X ] <3: # so if going up or down already if in midpoint then if clear to belwo or up you can turn up and down
                    U_R_L_D[3] = True
                if Game_Board[(MID_Y - Colision_of_Walls) // Num_Of_Y][MID_X // Num_Of_X ] <3: # so if going up or down already if in midpoint then if clear to belwo or up you can turn up and down
                    U_R_L_D[2] = True

            if 12 <= MID_Y % Num_Of_Y <=18: 
                if Game_Board[MID_Y // Num_Of_Y][(MID_X - Num_Of_X) // Num_Of_X ] <3: # now doing it for left and right using oppsoite logic and cheking for y transforming ceneter x  by Num_Of_X insted of y by Colision_of_Walls
                    U_R_L_D[1] = True
                if Game_Board[MID_Y // Num_Of_Y][(MID_X +Num_Of_X)// Num_Of_X ] <3:
                    U_R_L_D[0] = True

        if Location_of_movement == 0 or Location_of_movement == 1:
            if 12 <= MID_X % Num_Of_X <=18: 
                if Game_Board[(MID_Y + Num_Of_Y) // Num_Of_Y][MID_X // Num_Of_X ] <3: # let pacman hit walls without being able to turn with the left and right Location_of_movement 
                    U_R_L_D[3] = True
                if Game_Board[(MID_Y - Num_Of_Y) // Num_Of_Y][MID_X // Num_Of_X ] <3: 
                    U_R_L_D[2] = True

            if 12 <= MID_Y % Num_Of_Y <=18: 
                if Game_Board[MID_Y // Num_Of_Y][(MID_X - Colision_of_Walls) // Num_Of_X ] <3:  # now checking for Width of pacman
                    U_R_L_D[1] = True
                if Game_Board[MID_Y // Num_Of_Y][(MID_X +Colision_of_Walls)// Num_Of_X ] <3:
                    U_R_L_D[0] = True
    
    else:
        U_R_L_D[0] = True   # just as a check case so incase anything fails these condions should be true and then the game can realod the conditons to meet again.
        U_R_L_D[1] = True

    return U_R_L_D

def MOVE_PAC(PX, PY):  # this is just simple movement seen in lots of Pygame games created we have player speed which is at the start and based on direction commands we have created moves chrecter in spesifc direction as long as conditons allow
    if Location_of_movement == 0: # right
        if Moves_possible[0]: # these are moves possible what we created above with the case of if they can turn 
            PX += player_speed
    elif Location_of_movement == 1: # left
        if Moves_possible[1]:
            PX -= player_speed
    elif Location_of_movement == 2: # up
        if Moves_possible[2]:
            PY -= player_speed # this is - as up the board is less in value
    elif Location_of_movement == 3: # down
        if Moves_possible[3]:
            PY += player_speed # this is positive as down the board is larger values

    return PX, PY


def get_Player_Player_location(red_x,red_y,blue_x,blue_y,pin_x,pin_y,yellow_x,yellow_y):  # this is so the ghosts are trying to leave the box but actually get the updated player x and y co-ordinates in real time rather than is starting position
    if X_Pos_Player < 450:
        Escape_x = 900  # for power-up where eat ghosts
    else:
        Escape_x = 0
    
    if Y_Pos_Player < 450:
        Escape_y = 900
    else:
        Escape_y = 0
    return_Player_location = (380,400)

    if Reverse_Eat:  # this is the freeze/radar powerup i called it reverse eat as it makes more sense to me
        if not red.Ghost_Dead and not EATEN_GHOST[0]:  # this is going into the ghost class as we mentioned each ghost is indivisal and these were attributes set 
            red_Player_location = (Escape_x,Escape_y)  # if Reverse_Eat is active make them ghosts run away 
        elif not red.Ghost_Dead and EATEN_GHOST[0]:  # to get out of box and traget player when eaten 
            if 340 < red_x < 560 and 340 < red_y < 510:
                red_Player_location = (400,100) # go to box location
            else:
                red_Player_location = (X_Pos_Player,Y_Pos_Player)    # otherwis go and target the player 
        
        else:
            red_Player_location = return_Player_location # if power-up is actiave and you are dead and therfore want to remain as normal

        if not blue.Ghost_Dead and not EATEN_GHOST[1]:
            blue_Player_location = (Escape_x, Y_Pos_Player)  
        
        elif not blue.Ghost_Dead and EATEN_GHOST[1]:  # to get out of box and traget player when eaten 
            if 340 < blue_x < 560 and 340 < blue_y < 510:
                blue_Player_location = (400,100)
            else:
                blue_Player_location = (X_Pos_Player,Y_Pos_Player)   
        
        
        
        else:   
            blue_Player_location = return_Player_location
        
        if not pin.Ghost_Dead and not EATEN_GHOST[2]:
            pin_Player_location = (X_Pos_Player,Escape_y)  
        
        elif not pin.Ghost_Dead and EATEN_GHOST[2]:  # to get out of box and traget player when eaten 
            if 340 < pin_x < 560 and 340 < pin_y < 500:
                pin_Player_location = (400,100)
            else:
                pin_Player_location = (X_Pos_Player,Y_Pos_Player)   
        

        else:
            pin_Player_location = return_Player_location
        
        if not yellow.Ghost_Dead and not EATEN_GHOST[3]:
            yellow_Player_location = (450,450)  
        
        elif not yellow.Ghost_Dead and EATEN_GHOST[3]:  # to get out of box and traget player when eaten 
            if 340 < yellow_x < 560 and 340 < yellow_y < 499:
                yellow_Player_location = (400,100)
            else:
                yellow_Player_location = (X_Pos_Player,Y_Pos_Player)   
        
        
        else:
            yellow_Player_location = return_Player_location
    
    
    else: # Reverse_Eat not active setting condtions to get out of box and persue player just as a base case again
        
        if not red.Ghost_Dead:
            if 340 < red_x < 560 and 330 < red_y < 500:
                red_Player_location = (400,100)
            else:
                red_Player_location = (X_Pos_Player,Y_Pos_Player)   
        else:
            red_Player_location = return_Player_location 

        if not blue.Ghost_Dead:
            if 340 < blue_x < 560 and 330 < blue_y < 500:
                blue_Player_location = (400,100)
            else:
                blue_Player_location = (X_Pos_Player,Y_Pos_Player)   
        else:
            blue_Player_location = return_Player_location 

        
        if not pin.Ghost_Dead:
            if 340 < pin_x < 560 and 330 < pin_y < 500:
                pin_Player_location = (400,100)
            else:
                pin_Player_location = (X_Pos_Player,Y_Pos_Player)   
        else:
            pin_Player_location = return_Player_location 

        
        if not yellow.Ghost_Dead:
            if 340 < yellow_x < 560 and 330 < yellow_y < 500: # get them out the door 
                yellow_Player_location = (400,100)
            else:
                yellow_Player_location = (X_Pos_Player,Y_Pos_Player)   
        else:
            yellow_Player_location = return_Player_location 





    return [red_Player_location,blue_Player_location,pin_Player_location,yellow_Player_location]



START_OF_GAME = True # just to create a while loop for game running standered pygame code 
while START_OF_GAME:
    Time.tick(Frames) # starts the clock and bases fps variable set at the start
    Pointer += 1  # in game clock
    if Pointer >= 17:  # this code sets the blinker function by incresing the value the powerups blink slower so just a prefernce aestetic feature.
        Pointer = 0
        blink = True
    elif Pointer > 14:
        blink = False
    
    if Reverse_Eat:
        if POWER_POINT_CHECK < 600:
            POWER_POINT_CHECK += 1  # sets the duration of the freeze powerup for 10 seconds 600 == 10 seconds 
        else:
            POWER_POINT_CHECK = 0  # otherwise this is saying powerup is not active ghosts are definetly not dead and powerup is off.
            Reverse_Eat = False
            EATEN_GHOST = [False] * 4
   
    if Inital_Location_of_movement < 180 and not MATCH_LOST and not MATCH_WON:
        moving = False  
        Inital_Location_of_movement += 1 # so game dosnt start straight away and gives the user some time to increse this increse the 180
    else:
        moving = True

    WINDOW.fill("black")  # fills the screen background color this can be changed to any colour but black looks nice in my interviewees opinion
    GAME_SPACE(Game_Board)  # this passes in the array into the game space function
    center_x = X_Pos_Player + 23 # this is like intinatl Pacman location you can change it here or at the start
    center_y = Y_Pos_Player + 24
    if Reverse_Eat:
        ghost_speed = [1,1,1,1] # when the ghosts die the interviewee wanted to reduce their speeds so this does it as we can see we can do it indiviusally if we require
        
    else:
        ghost_speed = [2,2,2,2] # otherwise setting the ghost speeds to always a 2 this againcn change if requested and was a interviewee want 
    if red_dead == True:
        ghost_speed[0] = 5
    if blue_dead == True:
        ghost_speed[1] = 5
    if pin_dead == True:
        ghost_speed[2] = 5
    if yellow_dead == True:
        ghost_speed[3] = 5  # if they are dead then set their speed to 5 to get them back into the game as soon as possible
    
    MATCH_WON = True
    for i in range(len(Game_Board)):
        if 1 in Game_Board[i] or 2 in Game_Board[i] or 0.5 in Game_Board[i]:  # if all dots aand Reverse_Eats eaten game won is true 
            MATCH_WON = False # if there is any points left then match win is false


    player_circle = pygame.draw.circle(WINDOW,"black", (center_x, center_y), 22, 2 ) # this is what the ghosts collide with to reduce or increse collsions change the 22 as it will affect radius
    INITALISE_PACMAN() 
    
    red = Ghost(red_x, red_y, Player_Player_location[0], ghost_speed[0], red_img,red_Location_of_movement, red_dead,red_box,0 ) # creates each ghost from the Ghost class passes in the variables already eatblished and assigns to the colour of the ghost
    blue = Ghost(blue_x, blue_y, Player_Player_location[1], ghost_speed[1], blue_img,blue_Location_of_movement, blue_dead,blue_box,1 )
    pin = Ghost(pin_x, pin_y, Player_Player_location[2], ghost_speed[2], pin_img,pin_Location_of_movement, pin_dead,pin_box,2 )
    yellow = Ghost(yellow_x, yellow_y, Player_Player_location[3], ghost_speed[3], yellow_img,yellow_Location_of_movement, yellow_dead,yellow_box,3 )

    ADDED_FEATURES() # initalising functions
    Player_Player_location = get_Player_Player_location(red_x,red_y,blue_x,blue_y,pin_x,pin_y,yellow_x,yellow_y) # inistalising functions passing in the co-ordiantes of ghosts
    
    Moves_possible= Check_location_OF_POSITION(center_x,center_y) # if move is avalible for pacman
    if moving:
        X_Pos_Player, Y_Pos_Player = MOVE_PAC(X_Pos_Player,Y_Pos_Player) # updates his location based on x and y as he is constaly moving real time location
        
        if not blue_dead and blue.In_Main:
            blue_x, blue_y, blue_Location_of_movement = blue.move_blue()  # if not dead and in main location then move the ghosts and update their indivisual x and y co-ordinates
        else:
            blue_x, blue_y, blue_Location_of_movement = blue.move_yellow()
        
        if not pin_dead and not pin.In_Main:
            pin_x, pin_y, pin_Location_of_movement = pin.move_pin()
        else:
            pin_x, pin_y, pin_Location_of_movement = pin.move_yellow()
        
        
        red_x, red_y, red_Location_of_movement = red.move_yellow()
        yellow_x, yellow_y, yellow_Location_of_movement = yellow.move_yellow()
    
    Player_Score, Reverse_Eat, POWER_POINT_CHECK, EATEN_GHOST = Contact(Player_Score, Reverse_Eat, POWER_POINT_CHECK,EATEN_GHOST)
    
    def reset_game(): # as satted resets the game basically makes everything global to acess then relaods them one at a time and sets inital condions back hence the deep copy of board required
        global lives, Inital_Location_of_movement, Reverse_Eat, POWER_POINT_CHECK, X_Pos_Player, Y_Pos_Player, Location_of_movement, Location_of_movement_command
        global red_x, red_y, red_Location_of_movement, blue_x, blue_y, blue_Location_of_movement
        global pin_x, pin_y, pin_Location_of_movement, yellow_x, yellow_y, yellow_Location_of_movement
        global EATEN_GHOST, red_dead, blue_dead, pin_dead, yellow_dead
        
        lives -= 1
        Inital_Location_of_movement = 0
        Reverse_Eat = False
        POWER_POINT_CHECK = 0
        X_Pos_Player, Y_Pos_Player = 433, 618
        Location_of_movement, Location_of_movement_command = 0, 0

        red_x, red_y, red_Location_of_movement = 56, 58, 0
        blue_x, blue_y, blue_Location_of_movement = 390, 400, 2
        pin_x, pin_y, pin_Location_of_movement = 440, 388, 2
        yellow_x, yellow_y, yellow_Location_of_movement = 440, 388, 2

        EATEN_GHOST = [False] * 4
        red_dead, blue_dead, pin_dead, yellow_dead = False, False, False, False


    if not Reverse_Eat: # this is saying that if freeze/radar is not active and pacman hits the ghosts then this will always make Pacman lose a life as long as the ghosts are alive
        ghosts_alive = [(red.rect, red_dead), (blue.rect, blue_dead), (pin.rect, pin_dead), (yellow.rect, yellow_dead)]
        for ghost_rect, ghost_dead in ghosts_alive:
            if not ghost_dead and player_circle.colliderect(ghost_rect): # colliderect is a spesific pygame function
                if lives > 0: # so if lives are less than zero display the game end screen and set match lost to true if you wanted him to stop playing when he runs out of lives change the 0 to 1 
                    reset_game()
                else:
                    MATCH_LOST = True
                    moving = False
                    Inital_Location_of_movement = 0

    if Reverse_Eat and player_circle.colliderect(red.rect) and EATEN_GHOST[0] and not red.Ghost_Dead: # this is just for safty doing it with each indisial ghost defensive programming again
        if lives > 0:
            reset_game()
        else:
            MATCH_LOST = True
            moving = False
            Inital_Location_of_movement = 0

    def reset_game(): # repetes again
        global lives, Inital_Location_of_movement, Reverse_Eat, POWER_POINT_CHECK, X_Pos_Player, Y_Pos_Player, Location_of_movement, Location_of_movement_command
        global red_x, red_y, red_Location_of_movement, blue_x, blue_y, blue_Location_of_movement
        global pin_x, pin_y, pin_Location_of_movement, yellow_x, yellow_y, yellow_Location_of_movement
        global EATEN_GHOST, red_dead, blue_dead, pin_dead, yellow_dead
        
        lives -= 1
        Inital_Location_of_movement = 0
        Reverse_Eat = False
        POWER_POINT_CHECK = 0
        X_Pos_Player, Y_Pos_Player = 433, 618
        Location_of_movement, Location_of_movement_command = 0, 0

        red_x, red_y, red_Location_of_movement = 56, 58, 0
        blue_x, blue_y, blue_Location_of_movement = 390, 400, 2
        pin_x, pin_y, pin_Location_of_movement = 440, 388, 2
        yellow_x, yellow_y, yellow_Location_of_movement = 440, 388, 2

        EATEN_GHOST = [False] * 4
        red_dead, blue_dead, pin_dead, yellow_dead = False, False, False, False
        
        
    
    if Reverse_Eat and player_circle.colliderect(red.rect) and EATEN_GHOST[0] and not blue.Ghost_Dead: # does for blue
        if lives > 0:
            reset_game()
        else:
            MATCH_LOST = True
            moving = False
            Inital_Location_of_movement = 0

    def reset_game():
        global lives, Inital_Location_of_movement, Reverse_Eat, POWER_POINT_CHECK, X_Pos_Player, Y_Pos_Player, Location_of_movement, Location_of_movement_command
        global red_x, red_y, red_Location_of_movement, blue_x, blue_y, blue_Location_of_movement
        global pin_x, pin_y, pin_Location_of_movement, yellow_x, yellow_y, yellow_Location_of_movement
        global EATEN_GHOST, red_dead, blue_dead, pin_dead, yellow_dead
        
        lives -= 1
        Inital_Location_of_movement = 0
        Reverse_Eat = False
        POWER_POINT_CHECK = 0
        X_Pos_Player, Y_Pos_Player = 433, 618
        Location_of_movement, Location_of_movement_command = 0, 0

        red_x, red_y, red_Location_of_movement = 56, 58, 0
        blue_x, blue_y, blue_Location_of_movement = 390, 400, 2
        pin_x, pin_y, pin_Location_of_movement = 440, 388, 2
        yellow_x, yellow_y, yellow_Location_of_movement = 440, 388, 2

        EATEN_GHOST = [False] * 4
        red_dead, blue_dead, pin_dead, yellow_dead = False, False, False, False
        
    if Reverse_Eat and player_circle.colliderect(red.rect) and EATEN_GHOST[0] and not pin.Ghost_Dead: # does for pink
        if lives > 0:
            reset_game()
        else:
            MATCH_LOST = True
            moving = False
            Inital_Location_of_movement = 0

    def reset_game():
        global lives, Inital_Location_of_movement, Reverse_Eat, POWER_POINT_CHECK, X_Pos_Player, Y_Pos_Player, Location_of_movement, Location_of_movement_command
        global red_x, red_y, red_Location_of_movement, blue_x, blue_y, blue_Location_of_movement
        global pin_x, pin_y, pin_Location_of_movement, yellow_x, yellow_y, yellow_Location_of_movement
        global EATEN_GHOST, red_dead, blue_dead, pin_dead, yellow_dead
        
        lives -= 1
        Inital_Location_of_movement = 0
        Reverse_Eat = False
        POWER_POINT_CHECK = 0
        X_Pos_Player, Y_Pos_Player = 433, 618
        Location_of_movement, Location_of_movement_command = 0, 0

        red_x, red_y, red_Location_of_movement = 56, 58, 0
        blue_x, blue_y, blue_Location_of_movement = 390, 400, 2
        pin_x, pin_y, pin_Location_of_movement = 440, 388, 2
        yellow_x, yellow_y, yellow_Location_of_movement = 440, 388, 2

        EATEN_GHOST = [False] * 4
        red_dead, blue_dead, pin_dead, yellow_dead = False, False, False, False
    
    if Reverse_Eat and player_circle.colliderect(red.rect) and EATEN_GHOST[0] and not yellow.Ghost_Dead: # does for yelllow
        if lives > 0:
            reset_game()
        else:
            MATCH_LOST = True
            moving = False
            Inital_Location_of_movement = 0

    def reset_game():
        global lives, Inital_Location_of_movement, Reverse_Eat, POWER_POINT_CHECK, X_Pos_Player, Y_Pos_Player, Location_of_movement, Location_of_movement_command
        global red_x, red_y, red_Location_of_movement, blue_x, blue_y, blue_Location_of_movement
        global pin_x, pin_y, pin_Location_of_movement, yellow_x, yellow_y, yellow_Location_of_movement
        global EATEN_GHOST, red_dead, blue_dead, pin_dead, yellow_dead
        
        lives -= 1
        Inital_Location_of_movement = 0
        Reverse_Eat = False
        POWER_POINT_CHECK = 0
        X_Pos_Player, Y_Pos_Player = 433, 618
        Location_of_movement, Location_of_movement_command = 0, 0

        red_x, red_y, red_Location_of_movement = 56, 58, 0
        blue_x, blue_y, blue_Location_of_movement = 390, 400, 2
        pin_x, pin_y, pin_Location_of_movement = 440, 388, 2
        yellow_x, yellow_y, yellow_Location_of_movement = 440, 388, 2

        EATEN_GHOST = [False] * 4
        red_dead, blue_dead, pin_dead, yellow_dead = False, False, False, False
    # above is a check condition to ensure ghost cannot leave when they die and cannot be eaten multiple times in additon makeing sure that they go back to box == 9  but this is a check codnitom on top of the code belwo


    if Reverse_Eat and player_circle.colliderect(red.rect) and not red.Ghost_Dead and not EATEN_GHOST[0]:  # assigns score so if powerup is active and pacman collides with a ghost which is not dead then he gets 300 points 
        red_dead  = True
        EATEN_GHOST[0] = True 
        Player_Score += 300
    if Reverse_Eat and player_circle.colliderect(blue.rect) and not blue.Ghost_Dead and not EATEN_GHOST[1]:
        blue_dead  = True
        EATEN_GHOST[1] = True 
        Player_Score += 300
    if Reverse_Eat and player_circle.colliderect(pin.rect) and not pin.Ghost_Dead and not EATEN_GHOST[2]:
        pin_dead  = True
        EATEN_GHOST[2] = True 
        Player_Score += 300
    if Reverse_Eat and player_circle.colliderect(yellow.rect) and not yellow.Ghost_Dead and not EATEN_GHOST[3]:
        yellow_dead  = True
        EATEN_GHOST[3] = True 
        Player_Score += 300

   
   




    for event in pygame.event.get():  # is basic pyagem features
        if event.type == pygame.QUIT:
            START_OF_GAME = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  # this is seen in nearly all pygame features is universal this allows for key press with thre users hardware to act with software as mentioned in analysis
                Location_of_movement_command = 0 # right
            if event.key == pygame.K_LEFT:
                Location_of_movement_command = 1 # this is left
            if event.key == pygame.K_UP:
                Location_of_movement_command = 2 # up
            if event.key == pygame.K_DOWN:
                Location_of_movement_command = 3 #down
            if event.key == pygame.K_SPACE and (MATCH_LOST or MATCH_WON): # if the game win or loss screen comes up if they press space bar then reload all of the condtions again
                lives -= 1
                Inital_Location_of_movement = 0
                Reverse_Eat = False
                POWER_POINT_CHECK = 0
                X_Pos_Player = 433
                Y_Pos_Player = 618
                Location_of_movement = 0
                Location_of_movement_command = 0 

                red_x = 56
                red_y = 58 
                red_Location_of_movement = 0

                blue_x = 390
                blue_y = 400
                blue_Location_of_movement = 2

                pin_x = 440
                pin_y = 388
                pin_Location_of_movement = 2

                yellow_x = 440
                yellow_y = 388
                yellow_Location_of_movement = 2

                EATEN_GHOST = [False,False,False,False]
                red_dead = False
                blue_dead = False
                pin_dead = False
                yellow_dead = False
                Player_Score = 0 
                lives = original_lives
                Game_Board = copy.deepcopy(boards) # that deepcopy seen so the board reolds with all the points agiain so the original copy
                MATCH_LOST = False
                MATCH_WON = False

        if event.type == pygame.KEYUP: #in the case of two keys being pressed will continue with Location_of_movement going is like a control variable
            if event.key == pygame.K_RIGHT and Location_of_movement_command == 0:
                Location_of_movement_command = Location_of_movement
            if event.key == pygame.K_LEFT and Location_of_movement_command == 1:
                Location_of_movement_command = Location_of_movement
            if event.key == pygame.K_UP and Location_of_movement_command == 2:
                Location_of_movement_command = Location_of_movement
            if event.key == pygame.K_DOWN and Location_of_movement_command == 3:
                Location_of_movement_command = Location_of_movement


    for  i in range(4):
        if Location_of_movement_command == i and Moves_possible[i] == True:
            Location_of_movement = i  # this is just movement in a loop for ech direction 
    
    if X_Pos_Player > 900:
        X_Pos_Player = -47
    elif X_Pos_Player < -50:
        X_Pos_Player = 897  # get him back on WINDOW through moveemnt this can vary so play around with this alot may be the reason movement is wired.
    
    if red.In_Main and red_dead: # essentially saying that if th ghost has been eten and is in the box then bring himback to life
        red_dead = False
    if blue.In_Main and blue_dead: 
        blue_dead = False
    if pin.In_Main and pin_dead:
        pin_dead = False
    if yellow.In_Main and yellow_dead: 
        yellow_dead = False
    
    
    pygame.display.flip() # so each run the screen is normal

pygame.quit() # quits the game 