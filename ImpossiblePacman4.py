import pygame, sys
from pygame.locals import *
import time
import random
import re
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
DISPLAYSURF = pygame.display.set_mode((720,720))
pygame.display.set_caption("Impossible Pacman")
test_pos = []

# class World:
#   def __init__(self, map):
class MessageBox:
    def __init__(self, window_rect, font, message):
        self.window_rect = window_rect
        self.font = font
        self.background_colour = pygame.Color("#555555")
        self.text_colour = pygame.Color("#FFFFFF")
        
        # self.window_title_str = "Message"
        self.title_text_render = self.font.render("", True, self.text_colour)

        self.should_exit = False

        self.done_button = UTTextButton([self.window_rect[0] + (self.window_rect[2] / 2) + 45,
                                         self.window_rect[1] + self.window_rect[3] - 30, 70, 20], "Done", font)

        self.message = message
        self.message_text_render = self.font.render(self.message, True, self.text_colour)

    def handle_input_event(self, event):
        self.done_button.handle_input_event(event)

    def update(self):
        self.done_button.update()

        if self.done_button.was_pressed():
            print("pressed")
            self.should_exit = True

    def is_inside(self, screen_pos):
        is_inside = False
        if self.window_rect[0] <= screen_pos[0] <= self.window_rect[0] + self.window_rect[2]:
            if self.window_rect[1] <= screen_pos[1] <= self.window_rect[1] + self.window_rect[3]:
                is_inside = True
        return is_inside

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_colour, pygame.Rect(self.window_rect[0], self.window_rect[1],
                                                                     self.window_rect[2], self.window_rect[3]), 0)

        screen.blit(self.title_text_render,
                    self.title_text_render.get_rect(centerx=self.window_rect[0] + self.window_rect[2] * 0.5,
                                                    centery=self.window_rect[1] + 24))

        screen.blit(self.message_text_render,
                    self.message_text_render.get_rect(centerx=self.window_rect.centerx,
                                                      centery=self.window_rect[1] + 50))
        
        self.done_button.draw(screen)


class UTTextButton:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.text_colour = pygame.Color("#FFFFFF")
        self.background_colour = pygame.Color("#151515")
        self.text_render = self.font.render(self.text, True, self.text_colour)
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = self.rect.center
    
    def update(self):
        pass
    
    def was_pressed(self):
        mpos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos) and MOUSEPRESSED:
            return True
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.background_colour, self.rect)
        screen.blit(self.text_render, self.text_rect)


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
  def __init__(self, m, gate):
    self.map = m
    self.gate = gate
  #exemple : 30, 30  -> 90, 60
  def Distance(self, x1,y1,x2,y2):
    return abs(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)

  def check_take_tp(self, startx1, starty1, goalx2, goaly2):
    tmp_distance = 0
    tmp_tup =   None
    tmp_i = 0
    for i in range(len(self.gate)):
        
        d1 = self.Distance(startx1, starty1, self.gate[i][0], self.gate[i][1]) 
        d2 = 0
        d3 = self.Distance(startx1, starty1, goalx2, goaly2) 
        if(i%2 == 0):
          d2 = self.Distance(self.gate[i+1][0], self.gate[i+1][1],  goalx2, goaly2)
                 
        else:
          d2 = self.Distance(self.gate[i-1][0], self.gate[i-1][1],  goalx2, goaly2)
          
        
        if((d1 + d2) < d3):
          if(tmp_distance == None):
            
            tmp_distance = d3 - (d1+d2)
            tmp_i = i
          else:
            if(tmp_distance < (d3 - (d1 + d2))):
              
              tmp_distance = d3 - (d1+d2)
              tmp_i = i
    if(tmp_distance == 0):
      return None
    else:
      return tmp_i
      

  def best_first_search(self, start, end):
    go_to_tp = self.check_take_tp(start[0], start[1], end[0], end[1])
    if(go_to_tp != None):
      dl = self.best_first_search(start, (self.gate[go_to_tp][0], self.gate[go_to_tp][1]))
      if(go_to_tp % 2 == 0):
        dr = self.best_first_search((self.gate[go_to_tp+1][0], self.gate[go_to_tp+1][1]), end)
      else:
        dr = self.best_first_search(start, (self.gate[go_to_tp][0], self.gate[go_to_tp][1])) + self.best_first_search((self.gate[go_to_tp-1][0], self.gate[go_to_tp-1][1]), end)  
      if(dl == None):
        return dr
      elif(dr == None):
        return dl
      else:
        return dl + dr
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
  

  def update(self, map_modal, h, tupl, bfoj):
    for g in self.ghost_list:
      g.update(map_modal, h, tupl, bfoj)
      

  def addToList(self, g):
    self.ghost_list.append(g)
    # print(len(self.ghost_list))




class EnsembleOnEstPlusFort(GroupGhost):


 


  def update(self, map_modal, h, tupl, teleport):
    onehasbusted = False
    for g in self.ghost_list:
      g.update(map_modal, h, tupl, teleport)
      if(g.isBusting() == True):
        onehasbusted = True
    if(onehasbusted):
      for g in self.ghost_list:
          g.init_tab_chemin((tupl[0]//BLOCK_SIZE, tupl[1]//BLOCK_SIZE), map_modal, teleport)
      
      

class EnsembleOnEstPlusFortV2(EnsembleOnEstPlusFort):
  

  def subfct(self, mapm, current_node, n, tabl):
    if(n == 0):
      return tabl
    else:
      neigh = [nod.position for nod in mapm[current_node]["neighboor"] if mapm[nod.position]["signe"] != "=" and nod.position not in tabl]
    
      for new_pos in neigh :
        if( new_pos not in tabl):
          tabl += self.subfct(mapm, new_pos, n-1, tabl+[new_pos])
      return tabl

  def get_n_case_around_pacman(self, map_modal, h, tupl, n):
    pac_x = tupl[0] // BLOCK_SIZE
    pac_y = tupl[1] // BLOCK_SIZE
    return self.subfct(map_modal, (pac_x, pac_y), n, [(pac_x, pac_y)])

  def getallIntersection(self, map_modal):
    intersection = []
    for nod in map_modal:
      if(map_modal[nod]["signe"] != "="):
        possible_pos = map_modal[nod]["neighboor"] 
        cur = [p.position for p in possible_pos if(map_modal[p.position]["signe"] != "=")]
        if(len(cur) > 2):
          intersection.append(nod)
        else:
          if(len(cur) == 2):
            n1 = cur[0]
            n2 = cur[1]
            if(n1[0] != n2[0] and n1[1] != n2[1]): #on est pas sur une ligne droite

              intersection.append(nod)
    return intersection


  def closest_to_pacman(self, pacmanx, pacmany, map_modal):
    inter = self.getallIntersection(map_modal)
    bf = BFS_cheby(None, None)
    distance_from_paquitou = [(bf.Distance(nod[0]*30, nod[1]*30, pacmanx, pacmany), nod) for nod in inter]
    distance_from_paquitou.sort()
    return distance_from_paquitou
    

  def get_extremite_chemin(self, tuplee, visited, map_modal):
    possible_pos = [nd.position for nd in map_modal[tuplee]["neighboor"] if map_modal[nd.position]["signe"] != "="]
    for v in visited:
      if(v in possible_pos):
        possible_pos.remove(v)
    if(len(possible_pos) == 2 and len(visited) > 0):
      
      return tuplee
    else:
      t = []
      for pp in possible_pos:
       
        t.append(self.get_extremite_chemin(pp, visited+[tuplee], map_modal))
        if(len(t) > 0 and isinstance(t, list)):
          while (isinstance(t, list)):
            if(len(t) > 0):
              t = t[0]
            else:
              break
            if(not isinstance(t, list)):
              t = [t]
              break
          
      return t

  def update(self, map_modal, h, tupl, teleport):
    onehasbusted = False
    for g in self.ghost_list:
      g.update(map_modal, h, tupl, teleport)
      if(g.isBusting() == True):
        onehasbusted = True
    if(onehasbusted):
      dst_inter_to_pac = self.closest_to_pacman(tupl[0], tupl[1], map_modal)
      g_equipier = []
      for g in self.ghost_list:
          if(g.isBusting()):
            g.init_tab_chemin((tupl[0]//BLOCK_SIZE, tupl[1]//BLOCK_SIZE), map_modal, teleport)
          else:
            g_equipier.append(g)
      nb_equipier = len(g_equipier)
      if (nb_equipier > len(dst_inter_to_pac)):
        dst_inter_to_pac= dst_inter_to_pac[:nb_equipier]
      tu = self.get_extremite_chemin((tupl[0]//BLOCK_SIZE, tupl[1]//BLOCK_SIZE), [], map_modal)
      final_t = []
      for xj in tu:
        if(isinstance(xj, list)):
          final_t.append(xj[0])
        else:
          final_t.append(xj)
      b = BFS_cheby(None, None)
      teamate_a_charge = []
      all_chemin = []
      distance_from_paq = [(b.Distance(tupl[0], tupl[1], f[0], f[1]), f) for f in final_t]
      #on classe les intersections du chemins courant de pacman dans l'ordre de priorité, autrement dit, la fin du chemin la plus proche de pacman est la plus importante et ainsi de suite
      distance_from_paq.sort(key=lambda tup: tup[0])

      # Maintenant qu'on a toutes les intersections de la map et toutes les intersections du chemin de pacman on met en priorité celles du chemin



      """

      O
      |---------
      | *
      |
      |
      
      Car même si on a trier toutes les intersections par ordre de distance avec Pacman on a pas vérifier la longeur du chemin pour aller de ce point 
      jusqua pacman et si il existait des murs 
      d'ou le fait de mettre en priorité les intersections du chemin courant de Pacman
      """


      teamate_used = {}
      #pour chaque distance on tri les fantomes dans l'ordre du plus proches          
      for dst in distance_from_paq:
        dst2_tab = [(b.Distance(g2.getX(), g2.getY(), dst[1][0], dst[1][1]), g2) for g2 in g_equipier]
        dst2_tab.sort(key=lambda tup: tup[0]) 
        teamate_used[dst[1]] = dst2_tab

      for k, val in teamate_used.items():
        
        for v in val:
          
          if(v[1].getId() not in teamate_a_charge):
            teamate_a_charge.append(v[1].getId())
            all_chemin.append((v[1], k))
            break
      print("all chemin apres intersections chemin")
      print(all_chemin)




      for dst in dst_inter_to_pac:
        dst_tab = [(b.Distance(g2.getX(), g2.getY(), dst[1][0], dst[1][1]), g2) for g2 in g_equipier if g2.getId() not in teamate_a_charge]
        dst_tab.sort(key=lambda tup: tup[0]) 
        teamate_used[dst[1]] = dst_tab
      
      
      
      for k, val in teamate_used.items():
        print(k)
        print("=======")
        print(val)
        for v in val:
          print("+++++++++++++")
          print(v[1])
          if(v[1].getId() not in teamate_a_charge):
            teamate_a_charge.append(v[1].getId())
            all_chemin.append((v[1], k))
            break
      print("all chemin apres tout")
      print(all_chemin)
      for ghst, goal_case in all_chemin:
        ghst.init_tab_chemin(goal_case,map_modal, teleport)
   
class EnsembleOnEstPlusFortV3(EnsembleOnEstPlusFortV2):
  """
  Trouve toutes les fins de chemins de pacman a partir du moment ou il est busted pour que les fantomes l'encerclent
  """
  def __init__(self, fm):
    super().__init__()
    self.food_m = fm


 
    


  def update(self, map_modal, h, tupl, teleport, map_referentiel):
    onehasbusted = False
    for g in self.ghost_list:
      ix, iy = int(g.getX() / BLOCK_SIZE), int(g.getY() / BLOCK_SIZE)
      if (ix, iy) in self.food_m and (ix, iy) not in map_referentiel:
          self.food_m.remove((ix, iy))

    for g in self.ghost_list:
      g.update(map_modal, h, tupl, teleport)
      if(g.isBusting() == True):
        onehasbusted = True
    
    


    if(onehasbusted):
      dst_inter_to_pac = self.closest_to_pacman(tupl[0], tupl[1], map_modal)
      g_equipier = []
      for g in self.ghost_list:
          if(g.isBusting()):
            g.init_tab_chemin((tupl[0]//BLOCK_SIZE, tupl[1]//BLOCK_SIZE), map_modal, teleport)
          else:
            g_equipier.append(g)
      nb_equipier = len(g_equipier)
      if (nb_equipier > len(dst_inter_to_pac)):
        dst_inter_to_pac= dst_inter_to_pac[:nb_equipier]
      tu = self.get_extremite_chemin((tupl[0]//BLOCK_SIZE, tupl[1]//BLOCK_SIZE), [], map_modal)
      final_t = []
      for xj in tu:
        if(isinstance(xj, list)):
          final_t.append(xj[0])
        else:
          final_t.append(xj)
      b = BFS_cheby(None, None)
      teamate_a_charge = []
      all_chemin = []
      distance_from_paq = [(b.Distance(tupl[0], tupl[1], f[0], f[1]), f) for f in final_t]
      #on classe les intersections du chemins courant de pacman dans l'ordre de priorité, autrement dit, la fin du chemin la plus proche de pacman est la plus importante et ainsi de suite
      distance_from_paq.sort(key=lambda tup: tup[0])

      # Maintenant qu'on a toutes les intersections de la map et toutes les intersections du chemin de pacman on met en priorité celles du chemin



      """

      O
      |---------
      | *
      |
      |
      
      Car même si on a trier toutes les intersections par ordre de distance avec Pacman on a pas vérifier la longeur du chemin pour aller de ce point 
      jusqua pacman et si il existait des murs 
      d'ou le fait de mettre en priorité les intersections du chemin courant de Pacman
      """


      teamate_used = {}
      #pour chaque distance on tri les fantomes dans l'ordre du plus proches          
      for dst in distance_from_paq:
        dst2_tab = [(b.Distance(g2.getX(), g2.getY(), dst[1][0], dst[1][1]), g2) for g2 in g_equipier]
        dst2_tab.sort(key=lambda tup: tup[0]) 
        teamate_used[dst[1]] = dst2_tab

      for k, val in teamate_used.items():
        
        for v in val:
          
          if(v[1].getId() not in teamate_a_charge):
            teamate_a_charge.append(v[1].getId())
            all_chemin.append((v[1], k))
            break
      print("all chemin apres intersections chemin")
      print(all_chemin)




      for dst in dst_inter_to_pac:
        dst_tab = [(b.Distance(g2.getX(), g2.getY(), dst[1][0], dst[1][1]), g2) for g2 in g_equipier if g2.getId() not in teamate_a_charge]
        dst_tab.sort(key=lambda tup: tup[0]) 
        teamate_used[dst[1]] = dst_tab
      
      
      
      for k, val in teamate_used.items():
        print(k)
        print("=======")
        print(val)
        for v in val:
          print("+++++++++++++")
          print(v[1])
          if(v[1].getId() not in teamate_a_charge):
            teamate_a_charge.append(v[1].getId())
            all_chemin.append((v[1], k))
            break
      print("all chemin apres tout")
      print(all_chemin)
      for ghst, goal_case in all_chemin:
        ghst.init_tab_chemin(goal_case,map_modal, teleport)
    



    
   



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
      'O': 'images/marker2.png',
    }
    self.w = 0
    self.h = 0
    self.food_left = 0
    self.map_modal = dict()
    self.food_map = []
    self.pacman = None
    self.groupGhost = None
    self.score = 0
    self.test_path_bfs = []
    self.tp = []

  def load_level(self, number):
    file = "level-%s.txt" % number
    self.food_left = 0

    with open(file) as f:
      map_tmp = [[b for b in line.strip()] for line in f]
      self.h = len(map_tmp)
      self.map_modal = {(j, i):{"signe":b, "neighboor":[Node((j-1, i), None), Node((j, i-1), None), Node((j+1, i), None), Node((j, i+1), None)]} for i, l in enumerate(map_tmp)  for j, b in enumerate(l)}
      
      self.food_map = [(j, i) for i, l in enumerate(map_tmp)  for j, b in enumerate(l) if b == "."  ]
      self.food_left = len(self.food_map)

      self.groupGhost= EnsembleOnEstPlusFortV3(self.food_map.copy())
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
        if(k[0] == 0 and v["signe"] == "."):
          self.tp += [k]
          self.tp += [((len(self.map_modal)//self.h)-1 , k[1])]
        if(k[1] ==0 and v["signe"] == "."):
          self.tp += [k]
          self.tp += [(k[0], self.h-1)]
         

        if(v["signe"] == "p"):
        
          self.pacman = IAPacmanHungry(k[0], k[1])
        
        else:
          if(v["signe"] == "g" or v["signe"] == "G" or v["signe"] == "h" or v["signe"] == "H"):
            gosth = IAPhantomBFS3(k[0], k[1], self.char_to_image[v["signe"]], self.food_map)
            self.groupGhost.addToList(gosth)
      for g in self.groupGhost:
        print(g)
          



  
      
  def from_pacman_to_ghost(pos):

    x, y = pos
    i = max(0, int(x / 30))
    j = max(0, int(y / 30))

    return i, j       

  def get_collision(self):
    pcx = self.pacman.getX()
    pcy = self.pacman.getY()
    pac_rect = pygame.Rect(pcx, pcy, BLOCK_SIZE, BLOCK_SIZE)
    for g in self.groupGhost:
      
      gx = g.getX()
      gy = g.getY()
      rect_g = pygame.Rect(gx, gy, BLOCK_SIZE, BLOCK_SIZE)
      if((pac_rect).colliderect(rect_g)):
        return True
    #     """Retourne la liste des rectangles autour de la position (i_start, j_start).
 
    # Vu que le personnage est dans le carré (i_start, j_start), il ne peut
    # entrer en collision qu'avec des blocks dans sa case, la case en-dessous,
    # la case à droite ou celle en bas et à droite. On ne prend en compte que
    # les cases du niveau avec une valeur de 1.
    # """
    
      
    return False  


  def update(self):
    Bf = BFS_cheby(self.map_modal, self.tp)
    
    res =self.pacman.update2(self.map_modal, self.h, self.food_map, self.score)
    self.score = res[0]
    print(self.score)
    if(isinstance(self.groupGhost, EnsembleOnEstPlusFortV3)):

      self.groupGhost.update(self.map_modal, self.h, (self.pacman.getX(), self.pacman.getY()), Bf, self.food_map)
    else:
      self.groupGhost.update(self.map_modal, self.h, (self.pacman.getX(), self.pacman.getY()), Bf)
    
    if(self.get_collision()):
      return False
    else:
      return True

    # is_collision = self.get_collision()
    # if(is_collision):
    #   print("perdu")
    #   exit(1)



  def draw(self, surface):
  
    for k, v in self.map_modal.items():
      if(v["signe"] == "="):
        image = self.char_to_image.get(v["signe"], None)
        if image:
          surface.blit(pygame.image.load(self.char_to_image[v["signe"]]), (k[0]*30, k[1]*30))
    
    for food in self.food_map:
      surface.blit(pygame.image.load(self.char_to_image["."]), (food[0]*30, food[1]*30))
    for pa in self.test_path_bfs:
      
      surface.blit(pygame.image.load(self.char_to_image["M"]), (pa[0]*30, pa[1]*30))
   
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
        self.id = time.time()
        print(self.id)
        self.image = pygame.image.load(signe)
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        self.dx = 0
        self.dy = 0
        self.x = x*BLOCK_SIZE
        self.y = y*BLOCK_SIZE
        self.signe = signe
        self.rot = 0
        self.busted = False
        self.tab_chemin = []
        self.last_dir = None

      
          # elif(self.dx > 0): #go on right
          # elif(self.dy >  0): #go down
          # else: #go top

        # else:
       
          # g.dy = random.choice([-GHOST_SPEED, GHOST_SPEED])
        
      def getId(self):
        return self.id

      def getX(self):
        return self.x

      def getY(self):
        return self.y

      def isBusting(self):
        return self.busted

      def isRandom(self):
        if(len(self.tab_chemin) == 0):
          return True
        else:
          return False

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
        tp = False
        if (self.x >= (len(tab_mod) / heigt) * 30 - 30):
            self.x = 5
        elif (self.x <= 0):
            self.x = ((len(tab_mod) / heigt) * BLOCK_SIZE) - BLOCK_SIZE - 5

        elif (self.y >= (heigt) * 30 - 30):
            self.y = 5

        elif (self.y <= 0):
            self.y = (heigt * BLOCK_SIZE) - BLOCK_SIZE - 5
        else:

          nh = tab_mod[(tmpx, tmpy)]["neighboor"]
          if(moduloX == 0 and moduloY == 0):

            
          
            
            nh = tab_mod[(tmpx, tmpy)]["neighboor"]
            possible_pos = [ n for n in nh if(tab_mod[n.position]["signe"] != "=")]
            if(len(possible_pos) == 2): # possible ligne  droite
              n1 = possible_pos[0].position
              n2 = possible_pos[1].position
              if( n1[0] == n2[0] or n1[1] == n2[1] ): # on rentre dans le use case d'un ligne droite horizontal ou vertical
                if(self.dx == 0 and self.dy == 0): # si le fantome est arreter (AU DÉ)
                  
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
          if(self.dx == -5):
            self.last_dir = "LEFT"
          elif(self.dx == 5):
            self.last_dir = "RIGHT"
          elif(self.dy == 5):
            self.last_dir = "BOT"
          else:
            self.last_dir = "TOP"
          
          
          self.x += self.dx
          self.y += self.dy
          self.rect.move_ip(self.x, self.y)


class IAPhantomBFS(IAPhantomNaive):
  
  def check_line(self, posx_line, posy_line, vecteur,pac_pos,tab_mod, h_map):
    while(True):
      if(posx_line == pac_pos[0] and posy_line== pac_pos[1]):
        return True
      if(posx_line < 0 or posy_line < 0):
        return False
      if(posy_line >= h_map):
        return False
      if(posx_line >= len(tab_mod)//h_map):
        return False  
      if(tab_mod[(posx_line + vecteur[0], posy_line + vecteur[1])]["signe"] == "="):
        return False
    
        
        
      posx_line += vecteur[0]
      posy_line += vecteur[1]

    return False

  def init_tab_chemin(self, goal_case, map_case, bfobj):
        
        self.tab_chemin = bfobj.best_first_search((self.x//BLOCK_SIZE, self.y // BLOCK_SIZE), goal_case)
        
        if(self.x % BLOCK_SIZE != 0 or self.y % BLOCK_SIZE != 0):
          self.tab_chemin = [(self.x//BLOCK_SIZE, self.y // BLOCK_SIZE)] + self.tab_chemin
     
        if(self.tab_chemin == None):
          self.tab_chemin = []

  def continue_chemin(self):
    if(len(self.tab_chemin) != 0):
      mycaseX = self.x // BLOCK_SIZE
      mycaseY = self.y // BLOCK_SIZE
      obj = self.tab_chemin[0]
      if(self.x % BLOCK_SIZE == 0 and self.y % BLOCK_SIZE == 0):
        
        if(mycaseX  == obj[0] and mycaseY  == obj[1]): #on est sur la case désiré, on supprime du tableau et on relance
          self.tab_chemin.pop(0)
         
          return self.continue_chemin()
        else:
          if(self.x  < obj[0]*BLOCK_SIZE):
            self.dx = 5
            self.dy = 0
          elif(self.x > obj[0] * BLOCK_SIZE):
            self.dx = -5
            self.dy = 0
          elif(self.y < obj[1]*BLOCK_SIZE):
            self.dx = 0
            self.dy = 5
          else:
            self.dx = 0
            self.dy = -5
      

      self.x = self.x + self.dx
      self.y = self.y + self.dy   
        




  def update(self, tab_mod, heigt, pacman_pos, Bf):
    
      
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
      self.busted = True
      self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)

      # self.tab_chemin = Bf.best_first_search((mycaseX, mycaseY), (pac_pos_x, pac_pos_y))
    
     
      # print(self.tab_chemin)
      # print((mycaseX, mycaseY), " ", (pac_pos_x, pac_pos_y))
      if(len(self.tab_chemin) != 0):
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
        elif(self.x <= 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y > (heigt*30)-30  and self.dy > 0):
          self.y = 0
          if(self.tab_chemin[0][1] == heigt-1):
              self.tab_chemin.pop(0)
          
      
        else:
          if(self.y == 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    else:
      self.busted = False
      if(len(self.tab_chemin) == 0):
        return IAPhantomNaive.update(self, tab_mod, heigt, pacman_pos)
      else:
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
             
        elif(self.x == 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
          
        elif(self.y >= heigt*30-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
          
      
        else:
          if(self.y <= 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    
    self.rect.move_ip(self.x, self.y)

    #je continue mon chemin

class IAPhantom(IAPhantomBFS):
  def update(self, tab_mod, heigt, bfobj,fm):
        choices = [5, -5]
    
        

        tmpx = self.x / BLOCK_SIZE
        tmpy = self.y / BLOCK_SIZE

        moduloX = self.x % BLOCK_SIZE
        moduloY = self.y % BLOCK_SIZE
        tp = False
        if (self.x >= (len(tab_mod) / heigt) * 30 - 30):
            self.x = 5
        elif (self.x <= 0):
            self.x = ((len(tab_mod) / heigt) * BLOCK_SIZE) - BLOCK_SIZE - 5

        elif (self.y >= (heigt) * 30 - 30):
            self.y = 5

        elif (self.y <= 0):
            self.y = (heigt * BLOCK_SIZE) - BLOCK_SIZE - 5
        else:
            nourriture = random.choices(fm)[0]
            
            self.init_tab_chemin(nourriture, tab_mod, bfobj)
            #retourne une position de nourritures qui n'as pas était mangé

class IAPhantomBFS2(IAPhantomBFS):




  def update(self, tab_mod, heigt, pacman_pos, Bf):
    
      
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
      self.busted = True
      if(len(self.tab_chemin) != 0):
        if(self.tab_chemin[-1] != (pac_pos_x, pac_pos_y)):
          self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)
      else:
          self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)

      # self.tab_chemin = Bf.best_first_search((mycaseX, mycaseY), (pac_pos_x, pac_pos_y))
    
     
      # print(self.tab_chemin)
      # print((mycaseX, mycaseY), " ", (pac_pos_x, pac_pos_y))
      if(len(self.tab_chemin) != 0):
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
             
        elif(self.x <= 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y > (heigt*30)-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
      
        else:
          if(self.y == 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    else:
      self.busted = False
      if(len(self.tab_chemin) == 0):
        return IAPhantomNaive.update(self, tab_mod, heigt, pacman_pos)
      else:
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
        elif(self.x == 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y >= heigt*30-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
      
        else:
          if(self.y <= 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    self.rect.move_ip(self.x, self.y)


class IAPhantomBFS3(IAPhantomBFS2):

  def __init__(self, x, y, signe, food_in_map):
    super().__init__( x, y, signe)
    self.food_in_map = food_in_map


  def update(self, tab_mod, heigt, pacman_pos, Bf):
    
      
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
      self.busted = True
      if(len(self.tab_chemin) != 0):
        if(self.tab_chemin[-1] != (pac_pos_x, pac_pos_y)):
          self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)
      else:
          self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)

      # self.tab_chemin = Bf.best_first_search((mycaseX, mycaseY), (pac_pos_x, pac_pos_y))
    
     
      # print(self.tab_chemin)
      # print((mycaseX, mycaseY), " ", (pac_pos_x, pac_pos_y))
      if(len(self.tab_chemin) != 0):
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
             
        elif(self.x <= 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y > (heigt*30)-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
          
      
        else:
          if(self.y == 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    else:
      self.busted = False
      if(len(self.tab_chemin) == 0):
        return IAPhantom.update(self, tab_mod, heigt, Bf, self.food_in_map)
      else:
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
             
        elif(self.x == 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y >= heigt*30-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
      
        else:
          if(self.y <= 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    self.rect.move_ip(self.x, self.y)

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
        self.register_parcour = []
        

    

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
        has_eat = False
        if (ix, iy) in map_food:
            map_food.remove((ix, iy))
            print("hummmmm!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #self.food_left -= 1
            score += 1
            has_eat = True
            # print("scoreeat = ", score)
        #pacman.powerup = POWER_UP_START
        #set_banner("Power Up!", 5)
        #for g in ghosts: new_ghost_direction(g)
        #pacman.score += 5
        if(has_eat == True):
          return (score, tuple((ix, iy)))
        else:
          return (score, None)

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


class IAPacmanHungry(Pacman):
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
          self.y = 10
          
        elif(self.y <= 0):
          self.y = heigt*30-30-10
         
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
        print(score)

        # print(self.dx, "  ", self.dy)
        self.rect.move_ip(self.x + self.dx, self.y + self.dy)
        # print("score = ", score)

        return score
        


class IANaive(Pacman):

  def update2(self, tab_mod, heigt, food_map, score):
        
        choices = [5, -5]
      

        tmpx = self.x // BLOCK_SIZE
        tmpy = self.y // BLOCK_SIZE

        moduloX = self.x % BLOCK_SIZE
        moduloY = self.y % BLOCK_SIZE

        if(self.x >= (len(tab_mod) / heigt) * 30 - 30):
          self.x = 5
         
        elif(self.x <= 0):
          self.x = ((len(tab_mod)/ heigt) * BLOCK_SIZE)  - BLOCK_SIZE - 5
          
        elif(self.y >= heigt*30-30):
          self.y = 10
          
        elif(self.y <= 0):
          self.y = heigt*30-30-10
         
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
        print("bbbb")
        print(score)
        # print(self.dx, "  ", self.dy)
        self.x += self.dx
        self.y += self.dy
        self.rect.move_ip(self.x, self.y)
        # print("score = ", score)

        return score
        
         
# P1 = Pacman()
# E1 = Ghost()
M = Map()
M.load_level(1)


screen_rect = DISPLAYSURF.get_rect()
window_rect = pygame.Rect(0, 0, 400, 250)
window_rect.center = screen_rect.center
font = pygame.font.SysFont('Arial', 24)
message = 'Game Over'
box = MessageBox(window_rect, font, message)
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

     
    DISPLAYSURF.fill(BLACK)
    su = M.update()
    M.draw(DISPLAYSURF)

    if(su == False):
      DISPLAYSURF.fill(BLACK)
      while True:
        
        box.update()
        DISPLAYSURF.fill(BLACK)
        if not box.should_exit:
          box.draw(DISPLAYSURF)

        # if box.should_exit == True:
        #    pygame.quit()  

        pygame.display.update()
    pygame.display.update()
    FramePerSec.tick(FPS)


pygame.quit()