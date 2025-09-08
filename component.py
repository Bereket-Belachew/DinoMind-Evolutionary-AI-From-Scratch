import pygame
import random
class Ground:
    ground_area = 400

    def __init__(self, win_width):
        self.x, self.y = 0, self.ground_area
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)
    
    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Dino:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.velocity_y = 0  # Add velocity for jumping
        self.on_ground = True  # Track if dino is on ground
        self.alive=True
        self.score = 0
    
    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)
    
    def jump(self):
        if self.on_ground:  # Only jump if on ground
            self.velocity_y = -15  # Jump velocity (negative = up)
            self.on_ground = False
    
    def update(self):
        # Apply gravity
        self.velocity_y += 0.8  # Gravity
        self.y += self.velocity_y
        
        # Check if dino hits ground
        if self.y >= 370:  # Ground level
            self.y = 370
            self.velocity_y = 0
            self.on_ground = True
        
        # Update rectangle position
        self.rect.y = self.y
        self.score +=1

class Blockes:

    def __init__(self,x,y,block_height):
        self.x,self.y=x,y
        self.rect=pygame.Rect(self.x,self.y,30,block_height)
    
    def draw(self,window):
        pygame.draw.rect(window,(255, 255, 255),self.rect)
    
    def updates(self):
        # Move block left by 2 pixels each frame
        self.x -= 2
        # Update the rectangle position
        self.rect.x = self.x
        
        # Reset block position when it goes off screen (infinite loop)
        if self.x + 30 < 0:  # When block completely exits left side
            # Generate new random height each time block resets
            new_height = random.randint(50, 100)
            # Calculate new y position so bottom touches ground
            self.y = 400 - new_height
            # Update rectangle with new dimensions
            self.rect = pygame.Rect(self.x, self.y, 30, new_height)
            self.x = 550  # Reset to right side of screen
            self.rect.x = self.x