import pygame, sys
from pygame.locals import *
import time

import random
from pygame import rect
 
# Initialize program
pygame.init()
 
# Assign FPS a value
FPS = 30
FramePerSec = pygame.time.Clock()
 

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
world = dict()
BLOCK_SIZE = 30
DISPLAYSURF = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("Invicible Pacman")
test_pos = []
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
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)
    
    # Loop until the open list is empty
    while len(open) > 0:
        open.sort()
        # Get the node with the lowest cost
        current_node = open.pop(0)
     
        closed.append(current_node)
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            
            return path[::-1]
        
        (x, y) = current_node.position
        # Get neighbors
        neighbors = self.map[current_node.position]["neighboor"]
       
       
        # Loop neighbors
        for next in neighbors:
            # Get value from map
           
            map_value = self.map.get(next.position)
           
            # Check if the node is a wall
            if(map_value == None):
              continue
            if(map_value["signe"] == "="):
              
                continue
            # Create a neighbor node
            neighbor = Node(next.position, current_node)
           
            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue
            
            neighbor.g = max(abs(neighbor.position[0] - start_node.position[0]), abs(neighbor.position[1] - start_node.position[1]))
            neighbor.h = max(abs(neighbor.position[0] - goal_node.position[0]), abs(neighbor.position[1] - goal_node.position[1]))
            neighbor.f = neighbor.h
           
            if(add_to_open(open, neighbor) == True):
               
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
    if self.n <  len(self.ghost_list):
      res = self.ghost_list[self.n]
      self.n += 1
      return res  
    else:
      raise StopIteration
  
  def addToList(self, g):
    self.ghost_list.append(g)
    # print(len(self.ghost_list))


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
      'M': 'images/marker.png',
    }
    self.w = 0
    self.h = 0
    self.food_left = 0
    self.map_modal = dict()
    self.food_map = []
    self.pacman = None
    self.groupGhost = None
    self.score = 0
    

  def load_level(self, number):
    file = "level-%s.txt" % number
    self.food_left = 0

    with open(file) as f:
      map_tmp = [[b for b in line.strip()] for line in f]
      self.h = len(map_tmp)
      self.map_modal = {(j, i):{"signe":b, "neighboor":[Node((j-1, i), None), Node((j, i-1), None), Node((j+1, i), None), Node((j, i+1), None)]} for i, l in enumerate(map_tmp)  for j, b in enumerate(l)}
      
      self.food_map = [(j, i) for i, l in enumerate(map_tmp)  for j, b in enumerate(l) if b == "."  ]
      self.food_left = len(self.food_map)
      self.groupGhost= GroupGhost()
      for k, v in self.map_modal.items():
        if((v["signe"] == "." or v["signe"] == "*") and k[0] == 0):
          v["neighboor"][0].position = (len(map_tmp[0])-1, v["neighboor"][0].position[1])
          print("changed 1")
        if((v["signe"] == "." or v["signe"] == "*") and k[1] == 0):
          v["neighboor"][1].position = (v["neighboor"][0].position[0], self.h - 1)
          print("changed 2")
        if((v["signe"] == "." or v["signe"] == "*") and k[0] == len(map_tmp[0])- 1):
          v["neighboor"][2].position = (0, v["neighboor"][0].position[1])
          print("changed 3")
        if((v["signe"] == "." or v["signe"] == "*") and k[1] == self.h - 1):
          v["neighboor"][3].position = (v["neighboor"][0].position[0], 0)
          print("changed 4")


        if(v["signe"] == "p"):
          self.pacman = IANaive(k[0], k[1])
        else:
          if(v["signe"] == "g" or v["signe"] == "G" or v["signe"] == "h" or v["signe"] == "H"):
            gosth = IAPhantomBFS(k[0], k[1], self.char_to_image[v["signe"]])
            self.groupGhost.addToList(gosth)
      for g in self.groupGhost:
        print(g)

  def from_pacman_to_ghost(pos):

    x, y = pos
    i = max(0, int(x / 30))
    j = max(0, int(y / 30))

    return i, j         

  
  def get_collision(self):

     for g in self.groupGhost:
      pcx = self.pacman.getX()
      pcy = self.pacman.getY()
      gx = g.getX()
      gy = g.getY()
    #     """Retourne la liste des rectangles autour de la position (i_start, j_start).
 
    # Vu que le personnage est dans le carré (i_start, j_start), il ne peut
    # entrer en collision qu'avec des blocks dans sa case, la case en-dessous,
    # la case à droite ou celle en bas et à droite. On ne prend en compte que
    # les cases du niveau avec une valeur de 1.
    # """
     blocks = list()
     i, j = from_pacman_to_ghost(pos)

     for j in range(gx, gy+2):
        for i in range(gx, gx+2):
            if niveau[j][i] == 1:
                topleft = i*30, j*30
                blocks.append(pygame.Rect((topleft), (30, 30)))
    
            for block in blocks:
             if rect.colliderect(block):
              return True
             return False  

     


      
      #si le pacman rencontre les fantomes
     
     # if(gy + BLOCK_SIZE >= pcy >= gy): #en hauuuuuut
       
        #return false
      # if(gy <= pcy + BLO): #en baaaaaaaaaaaaas
        #return false

      # if(): #a gauuuuuuuuuuuuuuche

        #return false

      # if():  #a droiiiiiiiiiiiiiite , CES SOIREES LA
        #return false

    # return True

  def update(self):
    
    
    
    # self.score=self.pacman.update2(self.map_modal, self.h, self.food_map, self.score)
    # for g in self.groupGhost:
    #   g.update(self.map_modal, self.h, (self.pacman.getX(), self.pacman.getY()))

    is_collision = self.get_collision()
    if(is_collision):
      print("perdu")
      exit(1)



  def draw(self, surface):
  
    for k, v in self.map_modal.items():
      if(v["signe"] == "="):
        image = self.char_to_image.get(v["signe"], None)
        if image:
          surface.blit(pygame.image.load(self.char_to_image[v["signe"]]), (k[0]*30, k[1]*30))
    
    for food in self.food_map:
      surface.blit(pygame.image.load(self.char_to_image["."]), (food[0]*30, food[1]*30))
    for g in self.groupGhost:
      g.draw(surface)


   

    self.pacman.draw(surface)
    
    # for g in ghosts: g.draw()
    # DISPLAYSURF.draw.text("Score: %s" % pacman.score, topleft=(8, 4), fontsize=40)
    # DISPLAYSURF.draw.text("Lives: %s" % pacman.lives, topright=(WIDTH-8,4), fontsize=40)

    # if pacman.banner and pacman.banner_counter > 0:
    #     screen.draw.text(pacman.banner, center=(WIDTH/2, HEIGHT/2), fontsize=120)

    


class Ghost(pygame.sprite.Sprite):
      def __init__(self, x, y, signe):
        super().__init__() 
        self.image = pygame.image.load(signe)
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        self.dx = 0
        self.dy = 0
        self.x = x*BLOCK_SIZE
        self.y = y*BLOCK_SIZE
        self.signe = signe
        self.rot = 0
        self.is_random = True
        self.tab_chemin = []

      
          # elif(self.dx > 0): #go on right
          # elif(self.dy >  0): #go down
          # else: #go top

        # else:
       
          # g.dy = random.choice([-GHOST_SPEED, GHOST_SPEED])
        
 
      def getX(self):
        return self.x

      def getY(self):
        return self.y

      def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        for t in self.tab_chemin:
          surface.blit(pygame.image.load("images/marker.png"), (t[0]*BLOCK_SIZE, t[1]*BLOCK_SIZE))


      def __str__(self):  
        return "From x= %s, y = %s" % (self.x, self.y)  




class IAPhantomNaive(Ghost):
  def update(self, tab_mod, heigt, pacman_pos):
        choices = [5, -5]
    
        

        tmpx = self.x // BLOCK_SIZE
        tmpy = self.y // BLOCK_SIZE

        moduloX = self.x % BLOCK_SIZE
        moduloY = self.y % BLOCK_SIZE

        if(self.x >= (len(tab_mod) / heigt) * 30 - 30):
          self.x = 5
         
       
        elif(self.x <= 0):
          self.x = ((len(tab_mod)/heigt) * BLOCK_SIZE)  - BLOCK_SIZE - 5
          
        elif(self.y >= heigt*30-30):
          self.y = 5
          
        elif(self.y <= 0):
          self.y = heigt*30-25
         
        else:

          nh = tab_mod[(tmpx, tmpy)]["neighboor"]
          if(moduloX == 0 and moduloY == 0):

            
          
            
            nh = tab_mod[(tmpx, tmpy)]["neighboor"]
            possible_pos = [ n for n in nh if(tab_mod[n.position]["signe"] != "=")]
            if(len(possible_pos) == 2): # possible ligne  droite
              n1 = possible_pos[0].position
              n2 = possible_pos[1].position
              if( n1[0] == n2[0] or n1[1] == n2[1] ): # on rentre dans le use case d'un ligne droite horizontal ou vertical
                if(self.dx == 0 and self.dy == 0): # si le fantome s'est arreter
                  
                  if(n1[0] == n2[0]): #c'est vertical  
                    self.dy = random.choice(choices);
                  else:
                    self.dx = random.choice(choices);
              else:
               #on rentre dans le use case d'un angle
                self.dx = 0
                self.dy = 0
                tn = [n1, n2]
                n3 = random.choice(tn)
                
                if(tmpx - n3[0] > 0):
                  self.dx = -5
                  
                elif(tmpx - n3[0] < 0):
                  self.dx = 5

                elif(tmpy - n3[1] < 0):
                  self.dy = 5
                else:
                  self.dy = -5

            else:
              randy = random.choice(possible_pos)
              nrandy = randy.position
              self.dx = 0
              self.dy = 0
              if(tmpx - nrandy[0] > 0):
                  self.dx = -5
                  
              elif(tmpx - nrandy[0] < 0):
                self.dx = 5

              elif(tmpy - nrandy[1] < 0):
                self.dy = 5
              else:
                self.dy = -5
          self.x += self.dx
          self.y += self.dy
          self.rect.move_ip(self.x, self.y)

class IAPhantomBFS(IAPhantomNaive):
  
  def check_line(self, posx_line, posy_line, vecteur,pac_pos,tab_mod, h_map):
    while(True):
      if(tab_mod[(posx_line + vecteur[0], posy_line + vecteur[1])]["signe"] == "="):
        return False
      else:
        posx_line += vecteur[0]
        posy_line += vecteur[1]
        if(posx_line == pac_pos[0] and posy_line== pac_pos[1]):
          return True
        if(posx_line < 0 or posy_line < 0):
          break
        if(posy_line > h_map):
          break
        if(posx_line > len(tab_mod)//h_map):
          break;

    return False

  def continue_chemin(self):
    if(len(self.tab_chemin) != 0):

      
      
      obj = self.tab_chemin[0]
    
      mycaseX = self.x // BLOCK_SIZE
      mycaseY = self.y // BLOCK_SIZE
      print(mycaseX, "  ", mycaseY)
      if(self.x ==(obj[0]*BLOCK_SIZE) and self.y == (obj[1]*BLOCK_SIZE) ):
        self.tab_chemin.pop(0)
        self.continue_chemin()
      else:
        if(mycaseX < obj[0]):

          self.dx = 5
          self.dy = 0
        elif(mycaseX > obj[0]):
          self.dx = -5
          self.dy = 0
        elif(mycaseY > obj[1]):
          self.dy = -5
          self.dx = 0
        else:
          if(mycaseY < obj[1]):
            self.dy = 5
            self.dx = 0
        self.x += self.dx
        self.y += self.dy
        self.rect.move_ip(self.x, self.y)

        




  def update(self, tab_mod, heigt, pacman_pos):
    
      
    pac_pos_x_reel = pacman_pos[0]
    pac_pos_y_reel = pacman_pos[1]
    pac_pos_x = pac_pos_x_reel // BLOCK_SIZE
    pac_pos_y = pac_pos_y_reel // BLOCK_SIZE
    busted = False
    mycaseX = self.x // BLOCK_SIZE
    mycaseY = self.y // BLOCK_SIZE
    if(self.x < pacman_pos[0]  and  self.dx > 0 and ((self.y <= pac_pos_y_reel <= self.y + BLOCK_SIZE) or (self.y <= pac_pos_y_reel+30 <= self.y + BLOCK_SIZE)) ): #je regarde a droite et il y'a potentiellement pacman -> coup de calcul en moins si pacman est a ca gauche par exemple
      
      busted = self.check_line(mycaseX, mycaseY, (1, 0), (pac_pos_x, mycaseY), tab_mod, heigt)
    elif(self.x > pacman_pos[0] and self.dx < 0 and ((self.y <= pac_pos_y_reel <= self.y + BLOCK_SIZE) or (self.y <= pac_pos_y_reel+30 <= self.y + BLOCK_SIZE)) ):
      
      busted = self.check_line(mycaseX, mycaseY, (-1, 0), (pac_pos_x, mycaseY), tab_mod, heigt)
    elif(self.y > pac_pos_y_reel and self.dy < 0 and ((self.x <= pac_pos_x_reel <= self.x + BLOCK_SIZE) or (self.x <= pac_pos_x_reel+30 <= self.x + BLOCK_SIZE)) ): #je suis en bas et je remonte
      
     
      busted = self.check_line(mycaseX, mycaseY, (0, -1), (mycaseX,pac_pos_y), tab_mod, heigt)
      
      
    elif(self.y < pacman_pos[1] and self.dy > 0 and ((self.x <= pac_pos_x_reel <= self.x + BLOCK_SIZE) or (self.x <= pac_pos_x_reel+30 <= self.x + BLOCK_SIZE)) ):
     
      busted = self.check_line(mycaseX, mycaseY, (0, 1), (mycaseX,pac_pos_y), tab_mod, heigt)
    else:
      pass
    if(busted):
      Bf = BFS_cheby(tab_mod)

      self.tab_chemin = Bf.best_first_search((mycaseX, mycaseY), (pac_pos_x, pac_pos_y))
      print(self.tab_chemin)
     
      # print(self.tab_chemin)
      # print((mycaseX, mycaseY), " ", (pac_pos_x, pac_pos_y))
      if(len(self.tab_chemin) != 0):
        self.continue_chemin()
    else:
      if(len(self.tab_chemin) == 0):
         
        IAPhantomNaive.update(self, tab_mod, heigt, pacman_pos)
      else:
        print("continue chemin")
        self.continue_chemin()
        #je continue mon chemin



class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.image = pygame.image.load("images/pacman_o.png")
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        
        self.dx = 0
        self.dy = 0
        self.rot = 0
        self.score = 0
        self.dir = None
        self.x = x*BLOCK_SIZE
        self.y = y*BLOCK_SIZE
        

    

    def getX(self):
        return self.x

    def getY(self):
        return self.y

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

   
            


    def eat_food(self, map_food, score):
        ix, iy = int(self.x / BLOCK_SIZE), int(self.y / BLOCK_SIZE)
        if (ix, iy) in map_food:
            map_food.remove((ix, iy))
            # print("hummmmm!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #self.food_left -= 1
            score += 1
            # print("scoreeat = ", score)
        #pacman.powerup = POWER_UP_START
        #set_banner("Power Up!", 5)
        #for g in ghosts: new_ghost_direction(g)
        #pacman.score += 5
        return score

    def alternate(self, option1, option2):
        if time.time() % 1 <= (0.5):
            return option2
        else:
            return option1

    def load_image(self, image1, image2, angle):
        return pygame.transform.rotate(pygame.image.load(self.alternate(image1, image2)), angle)
    def update_image(self):
        if self.dir == "U":
            self.image = self.load_image("images/pacman_o.png", "images/pacman_c.png", 270)
        if self.dir == "L":
            self.image = self.load_image("images/pacman_or.png", "images/pacman_cr.png", 180)
        if self.dir == "R":
            self.image = self.load_image("images/pacman_o.png", "images/pacman_c.png", 0)
        if self.dir == "D":
            self.image = self.load_image("images/pacman_o.png", "images/pacman_c.png", 90)
   
    # def update(self):
       
    #     # self.eat_food()
    #     pressed_keys = pygame.key.get_pressed()
    #     self.image = pygame.image.load(self.alternate( "images/pacman_o.png", "images/pacman_c.png"))

    #     if pressed_keys[K_UP] or self.dir == "UP":
    #         storedy = -5
    #         storedx = 0
    #         self.dir = "UP"
    #         self.image = pygame.transform.rotate(
    #         pygame.image.load(self.alternate("images/pacman_o.png", "images/pacman_c.png")), 90)
    #         if self.rect.y==0:
    #             storedy=570
        
    #     if pressed_keys[K_DOWN] or self.dir == "DOWN":
    #         storedy = 5
    #         storedx = 0
    #         self.dir = "DOWN"
    #         self.image = pygame.transform.rotate(pygame.image.load(self.alternate("images/pacman_o.png", "images/pacman_c.png")),270)
    #         if self.rect.y==570:
    #             storedy=-570
         
    #     if pressed_keys[K_LEFT] or self.dir == "LEFT":
    #         storedx = -5
    #         storedy = 0
    #         self.dir = "LEFT"
    #         self.image = pygame.transform.rotate(
    #             pygame.image.load(self.alternate("images/pacman_or.png", "images/pacman_cr.png")), 180)
    #         if self.rect.x==0:
    #             storedx=570

    #     if pressed_keys[K_RIGHT] or self.dir == "RIGHT":
    #         storedx = 5
    #         storedy = 0
    #         self.dir = "RIGHT"
    #         if self.rect.x==570:
    #             storedx=-570

    #     # if self.dir is not None:
    #         # if ('=' not in self.blocks_ahead_of_pacman(storedx, storedy)):
    #         #     self.dx = storedx
    #         #     self.dy = storedy

    #         # if '=' not in self.blocks_ahead_of_pacman(self.dx, self.dy):
    #               #print("OK storedy:"+str(storedy)+"self.dy ="+str(self.dy))
    #     self.rect.move_ip(self.dx, self.dy)

 
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))     

class IANaive(Pacman):

  def update2(self, tab_mod, heigt, food_map, score):
        
        choices = [5, -5]
        self.x += self.dx
        self.y += self.dy

        tmpx = self.x // BLOCK_SIZE
        tmpy = self.y // BLOCK_SIZE

        moduloX = self.x % BLOCK_SIZE
        moduloY = self.y % BLOCK_SIZE

        if(self.x >= (len(tab_mod) / heigt) * 30 - 30):
          self.x = 5
         
        elif(self.x <= 0):
          self.x = ((len(tab_mod)/ heigt) * BLOCK_SIZE)  - BLOCK_SIZE - 5
          
        elif(self.y >= heigt*30-30):
          self.y = 5
          
        elif(self.y <= 0):
          self.y = heigt*30-30-5
         
        else:

          nh = tab_mod[(tmpx, tmpy)]["neighboor"]
          if(moduloX or moduloY):
            pass
          else:
            
            nh = tab_mod[(tmpx, tmpy)]["neighboor"]
            possible_pos = [ n for n in nh if(tab_mod[n.position]["signe"] != "=")]
            if(len(possible_pos) == 2): # possible ligne  droite
              n1 = possible_pos[0].position
              n2 = possible_pos[1].position
              if( n1[0] == n2[0] or n1[1] == n2[1] ): # on rentre dans le use case d'un ligne droite horizontal ou vertical
                if(self.dx == 0 and self.dy == 0): # si le fantome s'est arreter
                  self.dx = 0
                  self.dy = 0
                  if(n1[0] == n2[0]): #c'est vertical  
                    self.dy = random.choice(choices);
                  else:
                    self.dx = random.choice(choices);
              else:
               #on rentre dans le use case d'un angle
                self.dx = 0
                self.dy = 0
                tn = [n1, n2]
                n3 = random.choice(tn)
                
                if(tmpx - n3[0] > 0):
                  self.dx = -5
                  
                elif(tmpx - n3[0] < 0):
                  self.dx = 5

                elif(tmpy - n3[1] < 0):
                  self.dy = 5
                else:
                  self.dy = -5

            else:
              randy = random.choice(possible_pos)
              nrandy = randy.position
              self.dx = 0
              self.dy = 0
              if(tmpx - nrandy[0] > 0):
                  self.dx = -5
                  
              elif(tmpx - nrandy[0] < 0):
                self.dx = 5

              elif(tmpy - nrandy[1] < 0):
                self.dy = 5
              else:
        
                self.dy = -5
        if self.dx == 5:
            self.dir = "R"

        elif self.dx == -5:
            self.dir = "L"
        elif self.dy == 5:
            self.dir = "U"
        elif self.dy == -5:
            self.dir = "D"
        else:
            self.dir = None
        self.update_image()
        score = self.eat_food(food_map, score)
        # print(self.dx, "  ", self.dy)
        self.rect.move_ip(self.x + self.dx, self.y + self.dy)
        # print("score = ", score)

        return score
        
         
# P1 = Pacman()
# E1 = Ghost()
M = Map()
M.load_level(1)
 
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

     
    DISPLAYSURF.fill(BLACK)
    M.update()
    M.draw(DISPLAYSURF)
    
         
    pygame.display.update()
    FramePerSec.tick(FPS)
  