class StateManager:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.current_state = None

    def register(self, state_enum, state_instance):
        self.states[state_enum] = state_instance

    def change(self, state_enum):
        self.current_state = self.states[state_enum]
        self.current_state.enter()

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def render(self, surface):
        if self.current_state:
            self.current_state.render(surface)
