import pygame

W_WIDTH = 800
W_HEIGHT = 600


class MessageBox:
    def __init__(self, window_rect, font, message):
        self.window_rect = window_rect
        self.font = font
        self.background_colour = pygame.Color("#555555")
        self.text_colour = pygame.Color("#FFFFFF")
        
        # self.window_title_str = "Message"
        self.title_text_render = self.font.render("", True, self.text_colour)

        self.should_exit = False

        self.done_button = UTTextButton([self.window_rect[0] + (self.window_rect[2] / 2) + 45,
                                         self.window_rect[1] + self.window_rect[3] - 30, 70, 20], "Done", font)

        self.message = message
        self.message_text_render = self.font.render(self.message, True, self.text_colour)

    def handle_input_event(self, event):
        self.done_button.handle_input_event(event)

    def update(self):
        self.done_button.update()

        if self.done_button.was_pressed():
            self.should_exit = True

    def is_inside(self, screen_pos):
        is_inside = False
        if self.window_rect[0] <= screen_pos[0] <= self.window_rect[0] + self.window_rect[2]:
            if self.window_rect[1] <= screen_pos[1] <= self.window_rect[1] + self.window_rect[3]:
                is_inside = True
        return is_inside

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_colour, pygame.Rect(self.window_rect[0], self.window_rect[1],
                                                                     self.window_rect[2], self.window_rect[3]), 0)

        screen.blit(self.title_text_render,
                    self.title_text_render.get_rect(centerx=self.window_rect[0] + self.window_rect[2] * 0.5,
                                                    centery=self.window_rect[1] + 24))

        screen.blit(self.message_text_render,
                    self.message_text_render.get_rect(centerx=self.window_rect.centerx,
                                                      centery=self.window_rect[1] + 50))
        
        self.done_button.draw(screen)


class UTTextButton:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.text_colour = pygame.Color("#FFFFFF")
        self.background_colour = pygame.Color("#151515")
        self.text_render = self.font.render(self.text, True, self.text_colour)
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = self.rect.center
    
    def update(self):
        pass
    
    def was_pressed(self):
        mpos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos) and MOUSEPRESSED:
            return True
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.background_colour, self.rect)
        screen.blit(self.text_render, self.text_rect)

    
pygame.init()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
clock = pygame.time.Clock()

screen_rect = screen.get_rect()
window_rect = pygame.Rect(0, 0, 400, 250)
window_rect.center = screen_rect.center
font = pygame.font.SysFont('Arial', 24)
message = 'Game Over'

box = MessageBox(window_rect, font, message)

running = True
while running:
    clock.tick(60)
    MOUSEPRESSED = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MOUSEPRESSED = True
            
    box.update()
    screen.fill((0, 0, 0))
    if not box.should_exit:
        box.draw(screen)
    pygame.display.update()
    
    if box.should_exit == True:
        pygame.quit()
    
pygame.quit()