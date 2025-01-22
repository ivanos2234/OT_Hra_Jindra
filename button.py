from settings import  *

class Button():
    def __init__(self, x, y, image, scale, surf):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x - self.image.get_width() / 2, y)
        self.surf = surf
        self.clicked = False

    def draw(self):
        action = False
        # mouse pos
        pos = pygame.mouse.get_pos()
        if self.rect.left < pos[0] / 2.0 < self.rect.right and self.rect.top < pos[1] / 2.0 < self.rect.bottom:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.surf.blit(self.image, (self.rect.x, self.rect.y))
        return action
