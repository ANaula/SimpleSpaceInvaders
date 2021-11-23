# Simple Space Invaders

A simple space invaders game where the goal is to protect the planet by shooting down as many blue enemies as possible while avoiding enemy projectiles. The game is divided into levels and as the levels progress, more enemies will spawn but so will more drops which give the player either more health or armor if they do not have full health or armor already. There are two types of enemy projectiles, lasers and shells, which do different amounts of damage to the player. Enemies can also do damage to the planet by passing the bottom edge of the window. The game ends when either the player or planet health becomes 0. 

![Alt Text](<div style="width:100%;height:0;padding-bottom:56%;position:relative;"><iframe src="https://giphy.com/embed/qak75mmRepf1pAR2Fo" width="100%" height="100%" style="position:absolute" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div><p><a href="https://giphy.com/gifs/qak75mmRepf1pAR2Fo">via GIPHY</a></p>
)

## How it works

The game uses the Pygame module (which could be downloaded here https://www.pygame.org/download.shtml) for the window creation and multimedia components.  The audio used in this game is all under CC0 1.0 and were dedicated to the public domain. I do not own any of the sounds.  

The game is separated into states and the game is run by placing the states into a list which runs the state that is first. Each state has their own internal loop so once the loop has been stopped, it is deleted from the list. The only exception to this is the game state which, if paused, gets pushed back and the pause state get placed in front of it on the list.  The game class controls this process and what state is run depends on what the current_state member variable is. In each loop, the current_state variable changes and we check to see if there is an object with the class associated to that current_state in the list, which is called the state_queue. If there is, we push it to the front of the list. If there isn’t, we create one and put it first on the list. Like mentioned earlier each aspect of the game is separated into states, there is a main menu state, a pause state, a score screen state, an instructions state, and a game state (which is different from the game class which controls everything). 

![Alt Text](https://media.giphy.com/media/cE5UCasOyaaHa64s8Z/giphy.gif)

## Download

The .exe file is included in the repository, it is titled "SimpleSpaceInvaders.exe". You can either clone the repository and run the .exe or go to releases and download the "SimpleSpaceInvadersInstaller.exe" which downloads the repository files.
