### The purpose of this file is to record all the changes that have occurred within this project ###


|||| Changes Made |||

    Date: 11 / 07 / 2026
          1) Finally fixing the attack mechanic for the player [player.py] ----> Initially, when the player would press the 'Q' button, the attack animation would play continuously with no end. Now, thanks to some boolean operations and editing the animate() function, the attack animation only plays once when the button is pressed, and if the player needs to attack again, the button has to be pressed again
          
          2) Adding the attack mechanic for the enemy [enemy.py] ---> The enemy has two radii associated with it, where if the player crosses any of those two radii, the enemy acts accordingly; If the player crosses the attack radius, the enemy shall play the attack animation. I also changed the value of the radius to make it easier for the enemy to damage the player  

          3) Adding attack sound effect for enemy [enemy.py] ---> I added the attack sound effect for the enemy that plays alongside the animation, though it is currently a bit rusty, it does the job 