import pygame
import sys
import random


pygame.init()

window = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
foreground = (200, 200, 200)
background = (0, 0, 0)
ship_image = pygame.image.load("ship_normal.png")
bullet_image = pygame.image.load("bullet.png")
ship_image_up = pygame.image.load("ship_up.png")
ship_image_down = pygame.image.load("ship_down.png")
alien_image = pygame.image.load("alien_1.png")
alien_dead_image = pygame.image.load("alien_1_dead.png")
ship_image_destroyed = pygame.image.load("ship_destroyed.png")
gameover = pygame.image.load("gameover.png")
shoot = pygame.mixer.Sound("shoot.wav")


class Sprite:
    pass

def display_sprite(sprite):
    window.blit(sprite.image, (sprite.x, sprite.y))
    
ship = Sprite()
ship.x = 0
ship.y = 0
ship.red = 0
ship.alpha = 0
ship.image = ship_image
lives = 3
score = 0

bullets = []
aliens = []
stars = []

frames_until_next_alien = 50
frames_until_next_star = 0

for bullet in bullets:
    display_sprite(bullet)

def fire_bullet():
    bullet = Sprite()
    bullet.x = ship.x + 130
    bullet.y = ship.y + 100
    bullet.image = bullet_image
    bullet.used = False
    bullets.append(bullet)
def add_alien():
    alien = Sprite()
    alien.x = window.get_width()
    alien.y = random.randrange(100, window.get_height() - 100)
    alien.image = alien_image
    alien.hit = False
    alien.alpha = 255
    aliens.append(alien)
def add_star():
    star = Sprite()
    star.x = window.get_width()
    star.y = random.randrange(10, window.get_height() - 10)
    star_size = random.randrange(1, 4)
    star.image = pygame.Surface((star_size, star_size))
    star.image.fill((255, 255, 255))
    stars.append(star)
def get_sprite_rectangle(sprite):
    return sprite.image.get_rect().move(sprite.x, sprite.y)    
running=1
exitcode=0
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
            
            
    ship.image = ship_image        
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_UP]:
        ship.image = ship_image_up
        ship.y = ship.y - 10

    if pressed_keys[pygame.K_DOWN]:
        ship.image = ship_image_down
        ship.y = ship.y + 10

    if pressed_keys[pygame.K_LEFT]:
        ship.x = ship.x - 10

    if pressed_keys[pygame.K_RIGHT]:
        ship.x = ship.x + 10
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            shoot.play()
            fire_bullet()
    for bullet in bullets:
        bullet.x = bullet.x + 13

    bullets = [bullet for bullet in bullets if bullet.x < window.get_width() and not bullet.used]          
    
             
    frames_until_next_alien = frames_until_next_alien - 1
    if frames_until_next_alien <= 0:
        frames_until_next_alien = random.randrange(30, 100)
        add_alien()

    for alien in aliens:
        alien.x = alien.x - 3
        if alien.hit:
            alien.alpha = max(0, alien.alpha - 10)

    aliens = [alien for alien in aliens if alien.x > - alien_image.get_width() and not (alien.hit and alien.alpha == 0) ]

    frames_until_next_star = frames_until_next_star - 1
    if frames_until_next_star <= 0:
        frames_until_next_star = random.randrange(10, 30)
        add_star()

    for star in stars:
        star.x = star.x - 2

    stars = [star for star in stars if star.x > - 10]

    for alien in aliens:
        if alien.hit:
            continue
        alien_rect = get_sprite_rectangle(alien)
        if alien_rect.colliderect(ship_rect) and lives > 0:
            alien.hit = True
            alien.x = alien.x - 6
            alien.y = alien.y - 6
            lives = lives - 1
            if lives == 0:
                ship.x = ship.x - 50
                ship.alpha = 255
                
                
            else:
                ship.red = 255
            
            continue
        for bullet in bullets:
            if alien_rect.colliderect(get_sprite_rectangle(bullet)):
                alien.hit = True
                alien.x = alien.x - 6
                alien.y = alien.y - 6
                bullet.used = True
                score = score + 10
                continue

    window.fill(background)
    if lives==0:
        

    
        
        
        tmp = pygame.Surface(ship_image_destroyed.get_size(), pygame.SRCALPHA, 32)
        tmp.fill( (255, 255, 255, ship.alpha) )
        tmp.blit(ship_image_destroyed, (0,0), ship_image_destroyed.get_rect(), pygame.BLEND_RGBA_MULT)
        ship.image = tmp
        
        
        
        
        
    
        
        

    if ship.red > 0:
        tmp = pygame.Surface(ship.image.get_size(), pygame.SRCALPHA, 32)
        tmp.fill( (255, 255 - ship.red, 255 - ship.red, 255) )
        tmp.blit(ship.image, (0,0), ship.image.get_rect(), pygame.BLEND_RGBA_MULT)
        ship.image = tmp
        
        
        
    display_sprite(ship)
    
    
    for bullet in bullets:
        display_sprite(bullet)
    ship.red = max(0, ship.red - 10)
    ship.alpha = max(0, ship.alpha - 2)
    ship_rect = get_sprite_rectangle(ship)
    for alien in aliens:
        if alien.hit:
            tmp = pygame.Surface( alien_dead_image.get_size(), pygame.SRCALPHA, 32)
            tmp.fill( (255, 255, 255, alien.alpha) )
            tmp.blit(alien_dead_image, (0,0), alien_dead_image.get_rect(), pygame.BLEND_RGBA_MULT)
            alien.image = tmp
        display_sprite(alien)
    for star in stars:
        display_sprite(star)     

    # Stop ship going out of bounds
    if ship.y < 0:
        ship.y = 0

    if ship.y > window.get_height() - ship_image.get_height():
        ship.y = window.get_height() - ship_image.get_height()

    if ship.x < 0:
        ship.x = 0

    if ship.x > window.get_width() - ship_image.get_width():
        ship.x = window.get_width() - ship_image.get_width()
        
    score_text = font.render("SCORE: " + str(score), 1, foreground)
    score_text_pos = score_text.get_rect()
    score_text_pos.right = window.get_width() - 10
    score_text_pos.top = 10
    window.blit(score_text, score_text_pos)
    lives_text = font.render("LIVES: " + str(lives), 1, foreground)
    window.blit(lives_text, (10, 10))

        
        
        
    pygame.display.flip()
        
    clock.tick(50)
    
   

    

