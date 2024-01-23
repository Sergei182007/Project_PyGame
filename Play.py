import pygame
import sys

# Инициализация Pygame
pygame.init()

size = width, height = 800, 650
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60
menu_photo = pygame.image.load("ttanks.jpg")
menu_rect = menu_photo.get_rect(bottomright=(800, 650))
a = pygame.image.load("bousters.png")
a_rect = menu_photo.get_rect(center=(1200, 530))



def plat():
    pygame.display.set_caption("Танчики")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.Font(None, 36)



    # Класс кнопки
    class Button:
        def __init__(self, color, x, y, width, height, text):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self, screen, n = None):
            pygame.draw.rect(screen, n, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

            if self.text != '':
                text = font.render(self.text, 1, BLACK)
                screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        def is_over(self, pos):
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True
            return False


# Создание кнопки
    button = Button(WHITE, 720 // 2, 580, 100, 50, 'Назад')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button.is_over(pos):
                    import main
                    main()

        screen.blit(menu_photo, menu_rect)
        screen.blit(a, a_rect)
        button.draw(screen, (0, 0, 0))
        pygame.display.flip()