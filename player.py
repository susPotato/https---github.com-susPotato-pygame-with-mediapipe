from setting import *
import pygame 
import math
from handtracking import *
from queue import Queue
import threading
import pygame as pg
from sound import *
from axe import *
from punch import *


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.reset_game=True
        self.axe=False
        self.set_x=0
        self.set_y=0
        self.hand_z_prev=0
        self.use_count=50
        self.m1,self.m2,self.m3,self.m4=0,0,0,0
        self.mp = MediaPipe()   
        face_mesh_thread = threading.Thread(target=self.mp.face_mesh_tracking)
        hand_thread = threading.Thread(target=self.mp.hand_tracking)
        face_mesh_thread.start()
        hand_thread.start()
        
        self.health=PLAYER_MAX_HEALTH
        self.rel = 0
        self.diag_move_corr = 1 / math.sqrt(2)
         
    def get_damage(self,damage):
        self.health -=damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.game_over()
                   
    def quick_fix_the_hand(self):
        if not self.mp.hand_queue.empty():
            self.m1,self.m2,self.m3,self.m4=  self.mp.hand_queue.get()
    
    def axe_event(self):
        if self.m1<self.m2 and self.m3<self.m4:
            if not self.axe and not self.game.axe.reloading and not self.use_count==0:
                print (self.x,self.y)
                self.axe = True
                self.game.axe.reloading = True
                self.use_count-= 1
                self.m1,self.m2,self.m3,self.m4=0,0,0,0
            #    print(self.use_count)
            #else :
             #   self.game.sound.no_armo.play()
           #debug
              #  print("axe")
    
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        self.player_speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = self.player_speed * sin_a
        speed_cos = self.player_speed * cos_a
        keys = pygame.key.get_pressed()
        num_key_pressed = -1
        if keys[pygame.K_w]:   
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pygame.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos
        # diag move correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr
        self.check_wall_collision(dx, dy)
        
        self.angle %= math.tau
             
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        self.scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * self.scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.scale)):
            self.y += dy
            
    def draw(self):
        pygame.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                   (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15) 
    #debug using mouse        
    def mouse_control(self):
        if not self.mp.nose_queue.empty():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.set_x+=0.1
            if keys[pygame.K_LEFT]:
                self.set_x-=0.1
         #   if keys[pygame.K_UP]:
                self.set_y+=0.1
          #  if keys[pygame.K_DOWN]:
                self.set_y-=0.1
            
            mx,my = self.mp.nose_queue.get()
            print (mx)
            mx = int((mx+self.set_x) * WIDTH)
       #     my = int((my+self.set_y )* HEIGHT)
    #    mc = math.sqrt(mx ** 2 + my ** 2)
            if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
                mx = HALF_WIDTH
            self.rel = mx - HALF_WIDTH
            self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
        
  #  def mouse_control(self):
  #     mx, my = pygame.mouse.get_pos()
  #     if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
  #         pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
  #     self.rel = pygame.mouse.get_rel()[0]
  #     self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
  #     self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
  #     #debug
    #   print (mx)
    #   print (my)
    def game_over(self):
        if self.health < 1:
           self.game.object_renderer.game_over()
           pg.display.flip()
           self.reset_game=False          
               
    def win(self):
        if int (self.x)>=22 and int (self.y)>=17 :
            self.game.object_renderer.win()
            pg.display.flip()
            self.reset_game=False
                   
    def update(self):
        #self.draw()
        self.movement()
        self.mouse_control()
        self.quick_fix_the_hand()
        self.win()
              
    @property
    def pos(self):
        return self.x, self.y
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    