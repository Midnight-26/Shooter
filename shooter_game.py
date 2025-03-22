#Создай собственный Шутер!

from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < W - 85:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y +=self.speed
        if self.rect.y > H:
            self.rect.y = 0 
            self.rect.x = randint(80, W-80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill


W = 700
H = 500
window = display.set_mode((W, H))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"), (W, H))


clock = time.Clock()
FPS = 60 

score = 0 #кол-во очков
lost = 0 #кол-во пропущенных

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')


font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 60)
text_win = font2.render('You win', True, (0, 255, 0))
text_lose = font2.render('You lose', True, (255, 0 ,0))

score = 0
goal = 10
lost = 0
max_lost = 3
num_fire = 0

ship = Player("rocket.png",W//2, H-110, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(80, W - 80), -40, 80, 50, randint(1,3))
    monsters.add(monster)

bullets = sprite.Group()




game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if finish != True:
        window.blit(background, (0, 0))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)

        bullets.draw(window)


        collides = sprite.groupcollide(bullets, monsters , True, True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, W - 80), -40, 80, 50, randint(1, 4))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True 
            window.blit(text_lose, (240, 200))

        if score >= goal:
            finish = True
            window.blit(text_win, (240, 200))
         
        

        text_score = font1.render("Счёт: " + str(score), 1, (255, 255, 255))
        text_lost = font1.render("Пропущено: "+ str(lost), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))

        

        display.update()
    clock.tick(FPS)

