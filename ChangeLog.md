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
          2) Adding the basic logic for the player's attack [player.py] ---> The player has to first select between the blue blast or the purple blast attack by pressing its relevant button, and then press the attack button to actually initiate the attsck. {All that remains is to bring the animation for the attacks and then the collision detection for the player and enemy to complete the attack mechanic}