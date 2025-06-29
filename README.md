# Lava Escape
#### Video Demo:  <[URL HERE](https://youtu.be/12Czo9ZAyGQ)>

## Description: 

I created an endless runner game using the pygame module in python. The objective of the game is to collect the coins and avoid the lava and enemies(fly and bee). Once the play game button is clicked you will be able to move the character. The lava only starts rising once you have collected a coin, thus it is now possible for your character to die. To avoid the lava, blocks will fall from above and you have to stay on them before they hit the lava and then you move on to the next block. On each block there will be a coin which you are mean't to collect. After a certain scores are reached the game will become harder through enemies and the blocks becoming smaller. First enemies will start to appear moving from either left to right or vice versa. If these enemies and the player collide the game will end. Then the blocks will start to become smaller making it harder to stay alive. That's the game, stay alive for as long as possible to achieve the highest score possible. The game provides entertainment of for people who just want to play a fun and challenging game.

## Built with:

### Programming language:

- Python

### Libraries

```
import pygame
from sys import exit
from random import randint, choice
```

Install the [Pygame](https://www.pygame.org/docs/) folder by typing 
```
pip3 install pygame
```
into your terminal and pressing enter.

## How to run:

Click the run button or type the prompt in the terminal. The controls to move the character are at the bottom of the screen. Click play game button to start the game. Once you collect a coin the lava will start to rise.

## Files included:

- 1st Game
  - Audio
  - Images
    - Alien
    - Enemies
    - UI
  - Font
  - game.py

After all thse files have been download and the contents in them you should be able to run the game. The audio file contains all the audio that will be used in the game. The images file contains all the visual aspects of the game and the font file contains the true type font file for all the text used in the game. The 1st game file includes game.py file which is all of the code and a README.md file which explains the entire project.

## Challenges faced 

The main challenge I faced was figuring out how to make the player stay on the blocks. When the player and the blocks collide nothing happens they just pass through each other. The collision between the player and the block is complicated because the blocks are always moving. After struggling to do it myself I turned to Youtube where it took me a while to find a video which was dealing with the same type of collision as me. I was able create the collision through Coding With Russ's video which the link will be added to the acknowledgements. Another challenge was finding sprites but after I found sites like [Open game art](https://opengameart.org/) it was much easier.


## Acknowledgements

- Special thanks to Coding with Russ for help with the animations of sprites and the collisions of sprites. [Coding With Russ's channel](https://www.youtube.com/watch?v=0fXe-ij2ehc&t=66s).
- Special thanks to clear code how his into video to Pygame which taught me all of the basics of the [Pygame module](https://www.pygame.org/docs/). [Clear Code's Channel](https://www.youtube.com/watch?v=AY9MnQ4x3zk).
- Special thanks to Kenney Vleugels on most of the png's used in the game. [One of his sprite sheets I used](https://opengameart.org/content/platformer-art-deluxe).