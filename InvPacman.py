import pygame, sys
from pygame.locals import *
import time

import random
 
# Initialize program
pygame.init()
 
# Assign FPS a value
FPS = 30
FramePerSec = pygame.time.Clock()
 
# Setting up color objects
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
world = dict()
BLOCK_SIZE = 30
# Setup a 300x300 pixel display with caption
DISPLAYSURF = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("Invicible Pacman")

# class World:
#   def __init__(self, map):
class Node:
    # Initialize the class
    def __init__(self, position:(), parent:()):
        self.position = position
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost
    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f
    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))



class BFS_cheby():
  def __init__(self, m):
    self.map = m
  #exemple : 30, 30  -> 90, 60
  def best_first_search(self, start, end):
    
    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node((1, 1), None)
    goal_node = Node((3,3), None)
    # Add the start node
    open.append(start_node)
    
    # Loop until the open list is empty
    while len(open) > 0:
        # Sort the open list to get the node with the lowest cost first
        open.sort()
        # Get the node with the lowest cost
        current_node = open.pop(0)
        closed.append(current_node)
        
        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            #path.append(start) 
            # Return reversed path
            return path[::-1]
        # Unzip the current node position
        (x, y) = current_node.position
        # Get neighbors
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        # Loop neighbors
        for next in neighbors:
            # Get value from map
            map_value = self.map.get(next)
            # Check if the node is a wall
            if(map_value == '='):
                continue
            # Create a neighbor node
            neighbor = Node(next, current_node)
            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue
            
            neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(neighbor.position[1] - start_node.position[1])
            neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1])
            neighbor.f = neighbor.h
           
            if(add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.append(neighbor)
    # Return None, no path is found
    return None
# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True

class GroupGhost():
  def __init__(self):
    self.ghost_list = []

  def __iter__(self):
    self.n = 0
    return self

  def __next__(self):
    if self.n <=  len(self.ghost_list):
      res = self.ghost_list[self.n]
      self.n += 1
      return res  
    else:
      raise StopIteration
  
  def addToList(self):
    pass

		
class Map():
  def __init__(self):
    self.char_to_image = {
      '.': 'images/dot.png',
      '=': 'images/wall.png',
      '*': 'images/power.png',
      'g': 'images/ghost1.png',
      'G': 'images/ghost3.png',
      'h': 'images/ghost4.png',
      'H': 'images/ghost5.png',
    }
    self.w = 0
    self.h = 0
    self.food_left = 0
    



  def load_level(self, number):
    file = "level-%s.txt" % number
    self.food_left = 0

    with open(file) as f:
      map_tmp = [[b for b in line.strip()] for line in f]
      self.h = len(map_tmp)
      world = {(i, j):{"signe":b, "neighboor":[Node((i-1, j), None), Node((i, j-1), None), Node((i+1, j), None), Node((i, j+1), None)]} for i, l in enumerate(map_tmp)  for j, b in enumerate(l)}
      self.food_left = len([b for i, l in enumerate(map_tmp)  for j, b in enumerate(l) if b == "."  ])


          

  
  def draw(self, surface):
    
    for k, v in world.items():
        
      image = self.char_to_image.get(v["signe"], None)
      if image:
        surface.blit(pygame.image.load(self.char_to_image[v["signe"]]), (k[0]*30, k[1]*30))

    # for g in ghosts: g.draw()
    # DISPLAYSURF.draw.text("Score: %s" % pacman.score, topleft=(8, 4), fontsize=40)
    # DISPLAYSURF.draw.text("Lives: %s" % pacman.lives, topright=(WIDTH-8,4), fontsize=40)

    # if pacman.banner and pacman.banner_counter > 0:
    #     screen.draw.text(pacman.banner, center=(WIDTH/2, HEIGHT/2), fontsize=120)

    


class Ghost(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/ghost1.png")
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        self.dx = 5
        self.dy = 0
        self.rot = 0
        self.prevpos = None
 
      def move(self):
        # if pacman.powerup:
        #   g.dx = math.copysign(GHOST_SPEED*1.5, g.x - pacman.x)
        #   g.dy = math.copysign(GHOST_SPEED*1.5, g.y - pacman.y)
        # else:
        self.rect.move_ip(self.dx, self.dy)
          # g.dy = random.choice([-GHOST_SPEED, GHOST_SPEED])
        
 
      
      def draw(self, surface):
        surface.blit(self.image, self.rect) 
 
 
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/pacman_o.png")
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect(topleft=(30, 30))
        self.dx = 0
        self.dy = 0
        self.rot = 0
        self.score = 0
        self.dir = None

    
    def blocks_ahead_of_pacman(self, dx, dy):
        """Return a list of tiles at this position + delta"""

        # Here's where we want to move to
        x = self.rect.x + dx
        y = self.rect.y + dy

        # Find integer block pos, using floor (so 4.7 becomes 4)
        # ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
        # # Remainder let's us check adjacent blocks
        # rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE

        # blocks = [world[iy][ix]]
        # if rx: blocks.append(world[iy][ix + 1])
        # if ry: blocks.append(world[iy + 1][ix])
        # if rx and ry: blocks.append(world[iy + 1][ix + 1])

        #return blocks
        return None

    # def eat_food(self):
    #     ix, iy = int(self.rect.x / BLOCK_SIZE), int(self.rect.y / BLOCK_SIZE)
    #     if world[iy][ix] == '.':
    #         world[iy][ix] = None
    #         self.food_left -= 1
    #         self.score += 1
    #     elif world[iy][ix] == '*':
    #         world[iy][ix] = None
            #pacman.powerup = POWER_UP_START
            #set_banner("Power Up!", 5)
            #for g in ghosts: new_ghost_direction(g)
            #pacman.score += 5

    def alternate(self , option1, option2):
        if time.time()%1 <= (0.5):
            return option2
        else:
            return option1

    def update(self):
       
        # self.eat_food()
        pressed_keys = pygame.key.get_pressed()
        self.image = pygame.image.load(self.alternate( "images/pacman_o.png", "images/pacman_c.png"))

        if pressed_keys[K_UP] or self.dir == "UP":
            storedy = -2
            storedx = 0
            self.dir = "UP"
            self.image = pygame.transform.rotate(
            pygame.image.load(self.alternate("images/pacman_o.png", "images/pacman_c.png")), 90)
            if self.rect.y==0:
                storedy=570
        
        if pressed_keys[K_DOWN] or self.dir == "DOWN":
            storedy = 2
            storedx = 0
            self.dir = "DOWN"
            self.image = pygame.transform.rotate(pygame.image.load(self.alternate("images/pacman_o.png", "images/pacman_c.png")),270)
            if self.rect.y==570:
                storedy=-570
         
        if pressed_keys[K_LEFT] or self.dir == "LEFT":
            storedx = -2
            storedy = 0
            self.dir = "LEFT"
            self.image = pygame.transform.rotate(
                pygame.image.load(self.alternate("images/pacman_or.png", "images/pacman_cr.png")), 180)
            if self.rect.x==0:
                storedx=570

        if pressed_keys[K_RIGHT] or self.dir == "RIGHT":
            storedx = 2
            storedy = 0
            self.dir = "RIGHT"
            if self.rect.x==570:
                storedx=-570

        # if self.dir is not None:
            # if ('=' not in self.blocks_ahead_of_pacman(storedx, storedy)):
            #     self.dx = storedx
            #     self.dy = storedy

            # if '=' not in self.blocks_ahead_of_pacman(self.dx, self.dy):
                  #print("OK storedy:"+str(storedy)+"self.dy ="+str(self.dy))
        self.rect.move_ip(self.dx, self.dy)

 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     
 
         
P1 = Pacman()
E1 = Ghost()
M = Map()
M.load_level(1)
 
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    P1.update()
    E1.move()
     
    DISPLAYSURF.fill(BLACK)
    M.draw(DISPLAYSURF)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
         
    pygame.display.update()
    FramePerSec.tick(FPS)
