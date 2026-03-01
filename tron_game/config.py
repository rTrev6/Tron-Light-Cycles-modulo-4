import os
from arcade_machine_sdk.util import json
from tron_game.settings import CONFIG_FILE, DEFAULT_CONTROLS_P1, DEFAULT_CONTROLS_P2

def normalize_keys(d):
    return {k.lower(): v for k, v in d.items()}

def load_controls():
    if os.path.exists(CONFIG_FILE):
        data = json.load(CONFIG_FILE)  # ← SDK espera una ruta, no un archivo abierto
        p1 = normalize_keys(data.get("p1", {}))
        p2 = normalize_keys(data.get("p2", {}))
        return p1, p2
    return DEFAULT_CONTROLS_P1.copy(), DEFAULT_CONTROLS_P2.copy()

def save_controls(p1_controls, p2_controls):
    data = {
        "p1": normalize_keys(p1_controls),
        "p2": normalize_keys(p2_controls)
    }
    json.save(CONFIG_FILE, data)  # ← SDK guarda usando ruta + dict
