import pygame, random, time, sys
pygame.init()

# Global variables
WIDTH = 400
HEIGHT = 600
WHITE = 255, 255, 255
BLUE = 0, 0, 255
GREEN = 0, 255, 0
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
VIOLET = (255, 0, 255)
GB = (0, 255, 255)
DIFFICULTY = 'hard'
powerSpawn = None

death = pygame.mixer.Sound('resources/death.wav')
laser_shoot = [pygame.mixer.Sound('resources/sfx_laser1.ogg'), pygame.mixer.Sound('resources/sfx_laser2.ogg')]
theme_song = pygame.mixer.Sound('resources/theme.ogg')
hit = pygame.mixer.Sound('resources/hitmetal.ogg')

# Player variables
acceleration = 0.5
friction = -0.12
eacceleration = 0.7
gameRun = True

enemytypes = ["weak", "strong"]

font = pygame.font.Font('iomanoid front.ttf', 64)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(pygame.image.load('resources/assets/2.png'))
clock = pygame.time.Clock()
pygame.display.set_caption("SHOOTER")
fps = 60
vec = pygame.math.Vector2

# SpriteGroups
playerGroup = pygame.sprite.GroupSingle()
allSprites = pygame.sprite.Group()
platformGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
enemyBulletGroup = pygame.sprite.Group()
powerGroup = pygame.sprite.Group()
shieldGroup = pygame.sprite.Group()
lifeGroup = pygame.sprite.Group()

def game():
    running = True 

    while running:
        powerBar = pygame.Surface((30, player.powerHeight))
        powerBar.fill(GREEN)

        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.bullets != 0:
                    music = random.choice(laser_shoot)
                    music.play()
                    bulletGroup.add(Bullet(player.pos.x, player.rect.top))
                    player.bullets -= 1
            
        if len(enemyGroup) < enemySpawn:
            enemyGroup.add(Enemy(random.randint(20, 360), random.randint(-HEIGHT*2, 0), random.choice(enemytypes)))

        if len(powerGroup) < powerSpawn:
            if DIFFICULTY != 'easy':
                powerGroup.add(Bullet_PowerUP(random.randint(0,WIDTH), random.randint(-HEIGHT*2, 0)))

        if len(shieldGroup) < powerSpawn:
            shieldGroup.add(Shield_PowerUP(random.randint(0,WIDTH), random.randint(-HEIGHT*2, 0)))

        if len(lifeGroup) < lifeSpawn:
            if DIFFICULTY == 'hard':
                lifeGroup.add(Life_Powerup(random.randint(0, WIDTH), random.randint(random.randint(-(HEIGHT*3), -HEIGHT*2), 0)))
            else:
                lifeGroup.add(Life_Powerup(random.randint(0, WIDTH), random.randint(-HEIGHT*2, 0)))

        player.powerHeight = player.bullets * 10

        # Game events
        platform_hits = pygame.sprite.spritecollide(player, platformGroup, 0)
        player_hits = pygame.sprite.spritecollide(player, enemyBulletGroup, 1)
        Bullet_PowerUP_hits = pygame.sprite.spritecollide(player, powerGroup, True)
        enemy_plat_hits = pygame.sprite.groupcollide(enemyGroup, platformGroup, 1, 0)
        player_enemy_hits = pygame.sprite.spritecollide(player, enemyGroup, 0)
        life_hits = pygame.sprite.spritecollide(player, lifeGroup, 1)
        enemy_hit = pygame.sprite.spritecollide(player, enemyGroup, 1)

        if enemy_hit and not player.shield:
            player.life -= 1
            hit.play()

        if player_enemy_hits and  not player.shield:
            player.life -= 1
            hit.play()

        if life_hits:
            player.life += 1

        for shield in shieldGroup:
            if pygame.sprite.collide_rect(player, shield):
                player.shield = True
                shieldGroup.remove(shield)

        if enemy_plat_hits:
            player.score -= 1
            hit.play()

        if Bullet_PowerUP_hits and DIFFICULTY != 'easy':
            player.bullets += 10

        if player_hits and not player.shield:
            player.life -= 1
            hit.play()

        if platform_hits:
            player.pos.y = platform_hits[0].rect.top + 2
            player.vel.y = 0
            
        screen.fill((0, 0, 0))

        # Update srpitegroups
        allSprites.update()
        playerGroup.update()
        platformGroup.update()
        bulletGroup.update()
        enemyGroup.update()
        enemyBulletGroup.update()
        powerGroup.update()
        shieldGroup.update()
        lifeGroup.update()

        # Draw spritegroups
        allSprites.draw(screen)
        bulletGroup.draw(screen)
        playerGroup.draw(screen)
        platformGroup.draw(screen) 
        enemyGroup.draw(screen)
        enemyBulletGroup.draw(screen)
        powerGroup.draw(screen)
        shieldGroup.draw(screen)
        lifeGroup.draw(screen)

        if DIFFICULTY != 'easy':
            pygame.draw.rect(screen, GREEN, (20, 230, 10, -player.powerHeight))

        pygame.display.update()
