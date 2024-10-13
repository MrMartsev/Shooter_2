
from pygame import *
from random import randint
import linecache

font.init()

font_1 = font.SysFont('Arial', 36)
font_2 = font.SysFont('Arial', 36)

_time_ = 0

                  
x = 0
init()
missed = 0
killed = 0

display.set_caption("Шутер 666")

win_width = 600
win_height = 700

window = display.set_mode((win_width, win_height))
clock = time.Clock()

background = transform.scale(image.load('30.jpg'), (win_width, win_height))
lvl_fone = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))


  
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

line = linecache.getline(r"C:\Program Files\Algoritmika\vscode\data\extensions\algoritmika.algopython-20240404.120101.0\data\student\1715184\184431\open_levels.txt", 5)
data = line.split(' ')
volume = float(data[0])

mixer.music.set_volume(volume)

finish = True

class Area():
    def __init__(self, x, y, width, heigh, color):
        self.rect = Rect(x, y, width, heigh)
        self.fill_color = color
    def set_color(self, color):
        self.fill_color = color
    def outline(self, frame_color=(0, 0, 0), thickness=10):
        draw.rect(window, frame_color, self.rect, thickness)
    def fill(self):
        draw.rect(window, self.fill_color, self.rect)
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Label(Area):
    def set_text(self, text, fsize, text_color=(0, 0, 0)):
        self.text = text
        self.font1 = font.SysFont("Comic Sans", fsize)
        self.image = self.font1.render(text, True, text_color)
    def draw(self, shift_x, shift_y):
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_height, wall_width, wall_x, wall_y):
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.height = wall_height
        self.width = wall_width
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_w, player_h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class GameSprite_Maze(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player_Maze(GameSprite_Maze):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed 
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed 
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed 

class Enemy_Maze(GameSprite_Maze):
    def update(self, _type_, x1, y1):
        if _type_ == "x":
            if self.rect.x <= x1:
                self.direction = "right"
            if self.rect.x >= y1:
                self.direction = "left"

            if self.direction == "left":
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

        if _type_ == "y":
            if self.rect.y >= x1:
                self.direction = "up"
            if self.rect.y <= y1:
                self.direction = "down"

            if self.direction == "up":
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed

sprite3 = GameSprite_Maze('house.png', win_width - 120, win_height - 80, 0)
sprite1 = Player_Maze('Photo.png', 20, win_height - 140, 5)
sprite2 = Enemy_Maze('Police.png', win_width - 80, 280, 2)
sprite4 = Enemy_Maze('Police.png', win_width - 200, 150, 2)
sprite5 = Enemy_Maze('Police.png', win_width - 375, 350, 1)


w1 = Wall(19, 0, 189, 10, 300, 100, 100)
w2 = Wall(19, 0, 189, 300, 10, 100, 100)
w3 = Wall(19, 0, 189, 250, 10, 200, 200)
w4 = Wall(19, 0, 189, 250, 10, 300, 100)
w5 = Wall(19, 0, 189, 10, 200, 200, 450)

w6 = Wall(19, 0, 189, 160, 10, 400, 300)
w12 = Wall(19, 0, 189, 10, 100, 400, 300)

w7 = Wall(19, 0, 189, 70, 10, 400, 40)
w8 = Wall(19, 0, 189, 10, 250, 400, 40)
w9 = Wall(19, 0, 189, 260, 10, 650, 40)
w10 = Wall(19, 0, 189, 250, 10, 500, 200)
w11 = Wall(19, 0, 189, 10, 100, 400, 200)

walls = [w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12]

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed 

class Enemy(GameSprite):
    def __init__(self, enemy_image, enemy_x, enemy_y, enemy_speed, enemy_hp):
        
        self.image = transform.scale(image.load(enemy_image), (55, 55))
        self.speed = enemy_speed
        self.rect = self.image.get_rect()
        self.rect.x = enemy_x
        self.rect.y = enemy_y
        self.hp = enemy_hp

    def update(self):
        self.rect.y += self.speed 
        
        global missed
        
        if self.rect.y >= 700:
            self.rect.y = 0
            self.rect.x = randint(25, 550)
            self.speed = (randint(2,6))
            
            missed += 1


class Bullet(GameSprite):
    def __init__(self, bullet_image, bullet_x, bullet_y, bullet_speed):
        
        self.image = transform.scale(image.load(bullet_image), (20, 20))
        self.speed = bullet_speed
        self.rect = self.image.get_rect()
        self.rect.x = rocket.rect.x
        self.rect.x = bullet_x
        self.rect.y = bullet_y

    def update(self):
        self.rect.y -= self.speed 

def wait_for_key_press(time_win, missed):
    wait = True
    while wait:
        text_rules = font_2.render('Победа: продержатся ' + str(time_win) + ' секунд.', True, (255, 255, 255))
        window.blit(text_rules, (25, 300))

        text_rules1 = font_2.render('Поражение: пропустить ' + str(missed) + ' НЛО', True, (255, 255, 255))
        window.blit(text_rules1, (25, 350))

        text_rules2 = font_2.render('Нажмите любую кнопку,', True, (255, 255, 255))
        window.blit(text_rules2, (25, 400))

        text_rules2 = font_2.render('чтобы начать', True, (255, 255, 255))
        window.blit(text_rules2, (25, 450))

        display.update() 
        for e in event.get():
            if e.type == KEYDOWN:
                wait = False
                break
        
rocket = Player("rocket.png", 300, 625, 55, 55, 4)

buttons = list()

button_1 = GameSprite("button1.png", 100, 400, 110, 110, 0)
buttons.append(button_1)

button_2 = GameSprite("button2_off.png", 250, 400, 110, 110, 0)
button_2_on = GameSprite("button2_on.png", 250, 400, 110, 110, 0)
buttons.append(button_2)

button_3 = GameSprite("button3_off.png", 400, 400, 110, 110, 0)
button_3_on = GameSprite("button3_on.png", 400, 400, 110, 110, 0)
buttons.append(button_3)

button_4 = GameSprite("button4_off.png", 100, 400, 110, 110, 0)
button_4_on = GameSprite("button4_on.png", 100, 400, 110, 110, 0)
buttons.append(button_4)

button_5 = GameSprite("button2_off.png", 250, 400, 110, 110, 0)
button_5_on = GameSprite("button2_on.png", 250, 400, 110, 110, 0)
buttons.append(button_5)


button_Left = GameSprite("Arrow_Left.png", 210, 550, 66, 50, 0)
button_Right = GameSprite("Arrow_Right.png", 340, 550, 66, 50, 0)

button_exit = GameSprite("Exit.png", 134, 500, 332, 82, 0)

button_settings = GameSprite("settings.png", 440, 50, 110, 110, 0)
progress_button = GameSprite("progress_button.png", 175, 500, 250, 103, 0)

plus_volume = GameSprite("plus_.png", 325, 325, 80, 80, 0)
minus_volume = GameSprite("minus_.png", 195, 325, 80, 80, 0)

mob_hp = 1

monster = Enemy("ufo.png", randint(25, 550), 0, randint(1,4), 0)

bullets = list()

bullet = Bullet("bullet.png", 900, 500, 0)
bullets.append(bullet)

game = True

menu_1 = True
lvl_1 = False
lvl_2 = False
lvl_3 = False
lvl_4 = False

lvl_5 = False

menu_2 = False

menu_settings = False

time_win = 52
lose = 52
cur_lvl = 0
wait_counter = 1

monsters = list()
def mob_spawn(hp, speed_min, speed_max):
    for i in range(5):  
        monster = Enemy("ufo.png", randint(25, 550), 0, randint(speed_min, speed_max), hp)
        monsters.append(monster)


file = open("open_levels.txt", "r", encoding='utf-8')
line = linecache.getline(r"C:\Program Files\Algoritmika\vscode\data\extensions\algoritmika.algopython-20240404.120101.0\data\student\1715184\184431\open_levels.txt", 1)
data = line.split(' ')
data_stud = int(data[1])
if data_stud == 1:
    button_2 = button_2_on
    
line = linecache.getline(r"C:\Program Files\Algoritmika\vscode\data\extensions\algoritmika.algopython-20240404.120101.0\data\student\1715184\184431\open_levels.txt", 2)
data = line.split(' ')
data_stud = int(data[1])
if data_stud == 1:
    button_3 = button_3_on

line = linecache.getline(r"C:\Program Files\Algoritmika\vscode\data\extensions\algoritmika.algopython-20240404.120101.0\data\student\1715184\184431\open_levels.txt", 3)
data = line.split(' ')
data_stud = int(data[1])
if data_stud == 1:
    button_4 = button_4_on  

line = linecache.getline(r"C:\Program Files\Algoritmika\vscode\data\extensions\algoritmika.algopython-20240404.120101.0\data\student\1715184\184431\open_levels.txt", 4)
data = line.split(' ')
data_stud = int(data[1])
if data_stud == 1:
    button_5 = button_5_on 

file.close()

while game:    
    if menu_1 == True:
        window.blit(background, (0,0))
        button_1.reset()
        button_2.reset()
        button_3.reset()

        button_Left.reset()
        button_Right.reset()

        button_settings.reset()

        text_Page = font_2.render('1/2', True, (0, 0, 0))
        window.blit(text_Page, (286, 555))

    if menu_2 == True:
        window.blit(background, (0,0))

        button_4.reset()
        button_5.reset()

        button_Left.reset()
        button_Right.reset()

        button_settings.reset()

        text_Page = font_2.render('2/2', True, (0, 0, 0))
        window.blit(text_Page, (286, 555))

    if menu_settings == True:
        window.blit(background, (0,0))
        
        progress_button.reset()
        button_settings.reset()
        
        text_volume = font_2.render('Изменение громкости:', True, (255, 255, 255))
        window.blit(text_volume, (150, 280))
        
        plus_volume.reset()
        minus_volume.reset()


    for e in event.get():
        if e.type == QUIT:
            
            game = False

        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            if button_1.collidepoint(x, y) and menu_1 == True:
                menu_1 = False
                lvl_1 = True
                mob_spawn(1, 1, 4)
                finish = False

                wait_counter = 0

            if button_2 == button_2_on:
                if button_2.collidepoint(x, y) and menu_1 == True:
                    menu_1 = False
                    lvl_2 = True
                    mob_spawn(2, 1, 5)
                    finish = False
                
                    wait_counter = 0


            if button_3 == button_3_on:
                if button_3.collidepoint(x, y) and menu_1 == True:
                    menu_1 = False
                    lvl_3 = True
                    mob_spawn(2, 2, 5)
                    finish = False

                    wait_counter = 0
                
            if button_4 == button_4_on:
                if button_4.collidepoint(x, y) and menu_2 == True:
                    menu_2 = False
                    lvl_4 = True
                    mob_spawn(3, 2, 6)
                    finish = False

                    wait_counter = 0

            if button_5 == button_5_on:
                if button_5.collidepoint(x, y) and menu_2 == True:
                    menu_2 = False
                    lvl_5 = True
                    
                    finish = False
            
            if button_Right.collidepoint(x, y) and menu_2 == False:
                    menu_1 = False
                    menu_2 = True
                    button_1.kill()
                    button_2.kill()
                    button_3.kill()

            if button_Left.collidepoint(x, y) and menu_1 == False:
                    menu_1 = True
                    menu_2 = False
                    button_4.kill()
                    button_5.kill()

            if button_settings.collidepoint(x, y):
                    if menu_1 == True:
                        menu_1 = False
                        menu_2 = False
                        menu_settings = True
                        cur_menu = 1

                    elif menu_2 == True:
                        menu_1 = False
                        menu_2 = False
                        menu_settings = True
                        cur_menu = 2
                    
                    else:
                        menu_settings = False
                        if cur_menu == 1:
                            menu_1 = True
                        if cur_menu == 2:
                            menu_2 = True

            if plus_volume.collidepoint(x, y):
                volume += 0.1
                mixer.music.set_volume(volume)

            if minus_volume.collidepoint(x, y):
                volume -= 0.1
                mixer.music.set_volume(volume)

            if menu_settings == True:
                if progress_button.collidepoint(x, y):
                    with open("open_levels.txt", "w", encoding='utf-8') as file:
                        file.write("Lvl_2 0"+"\n"+"Lvl_3 0"+"\n"+"Lvl_4 0"+"\n"+"Lvl_5 0"+"\n"+str(volume))
                        
                    button_2 = GameSprite("button2_off.png", 250, 400, 110, 110, 0)
                    button_3 = GameSprite("button3_off.png", 400, 400, 110, 110, 0)
                    button_4 = GameSprite("button4_off.png", 100, 400, 110, 110, 0)
                    button_5 = GameSprite("button2_off.png", 250, 400, 110, 110, 0)        
                    
    for monster in monsters:
        for bullet in bullets:
            if bullet.rect.colliderect(monster.rect):
                monster.hp -= 1
                if monster.hp == 0:
                    monsters.remove(monster)
                    y = randint(1, 10)
                    if y == 10:
                        monster = Enemy("ufo.png", randint(25, 550), 0, 6, 5)
                    else:
                        monster = Enemy("ufo.png", randint(25, 550), 0, mob_speed, mob_hp)
                    monsters.append(monster)
                    killed += 1
                
                bullets.remove(bullet)
                


    if finish != True:
        window.blit(lvl_fone, (0,0))

        if lvl_1 == True or lvl_2 == True or lvl_3 == True or lvl_4 == True: 
            text_missed = font_2.render('Пропущено: ' + str(missed), True, (255, 255, 255))
            window.blit(text_missed, (25, 50))
                
            text_killed = font_2.render('Убито: ' + str(killed), True, (255, 255, 255))
            window.blit(text_killed, (25, 100))

            text_time = font_1.render('Время: ' + str(_time_) + '.' + str(x), True, (255, 255, 255))
            window.blit(text_time, (350, 50))

        for button in buttons:
            button.kill()

        #УРОВЕНЬ 1. УСЛОВИЯ
        if lvl_1 == True:
            x += 1 
            if x >= 60:
                _time_ += 1
                x = 1
            
            mob_speed = randint(1, 4)
            mob_hp = 1
            
            lose = 10
            time_win = 15
            cur_lvl = lvl_1

            rocket.reset()
            rocket.update()
            for monster in monsters:    
                monster.reset()
                monster.update()

            keys = key.get_pressed()
            if len(bullets) <= 7:
                if keys[K_SPACE]:
                    if bullets[len(bullets)-1].rect.y <= 570:
                        bullet = Bullet("bullet.png", rocket.rect.x + 20, 610, 5)
                        bullets.append(bullet)

            for bullet in bullets:
                bullet.reset()
                bullet.update()
                if bullet.rect.y < 200:
                    bullets.remove(bullet)
            
            Z = 2

        #УРОВЕНЬ 2. УСЛОВИЯ.
        if lvl_2 == True:
    
            x += 1 
            if x >= 60:
                _time_ += 1
                x = 0
            
            mob_speed = randint(2, 5)
            mob_hp = 2
            
            lose = 8
            time_win = 15
            cur_lvl = lvl_2

        
            rocket.reset()
            rocket.update()
            for monster in monsters:    
                monster.reset()
                monster.update()

            keys = key.get_pressed()
            if len(bullets) <= 7:
                if keys[K_SPACE]:
                    if bullets[len(bullets)-1].rect.y <= 570:
                        bullet = Bullet("bullet.png", rocket.rect.x + 20, 610, 5)
                        bullets.append(bullet)

            for bullet in bullets:
                bullet.reset()
                bullet.update()
                if bullet.rect.y < 200:
                    bullets.remove(bullet)
            
            Z = 3

        #УРОВЕНЬ 3. УСЛОВИЯ.
        if lvl_3 == True:
            x += 1 
            if x >= 60:
                _time_ += 1
                x = 0
            
            mob_speed = randint(3, 6)
            mob_hp = 2
            
            lose = 5
            time_win = 10
            cur_lvl = lvl_3

            rocket.reset()
            rocket.update()
            for monster in monsters:    
                monster.reset()
                monster.update()

            keys = key.get_pressed()
            if len(bullets) <= 7:
                if keys[K_SPACE]:
                    if bullets[len(bullets)-1].rect.y <= 570:
                        bullet = Bullet("bullet.png", rocket.rect.x + 20, 610, 5)
                        bullets.append(bullet)

            for bullet in bullets:
                bullet.reset()
                bullet.update()
                if bullet.rect.y < 200:
                    bullets.remove(bullet)
            
            Z = 4

        #УРОВЕНЬ 4. УСЛОВИЯ.
        if lvl_4 == True:
            x += 1 
            if x >= 60:
                _time_ += 1
                x = 0
            
            mob_speed = randint(3, 6)
            mob_hp = 2
            
            lose = 5
            time_win = 10
            cur_lvl = lvl_4

            rocket.reset()
            rocket.update()
            for monster in monsters:    
                monster.reset()
                monster.update()

            keys = key.get_pressed()
            if len(bullets) <= 7:
                if keys[K_SPACE]:
                    if bullets[len(bullets)-1].rect.y <= 570:
                        bullet = Bullet("bullet.png", rocket.rect.x + 20, 610, 5)
                        bullets.append(bullet)

            for bullet in bullets:
                bullet.reset()
                bullet.update()
                if bullet.rect.y < 200:
                    bullets.remove(bullet)
            
            Z = 5
    
        #УРОВЕНЬ 5. УСЛОВИЯ.
        if lvl_5 == True:
        
            sprite1.reset()
            sprite1.update()
            sprite2.reset()
            sprite2.update("x", 500, win_width - 100)
            sprite3.reset()

            sprite4.reset()
            sprite4.update("y", 150, 45)
            sprite5.reset()
            sprite5.update("y", 350, 100)
            
            for wall in walls:
                wall.draw_wall()

        if sprite.collide_rect(sprite1, sprite3):

            lvl_5 = False    
            window.fill((200, 255, 200))
            win_panel = Label(100, 200, 0, 0, (200, 255, 200))
            win_panel.set_text("Вы победили!!!", 70)
            win_panel.draw(0, 0)
            button_exit.reset()    
                    
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if button_exit.collidepoint(x, y):
                    sprite1 = Player_Maze('Photo.png', 20, win_height - 140, 5)
                    menu_1 = True
                    finish = True
                    lvl_5 = False
                            
                    #Победа
                
        if sprite.collide_rect(sprite1, sprite2) or sprite.collide_rect(sprite1, sprite4) or sprite.collide_rect(sprite1, sprite5) or sprite.collide_rect(sprite1, w1) or sprite.collide_rect(sprite1, w2) or sprite.collide_rect(sprite1, w3) or sprite.collide_rect(sprite1, w4) or sprite.collide_rect(sprite1, w5) or sprite.collide_rect(sprite1, w6) or sprite.collide_rect(sprite1, w7) or sprite.collide_rect(sprite1, w8) or sprite.collide_rect(sprite1, w9) or sprite.collide_rect(sprite1, w10) or sprite.collide_rect(sprite1, w11) or sprite.collide_rect(sprite1, w12):
            
            lvl_5 = False
            window.fill((250, 128, 114))
            lose_panel = Label(100, 200, 0, 0, (250, 128, 114))
            lose_panel.set_text("Вы проиграли(((", 70)
            lose_panel.draw(0, 0)
            button_exit.reset()

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if button_exit.collidepoint(x, y):
                    sprite1 = Player_Maze('Photo.png', 20, win_height - 140, 5)

                    menu_1 = True
                    finish = True
                    lvl_5 = False
                        #Поражение

        if missed >= lose:
            if cur_lvl == lvl_1:
                lvl_1 = False
            if cur_lvl == lvl_2:
                lvl_2 = False
            if cur_lvl == lvl_3:
                lvl_3 = False
            if cur_lvl == lvl_4:
                lvl_4 = False
            button_exit.reset()    
            
            text_dead = font_2.render('Вы проиграли:', True, (255, 255, 255))
            window.blit(text_dead, (100, 300))
            text_dead1 = font_2.render('пропущено ' + str(lose) + ' НЛО.', True, (255, 255, 255))
            window.blit(text_dead1, (100, 350))

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if button_exit.collidepoint(x, y):
                    monsters.clear()
                    bullets.clear()

                    menu_1 = True
                    finish = True
                    
                    if cur_lvl == lvl_1:
                        lvl_1 = False
                    if cur_lvl == lvl_2:
                        lvl_2 = False
                    if cur_lvl == lvl_3:
                        lvl_3 = False
                    if cur_lvl == lvl_4:
                        lvl_4 = False
                    
                    _time_ = 0
                    missed = 0
                    killed = 0

                    wait_counter = 0

                    bullet = Bullet("bullet.png", 900, 500, 0)
                    bullets.append(bullet)   

        keys = key.get_pressed()
        
        if keys[K_p]:
            time = time_win + 1        

        if _time_ >= time_win:
            if cur_lvl == lvl_1:
                lvl_1 = False
            if cur_lvl == lvl_2:
                lvl_2 = False
            if cur_lvl == lvl_3:
                lvl_3 = False
            if cur_lvl == lvl_4:
                lvl_4 = False
            
            button_exit.reset()

            text_win = font_2.render('Вы ВЫИГРАЛИ:', True , (255, 255, 255))
            window.blit(text_win, (25, 300))
            text_win1 = font_2.render('продержались ' + str(time_win) + ' секунд.', True, (255, 255, 255))
            window.blit(text_win1, (25, 350))

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if button_exit.collidepoint(x, y):
                    monsters.clear()
                    bullets.clear()
                    
                    if Z == 2:
                        button_2 = button_2_on
                        with open("open_levels.txt", "w", encoding='utf-8') as file:
                            file.write("Lvl_2 1"+"\n"+"Lvl_3 0"+"\n"+"Lvl_4 0"+"\n"+"Lvl_5 0"+"\n"+str(volume))
                    if Z == 3:
                        button_3 = button_3_on
                        with open("open_levels.txt", "w", encoding='utf-8') as file:
                            file.write("Lvl_2 1"+"\n"+"Lvl_3 1"+"\n"+"Lvl_4 0"+"\n"+"Lvl_5 0"+"\n"+str(volume))
                    if Z == 4:
                        button_4 = button_4_on
                        with open("open_levels.txt", "w", encoding='utf-8') as file:
                            file.write("Lvl_2 1"+"\n"+"Lvl_3 1"+"\n"+"Lvl_4 1"+"\n"+"Lvl_5 0"+"\n"+str(volume))
                    if Z == 5:
                        button_5 = button_5_on
                        with open("open_levels.txt", "w", encoding='utf-8') as file:
                            file.write("Lvl_2 1"+"\n"+"Lvl_3 1"+"\n"+"Lvl_4 1"+"\n"+"Lvl_5 1"+"\n"+str(volume))


                    menu_1 = True
                    lvl_1 = False
                    lvl_2 = False
                    lvl_3 = False
                    lvl_4 = False
                    lvl_5 = False
                    
                    finish = True

                    _time_ = 0
                    missed = 0
                    killed = 0
                    
                    wait_counter = 0

                    bullet = Bullet("bullet.png", 900, 500, 0)
                    bullets.append(bullet)

        if wait_counter == 0 and finish == False:
            display.update() 
            wait_for_key_press(time_win, lose)
            wait_counter = 1

    clock.tick(60)
    display.update()  