from sprite_object import *


class AXE(AnimatedSprite):
    
    def __init__(self, game, path='resources/sprites/weapon/axe/0.png', scale=1.4, animation_time=80):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
            for img in self.images])
        self.axe_pos = (((HALF_WIDTH - self.images[0].get_width()+(2*WIDTH//3) // 2)), HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 1
        
    def animate_shot(self):
        if self.reloading:
            self.game.player.axe = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
                    
    def draw(self):
        self.game.screen.blit(self.images[0], self.axe_pos)
        
    def update(self):
        self.check_animation_time()
        self.animate_shot()