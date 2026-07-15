import pygame , time
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, health, speed, attack_dmg, level, screen):
    
    # --- START OF STATS --- #  
        self.health = health
        self.speed = speed
        self.attack_dmg = attack_dmg
        self.level = level
        
    # --- END OF STATS --- #
        global health_being_updated
        self.health_being_updated = self.health
       
    # --- ASSETS --- # 
        
        original_image = pygame.image.load("Sprites/player_sprite/east_idle/east.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (150,150))

        self.when_not_running_image = pygame.transform.scale(pygame.image.load("UI related/BACKGROUNDS/when_not_running.png").convert_alpha(), (100,100))
        self.when_running_image = pygame.transform.scale(pygame.image.load("UI related/BACKGROUNDS/when_running.png").convert_alpha(), (100,100))

        level_image = pygame.image.load("UI related/BACKGROUNDS/level_template.png")
        self.level_image = pygame.transform.scale(level_image, (385,75))

        self.player_death = pygame.mixer.Sound("Sound Effects/player_death.mp3")
        self.player_heal = pygame.mixer.Sound("Sound Effects/player_heal.wav")

        self.blue_blast = pygame.mixer.Sound("Sound Effects/blue_blast.mp3")
        #self.blue_blast_button_not_selected = pygame.image.load("UI related/BUTTONS/blue_blast_button_not_selected.png").convert_alpha() ---> Needed for later
        #self.blue_blast_button_selected = pygame.image.load("UI related/BUTTONS/blue_blast_button_selected.png").convert_alpha() ---> Needed for later
        
        self.purple_blast = pygame.mixer.Sound("Sound Effects/purple_blast.mp3")

        self.level_font = pygame.font.Font("UI related/FONTS/rainyhearts.ttf",54)
        self.level_box_rect = None

    # --- END OF ASSETS --- #


    # --- DATA FOR SCREEN --- #
        self.screen = screen
        self.MAX_WIDTH = self.screen.get_width() # (x cordinate)
        self.MAX_HEIGHT = self.screen.get_height() # (y cordinate) 
    # --- END OF DATA --- #


    # --- PLAYER MOVEMENT --- #
        self.direction = pygame.math.Vector2() # The arrow that tells system where player wants to go

        self.player_x = 750
        self.player_y = 350

        self.pos = pygame.math.Vector2(self.player_x,self.player_y) #System will exactly remember where player actually is

        self.rect = self.image.get_rect(topleft = self.pos) #The picture frame of the player on the screen

        self.hitbox = self.rect.inflate(-40,-12) #The physics part of the player where collisions will be detected
    
        self.is_jumping = False
        self.jump_height = 40 #---> The reason for changing this value is to ensure that when the player jumps, they don't collide with the enemy and take damage.
        self.jump_speed = self.jump_height
        self.gravity = 3

        self.press_r = False
        self.is_sprinting = False
        self.sprint_speed = self.speed * 2

        
        self.is_player_attacking = False
 
    # --- END OF PLAYER MOVEMENT --- #

    # --- PLAYER ANIMATION --- #
        self.status = 'east'
        self.frame_index = 0
        self.animation_speed = 0.15
    # --- END OF PLAYER ANIMATION --- #

        self.clock = pygame.time.Clock()

        self.import_player_assets()


    def import_player_assets(self):
        character_path = "Sprites/player_sprite/"
        self.animations = {'east':[], 'west': [], 
                           'east_idle': [], 'west_idle':[], 
                           'east_death': [], 'west_death': [],
                           'east_attack':[], 'west_attack':[]}

        self.attack_animations = {'blue_blast': [], 'purple_blast': []}

        for animation in self.animations.keys():
            full_path_1 = character_path + animation
            self.animations[animation] = import_folder(full_path_1)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'east'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'west'
        else:
            self.direction.x = 0

        if pygame.KEYDOWN:
            if keys[pygame.K_SPACE]:
                self.is_jumping = True
    
            if keys[pygame.K_r] and self.press_r == False:
                
                if self.is_sprinting == False:
                    self.speed = self.sprint_speed
                    self.animation_speed = 0.25
            
                    self.is_sprinting = True
        
            else:
                self.speed = self.sprint_speed /2
                self.animation_speed = 0.15
                self.is_sprinting = False
            
            if keys[pygame.K_q]: #When the Q button is pressed, the player will attack, as for the change in self.status, that is to be seen in get_status() function
                if not self.is_player_attacking:
                    self.is_player_attacking = True
    
        if self.is_jumping == True:
            self.pos.y -= self.jump_speed
            self.jump_speed -= self.gravity

            if self.jump_speed < -self.jump_height and self.pos.y > self.player_y:
                self.is_jumping = False
                self.jump_speed = self.jump_height
                self.pos.y = self.player_y      

       
    def get_status(self):
    
        if '_' in self.status:
            self.status = self.status.split('_')[0]
        else:
            self.status = self.status


        action = ''

        if self.health_being_updated <= 0:
            action = 'death'
        else:

            if self.direction.x == 0 and self.direction.y == 0:
                if self.is_player_attacking == False:
                    action = '_idle'
                elif self.is_player_attacking == True:
                    action  = action.replace('_attack','_idle')
            
            if self.is_player_attacking == True: # ----> The animation for attack 1) will be played only when the player is moving 2) The code for the animation is in the animate() function
                if 'idle' in action:
                    action = action.replace('_idle','_attack')
                else:
                    action = '_attack'
        
        self.status = self.status + action

        #print(self.status)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0


        if self.is_player_attacking == True:  # ----> The reason as to why attack has its own animation is to ensure that the animation is not continuous, rather only one cycle is of the attack animation is played, and then the player goes back to idle or walk animation
            if self.frame_index >= len(animation) - 1:
                self.is_player_attacking = False
                self.frame_index = 0


        self.image = pygame.transform.scale((animation[int(self.frame_index)]),(150,150))
        self.screen.blit(self.image,self.rect)
        
        self.screen.blit(self.level_image,((self.MAX_WIDTH/2.7),(self.MAX_HEIGHT/9.9)))
        self.level_box_rect = self.level_image.get_rect(topleft = ((self.MAX_WIDTH/2.7),(self.MAX_HEIGHT/9.9)))


        level_text = self.level_font.render(f"LEVEL {self.level}", False, "white")
        self.screen.blit(level_text, ((self.MAX_WIDTH/2.23),(self.MAX_HEIGHT/8.5)))

            #DEBUG: Draw the Hitbox in Red and the Rect in Blue
      
        if self.is_sprinting == True:
            #pygame.draw.rect(self.screen, "green", self.rect, 2)   # The full sprite size
            self.screen.blit(self.when_running_image, (900,594))

        else:
            self.screen.blit(self.when_not_running_image, (900,594))
            pygame.draw.rect(self.screen, "blue", self.rect, 2) 
        
        pygame.draw.rect(self.screen, "red", self.hitbox, 2)  # The actual collision area
        
        pygame.draw.rect(self.screen, "black", self.level_box_rect, 2)
        
        #DEALING WITH PLAYER HEALTH
        
        self.health_bar = (self.health_being_updated / 95) * 100
        #print(f"Before drawing , the value of player health is {self.health_being_updated}")
        self.health_bar_empty = pygame.draw.rect(self.screen, "red", (800,600,30,95))
        self.health_bar_full = pygame.draw.rect(self.screen, "green", (800,600,30,self.health_bar))
    
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #Stops trigonometry from affecting diagonal movement

        self.pos += self.direction * speed # Updates the actual positon of player on the screen

    def staying_in_screen(self):
        
        # Checking whether if player is crossing the screen horizontally #

        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > self.MAX_WIDTH - self.rect.width:
            self.pos.x = self.MAX_WIDTH - self.rect.width

       
       # Checking whether if player is crossing the screen vertically #
        
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > self.MAX_HEIGHT - self.rect.height:
            self.pos.y = self.MAX_HEIGHT - self.rect.height

        self.rect.topleft = (self.pos.x, self.pos.y) #The picture frame should move to where the player actually is on screen
        self.hitbox.center = self.rect.center # Changing the physics part of player to the middle of the player picture frame


    def no_collision_with_level_box(self):
        
        if self.hitbox.colliderect(self.level_box_rect):
            print("COLLISION OCCURING!!")

    def attacking_animation_and_sound_effects(self):
        # The intent with this subroutine is to handle which attack the player selects, 
        # playing its corresponding animation and also its sound effect

        pass


    def update(self):
        self.clock.tick(60)
        self.input()
        self.get_status()
        self.move(self.speed)        
        self.staying_in_screen()
        self.animate()
        self.no_collision_with_level_box()        
