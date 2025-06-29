import pygame
from sys import exit
from random import randint, choice

# Load button images
first_button = pygame.image.load('images/UI/yellow_button.png')
second_button = pygame.image.load('images/UI/play_button.png')
third_button = pygame.image.load('images/UI/exit_button.png')

class Button():
    def __init__(self, x, y, image,type):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.type = type

        # Sounds
        self.button_sound = pygame.mixer.Sound('audio/button_click.mp3')
        
    def draw(self):
        # This function was adapted from Coding With Russ's implementation at https://www.youtube.com/watch?v=deeetAQhMQU&list=PLjcN1EyupaQnHM1I9SmiXfbT6aG4ezUvu&index=8
        action = False
        global game_active
        global start_menu
        global player_score
        
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Restart game button after chracter dies 
        if start_menu == False and self.type == 0:
            # Check mouse over and click conditions
            if self.rect.collidepoint(pos) and self.clicked == False:
                if pygame.mouse.get_pressed()[0] == 1:
                    game_active = True
                    action = True
                    self.clicked = True
                    self.button_sound.play()
                    player_score = 0
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            screen.blit(self.image,self.rect)
        
        # Play game button on the start menu
        if start_menu == True and self.type == 1:
            # Check mouse over and click conditions
            if self.rect.collidepoint(pos) and self.clicked == False:
                if pygame.mouse.get_pressed()[0] == 1:
                    game_active = True
                    start_menu = False
                    action = True
                    self.clicked = True
                    lava_class.reset(0,600)
                    self.button_sound.play()
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            screen.blit(self.image,self.rect)

        # Exit button on the start menu 
        if start_menu == True and self.type == 2:
            # Check mouse over and click conditions
            if self.rect.collidepoint(pos) and self.clicked == False:
                if pygame.mouse.get_pressed()[0] == 1:
                    self.button_sound.play()
                    pygame.quit()
                    exit()
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            screen.blit(self.image,self.rect)

        # Exit button after the character dies
        if start_menu == False and self.type == 2:
            # Check mouse over and click conditions
            if self.rect.collidepoint(pos) and self.clicked == False:
                if pygame.mouse.get_pressed()[0] == 1:
                    self.button_sound.play()
                    pygame.quit()
                    exit()
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            screen.blit(self.image,self.rect)
        return action

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reset()

    def update(self):
        # Character moves 3 pixels down when function is called
        self.rect.y += 3
        self.destroy()

    def destroy(self):
        # Destroy block when y value is greateer or equal to 450
        if self.rect.y >= 450:
            self.kill()

    def reset(self):
        pygame.sprite.Sprite.__init__(self)
        # List for storing coins
        self.coin_list = []

        self.image = pygame.image.load('images/coinGold.png').convert_alpha()

        # Tells Python that I want to use the global variable
        global x_axis

        self.rect = self.image.get_rect(midbottom = (x_axis, -100))

        # Store the image and rect in the image
        coin = (self.image,self.rect)
        self.coin_list.append(coin)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.reset(x,y) 
    
    def update(self):
        global game_active
        global start_menu
        global player_score

        if game_active == True and start_menu == False:
            # The implementation of the walking animation was adapted from Clear code's implementation at https://www.youtube.com/watch?v=AY9MnQ4x3zk&list=LL&index=3

            # Stores expected character x and y positions
            dx = 0
            dy = 0

            # The distance between the player and block to be a collision
            col_threshold = 20

            # Get key presses
            key = pygame.key.get_pressed()
             
            if key[pygame.K_a]:
                # Moves 5 pixels to the left
                dx -= 5
                
                #animation
                self.char_index += 0.1
                if self.char_index >= len(self.char_move):self.char_index = 0
                self.image = pygame.transform.flip(self.char_move[int(self.char_index)], True, False)

            if key[pygame.K_w] and self.jumped == False and self.in_air == False:
                # Moves 20 pixels up
                self.vel_y = -20
                
                self.jumped = True
                self.in_air = True
                self.image = self.char_jump
                self.jump_sound.play()

            # Allows the player to jump when 'W' is not clicked
            if key[pygame.K_w] == False:
                self.jumped = False

            if key[pygame.K_d]:
                # Moves 5 pixels to the right
                dx += 5
            
                # Animation
                self.char_index += 0.1
                if self.char_index >= len(self.char_move): self.char_index = 0
                self.image = self.char_move[int(self.char_index)]     

            # Add gravity 
            self.vel_y += 1 
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Thia collision detection was adapted from Coding With Russ's implementation at https://www.youtube.com/watch?v=rl0PiY9OQLo&list=PLjcN1EyupaQnHM1I9SmiXfbT6aG4ezUvu&index=13
            # Check for collision with platforms
            for element in block_group:
                # Check for collision in x direction
                if element.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # Check for collision in y direction 
                if element.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Check if player is below the block
                    if abs((self.rect.top + dy) - element.rect.bottom) < col_threshold:
                        self.vel_y = 0
                        dy = element.rect.bottom - self.rect.top + 10

                    # Check if player is above the block
                    elif self.vel_y >= 0:
                        dy = element.rect.top - self.rect.bottom + 3
                        self.vel_y = 0
                        self.in_air = False

            # Check for collisions with coins
            for element in coin_group:
                if element.rect.colliderect(self.rect):
                    # Increase the player's score
                    self.coin_sound.play()
                    player_score += 1

                    # Remove the coin from the screen
                    element.rect.y = 1000

            # Make sure character does not leave screen vertically
            if self.rect.y <= 0:
                self.rect.y = 0
                self.vel_y = 0

            # Make sure character does not leave screen horizontally
            if self.rect.x >= 750:
                self.rect.x = 750
            
            # Make sure character does not leave screen horizontally
            if self.rect.x <= 0:
                self.rect.x = 10

            # Update coordinates
            self.rect.x += dx
            self.rect.y += dy

            # Check for collision with lava       
            if pygame.sprite.spritecollide(self, lava_2, False):
                self.hurt.play()
                game_active = False

            # Check for collision with enemies
            if pygame.sprite.spritecollide(self, enemy_group, False):
                self.hurt.play()
                game_active = False
        
        elif game_active == False and start_menu == False:
            # If player loses game hurt image appears
            self.image = self.char_hurt

        # Prevents player from moving below the ground
        if self.rect.bottom > 500:
            self.rect.bottom = 500
            self.in_air = False

    # Function resets the position of the class
    def reset(self,x,y):
        # Import images
        self.char_jump = pygame.image.load('images/alien/alien_jump.png').convert_alpha()
        char_walk1 = pygame.image.load('images/alien/alien_walk1.png').convert_alpha()
        char_walk2 = pygame.image.load('images/alien/alien_walk2.png').convert_alpha()
        self.char_hurt = pygame.image.load('images/alien/alien_hurt.png').convert_alpha()
        
        # Scale images
        self.char_jump = pygame.transform.rotozoom(self.char_jump, 0, 0.7)
        char_walk1 = pygame.transform.rotozoom(char_walk1, 0, 0.7)
        char_walk2 = pygame.transform.rotozoom(char_walk2, 0, 0.7)
        self.char_hurt = pygame.transform.rotozoom(self.char_hurt, 0, 0.7)
        
        # Walking animation
        self.char_move = [char_walk1,char_walk2]
        self.char_index = 0
        self.gravity = 0

        # Image
        self.image = self.char_move[self.char_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.jumped = False
        self.in_air = False

        # Sounds
        if game_active == True:
            self.jump_sound = pygame.mixer.Sound('audio/jump_sound.mp3')
            self.hurt = pygame.mixer.Sound('audio/char_hurt.wav')
            self.coin_sound = pygame.mixer.Sound('audio/coin_sound.mp3')
        
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        # ground block
        self.image = pygame.image.load('images/ground.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        # Movement 
        self.rect.y += 2

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reset()

    def update(self):
        # Block moves 3 pixels down when function is called
        self.rect.y += 3
        self.destroy()
        
    def destroy(self):
        # Destroy block when y value is greateer or equal to 450
        if self.rect.y >= 450:
            self.kill()
    
    # Function resets the position of the class
    def reset(self):
        #list of the blocks
        self.block_list = []

        # Block surface
        ground_surf = pygame.image.load('images/ground.png')
        self.image = pygame.transform.scale(ground_surf, (200,50))

        # Make game harder
        global player_score
        block_length = randint(75,150)
        if player_score > 30:
            self.image = pygame.transform.scale(ground_surf, (block_length,50))
        
        # Tells Python that I want to use the global variable
        global x_axis

        # Copies axis position of the block
        copy = x_axis

        # 2 options right or left
        axis_left = copy - 150
        axis_right = copy + 150
        positions = []


        if axis_left >= 100:
            positions.append(axis_left)
        if axis_right <= 700:
            positions.append(axis_right)

        # Picks options added to position list
        x_axis = choice(positions)

        self.rect = self.image.get_rect(midbottom = (x_axis,randint(-50,0)))
        block = (self.image,self.rect)
        # Adds block to block list
        self.block_list.append(block)
        positions.clear
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self,position):
        self.reset(position)
    
    def update(self):
        # The implementation of the flying animation was adapted from Clear code's implementation at https://www.youtube.com/watch?v=AY9MnQ4x3zk&list=LL&index=3
        # Animation
        self.char_index += 0.15
        if self.char_index >= len(self.char_move): 
            self.char_index = 0

        # Flips image based on which side it is coming from
        if self.move_direction < 0:
            self.image = self.char_move[int(self.char_index)]

        else:
            self.image = pygame.transform.flip(self.char_move[int(self.char_index)],True,False)

        self.rect.x += self.move_direction

    # Rests the postion of the enemy
    def reset(self,position):
        pygame.sprite.Sprite.__init__(self)
        bee = pygame.image.load('images/enemies/bee.png').convert_alpha()
        bee_fly = pygame.image.load('images/enemies/bee_fly.png').convert_alpha()
        fly = pygame.image.load('images/enemies/fly.png').convert_alpha()
        fly_fly = pygame.image.load('images/enemies/fly_fly.png').convert_alpha()

        char_bee = [bee,bee_fly]
        char_fly = [fly,fly_fly]
        self.char_move = choice([char_bee,char_fly])
        self.char_index = 0

        self.image = self.char_move[self.char_index]
        if position == 0:
            self.rect = self.image.get_rect()
            self.rect.x = randint(-100,-50)
            self.rect.y = randint(0,400)
            self.move_direction = 2

        if position == 1:
            self.rect = self.image.get_rect()
            self.rect.x = randint(850,900)
            self.rect.y = randint(0,400)
            self.move_direction = -2

class lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.reset(x,y)
    
    def update(self):
        # The implementation of the flying animation was adapted from Clear code's implementation at https://www.youtube.com/watch?v=AY9MnQ4x3zk&list=LL&index=3
        # Animation
        self.index += 0.05
        if self.index >= len(self.list): 
            self.index = 0
        self.image = self.list[int(self.index)]

        # Make the lava rise
        if self.rect.y > 450:
            self.rect.y -= 0.6

    def reset(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('images/lava.png').convert_alpha()
        image = pygame.transform.scale(image,(800,200))
        image_2 = pygame.image.load('images/lava.png').convert_alpha()
        image_2 = pygame.transform.scale(image_2,(800,200))
        image_2 = pygame.transform.flip(image_2,True,False)
        self.list = [image,image_2]
        self.index = 0
        self.image = self.list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

pygame.init()
# Start up information
screen_height = 600
screen_width = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Lava escape')
clock = pygame.time.Clock()

# Game states
game_active = True
start_menu = True

# Player score
player_score = 0

# Font download
font = pygame.font.Font('font/Supply Center.ttf', 25)
font_2 = pygame.font.Font('font/Supply Center.ttf', 50)
font_3 = pygame.font.Font('font/Supply Center.ttf', 25)

# Text functions
def score(score):
    score_surf = font.render(f'Score: {score}',True,(0,0,0))
    score_rect = score_surf.get_rect(midtop = (400,50))
    screen.blit(score_surf,score_rect)

def game_over():
    text_surf = font_2.render('Game Over',True,(0,0,0))
    text_rect = text_surf.get_rect(midtop = (400,100))
    screen.blit(text_surf,text_rect)

def game_name():
    text_surf = font_2.render('Lava Escape',True,(0,0,0))
    text_rect = text_surf.get_rect(midtop = (400,100))
    screen.blit(text_surf,text_rect)

def game_controls():
    text_surf = font_3.render('W = up, A = left and D = right',True,(35,35,35))
    text_rect = text_surf.get_rect(midtop = (400,550))
    screen.blit(text_surf,text_rect)

# Coin disappearance when colliding with player variable
coin_appear = True

# Block placements
x_axis = randint(100,700)

# Create button types
restart = 0
start = 1
leave = 2

# create buttons
restart_button = Button(300,200,first_button,restart)
start_button = Button(300,200,second_button,start)
exit_button = Button(300,300,third_button,leave)

# Groups
player = pygame.sprite.GroupSingle()
character = Player(700,500)
player.add(character)

block_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

lava_2 = pygame.sprite.GroupSingle()
lava_class = lava(0,600)
lava_2.add(lava_class)

enemy_group = pygame.sprite.Group()
enemy_left = 0
enemy_right = 1   

plat_group = pygame.sprite.GroupSingle()
plat_class = Platform(0,500)
plat_group.add(plat_class)

# ground block
ground_surf = pygame.image.load('images/ground.png')

sky_surf = pygame.image.load('images/sky.png')
sky_surf = pygame.transform.scale(sky_surf,(screen_width,screen_height))

# Background sounds
bg_music = pygame.mixer.Sound('audio/bg_music.mp3')
bg_music.play(loops = -1)

# Block timer 
block_timer = pygame.USEREVENT + 1
pygame.time.set_timer(block_timer,1000)

# Enemy timer
enemy_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer,12000)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == block_timer and start_menu == False:
            func_block = Block()           
            block_group.add(func_block)
            func_coin = Coin()
            coin_group.add(func_coin)
        if event.type == enemy_timer and player_score > 10 and start_menu == False:
            enemy_type = choice([enemy_left,enemy_right])        
            enemy_group.add(Enemy(enemy_type))
    
    screen.blit(sky_surf,(0,0))
    screen.blit(ground_surf,(0,500))

    # Before user starts playing
    if start_menu == True:
        game_name()
        game_controls()
        start_button.draw()
        exit_button.draw()

    player.draw(screen)
    player.update()
    
    # When user is playing the game
    if game_active == True and start_menu == False:
        score(player_score)
        enemy_group.draw(screen)
        lava_2.draw(screen)

        if player_score >= 1:
            lava_2.update()
            enemy_group.update()

        block_group.draw(screen)
        block_group.update()
        coin_group.draw(screen)
        coin_group.update()

    # If player loses
    if game_active == False:
        exit_button.draw()
        game_over()
        score(player_score)
        if restart_button.draw():
            game_active = True
            lava_class.reset(0,600)
            block_group.empty()
            func_block.reset()
            coin_group.empty()
            enemy_group.empty()
            func_coin.reset()
            character.reset(700,500)
         
         
    pygame.display.update()
    clock.tick(60)