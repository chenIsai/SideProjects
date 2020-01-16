"""Author: Isaiah Chen

   Date: May 31 2017
   
   Description: This module contains all of the sprites used in the Plants vs Zombie game. The sprites include: Endzone, House, Player, Scorekeeper, Upgrade, and Zombie
"""

import pygame, random

class Player(pygame.sprite.Sprite):
    """This class represents the player Sprite"""
    def __init__(self, screen):
        """This method instantiates the player sprite, and loads 6 images for animation, it then uses the first image as it's main image and sets the position of the player"""
        #Calling Parent Init Method
        pygame.sprite.Sprite.__init__(self)
        self.image_list = ["./Images/plant1.png", "./Images/plant2.png", "./Images/plant3.png", "./Images/plant4.png", "./Images/plant5.png", "./Images/plant6.png"]
        self.image = pygame.image.load("./Images/plant1.png")
        
        self.__screen = screen
        self.reset()
        #Instance variables to keep track of in game stats
        self.__num = 8
        self.__firing = False
        self.__speed = 5
        
    def go_left(self):
        """This function moves the player left on the screen"""
        self.rect.centerx -= self.__speed
            
    def go_right(self):
        """This function moves the player right on the screen"""
        self.rect.centerx += self.__speed
            
    def go_up(self):
        """This function moves the plaer up on the screen"""
        self.rect.centery -= self.__speed
            
    def go_down(self):
        """THis function moves the player down on the screen"""
        self.rect.centery += self.__speed
        
    def firing(self):
        """This function sets two of the Instance variables which control the plants animation, and causes it to go through the firing animation"""
        self.__firing = True
        self.__num = 32
        
    def increase_speed(self):
        """This method increases the speed of the player"""
        self.__speed += 1

    def reset(self):
        """This method returns the player to their starting position on the game"""
        self.rect = self.image.get_rect()
        self.rect.center = (self.__screen.get_width()/3, self.__screen.get_height()/2)        
    
    def update(self):
        """This function checks to see if the player is outside of the grass in the game using x and y coordinates, and prevents the player from leaving the grass"""
        self.image = pygame.image.load(self.image_list[int(self.__num/8)])
        self.__num += 1
        if self.__num >= 24 and not self.__firing:
            self.__num = 1
        if self.__num == 40 and self.__firing:
            self.__firing = not self.__firing
        if self.rect.left < 169:
            self.rect.left = 170
        if self.rect.right > 684:
            self.rect.right = 683
        if self.rect.bottom < 68:
            self.rect.bottom = 69
        if self.rect.bottom > self.__screen.get_height()-20:
            self.rect.bottom = self.__screen.get_height()-21
            
class Zombie(pygame.sprite.Sprite):
    """This class represents the main enemy of the game"""
    def __init__(self, x_position, waves):
        """This function instantiates a zombie sprite, which has 3 images for animation, and a random range for its points"""
        #Calling Parent Init Method
        pygame.sprite.Sprite.__init__(self)
        
        self.image_list = ["./Images/zombie1.png", "./Images/zombie2.png", "./Images/zombie3.png"]
        self.image = pygame.image.load("./Images/zombie1.png")
        self.image = self.image.convert()
        #Instance variables to keep track of in game stats
        self.set_points(random.randrange(5, 11))
        self.__originalHealth = 10
        self.__health = 10
        self.__speed = random.randrange(1, waves+2)
        
        self.__imagenum = 0
        self.__count = 0
        
        self.rect = self.image.get_rect()
        self.__possibley = [63, 139, 215, 291, 367]
        self.__temp = random.randrange(5)
        self.rect.center = (x_position, self.__possibley[self.__temp])
                         
        
    def update(self):
        """This method changes the zombies position on the screen, by subtracting the speed from the centerx. This function is also responsible for animation"""
        self.rect.centerx -= self.__speed
        self.__count += 1
        self.image = pygame.image.load(self.image_list[int(self.__count/15)])
        if self.__count > 43:
            self.__count = 0
        
    def get_points(self):
        """This function returns the point value of the zombies"""
        return self.__points
    
    def set_points(self, points):
        """This function sets the point value of the zombies"""
        self.__points = points
        
    def lose_health(self, damage):
        """This function subtracts any damage taken from the total health of the zombie, and in turn increases its speed"""
        self.__health -= damage
        if self.__health < self.__originalHealth/self.__speed:
            self.__speed += .5

    def get_health(self):
        """This function returns the total hitpoints of the zombie"""
        return self.__health
        
class Scorekeeper(pygame.sprite.Sprite):
    """This class defines a label sprite to display the score."""
    def __init__(self):
        """This initializer loads the system font "Arial", and
        sets the starting score to 0"""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load system font, and initialize the starting score.
        self.__font = pygame.font.Font("Litty.ttf", 16)
        self.__player_score = 0
        self.__lives = 3
        self.__waves = 0
        self.__time = 0
        self.__zombies_killed = 0
        self.__funds = 0
         
    def player_scored(self, scored):
        """This method increases the player score by the value passed into it"""
        self.__player_score += scored
        
    def lose_life(self):
        """This method subtracts one from the total lives of the player"""
        self.__lives -= 1
        
    def add_lives(self):
        """This function adds one life to the total amount of lives the player has"""
        self.__lives += 1

    def add_funds(self, amount):
        self.__funds += amount
    
    def get_lives(self):
        """This method returns the total lives of the player"""
        return self.__lives
 
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        message = "Player Score: %d    Player Lives: %d   Waves Won: %d    Time Passed: %d    Zombies Killed: %d    Gold Available: %d" % (self.__player_score, self.__lives, self.__waves, self.__time, self.__zombies_killed, self.__funds)
        self.image = self.__font.render(message, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (480, 15)
        
    def get_score(self):
        """This method returns the score of the player"""
        return self.__player_score
    
    def add_score(self, score):
        """This function increases the players score on the scoreboard"""
        self.__player_score += score
    
    def get_waves(self):
        """This function returns the number of waves the player has successfully completed"""
        return self.__waves
    
    def win_wave(self):
        """This method increases the waves won counter by one"""
        self.__waves += 1
        
    def set_time(self, time):
        """This function sets the time on the scorekeeper"""
        self.__time = time
        
    def get_time(self):
        """This function returns the time on the scorekeeper"""
        return self.__time
    
    def killed_zombie(self):
        """This function increases the counter for the number of zombies the player has killed by one"""
        self.__zombies_killed += 1
        

class House(pygame.sprite.Sprite):
    """This class defines the sprite for the house in the PvZ Game, which is used to detect when a zombie has reached its destination, and in turn, damaging the player"""
    def __init__(self, x_position, y_position):
        """This initializer takes the screen, an integer value for the left rect of the sprite, and the width and length of the sprite"""
        #Call the parent __init__ method
        pygame.sprite.Sprite.__init__(self)
        #Draw a rectangle to use as the walls
        self.image = pygame.image.load("./Images/house.png")
        self.image = self.image.convert()
        #Set the rect of the sprite
        self.rect = self.image.get_rect()
        self.rect.left = x_position
        self.rect.top = y_position
        
class EndZone(pygame.sprite.Sprite):
    """This class defines the sprite for the end of the map in the PvZ game, and deletes any stray bullets that reach this point"""
    def __init__(self, screen):
        """This initializer takes the screen, an integer value for the left rect of the sprite, and the width and length of the sprite"""
        #Call the parent __init__ method
        pygame.sprite.Sprite.__init__(self)
        #Draw a rectangle to use as the walls
        self.image = pygame.Surface((1, screen.get_height()))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
         #Set the rect of the sprite
        self.rect = self.image.get_rect()
        self.rect.left = screen.get_width()-1
        self.rect.top = 0
        
class Projectile(pygame.sprite.Sprite):
    """This class defines the bullets that the player will fire in the game"""
    def __init__(self, x, y, dx, damage, bul_health):
        """This method instantiates a bullet, and takes in parameters for damage, health, and where the player is, to create a bullet relative to the location of the player, and their upgrades"""
        #Call Parent Init Method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./Images/bullet.png")
        self.image = self.image.convert()
        #Instance variables to keep track of in game stats
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y+10
        self.__dx = dx
        self.__damage = damage
        self.__health = bul_health
        self.__zomhits = []
        
    def update(self):
        """This function moves the bullet accross the screen"""
        self.rect.left += self.__dx
        
    def get_damage(self):
        """This function returns an integer value representing the amount of damage the bullet will do on collision"""
        return self.__damage
    
    def upgrade(self):
        """This function increases the amount of damage the bullet will do by one"""
        self.__damage += 1
        
    def hit(self):
        """This function is called when the bullet has colided with another sprite, and decreases the bullets overall health by one"""
        self.__health -= 1
    
    def get_health(self):
        """This function returns the health of the bullet"""
        return self.__health
    
    def get_zomhits(self):
        """This function returns a list containing all of the zombies that the bullet has collided with to avoid multiple collisions with the same zombie"""
        return self.__zomhits
    
    def add_zomhits(self, zomhit):
        """This function adds a zombie into the list of zombies a bullet has collided with"""
        self.__zomhits.append(zomhit)
    
    
class Upgrade(pygame.sprite.Sprite):
    """This class represents the upgrade image shown after every wave is won"""
    def __init__(self):
        """This method instantiates the upgrade class, loading an image, and hiding it off screen"""
        #Call Parent Init
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./Images/upgrade.png")
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        self.hide_image()
        
    def show_image(self):
        """This function displays the image on the screen"""
        self.rect.left = 0
        self.rect.top = 285
        
    def hide_image(self):
        """This function hides the image on the screen"""
        self.rect.left = 960
        self.rect.top = 480
