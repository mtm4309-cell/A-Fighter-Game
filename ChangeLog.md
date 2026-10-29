### The purpose of this file is to record all the changes that have occurred within this project ###


|||| Changes Made |||

      Date: 11 / 07 / 2026:
            1) Finally fixing the attack mechanic for the player [player.py] ----> Initially, when the player would press the 'Q' button, the attack animation would play continuously with no end. Now, thanks to some boolean operations and editing the animate() function, the attack animation only plays once when the button is pressed, and if the player needs to attack again, the button has to be pressed again
            
            2) Adding the attack mechanic for the enemy [enemy.py] ---> The enemy has two radii associated with it, where if the player crosses any of those two radii, the enemy acts accordingly; If the player crosses the attack radius, the enemy shall play the attack animation. I also changed the value of the radius to make it easier for the enemy to damage the player  

            3) Adding attack sound effect for enemy [enemy.py] ---> I added the attack sound effect for the enemy that plays alongside the animation, though it is currently a bit rusty, it does the job 


      Date: 14 / 07 / 2026:
            1) Refining the Attack Animation and Sound Effect of the Enemy [enemy.py] ---> Before the changes, there would be a delay between the animation and the sound effect and the sound would be continous even if the player escaped from the enemy. By increasing the animation speed by a small margin (0.15 --> 0.175), and setting the relevant variable false if the player enters the notice radius, the attack animation is alot more smoother leading to a more cohesive experience for the player

            2) One of the attacks the player can choose is the blue blast; today I drew its animation and the button for which the player must press for the attack to occur, using aseprite. 

      Date: 15 / 07 / 2026:
            1) Refining the buttons for the Blue Blast and the Purple Blast --> For the Blue Blast, a design for when the player presses that button and when it is not selected was drawn, and likewise for the Purple Blast
            2) Changing the Jump Height --> Initially, if the player were to jump, it would still be in the proximity of the enemy, but by increasing it, no unnecessary damage will be afflicted onto the player.

      Date: 27 / 07 / 2026:
            1) Finalising the animation for the Purple Blast
            2) Changing the attack mechanism of the player [player.py] ---> The code initially checks if an attack has been selected, if a selection has not been made, a text will pop up in red asking the player to select an attack.


      Date: 30 / 07 / 2026:
            1) Adding the buttons for both the blue blast and the purple blast on screen --> Initially, the images were 32x32, which was unfortunately too small, hence I transformed the images and so increased its size by a scale factor to 100x100 (3.125x scale factor)
            2) Adding the basic logic for the player's attack [player.py] ---> The player has to first select between the blue blast or the purple blast attack by pressing its relevant button, and then press the attack button to actually initiate the attack. {All that remains is to bring the animation for the attacks and then the collision detection for the player and enemy to complete the attack mechanic}


      Date: 13 / 08 / 2026:
            1) Minimising CPU Utilisation --> Before, there were various places of code where when it is running, it would maximise the Utilisation of the CPU; This would increase the latency of the game, causin more lags and delays, affecting the User Experience. Now, these places have been changed so that the FPS is always at 60, maintaining consistency all across the game.
            2) Refining the Player Health Bar --> The elements regarding the health bar has changed so that its position is consistent for many diffirent players, it has also been designed to improve its aesthetics, trying to give a 'fantasy-like'vibe
            3) Altering coordinates for various assets --> At first, I had given these assets fixed coordinates that would work on my screen. However, this would obviously not work with other screens for other players. Hence, I changed this coordinates from it being fixed to using calculations based on the widths of the player screen, ensuring consistency and improving User Experience.
            4) Refining the Enemy Health Bar --> The Health Bar has been position using the Rect Values of the Enemy sprite so that it is placed 10 pixels above the enemy, and travels with the enemy wherever it goes; Just like the Player Health Bar, the colours that were chosen aee meant to give a 'fantasy-like' vibe 


      Date: 14 / 08 / 2026:
            1) Restructing the Player Attack Code --> Gathered scattered attack code and placed it into the attacking_animation_and_sound_effects() subroutine to streamline debugging and maintenance.
            2) Animation of the Blast Attacks --> Added frame-indexed asset loading and rendering for blue and purple blast attacks.
            3) The Movement of Blast Attacks --> Set up dynamic spawn coordinates based on the player's position, with horizontal movement driven by the player's coordinates and the blast velocity.

      Date: 19 / 08 / 2026:
            1) Adding a cool down for the blasts --> The Problem was that the blast would constantly reset back to the player depending on whether the 'Q' button was pressed; This would increase CPU Utilisation causing more latency. Hence; a cooldown system has been implemented using Pygame clock ticks using nested if statements. [I could restructure the code to using FSM's instead...]
      
      
      Date: 18 / 10 / 2026:     
                  
            1) Refining and cleaning up the attack code in player.py:

                  i)  Instead of having to go over the conditions (the _selected variables) which is looped by a condition (is_blast_released), a concrete variable is used such that the type of the blast chosen by the player is set in stone, such that it doesn't change whilst the attack is flying mid-air.
                  
                  ii) Initially, the attack button being pressed was checked inside the loop, and so the attack logic would be triggered again and again based upon the conditions. Now, the point at which the key was exactly presssed is now checked, so as as to stop rapid re-triggering of the attack logic.

                  iii) Instead of using the relevant dimensions of the screen of the user, I used a 150 pixel offset matching the width of the blast images, ensuring that the blast properly goes away from the screen.  

            2) Changing the point at which both the player and the enemy takes damage from self.rect to 
            self.hitbox in the case of direct contact between the player and the enemy.


      Date : 20 / 10 / 2026:

            1) Fixing the code relating to damage of the enemy by the blast:

                  Initial Issues:
                        i) When the blast would collide with the enemy, the enemy would completely lose its health, though the blast should only causes not that much damage. This was due to the code causing the blast to be in constant collision even if it is not visible on the screen.
                        ii) Two functions were made, one in the player class and the other in the enemy class, though they were not coordinated and rather executed in their own ways, this would cause unnecessary optimisation of the CPU. 
                        iii) Despite the prescence of two diffirent blasts, the damage that would be incurred onto the enemy would still remain the same.
                        
                  Fixes:
                        i) The coordination of both functions such that the function in the player class detects if there is a collision in the first place. The enemy class detects the type of blast from the player class, and then deals the respective damage onto the enemy.
                        ii) Attributes for the blue and purple blasts have been made respectively (though not applied fully for all characteristics) for the damage to be dealt onto the enemy.
                        iii) The stopping of the extra damage being dealt to the enemy the moment at which the collision occurs, via the coordination of the respective functions in the player and enemy class.
            
      Date: 23 / 10 / 2026:

           1) Fixing enemy kick attack timing and damage detection:
              
                  Initial Issues:
                        i) The sound effect would be played at the exact point the enemy goes into attack mode, and so there was a mismatch between the sound and the exact point of contact with the player, which appeared to be dissatisfactory for the user experience.
                        ii) Similar to the issue with the blast affecting the health of the enemy, the player's health would drastically go down whenever the enemy is in attack mode, with no regard as to when the player is actually hit by the kick of the enemy.

                  Fixes:
                        i) For both the instance at which the sound effect is being played and when the player's health goes down, a condition has been placed based upon the frame index of the animation of the enemy attack, which is the 5th-6th frame where there is contact between the enemy and the player. 

            2) Discrepancies between the attack sound effect of both player and enemy

                  Initial Issues:
  
                        i) Whenever the enemy is in attack mode whilst the player is attacking at the same time, the blast sound effects were given a priority over the enemy sound effect, and so the enemy sound effect is not being played yet the animation of the enemy attack is being played
                        ii) The removal of  the pygame.mixer.getbusy() condition allows the enemy's sound to play, but causes repeated playback triggers and overlapping audio, resulting in an unpleasant listening experience.

                  Fixes:
                        i) Dedicating a mixer channel for the enemy attack sound effect and likewise for the player attack sound effects --> The blue blast is assigned to channel 1. The purple blast is assigned to channel 2. The enemy attack sound effect is assigned to channel 3. This ensures that there are no interference between the sound effects if they were to both occur on one instance.
                        ii) Improving the sound channel management by using the condition {"pygame.mixer.Channel(3).gotbusy"} to check whether if the enemy's dedicated sound effect is being played before triggering another playback, removing the unpleasant overlapping of audio, whilst being independent from other sound effects.

            3) Finished the animation for the explosion of the blue blast and the purple blast --> This will happen whenever the blue / purple blast collides with the enemy, the code to implement the animation is yet to be done and the animation will be updated, this is currently a first draft.
      
      Date: 24 / 10 / 2026

            1) Changing the position of the run and the blasts button vertically and their respective dimenstions --> They are now placed next below the health bar, and have been resized so as to not overpower the health bar.  

      Date: 26 / 10 / 2026

            1) Implementation of the explosion animations when the blasts colllide with the enemy.

                  Initial Issue: Although the animation was complete, it would not appear on the screen when the blast collides with the enemy.

                  Fix: Two subroutines were made that works alongside the  collision_of_blast_with_enemy() function to handle the activation and the display of the explosion animation. 
                  
                        i) The first subroutine checks if the blast has been released AND has collided with the enemy. Once those two conditions are fulfilled, then the explosion is to be activated and its coordinates set to match the position of the blast.
                        
                        ii)The second subroutine handles the appropriate explosion animation for their respective blast type, and renders it on the screen. 

            2) Complete Integration of the individual blast attributes into their respective animations

                  Initial Issue : Both blast types were given the same attributes such as the speed at which they travel with, instead of accounting the diffirences between the blue and the purple blast. Essentially, there is no point in making two attacks if there are no diffirences between them. The only exception is the damage they cause to the enemy

                  Fix:
                        i) I removed the self.blast_velocity and self.blast_cooldown variables from the main player class and rather assigned them in the attacking_animation_and_sound_effects() subroutine, so that they do not get in the way when they are reassigned to the relevant blast attribute.
                        ii) I made the blast_attributes variable which gets the relevant properties of the blasts depending on the blast type using the getattr() function, and then brought back the two variables and assigned them to their respective attributes.

            3) Displaying the cooldown time

                  Initial Issue : If the player has attacked once, and is in cooldown, all they are told is that they have to wait for cooldown, but they are not informed of how much time remains, and also due to the lack of information of the time of cooldown, they are more likely to press the attack button, and hence spam it.

                  Fix : Under the condition that the time taken of the last blast and also that of the cooldown is greater than 0, the time in which the cooldown remains for is calculated first in miliseconds and then divided by 1000 to convert into seconds. This is then displayed onto the screen.  

      Date: 27 / 10 / 2026

            1) Making the blast explode when it has not collided with the enemy and has gone out of the screen.
                  Problem : Since the players are confined to the screen that they are in, making the blast to appear that they go out of the screen appearing that they have moved out of the screen gives the game an unappealing look.
                  Fix : I wrote a new subroutine (self.collision_of_blast_with_wall) which first makes a blast_rect, using the appropriate coordinates of the blast, and compares it with the dimensions of the screen (or 0), with which if the conditions are met, is then fed through the other relevant subroutines that bring forth the explosion animation.

            2) Made a potential ideas file to brainstorm some possibilities which if materialised will go on the project checklist.

      Date: 28 / 10 / 2026

            1) Animation and outline for the appearance of the health orb has been completed
            2) New file (and class) has been made to dedicate any sort of upgrades or boosts called 'droppable.py', with which the foundation has been started.
            3) Adding a black outline onto both the blue and purple blasts' explosion, to improve the look of the animation.

      Date: 29 / 10 / 2026:

            1) Completing the foundation for the health orb.

                  i) Adding a collison based collision depending on the rects of both the player and the health orb
                  ii) I update the orb's size and animation to use frames from the health_orb folder, and also manipulating what frames are to be played depending on whether certain conditions are met (Though there is still some logic error present)
                  iii) Fixing the maximum recursion depth error which was caused by the cycling between two subroutines in the droppable class.
                  iv) Adding a 20 point health boost which is capped at 100 health.

            [Note: This is still incomplete, as there are still some logic errors present,and I have more ideas regarding it]