import pygame as pg 
from setting import *


class ObjectRenderer:
    def __init__(self,game):
        self.game=game
        self.screen= game.screen
        self.wall_texture= self.load_wall_texture()
        self.sky_image = self.get_texture('resources/textures/skybox.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen =self.get_texture('resources/textures/blood.png', RES)
        self.game_over_image = self.get_texture('resources/textures/over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        
    def player_damage(self):
        self.screen.blit(self.blood_screen,(0,0)) 
    #will check if i have time
   # def draw_player_health(self):
      #  health = int(self.game.player.health)
      #  pain_screens = {
       #     4: self.get_texture('resources/textures/pain_screen/1.png', RES),
       #     3: self.get_texture('resources/textures/pain_screen/2.png', RES),
       #     2: self.get_texture('resources/textures/pain_screen/3.png', RES),
      #      1: self.get_texture('resources/textures/pain_screen/4.png', RES),
     #   }
     #   if health in pain_screens:
      #      pain_screen = pain_screens[health]
      #      self.screen.blit(pain_screen, (0, 0))   
        
    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))
        
    def win(self):
        self.screen.blit(self.win_image, (0, 0))
    
    def draw (self):
        self.draw_background()
        self.render_game_object()
               
    def render_game_object(self):
        list_objects = sorted(self.game.raycasting.objects_to_render,key=lambda t: t[0],reverse=True )
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)
            
    def draw_background(self):
       self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
       self.screen.blit(self.sky_image, (-self.sky_offset, 0))
       self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
       # floor
       pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))
            
    @staticmethod
    def get_texture (path, res= (TEXTURE_SIZE,TEXTURE_SIZE)):
        texture= pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture,res)
    
    def load_wall_texture (self):
        return{
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
        }
        