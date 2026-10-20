### The purpose of this file is to record all the changes that have occurred within this project ###


|||| Changes Made |||

      Date: 11 / 07 / 2026
            1) Finally fixing the attack mechanic for the player [player.py] ----> Initially, when the player would press the 'Q' button, the attack animation would play continuously with no end. Now, thanks to some boolean operations and editing the animate() function, the attack animation only plays once when the button is pressed, and if the player needs to attack again, the button has to be pressed again
            
            2) Adding the attack mechanic for the enemy [enemy.py] ---> The enemy has two radii associated with it, where if the player crosses any of those two radii, the enemy acts accordingly; If the player crosses the attack radius, the enemy shall play the attack animation. I also changed the value of the radius to make it easier for the enemy to damage the player  

            3) Adding attack sound effect for enemy [enemy.py] ---> I added the attack sound effect for the enemy that plays alongside the animation, though it is currently a bit rusty, it does the job 


      Date: 14 / 07 / 2026
            1) Refining the Attack Animation and Sound Effect of the Enemy [enemy.py] ---> Before the changes, there would be a delay between the animation and the sound effect and the sound would be continous even if the player escaped from the enemy. By increasing the animation speed by a small margin (0.15 --> 0.175), and setting the relevant variable false if the player enters the notice radius, the attack animation is alot more smoother leading to a more cohesive experience for the player

            2) One of the attacks the player can choose is the blue blast; today I drew its animation and the button for which the player must press for the attack to occur, using aseprite. 

      Date: 15 / 07 / 2026
            1) Refining the buttons for the Blue Blast and the Purple Blast --> For the Blue Blast, a design for when the player presses that button and when it is not selected was drawn, and likewise for the Purple Blast
            2) Changing the Jump Height --> Initially, if the player were to jump, it would still be in the proximity of the enemy, but by increasing it, no unnecessary damage will be afflicted onto the player.

      Date: 27 / 07 / 2026
            1) Finalising the animation for the Purple Blast
            2) Changing the attack mechanism of the player [player.py] ---> The code initially checks if an attack has been selected, if a selection has not been made, a text will pop up in red asking the player to select an attack.


      Date: 30 / 07 / 2026
            1) Adding the buttons for both the blue blast and the purple blast on screen --> Initially, the images were 32x32, which was unfortunately too small, hence I transformed the images and so increased its size by a scale factor to 100x100 (3.125x scale factor)
            2) Adding the basic logic for the player's attack [player.py] ---> The player has to first select between the blue blast or the purple blast attack by pressing its relevant button, and then press the attack button to actually initiate the attack. {All that remains is to bring the animation for the attacks and then the collision detection for the player and enemy to complete the attack mechanic}


      Date: 13 / 08 / 2026
            1) Minimising CPU Utilisation --> Before, there were various places of code where when it is running, it would maximise the Utilisation of the CPU; This would increase the latency of the game, causin more lags and delays, affecting the User Experience. Now, these places have been changed so that the FPS is always at 60, maintaining consistency all across the game.
            2) Refining the Player Health Bar --> The elements regarding the health bar has changed so that its position is consistent for many diffirent players, it has also been designed to improve its aesthetics, trying to give a 'fantasy-like'vibe
            3) Altering coordinates for various assets --> At first, I had given these assets fixed coordinates that would work on my screen. However, this would obviously not work with other screens for other players. Hence, I changed this coordinates from it being fixed to using calculations based on the widths of the player screen, ensuring consistency and improving User Experience.
            4) Refining the Enemy Health Bar --> The Health Bar has been position using the Rect Values of the Enemy sprite so that it is placed 10 pixels above the enemy, and travels with the enemy wherever it goes; Just like the Player Health Bar, the colours that were chosen aee meant to give a 'fantasy-like' vibe 


      Date: 14 / 08 / 2026
            1) Restructing the Player Attack Code --> Gathered scattered attack code and placed it into the attacking_animation_and_sound_effects() subroutine to streamline debugging and maintenance.
            2) Animation of the Blast Attacks --> Added frame-indexed asset loading and rendering for blue and purple blast attacks.
            3) The Movement of Blast Attacks --> Set up dynamic spawn coordinates based on the player's position, with horizontal movement driven by the player's coordinates and the blast velocity.

      Date: 19 / 08 / 2026
            1) Adding a cool down for the blasts --> The Problem was that the blast would constantly reset back to the player depending on whether the 'Q' button was pressed; This would increase CPU Utilisation causing more latency. Hence; a cooldown system has been implemented using Pygame clock ticks using nested if statements. [I could restructure the code to using FSM's instead...]
      
      
      Date: 18 / 10 / 2026       
                  
            1) Refining and cleaning up the attack code in player.py:

                  i)  Instead of having to go over the conditions (the _selected variables) which is looped by a condition (is_blast_released), a concrete variable is used such that the type of the blast chosen by the player is set in stone, such that it doesn't change whilst the attack is flying mid-air.
                  
                  ii) Initially, the attack button being pressed was checked inside the loop, and so the attack logic would be triggered again and again based upon the conditions. Now, the point at which the key was exactly presssed is now checked, so as as to stop rapid re-triggering of the attack logic.

                  iii) Instead of using the relevant dimensions of the screen of the user, I used a 150 pixel offset matching the width of the blast images, ensuring that the blast properly goes away from the screen.  

            2) Changing the point at which both the player and the enemy takes damage from self.rect to 
            self.hitbox in the case of direct contact between the player and the enemy.


      Date : 20 / 10 / 2026

            1) Fixing the code relating to damage of the enemy by the blast:

                  Initial Issues:
                        i) When the blast would collide with the enemy, the enemy would completely lose its health, though the blast should only causes not that much damage. This was due to the code causing the blast to be in constant collision even if it is not visible on the screen.
                        ii) Two functions were made, one in the player class and the other in the enemy class, though they were not coordinated and rather executed in their own ways, this would cause unnecessary optimisation of the CPU. 
                        iii) Despite the prescence of two diffirent blasts, the damage that would be incurred onto the enemy would still remain the same.
                        iv)  

                  Fixes:
                        i) The coordination of both functions such that the function in the player class detects if there is a collision in the first place. The enemy class detects the type of blast from the player class, and then deals the respective damage onto the enemy.
                        ii) Attributes for the blue and purple blasts have been made respectively (though not applied fully for all characteristics) for the damage to be dealt onto the enemy.
                        iii) The stopping of the extra damage being dealt to the enemy the moment at which the collision occurs, via the coordination of the respective functions in the player and enemy class.
            

      