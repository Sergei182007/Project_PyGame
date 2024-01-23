import pygame
import random
import sqlite3

fontUI = pygame.font.Font(None, 30)
# Звуковые эффекты
sound_effect = pygame.mixer.Sound("babahz.mp3")
sound_damage = pygame.mixer.Sound("probitie1.mp3")
sound_bang = pygame.mixer.Sound("tank-unichtozhen.mp3")
sound_no = pygame.mixer.Sound("32045-bronja-ne-probita.mp3")
pygame.display.set_caption("Танчики")


def osnovnaya():
    pygame.init()
    size = width, height = 800, 650
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60

    # Спрайты: изображения коробок с бустерами и блоков
    a = pygame.image.load("block.jpg")
    b = pygame.image.load("boust.png")
    imgBrick = pygame.transform.scale(a, (36, 36))
    im = pygame.transform.scale(b, (36, 36))

    objects = []
    bullets = []
    bousters = []
    a_time = 0
    b_timer = 0
    fl_timer = 0
    shot_timer = 0
    interval = 17000
    # Танк обездвижен на 5 секунд
    inter = 5000
    interval_black = 4000
    # Красная пуля
    red_time = 7000

    back = pygame.image.load(random.choice(["back-1.png", "background-2.jpg", "back-5.jpg", "back-7.jpg"]))
    background = pygame.transform.scale(back, (800, 650))


    DIRECTS = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    tanks = ["gray", "yellow", "red", "blue", "green", "orange"]

    class User:
        def __init__(self):
            pass

        def update(self):
            pass

        def draw(self):
            i = 0
            for obj in objects:
                if obj.type == "tank":
                    pygame.draw.rect(screen, obj.color, (650 // 2 + i * 70, 5, 22, 22))
                    text = fontUI.render(str(obj.hp), 1, obj.color)
                    rect = text.get_rect(center=(650 // 2 + i * 70 + 32, 5 + 11))
                    screen.blit(text, rect)
                    i += 1

    class Tank:
        def __init__(self, color, px, py, direct, listi, rang):
            objects.append(self)
            self.type = "tank"
            self.color = color
            self.direct = direct
            self.rect = pygame.Rect(px, py, 50, 50)
            con = sqlite3.connect("Tanks")
            cur = con.cursor()
            result_1 = cur.execute(f"SELECT Speed FROM Tanks WHERE color = '{self.color}'").fetchall()
            result_2 = cur.execute(f"SELECT Strength FROM Tanks WHERE color = '{self.color}'").fetchall()
            result_3 = cur.execute(f"SELECT Speed_bullet FROM Tanks WHERE color = '{self.color}'").fetchall()
            result_4 = cur.execute(f"SELECT Damage FROM Tanks WHERE color = '{self.color}'").fetchall()
            result_5 = cur.execute(f"SELECT Reload FROM Tanks WHERE color = '{self.color}'").fetchall()
            self.speed = int(result_1[0][0])
            self.hp = int(result_2[0][0])
            self.bulletSpeed = int(result_3[0][0])
            self.bulletDamage = int(result_4[0][0])
            self.shotTimer = 0
            self.shotDelay = int(result_5[0][0])
            self.keyLEFT = listi[0]
            self.keyRIGHT = listi[1]
            self.keyUP = listi[2]
            self.keyDOWN = listi[3]
            self.keySHOT = listi[4]
            self.rang = rang
            con.close()

        def update(self):
            X, Y = self.rect.topleft
            if keys[self.keyLEFT]:
                self.rect.x -= self.speed
                self.direct = 0

            elif keys[self.keyRIGHT]:
                self.rect.x += self.speed
                self.direct = 1

            elif keys[self.keyUP]:
                self.rect.y -= self.speed
                self.direct = 2

            elif keys[self.keyDOWN]:
                self.rect.y += self.speed
                self.direct = 3
            # чтобы танк не выезжал за границы карты и не "проскальзывал" через блоки
            for obj in objects:
                if obj != self and obj.type == "block" and self.rect.colliderect(
                        obj.rect) or (obj == self and (
                        self.rect.x > 750 or self.rect.y > 600 or self.rect.x < 0 or self.rect.y < 0)):
                    self.rect.topleft = X, Y
                # чтобы танк не проезжал через другой танк
                if obj != self and obj.type == "tank" and self.rect.colliderect(
                        obj.rect):
                    self.rect.topleft = X, Y

            if keys[self.keySHOT] and self.shotTimer == 0:
                dx = DIRECTS[self.direct][0] * self.bulletSpeed
                dy = DIRECTS[self.direct][1] * self.bulletSpeed
                Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage, self.bulletSpeed)
                self.shotTimer = self.shotDelay

            if self.shotTimer > 0:
                self.shotTimer -= 2

        def draw(self):
            pygame.draw.rect(screen, self.color, self.rect)
            x = self.rect.centerx + DIRECTS[self.direct][0] * 30
            y = self.rect.centery + DIRECTS[self.direct][1] * 30
            pygame.draw.line(screen, (255, 255, 255), self.rect.center, (x, y), width=4)

        def damage(self, value):
            self.hp -= value
            # переход к финальному окну, если прочность танка стала равной 0
            if self.hp <= 0:
                objects.remove(self)
                final_window()

    class Bullet:
        def __init__(self, parent, px, py, dx, dy, damage, speed_bullet):
            bullets.append(self)
            self.parent = parent
            self.px, self.py = px, py
            self.dx, self.dy = dx, dy
            self.damage = damage
            self.speed_bullet = speed_bullet

        def update(self):
            self.px += self.dx
            self.py += self.dy

            if self.px < 0 or self.px > 800 or self.py < 0 or self.py > 650:
                bullets.remove(self)
            else:
                for obj in objects:
                    if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        if obj.type == "block":
                            sound_effect.set_volume(0.25)
                            sound_effect.play(0, 3000)
                        # столкновение пули с танком
                        elif obj.type == "tank" and obj.hp > 0:
                            sound_damage.set_volume(1.25)
                            sound_damage.play()

                        else:
                            sound_bang.play()
                        bullets.remove(self)
                for b in bousters:
                    if b.rect.collidepoint(self.px, self.py):
                        bousters.remove(b)
                        bullets.remove(self)

        def draw(self):
            if self.parent.bulletDamage != 100:
                pygame.draw.circle(screen, "yellow", (self.px, self.py), radius=2)
            else:
                pygame.draw.circle(screen, "red", (self.px, self.py), radius=2)

    class Block:
        def update(self):
            pass

        def __init__(self, x, y, size):
            objects.append(self)  # добавляем каждый блок в список всех объектов
            self.type = "block"

            self.rect = pygame.Rect(x, y, size, size)
            self.hp = 1  # Прочность каждого блока 1

        def draw(self):
            screen.blit(imgBrick, self.rect)

        def damage(self, value):
            self.hp -= value
            if self.hp <= 0:
                objects.remove(self)

    class Bouster:
        def __init__(self, boust, x, y, size):
            bousters.append(self)
            self.type = "bouster"
            self.boust = boust
            self.x, self.y = x, y
            self.size = size

            self.rect = pygame.Rect(x, y, size, size)
            self.hp = 1

        def update(self):
            for obj in objects:
                if obj.rect.collidepoint(self.x, self.y):
                    if self.boust == 1:
                        obj.hp += random.choice([3, 4, 5, 6, 7])
                    elif self.boust == 2:
                        obj.speed = 0
                    elif self.boust == 3:
                        for k in objects:
                            if k != obj:
                                k.hp -= 2
                    elif self.boust == 4:
                        obj.speed += 3
                    elif self.boust == 5:
                        obj.bulletDamage = 100
                        Flag = True
                    bousters.remove(self)

        def draw(self):
            screen.blit(im, self.rect)

        def damage(self, value):
            self.hp -= value
            if self.hp <= 0:
                bousters.remove(self)

    Block(100, 30, 42)
    Tank(random.choice(tanks), 100, 100, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE),
         1)
    Tank(random.choice(tanks), 500, 230, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_v), 2)

    for _ in range(45):
        while True:
            x = random.randint(0, width // 42 - 1) * 42
            y = random.randint(1, height // 42 - 1) * 42
            rect = pygame.Rect(x, y, 42, 42)
            flag = False
            for obj in objects:
                if rect.colliderect(obj.rect):
                    flag = True

            if not flag:
                break

        Block(x, y, 42)

    def bou():
        while True:
            x = random.randint(0, width // 32 - 1) * 32
            y = random.randint(1, height // 32 - 1) * 32
            rect = pygame.Rect(x, y, 32, 32)
            flag = False
            for obj in objects:
                if rect.colliderect(obj.rect):
                    flag = True

            if not flag:
                break

        Bouster(random.choice([1, 2, 3, 4, 5]), x, y, 36)

    def fix():
        for obj in objects:
            if obj.type == "tank" and obj.speed == 0:
                con = sqlite3.connect("Tanks")
                cur = con.cursor()
                result_1 = cur.execute(f"SELECT Speed FROM Tanks WHERE color = '{obj.color}'").fetchall()
                obj.speed = result_1[0][0]
                con.close()

    def fix_red_bullet():
        for obj in objects:
            if obj.type == "tank" and obj.bulletDamage == 100:
                con = sqlite3.connect("Tanks")
                cur = con.cursor()
                result = cur.execute(f"SELECT Damage FROM Tanks WHERE color = '{obj.color}'").fetchall()
                obj.bulletDamage = result[0][0]
                con.close()

    u = User()

    def final_window():
        sound_bang.play()
        running = True
        dog_surf = pygame.image.load(random.choice(["final.jpg", "final_2.jpg"]))
        dog_rect = dog_surf.get_rect(bottomright=(800, 650))
        screen.blit(dog_surf, dog_rect)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        from main import main_func
                        main_func()

            for obj in objects:
                if obj.type == "tank" and obj.hp > 0:
                    text = fontUI.render(f"Игра окончена. Победил Игрок {obj.rang}", True, (255, 255, 255))
                    text_2 = fontUI.render(f"Для возвращения в меню нажмите пробел", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(800 // 2, 650 // 2))
                    text_rect_2 = text.get_rect(center=(800 // 2, 750 // 2))
            screen.blit(text, text_rect)
            screen.blit(text_2, text_rect_2)

            # Обновление экрана
            pygame.display.flip()

            clock.tick(FPS)
        pygame.quit()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                from main import main_func
                main_func()
        current_time = pygame.time.get_ticks()
        # Проверка на истечение времени действия бустеров
        if current_time - shot_timer > interval:
            bou()
            shot_timer = current_time
        if current_time - a_time > inter:
            fix()
            a_time = current_time
        if current_time - b_timer > interval_black:
            b_timer = current_time

        if current_time - fl_timer > red_time:
            fix_red_bullet()
            fl_timer = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        for obj in objects:
            obj.update()
            u.draw()
        for bul in bullets:
            bul.update()
            u.draw()
        screen.blit(background, (0, 0))
        for bul in bullets:
            bul.draw()
        for obj in objects:
            obj.draw()
            u.draw()

        for boust in bousters:
            boust.draw()
            boust.update()

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
