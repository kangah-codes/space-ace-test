from resources import *

# Making classes for game objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shield = False
        self.image = pygame.transform.scale(pygame.image.load('resources/assets/2.png'), (40, 50))
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        if DIFFICULTY == 'easy':
            self.life = 11
            self.copy_life = 10
        elif DIFFICULTY == 'normal':
            self.life = 8
            self.copy_life = 7
        else:
            self.life = 6
            self.copy_life = 5
        self.gameOver = False
        self.score = 0
        self.shield_timer = 0
        self.powerHeight = 100
        # Choosing number of bullets depending on difficulty
        if DIFFICULTY == 'easy':
            self.bullets = 20
        elif DIFFICULTY == 'normal':
            self.bullets = 20
        elif DIFFICULTY == 'hard':
            self.bullets = 10

    def update(self):
        if self.shield:
            self.image = pygame.transform.scale(pygame.image.load('resources/assets/4.png'), (40, 40))
        else:
            self.image = pygame.transform.scale(pygame.image.load('resources/assets/2.png'), (40, 40))

        if self.life >= 10:
            self.life = 10

        if DIFFICULTY == 'easy':
            if self.bullets <= 20:
                self.bullets = 20
            if self.shield:
                self.shield_timer += 1
                if self.shield_timer % 900 == 0:
                    self.shield = False
                    self.shield_timer = 0
        elif DIFFICULTY == 'normal':
            if self.bullets >= 20:
                self.bullets = 20
            if self.shield:
                self.shield_timer += 1
                if self.shield_timer % 700 == 0:
                    self.shield = False
                    self.shield_timer = 0
        elif DIFFICULTY == 'hard':
            if self.bullets >= 10:
                self.bullets = 10
            if self.shield:
                self.shield_timer += 1
                if self.shield_timer % 500 == 0:
                    self.shield = False
                    self.shield_timer = 0
            
        if self.life <= 0:
            self.gameOver = True
            self.life = 0
            
        self.acc = vec(0, 0.5)

        key = pygame.key.get_pressed()

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.acc.x = -acceleration

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.acc.x = acceleration

        if self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.x > WIDTH:
            self.pos.x = 0

        self.acc.x += self.vel.x * friction

        self.vel += self.acc
        self.pos += self.vel + acceleration * self.acc

        self.rect.midbottom = self.pos

class Bullet_PowerUP(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('resources/assets/91.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.spawnRate = 2
        self.acct = 0.5

    def update(self):
        self.acct += 0.01
        self.acc = vec(0, 0.5)
        self.pos += self.acct * self.acc
        self.rect.midbottom = self.pos
        if self.pos.y > HEIGHT:
            powerGroup.remove(self)

class Shield_PowerUP(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('resources/assets/shield_gold.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.spawnRate = 2
        self.acct = 0.5

    def update(self):
        self.acct += 0.01
        self.acc = vec(0, 0.5)
        self.pos += self.acct * self.acc
        self.rect.midbottom = self.pos
        if self.pos.y > HEIGHT:
            shieldGroup.remove(self)

class Life_Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('resources/assets/65.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.spawnRate = 2
        self.acct = 0.5

    def update(self):
        self.acct += 0.01
        self.acc = vec(0, 0.5)
        self.pos += self.acct * self.acc
        self.rect.midbottom = self.pos
        if self.pos.y > HEIGHT:
            lifeGroup.remove(self)
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.time = 0
        self.eneacc = 0.5
        self.life = None
        self.type = type
        if self.type == 'weak':
            self.image = pygame.transform.scale(pygame.image.load('resources/assets/3.png'), (40, 40))
            self.life = 1
        else:
            self.image = pygame.transform.scale(pygame.image.load('resources/assets/1.png'), (40, 40))
            if DIFFICULTY == 'easy':
                self.life = 2
            elif DIFFICULTY == 'normal':
                self.life = 3
            else:
                self.life = 4

    def update(self):
        if self.life <= 0:
            player.score += 1
            enemyGroup.remove(self)

        if DIFFICULTY != 'hard':
            self.eneacc += 0.01
        else:
            self.eneacc += 0.001
        self.acc = vec(0, 0.5)
        self.pos += self.eneacc * self.acc
        self.rect.midbottom = self.pos
        self.time += 1
        if self.time - last_shot >= 0 and self.pos.y >= 0:
            self.shoot()
        if pygame.sprite.spritecollide(self, bulletGroup, 1):
            self.life -= 1
            hit.play()

    def shoot(self):
        shot = random.choice(laser_shoot)
        shot.play()
        enemyBulletGroup.add(EnemyBullet(self.pos.x, self.rect.bottom-5))
        self.time = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height = 50):
        self.groups = allSprites, platformGroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.time = 0


    def update(self):
        for player in playerGroup:
            if player.life >= player.copy_life / 2:
                self.image.fill(GREEN)
            elif player.life > player.copy_life / 3 and player.life < player.copy_life / 2:
                self.image.fill(BLUE)
            else:
                self.image.fill(RED)
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale((pygame.image.load('resources/assets/pbullet.png')), (10, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 15

        if self.rect.y < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('resources/assets/ebullet.png'), (10, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 15

        if self.rect.y > HEIGHT:
            self.kill()

player = Player()
platform = Platform(0, HEIGHT-50, WIDTH)

playerGroup.add(player)
allSprites.add(player)

platformGroup.add(platform)
allSprites.add(platform)

enemySpawn = 0
checkspawn = 0
i = 0

if DIFFICULTY == "easy":
    enemySpawn = 5
    last_shot = 150
    powerSpawn = 2
    lifeSpawn = 2

elif DIFFICULTY == "normal":
    enemySpawn = 8
    last_shot = 100
    powerSpawn = 2
    lifeSpawn = 2

elif DIFFICULTY == "hard":
    enemySpawn = 12
    last_shot = 60
    powerSpawn = 2
    lifeSpawn = 3

def mainMenu():
    run = True

    name = font.render('Space Ace', True, (255, 255, 255))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                game()
                run = False
                sys.exit()
                
        screen.fill(BLACK)

        screen.blit(name, (WIDTH/2 - name.get_width()/2, 100))

        pygame.display.update()

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

if __name__ == "__main__":
    mainMenu()

