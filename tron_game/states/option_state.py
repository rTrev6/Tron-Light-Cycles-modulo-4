import pygame
from tron_game.state_definitions import State
from tron_game.ui import *
from tron_game.config import save_controls
from tron_game.settings import *

KEY_NAMES = {
    pygame.K_w: "W", 
    pygame.K_s: "S", 
    pygame.K_a: "A", 
    pygame.K_d: "D",
    pygame.K_UP: "↑", 
    pygame.K_DOWN: "↓", 
    pygame.K_LEFT: "←", 
    pygame.K_RIGHT: "→"
}

class OptionsState:
    def __init__(self, game):
        self.game = game
        self.awaiting_key = False
        self.control_target = None
        self.step = 0
        self.sequence = ["up", "down", "left", "right"]
        self.player_config = None
        self.selected = 0
        self.message = ""
        self.message_timer = 0
        self.last_prompt = ""
        self.message_color = WHITE
        self.selector = SELECTOR
        self.background = None

        self.buttons = []
        font = self.game.menu_font
        options = ["CAMBIAR CONTROLES [P1]", "CAMBIAR CONTROLES [P2]", "RESTAURAR CONTROLES", "VOLVER"]
        spacing = 70
        base_y = HEIGHT // 2  
        offset = -70

        for i, option in enumerate(options):
            text_width, text_height = font.size(option)
            padding_x = 40
            padding_y = 20
            button_width = text_width + padding_x
            button_height = text_height + padding_y
            x = (WIDTH - button_width) // 2
            y = base_y + i * spacing + offset

            # Colores por opción
            if option == "CAMBIAR CONTROLES [P1]":
                color, hover = GRAY, CYAN
            elif option == "CAMBIAR CONTROLES [P2]":
                color, hover = GRAY, CYAN
            elif option == "RESTAURAR CONTROLES":
                color, hover = GRAY, CYAN
            else:  # SALIR
                color, hover = GRAY, CYAN

            self.buttons.append(Button((x, y), (button_width, button_height), color, hover))

        self.color_timer = 0
       
        
    def enter(self):
        if self.background is None:
            try:
                self.background = pygame.image.load(str(BACKGROUND_SELECT)).convert()
                self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            except Exception as e:
                #print(f'Error cargando fondo del modo de seleccion: {e}')
                self.background = None
        self.awaiting_key = False
        self.control_target = None
        self.step = 0
        self.player_config = None
        self.message = ""
        self.selector = pygame.transform.scale(pygame.image.load((SELECTOR)).convert_alpha(), (50,50))

    def handle_events(self, events):
        for event in events:
            if self.awaiting_key:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.awaiting_key = False
                        self.message = "Configuracion cancelada."
                        self.message_color = WHITE
                        self.message_timer = pygame.time.get_ticks()
                        return
                    key = event.key
                    player = self.player_config
                    action = self.sequence[self.step]

                    current_controls = self.game.controls_p1 if player == "p1" else self.game.controls_p2
                    other_controls = self.game.controls_p2 if player == "p1" else self.game.controls_p1

                    if key in current_controls.values() or key in other_controls.values():
                        self.message = f"Tecla ya en uso. Elige otra para {action.upper()}"
                        self.message_color = RED
                        self.message_timer = pygame.time.get_ticks()
                        return

                    current_controls[action] = key
                    self.step += 1

                    if self.step >= len(self.sequence):
                        self.awaiting_key = False
                        save_controls(self.game.controls_p1, self.game.controls_p2)
                        self.message = f"Controles de {player.upper()} actualizados"
                        self.message_timer = pygame.time.get_ticks()
                    else:
                        next_action = self.sequence[self.step].upper()
                        self.last_prompt = f"{player.upper()}: Presiona tecla para {next_action}"
                        self.message = self.last_prompt
                        self.message_color = WHITE
                        self.message_timer = pygame.time.get_ticks()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game.sfx_button.play()
                        self.selected = (self.selected - 1) % len(self.buttons)
                    elif event.key == pygame.K_DOWN:
                        self.game.sfx_button.play()
                        self.selected = (self.selected + 1) % len(self.buttons)
                    elif event.key == pygame.K_RETURN:
                        self.game.sfx_start.play()
                        if self.selected == 0:
                            self._start_config("p1")
                        elif self.selected == 1:
                            self._start_config("p2")
                        elif self.selected == 2:
                            self.game.controls_p1 = DEFAULT_CONTROLS_P1.copy()
                            self.game.controls_p2 = DEFAULT_CONTROLS_P2.copy()
                            save_controls(self.game.controls_p1, self.game.controls_p2)
                            self.message = "Controles restaurados a los valores por defecto"
                            self.message_timer = pygame.time.get_ticks()
                        elif self.selected == 3:
                            self.game.state_manager.change(State.MENU, self.game)



    def _start_config(self, player):
        
        self.awaiting_key = True
        self.player_config = player
        self.step = 0
        self.last_prompt = f"{player.upper()}: Presiona tecla para {self.sequence[0].upper()}"
        self.message = self.last_prompt
        self.message_color = WHITE
        self.message_timer = pygame.time.get_ticks()


    def update(self, dt):
        
        if self.message and pygame.time.get_ticks() - self.message_timer > 1000:
            if self.awaiting_key and self.message != self.last_prompt:
                self.message = self.last_prompt
                self.message_color = WHITE
                self.message_timer = 0 # evita que se borre de nuevo
            elif not self.awaiting_key:
                self.message = ""
        self.color_timer += dt
       
        # Alterna cada 0.5 segundos (500 ms)
        if int(self.color_timer * 1) % 2 == 0:
            self.menu_text_color = WHITE
        else:
            self.menu_text_color = BLACK


    def render(self, surface):
        
        surface.blit(self.background, (0,0))
        draw_centered_text(surface, "OPCIONES", self.game.title_font, WHITE, WIDTH // 2, HEIGHT // 4 )

        key_l = [
                f"P1: ↑ {self._key_name(self.game.controls_p1['up'])} ↓ {self._key_name(self.game.controls_p1['down'])} ← {self._key_name(self.game.controls_p1['left'])} → {self._key_name(self.game.controls_p1['right'])}",
                f"P2: ↑ {self._key_name(self.game.controls_p2['up'])} ↓ {self._key_name(self.game.controls_p2['down'])} ← {self._key_name(self.game.controls_p2['left'])} → {self._key_name(self.game.controls_p2['right'])}"
            ]
            
        for button in self.buttons:
                button.draw(surface)
            
        font = self.game.menu_font

        for i, option in enumerate(["CAMBIAR CONTROLES [P1]", "CAMBIAR CONTROLES [P2]", "RESTAURAR CONTROLES", "VOLVER"]):
                is_selected = (i == self.selected)
                color = BLACK if is_selected else WHITE

                # Texto centrado
                text_surface = font.render(option, True, color)
                text_rect = text_surface.get_rect(center=self.buttons[i].rect.center)
                surface.blit(text_surface, text_rect)

                # Flecha parpadeante
                if is_selected and int(self.color_timer * 2) % 2 == 0:
                    selector_rect = self.selector.get_rect()
                    selector_rect.centery = self.buttons[i].rect.centery
                    selector_rect.right = self.buttons[i].rect.left - 10
                    surface.blit(self.selector, selector_rect)
            

            # Mostrar controles actuales de P1 y P2
        font = self.game.menu_font
        for i, line in enumerate(key_l):
                text_surface = font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 220 + i * 40))
                surface.blit(text_surface, text_rect)

        if self.message:
            if self.awaiting_key:
                y = HEIGHT // 2 - 120
            else:
                y = HEIGHT // 2 - 120
            draw_centered_text(surface, self.message, self.game.menu_font, self.message_color, WIDTH // 2, y)


    def _key_name(self, key):
        return KEY_NAMES.get(key, pygame.key.name(key).upper())
