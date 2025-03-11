import pygame
from sys import exit
from random import randint

# pygame
pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
dt = 0
laser_active = False
test_font = pygame.font.Font("graphics/Pixeltype.ttf", 50)
pygame.display.set_caption("Galaga Trek")

# Player 
ship_surf = pygame.image.load("galaga/ship.png").convert_alpha()
ship_surf = pygame.transform.rotozoom(ship_surf, 90, 0.15)
ship_rect = ship_surf.get_rect(center=(300, 700))
ship_laser_surf = pygame.image.load("galaga/laser.png")
ship_laser_surf = pygame.transform.scale(ship_laser_surf, (100, 100 ))
ship_laser_rect = ship_laser_surf.get_rect(midbottom=ship_rect.midbottom)
ship_laser_cooldown = 0
torpedo_list = []
ship_health = 100
Alive = True
score = 0

bg_surf = pygame.image.load('galaga/background.JPG')

# Enemies
bop_surf = pygame.image.load("galaga/enemy.png").convert_alpha()
bop_surf = pygame.transform.rotozoom(bop_surf, 180, 0.1)
borg_surf = pygame.image.load("galaga/borg.png").convert_alpha()
borg_surf = pygame.transform.rotozoom(borg_surf, 0, 0.1)
death_timer = 0

class Enemy:
    def __init__(self, surface, x, y, is_borg=False):
        self.surf = surface
        self.rect = self.surf.get_rect(center=(x, y))
        self.is_borg = is_borg
        self.hit_points = 2 if is_borg else 1 

enemy_list = []

def create_enemy():
    x_pos = randint(50, 550)
    y_pos = randint(-150, -50)

    if randint(0, 100) < 65:
        enemy = Enemy(bop_surf, x_pos, y_pos)
    else:
        enemy = Enemy(borg_surf, x_pos, y_pos, is_borg=True)
    
    enemy_list.append(enemy)

def move_enemies():
    global ship_health
    global Alive
    for enemy in enemy_list:
        enemy.rect.y += 2 
        if enemy.rect.y >= 800:
            if enemy.is_borg:
                ship_health -= 20
                enemy_list.remove(enemy)
            else:
                ship_health -= 10
                enemy_list.remove(enemy)
            if ship_health <= 0:
                Alive = False
                pygame.quit()
                exit()

def draw_enemies():
    global score
    for enemy in enemy_list[:]:
        screen.blit(enemy.surf, enemy.rect)

        for torpedo in torpedo_list[:]:
            if enemy.rect.colliderect(torpedo.rect):
                if enemy.is_borg:
                    enemy.hit_points -= 1
                    if enemy.hit_points <= 0:
                        enemy_list.remove(enemy) 
                        torpedo_list.remove(torpedo)
                        score += 20

                        break 
                    else:
                        torpedo_list.remove(torpedo)
                else:
                    enemy_list.remove(enemy) 
                    torpedo_list.remove(torpedo)
                    score += 10
                    break  

class Torpedo:
    def __init__(self, x, y, surface):
        self.surf = surface
        self.rect = self.surf.get_rect(center=(x, y))

    def move(self):
        self.rect.y -= 10  

def fire_torpedo():
    for torpedo in torpedo_list:
        torpedo.move() 
        screen.blit(torpedo.surf, torpedo.rect)

while True:
    while Alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(bg_surf, (0, 0)) 
        ship_laser_rect = ship_laser_surf.get_rect(midbottom=ship_rect.center)

        if ship_laser_cooldown < 100:
            ship_laser_cooldown += 2

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            ship_rect.x -= 300 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            ship_rect.x += 300 * dt
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and ship_laser_cooldown == 100:
            torpedo = Torpedo(ship_rect.centerx, ship_rect.top, ship_laser_surf)
            torpedo_list.append(torpedo)
            ship_laser_cooldown = 0

        if ship_rect.left <= 5:
            ship_rect.left = 5
        if ship_rect.right >= 595:
            ship_rect.right = 595
        if randint(0, 1000) < 15:
            create_enemy()

        move_enemies()
        draw_enemies()

        screen.blit(ship_surf, ship_rect)

        fire_torpedo()

        laser_charge_surf = test_font.render("Laser Charge: " + str(int(ship_laser_cooldown / 10)), False, "White")
        laser_charge_rect = laser_charge_surf.get_rect(midright = (600, 775))
        screen.blit(laser_charge_surf, laser_charge_rect)

        health_surf = test_font.render("Health: " + str(ship_health), False, "White")
        health_rect = laser_charge_surf.get_rect(midleft = (10, 775))
        screen.blit(health_surf, health_rect)

        score_surf = test_font.render("Score: " + str(score), False, "White")
        score_rect = score_surf.get_rect(topleft = (10, 5))
        screen.blit(score_surf, score_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
