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
        self.health_being_updated = 50 # --> This variable changes based on the collisions it experiences against the enemy, it is less than 100 to see a change in health bar
       
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
        self.blue_blast_button_not_selected = pygame.transform.scale(pygame.image.load("UI related/BUTTONS/blue_blast_button_not_selected.png").convert_alpha(), (100,100))
        self.blue_blast_button_selected = pygame.transform.scale(pygame.image.load("UI related/BUTTONS/blue_blast_button_selected.png").convert_alpha(), (100,100))
        
        self.purple_blast = pygame.mixer.Sound("Sound Effects/purple_blast.mp3")
        self.purple_blast_button_not_selected = pygame.transform.scale(pygame.image.load("UI related/BUTTONS/purple_blast_button_not_selected.png").convert_alpha(), (100,100))
        self.purple_blast_button_selected = pygame.transform.scale(pygame.image.load("UI related/BUTTONS/purple_blast_button_selected.png").convert_alpha(), (100,100))


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

        
        # -- Attack related variables -- #
        self.is_player_attacking = False
        self.is_blue_blast_selected = False #--- > Will Later help us to see which attack the player selects, and then playing its respective animation and sound effect.
        self.is_purple_blast_selected = False 
        self.is_blast_released = False
        self.blast_cooldown = 1500 # (1.5 seconds)
        self.last_blast_time = 0

        self.attack_frame_index = 0
        self.attack_animation_speed = 0.10
        self.blast_velocity = 10 # --> The speed at which the attack animation moves across the screen, this is to be used in the future when we implement the attack animations to move across the screen
        self.blast_x = self.player_x
        self.blast_y = self.player_y
        self.blast_facing_right = True
        self.blast_direction = None # --> The direction in which the attack animation moves across the screen, this is to be used in the future when we implement the attack animations to move across the screen



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

        for attack_animation in self.attack_animations.keys():
            full_path_2 = character_path + attack_animation
            self.attack_animations[attack_animation] = import_folder(full_path_2)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'east'
            self.blast_facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'west'
            self.blast_facing_right = False
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
      
        ## -- Instead of using fixed coordinates making it hard for the game to player on other laptops, we will be making calculations using the width of the screen -- ##
        
        ui_start_x = self.MAX_WIDTH - 300

        if self.is_sprinting == True:
            #pygame.draw.rect(self.screen, "green", self.rect, 2)   # The full sprite size
            self.screen.blit(self.when_running_image, (ui_start_x,594))

        else:
            self.screen.blit(self.when_not_running_image, (ui_start_x,594))
            pygame.draw.rect(self.screen, "blue", self.rect, 2) 
        

        if self.is_blue_blast_selected == False: # ---> Once a player selects an attack, the button for that attack will darken slightly, and the button for the other attack will remain bright, indicating that it is not selected.
            self.screen.blit(self.blue_blast_button_not_selected, (ui_start_x + 100,594))
        else:
            self.screen.blit(self.blue_blast_button_selected, (ui_start_x + 100,594))

        if self.is_purple_blast_selected == False:
            self.screen.blit(self.purple_blast_button_not_selected, (ui_start_x + 200,594))
        else:
            self.screen.blit(self.purple_blast_button_selected, (ui_start_x + 200,594))
       
    
        pygame.draw.rect(self.screen, "red", self.hitbox, 2)  # The actual collision area
        
        pygame.draw.rect(self.screen, "black", self.level_box_rect, 2)
            
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

    def player_health(self): # --> Giving a proper health bar to the player, which changes based on how damaged the player gets.

        bar_width = 200 # --> Defining the elements for the health bar
        bar_height = 20
        margin = 20

        bar_x = self.MAX_WIDTH - bar_width - margin # --> For the bar to appear on the top right part of the screen
        bar_y = margin
      

        health_ratio = self.health_being_updated / self.health # --> The ratio of the health bar to the actual health of the player
        current_bar_width = bar_width * health_ratio # --> The current width of the health bar will be determined by the ratio of the health bar to the actual health of the player

        # 1) Drawing the red background of the health bar

        back_health_bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (20, 30, 20), back_health_bar_rect) #---> Rotting Earth Colour

        #2) Drawing the green foreground of the health bar

        if current_bar_width > 0:
            fore_health_bar_rect = pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)
            pygame.draw.rect(self.screen, (39, 174, 96), fore_health_bar_rect) #---> Flask Vitality Green Colour
        
        # 3) Drawing the border of the health bar

        border_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (120, 120, 125), border_rect, 2) # ---> Tarnished Steel Grey Color

    def no_collision_with_level_box(self):
        
        if self.hitbox.colliderect(self.level_box_rect):
            print("COLLISION OCCURING!!")

    def attacking_animation_and_sound_effects(self):
        # The intent with this subroutine is to handle which attack the player selects, playing its corresponding animation and also its sound effect
        # Blue Blast button --> E, Purple Blast button --> F
        current_time = pygame.time.get_ticks()
        if (self.is_blast_released == True) and (current_time - self.last_blast_time >= self.blast_cooldown):
            self.blast_state = False


        keys = pygame.key.get_pressed()


        if keys[pygame.K_e]: # To select Blue Blast
            self.is_blue_blast_selected = True
            self.is_purple_blast_selected = False
        if keys[pygame.K_f]: # To select Purple Blast
            self.is_purple_blast_selected = True
            self.is_blue_blast_selected = False


        if keys[pygame.K_q]: # 

            if self.is_blue_blast_selected == False and self.is_purple_blast_selected == False: # --> Player pressing attack button without selecting any attack, will be prompted to select an attack first.
                self.is_player_attacking = False
                self.is_blast_released = False
                
                self.select_attack_text = self.level_font.render(f"Select an attack first!", False, "red")
                self.screen.blit(self.select_attack_text, ((self.MAX_WIDTH/2.5),(self.MAX_HEIGHT/3.5)))

            else:
                if not self.is_player_attacking and self.is_blast_released == False: # --> This condition ensures that the player cannot spam the attack button, and that the blast is released only once per attack button press.
                    self.is_player_attacking = True
                    self.is_blast_released = True # --> This variable is needed so that the blast can continue to go, whilst not being dependent on the player pressing the attack button.

                    self.attack_frame_index = 0

                    self.blast_x = self.pos.x # --> Starting coordinates by which the blast emerges from 
                    self.blast_y = self.pos.y # --> [Fix --> Taking the Player's current position instead of the starting position of the player, so that the blast can be released from wherever the player is on the screen]

                    if self.blast_facing_right: # --> Helps us determine as to which direction the blast should go, based on the direction the player is facing.
                        self.blast_direction = 1
                    else:
                        self.blast_direction = -1

                    if self.is_blue_blast_selected:
                        self.blue_blast.play()
                    if self.is_purple_blast_selected:
                        self.purple_blast.play()

                elif self.is_blast_released == True:
                    self.select_attack_text = self.level_font.render(f"Blast is on cooldown!", False, "red")
                    self.screen.blit(self.select_attack_text, ((self.MAX_WIDTH/2.5),(self.MAX_HEIGHT/3.5)))

        if self.is_blue_blast_selected == True and self.is_purple_blast_selected == False:
            attack_animation = self.attack_animations['blue_blast'] # --> To load the relevant animation for the respective attack
        elif self.is_purple_blast_selected == True and self.is_blue_blast_selected == False:
            attack_animation = self.attack_animations['purple_blast']
        else:
            attack_animation = None # --> If the player has not selected any attack, the default animation will be blue blast animation

        if self.is_blast_released == True and attack_animation is not None:
            self.attack_frame_index =  (self.attack_frame_index + self.attack_animation_speed) % len(attack_animation) # --> So that the animation repeats itself rather than stopping at the last frame of the animation.


            self.blast_x += self.blast_velocity * self.blast_direction # --> What causes the blast to move
            
            # Boundary checks: Stop attacking only when the blast goes completely off-screen
            if self.blast_direction == 1:  # Moving right
                if self.blast_x > self.MAX_WIDTH:
                    self.is_blast_released = False
            else:  # Moving left
                if self.blast_x < -self.MAX_WIDTH:
                    self.is_blast_released = False

            if self.is_blast_released == True and attack_animation is not None:
                if self.blast_direction == 1: # --> The animations were drawn assuming that it would go to the left, hence the image is inverted to make the blast look like it travels to the right --> CONSISTENCY IN ANIMATION
                    self.attack_image = pygame.transform.flip(pygame.transform.scale((attack_animation[int(self.attack_frame_index)]),(150,150)), True, False)
                else:
                    self.attack_image = pygame.transform.scale((attack_animation[int(self.attack_frame_index)]),(150,150))

                self.screen.blit(self.attack_image,(self.blast_x, self.blast_y))

    def update(self):
        self.clock.tick(60)
        self.input()
        self.get_status()
        self.move(self.speed)        
        self.staying_in_screen()
        self.animate()
        self.player_health()
        self.no_collision_with_level_box()        
        self.attacking_animation_and_sound_effects()

