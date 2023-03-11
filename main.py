import pygame
from random import randint
#import time
pygame.init()

mw = pygame.display.set_mode((700, 500))

background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (700, 500))
pygame.display.set_caption("Shooter")
# pygame.mixer.music.load("space.ogg")
# pygame.mixer.music.play(-1)
fire = pygame.mixer.music.load("fire.ogg")

#local_time = float(1)
#local_time = local_time * 60
#time.sleep(local_time)

clock = pygame.time.Clock()
FPS = 120

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__()
        self.image = pygame.transform.scale(image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = x,y
        self.speed = speed
    def reset(self):
        mw.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    #def __init__(self,wight,hight,image,speed,x,y):
        #super().__init__
        def move(self):    
            k = pygame.key.get_pressed()
            if k[pygame.K_a] and self.rect.x >= 0:
                self.rect.x -= self.speed 
            if k[pygame.K_d] and self.rect.right <= 700:
                self.rect.x += self.speed
        def shoot(self):
            #if pygame.key.get_pressed()[pygame.K_w]:
            bullet2 = Bullet(self.rect.centerx-13,self.rect.y, 30,45,bullet_img,15)
            bullet4 = Bullet(self.rect.centerx-40,self.rect.y, 50,70,bullet_img,7)  
            bullet5 = Bullet(self.rect.centerx-5,self.rect.y, 50,70,bullet_img,7)
            bullets.add(bullet2)
            bullets.add(bullet4)
            bullets.add(bullet5)

class Enemy(GameSprite):
    def update(self):
        global lost1
        if self.rect.bottom <= 500:
            self.rect.y += self.speed
        else:
            player.lost += 1
            lost1 = font.render(f'Пропущено:{player.lost}',1,white)
            self.rect.y = randint(-150,-50)
            self.rect.x = randint(0,650)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -150:
            self.kill()

class Metheorite(GameSprite):
    def update(self):
        if self.rect.bottom <= 500:
            self.rect.y += self.speed           
        else:
            self.rect.y = randint(-150,-50)
            self.rect.x = randint(0,650)

bullet_img = pygame.image.load("laser.png")

player_img = pygame.image.load("discovery.png")
player = Player(0, 400, 90, 75, player_img, 5)
player.lost = 0
player.score = 0

font = pygame.font.SysFont('tahoma',32)
white = (255,255,255)
count = font.render('Рахунок:0',1,white)
lost1 = font.render('Пропущено:0',1,white)
new_game = font.render('Щоб грати знову натисни Enter',1,white)

font1 = pygame.font.SysFont('tahoma',80)
you_lose = font1.render('YOU LOSE!',1,white)
you_won = font1.render('YOU WON!',1,white)

enemies = pygame.sprite.Group()

enemy_img = pygame.image.load("ufo.png")
for i in range(7):
    enemy = Enemy(randint(0,650),randint(-150,-50), 100, 80, enemy_img, 1)
    enemies.add(enemy)

metheorites = pygame.sprite.Group()

metheorite_img = pygame.image.load("asteroid.png")
for i in range(3):
    metheorite = Metheorite(randint(0,650),randint(-150,-50), 70, 50, metheorite_img, 1)
    metheorites.add(metheorite)

bullets = pygame.sprite.Group()

game = True
finish = False
stop = False
while game:

    if not finish and not stop:
        mw.blit(background, (0,0))
        mw.blit(lost1,(5,7))
        mw.blit(count,(5,40))
        player.reset()
        player.move()
        
        enemies.draw(mw)
        enemies.update()
        metheorites.draw(mw)
        metheorites.update()
        bullets.draw(mw)
        bullets.update()

        for en in pygame.sprite.groupcollide(enemies, bullets, True, True):
            enemy = Enemy(randint(0,650),randint(-150,-50), 70, 50, enemy_img, 1)
            enemies.add(enemy)
            player.score += 1
            count = font.render(f'Рахунок:{player.score}',1,white)
        
        #for me in pygame.sprite.groupcollide(metheorites, bullets, True, True):
            #metheorite = Metheorite(randint(0,650),randint(-150,-50), 70, 50, metheorite_img, 1)
            #metheorites.add(metheorite)


        if player.lost >= 2 or len(pygame.sprite.spritecollide(player, enemies, False)) != 0 or len(pygame.sprite.spritecollide(player, metheorites, False)) != 0:
            mw.blit(you_lose,(170,190))
            mw.blit(new_game,(60,400))
            finish = True

        if player.score >= 1000:
            mw.blit(you_won,(170,190))
            mw.blit(new_game,(60,400))
            finish = True


    for ev in pygame.event.get():
        if not finish:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    player.shoot()
                #if ev.key == pygame.K_w:
                    #if stop == False:    
                        #stop == True
                    #if stop == True: 
                        #stop == False       
        else:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    finish = False
                    player.lost = 0
                    player.score = 0
                    count = font.render('Рахунок:0',1,white)
                    lost1 = font.render('Пропущено:0',1,white)
                    enemies.empty()
                    bullets.empty()
                    metheorites.empty()
                    for i in range(7):
                        enemy = Enemy(randint(0,650),randint(-150,-50), 70, 50, enemy_img, 1)
                        enemies.add(enemy)
                    for i in range(3):
                        metheorite = Metheorite(randint(0,650),randint(-150,-50), 70, 50, metheorite_img, 1)
                        metheorites.add(metheorite)

        if ev.type == pygame.QUIT:
            game = False
    pygame.display.update()
    clock.tick(FPS)