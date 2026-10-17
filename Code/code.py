import pygame, random, os, sys #IMPORTING NECESSARY LIBRARIES
import button #IMPORTING MODULE FOR MAIN MENU AND FOR PAUSE
from player import Player
from enemy import Enemy

pygame.init() # Initialising Pygame

HEIGHT = 680
WIDTH = 800
# Two variables above helps in setting up the basic window

WIN = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE) #Setting up the basic window for the game


fullscreen = False #Checks if the user is in fullscreen or not
before_fullscreen_sound = False #If this is false, the [no_fullscreen sound] is played
after_fullscreen_sound = True #When True, an audio is played for the mainmenu
# The three variables above will aid in checking whether if the window is in fullscreen or in the values of WIDTH AND HEIGHT


clock = pygame.time.Clock() #Helps to set FPS for the game


# -------------- GETTING ASSETS --------------------------- #

first_font = pygame.font.Font("UI related/FONTS/rainyhearts.ttf",24)
second_font = pygame.font.Font("UI related/FONTS/dogica.otf",40)
third_font = pygame.font.Font("UI related/FONTS/Retro Gaming.ttf",24)

game_icon = pygame.image.load("UI related/ICON/myicon.ico")

background_after_fullscreen = pygame.image.load("UI related/BACKGROUNDS/maybe_main_menu.png")
after_fullscreen = pygame.mixer.Sound("Sound Effects/after_fullscreen.mp3")
no_fullscreen = pygame.mixer.Sound("Sound Effects/no_fullscreen.mp3")

arena = pygame.image.load("UI related/BACKGROUNDS/arena.png")

game_paused_image = pygame.transform.scale(pygame.image.load("UI related/BACKGROUNDS/game_paused.png"),(420,330))
resume_button_image = pygame.transform.scale(pygame.image.load("UI related/BUTTONS/resume_button.png"), (350,250))

back_to_main_menu = pygame.transform.scale(pygame.image.load("UI related/BUTTONS/back_mainmenu.png").convert_alpha(), (300,300))

start_button_img = pygame.transform.scale(pygame.image.load("UI related/BUTTONS/start_button.png"), (350,350))
exit_button_img = pygame.transform.scale(pygame.image.load("UI related/BUTTONS/exit_button.png"), (350,350))

game_over = pygame.mixer.Sound("Sound Effects/game_over.mp3")
game_pause = pygame.mixer.Sound("Sound Effects/game_pause.mp3")

click_button_sound = pygame.mixer.Sound("Sound Effects/button_click.mp3")
win_level = pygame.mixer.Sound("Sound Effects/win_level.mp3")
new_level = pygame.mixer.Sound("Sound Effects/new_level.mp3")

# -------- END OF ASSETS ------ #

pygame.display.set_icon(game_icon) #Removes the ugly snake on the window (finally)

running = True # Checks if the actual game is running


def loading_screen():
    progress_bar_value = 0 #Helps us to fill the loading bar and to get the percentage of loading bar filled
    
    pygame.display.set_caption("LOADING...") #Diffirentiates this screen from other screens 
    
    after_fullscreen.fadeout(1000) #Stops all audio played previously
    
    loading_message = ["Zain is a beautiful kid" , "Give Zain a big kiss", "Talha is the best Big bro"] 
    random_message = random.choice(loading_message) #Gives user a message to read as they wait for the game to load
    
    while progress_bar_value < 400: #When the loading bar isn't filled
        WIN.fill("grey26") # Colour of the screen

        loading_bar_empty = pygame.draw.rect(WIN,"azure3", (WIDTH*0.36,HEIGHT * 0.525,400,10), 1) #The loading bar
        loading_bar_full = pygame.draw.rect(WIN,"white", (WIDTH*0.36,HEIGHT * 0.525,progress_bar_value,10)) #This is what fills up the loading bar

        loading_message_display = first_font.render(f"Tip : {random_message}", True, "white") #Outputs a tip for the player (how generous)
        WIN.blit(loading_message_display, ((WIDTH*0.42),(HEIGHT * 0.45))) #Actual display of the message
        progress_bar_value += 100 #random.uniform(0.3,0.8) #How much does the bar get filled up by
        
        loading_percentage = round(((progress_bar_value / 400) * 100),1)
        loading_percentage_message = first_font.render(F"Loading : {loading_percentage}%", True, "white")
        WIN.blit(loading_percentage_message, ((WIDTH*0.47),(HEIGHT * 0.55))) #Outputting the percentage of how much loading is completed
            
        clock.tick(60)

        pygame.display.flip()
    pygame.event.clear()

def play(play_width,play_height): # This subroutine is where the actual game will occur
    playing = True
    arena_bigger = pygame.transform.scale(arena, (WIDTH,HEIGHT))
    WIN.blit(arena_bigger, (0,0))
    pygame.display.flip()
    me = Player(100,5,100,1,WIN)

    enemy_1 = Enemy(100,100,5,5,WIN)

    pygame.display.set_caption("Zain's Game")

# ---- Changes above are to set up for what is to come next ---

    while playing:
        WIN.blit(arena_bigger, (0,0)) #Remove everything from main menu
        me.player_update(enemy_1)
        me.update()

        enemy_1.enemy_update(me)
        enemy_1.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    status =  pause(play_width, play_height) # Goes into a diffirent subroutine
                    
                    if status == "MAIN MENU": #We leave this subroutine to go to the main menu
                        WIN.fill("black")
                        playing = False

        pygame.display.flip()
        clock.tick(60) #To not fry the CPU when the game is paused

def pause(screen_width,screen_hEIGHT):
    
    pause_active = True #Checks if the user has paused the game
    game_pause.play()
    pygame.display.set_caption("Pause")
    pygame.display.flip()
    #print(f"WIDTH: {screen_width}, HEIGHT: {screen_hEIGHT}")

    pygame.display.flip()

    while pause_active:
        
        WIN.fill("black")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    # -- Outputting Assets for the pause section of the game -- #
    
        WIN.blit(game_paused_image,(screen_width*0.35,screen_hEIGHT*0.05))
        resume_button = button.Button((screen_width*0.15),(screen_hEIGHT*0.5),resume_button_image, 1,0,0)
        back_to_main_menu_button = button.Button((screen_width*0.5),(screen_hEIGHT*0.5),back_to_main_menu,1,0,0 )
    
    # -- End of outputting asssets -- #


        if resume_button.draw(WIN): #If the user wants to continue the game
            click_button_sound.play() # Sound effect to show the button is pressed
            
            while pygame.mouse.get_pressed()[0]: #Ensures that the button  is only clicked once
                pygame.event.pump()
            pygame.time.delay(25) #Small delay between button being pressed and output to make it look smoother
            
            return "MENU" #Goes back to the play subroutine
        
        elif back_to_main_menu_button.draw(WIN): #If the user wants to return to main menu
            click_button_sound.play() # Sound effect to show the button is pressed
            
            while pygame.mouse.get_pressed()[0]:  #Ensures that the button  is only clicked once
                pygame.event.pump()
            pygame.time.delay(25) #Small delay between button being pressed and output to make it look smoother

            return "MAIN MENU"  #Goes back to the play subroutine

        pygame.display.flip()

        clock.tick(60)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.WINDOWMAXIMIZED: # When the user's window takes up the fullscreen
            fullscreen = True
            
            get_width , get_height = pygame.display.get_window_size() #We get the dimensions of the user's actual screen
            WIDTH = get_width
            HEIGHT = get_height #The two values WIDTH AND HEIGHT will update the WIN dimensions
            
            after_fullscreen.play(-1,0,500) #This will play the main menu audio
            after_fullscreen_sound = True   

        elif event.type == pygame.WINDOWRESTORED: # When the user presses the middle button
            
            fullscreen = False
            after_fullscreen.fadeout(1000) #No audio shall play

        elif event.type == pygame.WINDOWMINIMIZED: #The game screen is gone but NOT stopped
            
            after_fullscreen_sound = False
            after_fullscreen.fadeout(1000) #No audio is to play
            
## -- Performance Fix --> Minimising CPU Utilisation by fixing loop indenation and timing -- ##
    if fullscreen == False: # When the user is not in fullscreen
        if before_fullscreen_sound == False: #And no audio is being played
                
            before_fullscreen_sound = True #The before fullscreen audio shall play
            no_fullscreen.play(-1,0,500)

            # ----- Telling user to go fullscreen ----- #

            pygame.display.set_caption("Fullscreen Needed")
                
            WIN.fill("antiquewhite4")

            message = first_font.render("Fullscreen is needed to play this game ", False, "white")
            WIN.blit(message, (220,330))

    else: #When the user goes into fullscreen
        if before_fullscreen_sound == True: #Checks if the before_fullscreen audio plays
                
            no_fullscreen.fadeout(1000)
            before_fullscreen_sound = False #The before audio is gone
            
            # ---- The Main Menu ---- #
        if after_fullscreen_sound == False: # This will aid us in playing this audio once the user returns from the pause menn
            pygame.mixer.music.set_volume(0.3)
            after_fullscreen.play(-1,0,500)
            after_fullscreen_sound = True

        pygame.display.set_caption("Main Menu")
        WIN.blit(pygame.transform.scale(background_after_fullscreen,(WIDTH,HEIGHT)), (0, 0))

        greetings = second_font.render("A Fighter Game", False, "white")
            #pygame.draw.rect(WIN,"gray68", (WIDTH*0.35,HEIGHT*0.075, 445,HEIGHT*0.1))

        WIN.blit(greetings,(WIDTH*0.325,HEIGHT*0.15))

        start_button_actual = button.Button((WIDTH*0.375),(HEIGHT * 0.2), start_button_img,1, 0,-230)
        exit_button_actual = button.Button((WIDTH*0.375),(HEIGHT*0.5), exit_button_img,1,0,-230)

        if start_button_actual.draw(WIN): #When the user clicks on the start button
            after_fullscreen_sound = False #Stops audio being played
                
            click_button_sound.play() #Shows that button is pressed
                
            while pygame.mouse.get_pressed()[0]:  #Ensures that the button  is only clicked once
                pygame.event.pump()
            pygame.time.delay(25) #Makes things look smoother
                
            loading_screen()
            play(WIDTH,HEIGHT) # The game starts

        if exit_button_actual.draw(WIN): # When exit button is pressed                                
            click_button_sound.play()
                
            while pygame.mouse.get_pressed()[0]:  #Ensures that the button  is only clicked once
                after_fullscreen.fadeout(20)
                pygame.event.pump()

                pygame.time.delay(20) #Makes things look smoother


                running = False # The game stops
                     

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
