### The purpose of this file is to record all the changes that have occurred within this project ###


|||| Changes Made |||

    Date: 11 / 07 / 2026
          1) Finally fixing the attack mechanic for the player [player.py] ----> Initially, when the player would press the 'Q' button, the attack animation would play continuously with no end. Now, thanks to some boolean operations and editing the animate() function, the attack animation only plays once when the button is pressed, and if the player needs to attack again, the button has to be pressed again
          
          2) Adding the attack mechanic for the enemy [enemy.py] ---> The enemy has two radii associated with it, where if the player crosses any of those two radii, the enemy acts accordingly; If the player crosses the attack radius, the enemy shall play the attack animation. I also changed the value of the radius to make it easier for the enemy to damage the player  

          3) Adding attack sound effect for enemy [enemy.py] ---> I added the attack sound effect for the enemy that plays alongside the animation, though it is currently a bit rusty, it does the job 


    Date: 14 / 07 / 2026
          1) Refining the Attack Animation and Sound Effect of the Enemy [enemy.py] ---> Before the changes, there would be a delay between the animation and the sound effect and the sound would be continous even if the player escaped from the enemy. By increasing the animation speed by a small margin (0.15 --> 0.175), and setting the relevant variable false if the player enters the notice radius, the attack animation is alot more smoother leading to a more cohesive experience for the player