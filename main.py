import pygame

pygame.init()


font2 = pygame.font.Font(None, 56)
sound = pygame.mixer.Sound("b19fd19cd041148.mp3")
fontUI = pygame.font.Font(None, 30)

menu_photo = pygame.image.load("menuu.jpg")
menu_rect = menu_photo.get_rect(bottomright=(800, 650))
pygame.display.set_caption("Танчики")


def main_func():
    size = width, height = 800, 650
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60

    sp = ["Играть", "", "Об игре", "", "Выход"]
    sel = 0
    new = 0
    # фоновая музыка_воспроизведение
    sound.play()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    new = -1
                elif event.key == pygame.K_DOWN:
                    new = 1
                elif event.key == pygame.K_SPACE:
                    sound.stop()
                    if sel == 0:
                        from Menu import osnovnaya
                        osnovnaya()
                    elif sel == 4:
                        running = False
                    elif sel == 2:
                        from Play import plat
                        plat()

                sel = (new + sel) % len(sp)
                while sp[sel] == "":
                    sel = (new + sel) % len(sp)
                new = 0
        # основной фон меню игры

        screen.blit(menu_photo, menu_rect)
        # управление меню стрелочками вверх-вниз
        for i in range(len(sp)):
            if i == sel:
                text = font2.render(sp[i], 1, (255, 255, 255))
            else:
                text = font2.render(sp[i], 1, "gray")
            rect = text.get_rect(center=(800 // 2, 200 + 50 * i))
            screen.blit(text, rect)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
main_func()


