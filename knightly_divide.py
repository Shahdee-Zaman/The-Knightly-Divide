import pygame
from animate import Animate
from player import Player
from arrows import Arrows
from random import randint
"""
Imports:
This combines all the class and calls them to create the game.
The animate class is called to use the spritesheet and image to animate the game.
The player class is called to create the player that users will control.
The arrows class is called to create the arrows that will fall.
The random class is called to ensure the arrows are always random.(You may remove this class and change it as you wish.)

Functions:
score - Keep track of the score. Score increase corresponds to game time,
knight_run - Right running animation for the player.
knight_run_backwards - Left running animation for the player.
knight_idle - Idle animation for the player.
spawn_obstacles - Spawns arrows that fall from the sky. Arrow spawn increases with Game duration.
collision_check - Checks if the player has collided with an arrow.
"""
# ---------------------------------Game Display Settings---------------------------------
# Starting Game
pygame.init()

# Game Title
pygame.display.set_caption('The Knightly Divide')

# Setting Display
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Camera Setting
camera_x = 0
camera_y = 0

# BackGround Settings
background = pygame.image.load('Background\castle_backround.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


# ---------------------------------End of Game Display Settings---------------------------------


# ---------------------------------Game Variables---------------------------------
# Score Text Customization
font = pygame.font.SysFont('Arial', 30)
# Score Settings
def score():
    time_start = pygame.time.get_ticks()
    score_board = font.render(f'Score: {time_start//100}', True, (255, 255, 255))
    score_rect = score_board.get_rect(topleft = (30,30))
    screen.blit(score_board,score_rect)
    return time_start

# Player Settings
starting_y = 540
starting_x = 400
player_width = 50
player_height = 70
# Starting player animation
sprite_idle = Animate("Sprite\IDLE_", 1, player_width,player_height).combine_sprite()
player = Player(sprite_idle, starting_x, starting_y)

# PLayer running animation when moving right.
def Knight_run():
    sprite_run = pygame.image.load('Sprite\RUN.png').convert_alpha()
    sprite_run = Animate(sprite_run, 8, player_width,player_height).split_sprite()
    player.frames = sprite_run
    player.num_of_frames = 8

# Player running animation when moving left.
def Knight_run_backwards():
    sprite_run = pygame.image.load('Sprite\RUN.png').convert_alpha()
    sprite_run = pygame.transform.flip(sprite_run, True, False).convert_alpha()
    sprite_run = Animate(sprite_run, 8, player_width,player_height).split_sprite()
    player.frames = sprite_run
    player.num_of_frames = 8

# Player idle animation when not moving.
def Knight_idle():
    sprite_idle = Animate("Sprite\IDLE_", 1, player_width,player_height).combine_sprite()
    player.frames = sprite_idle
    player.num_of_frames = 6


# Arrow Settings
# Create a sprite group for easier control.
arrow_obstacles = pygame.sprite.Group()
def spawn_obstacles():
    arrow = pygame.image.load('Arrow\Arrow.png').convert_alpha()
    arrows = pygame.transform.flip(arrow, False, True).convert_alpha()
    arrows = Animate(arrows, 1, 30,30).split_sprite()
    # Randomize the arrow starting positions.
    obstacle = Arrows(arrows,randint(1,709),randint(-200,0))
    # Add the arrows created into the sprite group to update eaasily.
    arrow_obstacles.add(obstacle)

# Check collisions between the arrows and the players.
# The arrows parameter takes in a sprite group.
def collision_check(player, arrows):
    original_hitbox = player.rect
    new_hitbox = pygame.Rect(original_hitbox.centerx-(original_hitbox.width*0.5)/2,
                             original_hitbox.top + original_hitbox.height*0.2,
                             original_hitbox.width*0.7,
                             original_hitbox.height*0.7)
    # Check the indiviual arrows within the group for collisions with the player.
    if any(new_hitbox.colliderect(arrow) for arrow in arrows):
            return True
    return False



# Frame rate
clock = pygame.time.Clock()

# -------------------------------- UserEvent---------------------------------
# Two different arrow spawn event to ensure arrows are not always overlapping.
respawn = pygame.USEREVENT + 1
respawn_2 = pygame.USEREVENT + 2
pygame.time.set_timer(respawn, 1000)
pygame.time.set_timer(respawn_2, 3000)
times = 1


# ---------------------------------END OF Game FUNCTIONS---------------------------------
game_ongoing = True
# Game loop
running = True
while running:
    # Run the game at 60 fps.
    clock.tick(60)
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # Stop the program when the user quits
        if event.type == pygame.QUIT:
            running = False
        # Spawn the event whenever the user event returns true
        if event.type == respawn:
            spawn_obstacles()
        if event.type == respawn_2:
            for i in range(curve_increase):
                print(curve_increase)
                spawn_obstacles()

    # As long game_ongoing is true, keep calling the classes and functions.
    if game_ongoing:
        arrow_obstacles.draw(screen)
        # Intizalize the arrow dropping speed to 15 pixels.
        arrow_obstacles.update(15)
        for arrow in arrow_obstacles:
            ## Remove any arrow from the reaches the surface of the background.
            ## Stop the game from continously rendering the arrow even after it cannot be seen on the screen.
            if arrow.rect.y > 600 - 15:
                arrow.kill()
        # Check for collsions between the player and the arrows and stop the game if it returns True.
        if collision_check(player, arrow_obstacles):
            game_ongoing = False
        time_elapsed = score()/1000
        # Increase difficulty curve as the game goes on.
        curve_increase = int(time_elapsed / 5)

        # Save the move_set returned from playformer_moveset() to check whether the player is moving left or right.
        move_set = player.platformer_moveset(11.5)
        # Call right moving sprite animation if moving right.
        if move_set[0] > 0:
            Knight_run()
        # Call left moving sprite animation if moving left.
        elif move_set[0] < 0:
            Knight_run_backwards()
        else:
        # Call idle moving sprite animation if no movement command is received.
            Knight_idle()
        player.start(screen)
        pygame.display.update()
