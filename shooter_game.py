from pygame import *
from random import randint

#-------------------НАСТРОЙКИ-------------------#
window = display.set_mode((700, 500))
display.set_caption('Шутер')
mixer.init()
mixer.music.load('space.ogg')
shoot = mixer.Sound('fire.ogg')
#mixer.music.play()
#-------------------НАСТРОЙКИ-------------------#

#-------------------КЛАССЫ-------------------#
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        shoot.play()
        bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.top, 15, 25, 3)
        bullets.add(bullet)
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 435:
            lost = lost + 1
            self.rect.y = 0
            self.rect.x = randint(0, 700)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 435:
            self.rect.y = 0
            self.rect.x = randint(0, 700)
#-------------------КЛАССЫ-------------------#

#-------------------ПЕРЕМЕННЫЕ-------------------#
background = transform.scale(image.load('galaxy.jpg'),(700, 500))
clock = time.Clock()
FPS = 60
game = True
finish = False
player = Player('rocket.png', 100, 400, 70, 100, 15)
enemy = Enemy('ufo.png', randint(0, 700), 100, 100, 65, 0.5)
asteroid = Asteroid('asteroid.png', randint(0, 700), 100, 100, 65, 1)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range (5):
    enemy = Enemy('ufo.png', randint(0, 640), -100, 100, 65, randint(1, 3))
    monsters.add(enemy)
for i in range (3):
    asteroid = Asteroid('asteroid.png', randint(0, 640), -100, 100, 65, randint(1, 2))
    asteroids.add(asteroid)
font.init()
font1 = font.Font(None, 36)
font_game = font.Font(None, 70)
font_life = font.Font(None, 70)
score_number = 0
bullet_count = 0
ticks = 0
life = 3
is_fire = True
win = font_game.render('YOU WIN!', True, (255, 215, 0))
lose = font_game.render('YOU LOSE!', True ,( 255, 50, 10))
#-------------------ПЕРЕМЕННЫЕ-------------------#

#-------------------ЦИКЛ-------------------#
while game:
    if finish != True:
        window.blit(background, (0,0))
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for monster in sprite_list:
            score_number += 1
            enemy = Enemy('ufo.png', randint(0, 635), -  100, 100, 65, randint(1,5))
            monsters.add(enemy)
        if lost >= 3:
            window.blit(lose, (250, 250))
            finish = True
        if sprite.spritecollide(player, monsters, True):
            enemy = Enemy('ufo.png', randint(0, 635), -  100, 100, 65, randint(1,5))
            monsters.add(enemy)
            life = life - 1
            if life <= 0:
                window.blit(lose, (250, 250))
                finish = True
        if sprite.spritecollide(player, asteroids, True):
            asteroid = Asteroid('asteroid.png', randint(0, 640), -100, 100, 65, randint(1, 2))
            asteroids.add(asteroid)
            life = life - 1
            if life <= 0:
                window.blit(lose, (250, 250))
                finish = True
        if score_number >= 10:
            window.blit(win, (250, 250))
            finish = True

        ticks = ticks + 1
        player.update()
        player.reset()
        bullets.update()
        asteroids.update()
        asteroids.draw(window)
        bullets.draw(window) 
        if life == 3:
            life_score = font_life.render(str(life), True, (0, 60, 0))
        if life == 2:
            life_score = font_life.render(str(life), True, (0, 0, 60))
        if life == 1:
            life_score = font_life.render(str(life), True, (100, 10, 10))
        score = font1.render('Счёт: ' + str(score_number), True, (255, 255, 255))
        skipped = font1.render('Пропущено: ' + str(lost), True ,( 255, 255, 255))
        window.blit(life_score, (650, 450))
        window.blit(score, (10, 20))
        window.blit(skipped, (10, 50))
        monsters.draw(window)
        monsters.update()
        if bullet_count == 10:
            reloadd = font1.render('Waiting reload!', True, (255, 10, 10))
            window.blit(reloadd, (250, 470))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and is_fire:
                player.fire()
                bullet_count += 1
                if bullet_count == 10:
                    reloadd = font1.render('Waiting reload!', True, (255, 10, 10))
                    window.blit(reloadd, (350, 450))
                    is_fire = False
    if ticks >= 180:
        ticks = 0
        bullet_count = 0
        is_fire = True
    clock.tick(FPS)
    display.update()
#-------------------ЦИКЛ-------------------#