import pygame
from tron_game.state_definitions import State
from tron_game.ui import draw_centered_text, Button
from tron_game.settings import *

class ModeSelectState:
    def __init__(self, game):
        self.game = game
        self.options = ["MODO CLASICO", "MODO ARCADE", "VOLVER"]
        self.selector = None
        self.color_timer = 0
        self.selected = 0
        self.buttons = []
        self.background= None

        font = self.game.menu_font
        spacing = 80
        base_y = HEIGHT // 2
        offset = -30

        for i, option in enumerate(self.options):
            text_width, text_height = font.size(option)
            padding_x = 40
            padding_y = 20
            button_width = text_width + padding_x
            button_height = text_height + padding_y
            x = (WIDTH - button_width) // 2
            y = base_y + i * spacing + offset

            # Colores distintos por tipo de opción
            if option == "MODO CLÁSICO":
                color, hover = GRAY, CYAN
            elif option == "MODO ARCADE (próximamente)":
                color, hover = GRAY, CYAN
            else:
                color, hover = GRAY, CYAN

            self.buttons.append(Button((x, y), (button_width, button_height), color, hover))


    def enter(self):
        if self.background is None:
            try:
                self.background = pygame.image.load(str(BACKGROUND_SELECT)).convert()
                self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            except Exception as e:
                #print(f'Error cargando fondo del modo de seleccion: {e}')
                self.background = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.sfx_button.play()
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.game.sfx_button.play()
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.game.sfx_start.play()
                    if self.selected == 0:
                        
                        self.game.reset_game()
                        self.game.state_manager.change(State.COUNTDOWN, self.game, arcade_mode = False)
                        pygame.mixer.music.stop()
                    elif self.selected == 1:
                        
                        self.game.reset_game()
                        self.game.state_manager.change(State.COUNTDOWN, self.game, arcade_mode = True)
                        pygame.mixer.music.stop()
                    elif self.selected == 2:
                        self.game.fadeout_music(400)
                        self.game.state_manager.change(State.MENU, self.game)
                elif event.key == pygame.K_ESCAPE:
                    self.game.state_manager.change(State.MENU, self.game)

    def update(self, dt):
        self.color_timer += dt #Parpadeo
    

    def render(self, surface):
        surface.blit(self.background, (0,0))
        draw_centered_text(surface, "MODO DE JUEGO", self.game.title_font, WHITE, WIDTH // 2, HEIGHT //3 -50)
        
        if self.selector is None:
            self.selector = pygame.transform.scale(pygame.image.load((SELECTOR)).convert_alpha(), (50,50))
            
        for i, button in enumerate(self.buttons):
            button.hovered = (i == self.selected)
            button.draw(surface)

        for i, option in enumerate(self.options):
            is_selected = self.buttons[i].hovered
            color = WHITE if is_selected else BLACK

            font = self.game.menu_font
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=self.buttons[i].rect.center)

            surface.blit(text_surface, text_rect)

            # Flecha a la izquierda si está seleccionado
            if is_selected and int(self.color_timer * 2) % 2 == 0:
                selector_rect = self.selector.get_rect()
                selector_rect.centery = self.buttons[i].rect.centery
                selector_rect.right = self.buttons[i].rect.left - 10
                surface.blit(self.selector, selector_rect)

