import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man Game")

# Define colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Create the game background
background = pygame.Surface(window.get_size())
background.fill(BLACK)

# Create Pac-Man character
pacman_radius = 15
pacman_pos = [width // 2, height // 2]  # Starting position of Pac-Man

# Create Ghost character
ghost_radius = 15
ghost_pos = [width // 4, height // 4]  # Starting position of the Ghost

# Create Dot properties
dot_radius = 5
dot_color = WHITE
dot_positions = [
    (100, 100), (200, 100), (300, 100), (400, 100), (500, 100), (600, 100), (700, 100),
    (100, 200), (200, 200), (300, 200), (400, 200), (500, 200), (600, 200), (700, 200),
    # Add more dot positions as desired
]

# Define scoring variables
score = 0
font = pygame.font.Font(None, 36)

# Load sound effects
dot_sound = pygame.mixer.Sound('dot_sound.wav')
collision_sound = pygame.mixer.Sound('collision_sound.wav')

# Load images
pacman_image = pygame.image.load('pacman_image.png')
ghost_image = pygame.image.load('ghost_image.png')

# Scale the images to the desired size
pacman_image = pygame.transform.scale(pacman_image, (2 * pacman_radius, 2 * pacman_radius))
ghost_image = pygame.transform.scale(ghost_image, (2 * ghost_radius, 2 * ghost_radius))

# Define variables for Pac-Man's movement
pacman_speed = 5
pacman_direction = [0, 0]


# Create Pac-Man character
def draw_pacman():
    window.blit(pacman_image, (pacman_pos[0] - pacman_radius, pacman_pos[1] - pacman_radius))


# Create Ghost character
def draw_ghost():
    window.blit(ghost_image, (ghost_pos[0] - ghost_radius, ghost_pos[1] - ghost_radius))


# Create Dot
def draw_dot(pos):
    pygame.draw.circle(background, dot_color, pos, dot_radius)


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman_direction = [0, -1]  # Move Pac-Man up
            elif event.key == pygame.K_DOWN:
                pacman_direction = [0, 1]  # Move Pac-Man down
            elif event.key == pygame.K_LEFT:
                pacman_direction = [-1, 0]  # Move Pac-Man left
            elif event.key == pygame.K_RIGHT:
                pacman_direction = [1, 0]  # Move Pac-Man right
            elif event.key == pygame.K_r:
                # Restart the game
                pacman_pos = [width // 2, height // 2]
                dot_positions = [...]
                score = 0

    # Update Pac-Man's position based on movement direction
    pacman_pos[0] += pacman_direction[0] * pacman_speed
    pacman_pos[1] += pacman_direction[1] * pacman_speed

    # Handle screen wrapping
    if pacman_pos[0] < 0:
        pacman_pos[0] = width
    elif pacman_pos[0] > width:
        pacman_pos[0] = 0
    if pacman_pos[1] < 0:
        pacman_pos[1] = height
    elif pacman_pos[1] > height:
        pacman_pos[1] = 0

    # Check collision between Pac-Man and Ghost
    if (abs(pacman_pos[0] - ghost_pos[0]) < pacman_radius + ghost_radius) and (
        abs(pacman_pos[1] - ghost_pos[1]) < pacman_radius + ghost_radius):
        # Handle collision (game over, score update, etc.)
        print("Game Over")
        pygame.time.wait(2000)  # Pause for 2 seconds before restarting
        # Reset game state
        pacman_pos = [width // 2, height // 2]
        dot_positions = [...]
        score = 0
        collision_sound.play()  # Play collision sound effect

    # Check collision between Pac-Man and Dots
    for dot_pos in dot_positions:
        if (abs(pacman_pos[0] - dot_pos[0]) < pacman_radius + dot_radius) and (abs(pacman_pos[1] - dot_pos[1]) < pacman_radius + dot_radius):
            dot_positions.remove(dot_pos)
            score += 10  # Increment score by 10 for each consumed dot
            dot_sound.play()  # Play dot consumption sound effect

    # Draw game elements
    window.blit(background, (0, 0))
    draw_pacman()
    draw_ghost()
    for dot_pos in dot_positions:
        draw_dot(dot_pos)

    # Draw score on the game screen
    score_text = font.render("Score: " + str(score), True, YELLOW)
    window.blit(score_text, (10, 10))

    # Update game display
    pygame.display.update()
