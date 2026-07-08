import pygame
from support import import_folder

class Enemy():
    def __init__(self, health, damage,speed, level,screen):
        self.health = health
        self.damage = damage
        self.level = level
        self.speed = speed

        self.screen = screen

        self.enemy_x = 200
        self.enemy_y = 300
        self.status = ''
        self.frame_index = 0
        self.animation_speed = 0.15


        original_image = pygame.image.load("Sprites/enemy_sprite/east_idle/east.png").convert_alpha()
        
        
        self.image = pygame.transform.scale(original_image, (500,500))
        self.pos = pygame.math.Vector2(self.enemy_x,self.enemy_y)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate(-400,-350)

        self.attack_radius = 60
        self.notice_radius = 320
 

    # --- START OF ASSETS --- #
    
        self.blue_blast = pygame.mixer.Sound("Sound Effects/blue_blast.mp3")
        self.purple_blast = pygame.mixer.Sound("Sound Effects/purple_blast.mp3")

    # --- END OF ASSETS --- #

        self.import_enemy_assets()

    def import_enemy_assets(self):
        enemy_path = "Sprites/enemy_sprite/"

        self.animations = {'east_idle': [], 'east_walk':[], 'east_attack':[], 'west_idle': [], 'west_walk': [], 'west_attack' : []}

        for animation in self.animations.keys():
            full_path = enemy_path + animation
            self.animations[animation] = import_folder(full_path)


    def get_player_distance_directions(self,player):
        enemy_vector= pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector-enemy_vector).magnitude()
        
        if distance > 0:
            direction =(player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2((0,0))

        if direction.x > 0:
            horizontal_pos = 'east'
        elif direction.x < 0:
            horizontal_pos = 'west'
        else:
            horizontal_pos = 'east' if 'east' in self.status else 'west'

        return (distance, direction, horizontal_pos)

    def get_status(self,player):
        distance,direction,horizontal_pos = self.get_player_distance_directions(player)
        #if distance <= self.attack_radius and self.can_attack :
            #if self.status !='attack':
             #   self.frame_index=0
            #self.status = 'attack'
        
        if distance <= self.notice_radius:
            state = '_walk'
            # Instead of separate get_actions, handle the movement vector directly here!
            self.direction = direction 
        else:
            state = '_idle'
            self.direction = pygame.math.Vector2(0, 0)

        # 2. Combine the pieces cleanly from scratch
        # This gives you exactly 'east_walk', 'west_idle', etc.
        new_status = horizontal_pos + state
    
        if new_status != self.status:
            self.frame_index = 0

        self.status = new_status

    def get_actions(self,player):
        if 'walk' in self.status:
            self.direction = self.get_player_distance_directions(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()        

        self.pos.x +=self.direction.x * speed
        #self.pos.x += self.speed
        self.rect.topleft = self.pos

        self.hitbox.center = self.rect.center


    def animate(self):
        animations = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animations):
            self.frame_index = 0

        self.image = animations[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (200,200))
        self.rect = self.image.get_rect(center = self.hitbox.center)


    def update(self):
        self.screen.blit(self.image, (self.rect.x, 300))
        self.move(self.speed)
        self.animate()
        pygame.draw.rect(self.screen,"green", self.rect,1)
        pygame.draw.rect(self.screen,"blue", self.hitbox,1)
    def enemy_update(self,player):
        self.get_status(player)
        self.get_actions(player)