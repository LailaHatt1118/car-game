import pygame
from pygame.locals import *
import random

pygame.init()

# Create the window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# Colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)
blue = (0, 0, 255)
orange = (255, 165, 0)
purple = (128, 0, 128)

# Road and marker sizes
road_width = 300
marker_width = 10
marker_height = 50

# Lane coordinates
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# Road and edge markers
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# Lane marker movement
lane_marker_move_y = 0

# Player's starting coordinates
player_x = 250
player_y = 400

# Frame settings
clock = pygame.time.Clock()
fps = 120

# Game settings
gameover = False
speed = 2
score = 0

# Vehicle class
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Create a simple rectangle car
        self.image = pygame.Surface((45, 80))
        self.image.fill(color)
        
        # Add some details (windows)
        pygame.draw.rect(self.image, white, (5, 10, 35, 25))
        pygame.draw.rect(self.image, white, (5, 45, 35, 25))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# PlayerVehicle class
class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        # Player car is blue
        super().__init__(blue, x, y)

# Sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Create the player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Vehicle colors for enemy cars
vehicle_colors = [red, orange, purple, yellow]

# Game loop
running = True
while running:
    clock.tick(fps)

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

    # Draw background
    screen.fill(green)

    # Draw the road
    pygame.draw.rect(screen, gray, road)
     
    # Draw edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # Draw lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    # Draw the player's car
    player_group.draw(screen)

    # Add a vehicle
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
        if add_vehicle:
            lane = random.choice(lanes)
            color = random.choice(vehicle_colors)
            vehicle = Vehicle(color, lane, -100)
            vehicle_group.add(vehicle)

    # Move vehicles
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1
            if score > 0 and score % 5 == 0:
                speed += 1

    # Draw vehicles
    vehicle_group.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, white)
    screen.blit(text, (10, 10))

    # Check for collisions
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        # Draw crash effect
        pygame.draw.circle(screen, red, player.rect.center, 40)
        pygame.draw.circle(screen, yellow, player.rect.center, 30)

    # Display game over
    if gameover:
        font = pygame.font.Font(None, 34)
        text = font.render('Game Over! Press Y to Restart or N to Quit', True, red)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        
        # Draw semi-transparent background for text
        overlay = pygame.Surface((width, 50))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, height // 2 - 25))
        screen.blit(text, text_rect)
        
        pygame.display.update()

        # Wait for input
        while gameover:
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameover = False
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        # Restart game
                        gameover = False
                        speed = 2
                        score = 0
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                    elif event.key == K_n:
                        gameover = False
                        running = False

    pygame.display.update()

pygame.quit()