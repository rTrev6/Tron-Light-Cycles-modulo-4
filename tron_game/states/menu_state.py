import pygame
from tron_game.state_definitions import *
from tron_game.ui import *
from tron_game.settings import *
from tron_game.grid_effects import *
from tron_game.fonts import *

class MenuState:
    def __init__(self, game):
        self.game = game
        self.options = ["COMO JUGAR","MODO DE JUEGO", "OPCIONES", "SALIR"]
        self.selected = 0
        self.color_timer = 0
        self.buttons = []
        self.background = None
        self.selector = None
        self.showing_help = False
        self.help_alpha = 0  # Transparencia inicial
        self.help_fade_in = False
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

            # Colores por opción
            if  option == "COMO JUGAR":
                color, hover = GRAY, CYAN
            elif option == "MODO DE JUEGO":
                color, hover = GRAY, CYAN
            elif option == "OPCIONES":
                color, hover = GRAY, CYAN
            else:  # SALIR
                color, hover = GRAY, CYAN

            self.buttons.append(Button((x, y), (button_width, button_height), color, hover))


    def enter(self):
        if self.background is None:
            try:
                self.background = pygame.image.load(str(BACKGROUND_MENU)).convert()
                self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            except Exception as e:
                #print(f'Error cargando fondo del menu: {e}')
                self.background = None
                
        self.game.play_menu_music()
        

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.sfx_button.play()
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.game.sfx_button.play()
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.game.current_track_index = (self.game.current_track_index + 1) % len(self.game.menu_music_paths)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.game.menu_music_paths[self.game.current_track_index])
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_RETURN:
                    self.game.sfx_start.play()
                    if self.showing_help:
                        self.showing_help = False # Ignora ENTER si está en modo ayuda
                    elif self.selected == 0:
                        self.showing_help = True # Activa la ayuda
                        self.help_alpha = 0
                        self.help_fade_in = True
                    elif self.selected == 1:
                        self.game.state_manager.change(State.MODE_SELECT, self.game)
                    elif self.selected == 2:
                        self.game.state_manager.change(State.OPTIONS, self.game)
                    elif self.selected == 3:
                        self.game.stop()
                elif event.key == pygame.K_ESCAPE:
                    if self.showing_help:
                        self.showing_help = False # Cierra ayuda
                    else:
                        self.game.stop()


    def update(self, dt):
        self.color_timer += dt # Alterna cada 0.5 segundos (500 ms)
        
        if self.showing_help and self.help_fade_in:
            self.help_alpha = min(self.help_alpha + dt * 500, 220)
            if self.help_alpha >= 220:
                self.help_fade_in = False

        
    
    def render(self, surface):
                
        surface.blit(self.background, (0,0))
        
        color = self.game.title_anim.get_color()
        
        draw_centered_text(surface, "TRON", self.game.first_font, color, WIDTH // 2, HEIGHT // 4 + 30)
        draw_centered_text(surface, "LIGHT CYCLES", self.game.first_font, color, WIDTH // 2, HEIGHT // 4 + 110)

        if self.selector is None:
            self.selector = pygame.transform.scale(pygame.image.load((SELECTOR)).convert_alpha(), (50,50))
        
        # Actualiza el estado de cada botón
        
        for i, button in enumerate(self.buttons):
            button.hovered = (i == self.selected)
            button.draw(surface)  # Dibuja primero el botón

        font = self.game.menu_font

        for i, option in enumerate(self.options):
            is_selected = self.buttons[i].hovered
            color = WHITE if is_selected else BLACK

            # Texto centrado en el botón
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=self.buttons[i].rect.center)
            surface.blit(text_surface, text_rect)

                # Flecha a la izquierda si está seleccionado y parpadea cada 0.5s
            if is_selected and int(self.color_timer * 2) % 2 == 0:
                selector_rect = self.selector.get_rect()
                selector_rect.centery = self.buttons[i].rect.centery
                selector_rect.right = self.buttons[i].rect.left - 10
                surface.blit(self.selector, selector_rect)
        
        if self.showing_help:
            draw_help_overlay(surface, self.game.title_font, self.game.menu_font, self.help_alpha)
