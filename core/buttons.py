import pygame as pg
import os

standard_btn_normal = os.path.join(
    os.path.dirname(__file__), "..", "assets", "standard_btn_normal.png"
)
standard_btn_hover = os.path.join(
    os.path.dirname(__file__), "..", "assets", "standard_btn_hover.png"
)
standard_btn_active = os.path.join(
    os.path.dirname(__file__), "..", "assets", "standard_btn_active.png"
)
large_btn_normal = os.path.join(
    os.path.dirname(__file__), "..", "assets", "large_btn_normal.png"
)
large_btn_hover = os.path.join(
    os.path.dirname(__file__), "..", "assets", "large_btn_hover.png"
)
large_btn_active = os.path.join(
    os.path.dirname(__file__), "..", "assets", "large_btn_active.png"
)
mid_btn_normal = os.path.join(
    os.path.dirname(__file__), "..", "assets", "mid_btn_normal.png"
)
mid_btn_hover = os.path.join(
    os.path.dirname(__file__), "..", "assets", "mid_btn_hover.png"
)
mid_btn_active = os.path.join(
    os.path.dirname(__file__), "..", "assets", "mid_btn_active.png"
)


class Button(pg.sprite.Sprite):
    def __init__(self, name, x, y, btn_color):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.y_active = y + 2
        self.y_normal = y
        self.type = {
            "standard": [standard_btn_normal, standard_btn_hover, standard_btn_active],
            "large": [large_btn_normal, large_btn_hover, large_btn_active],
            "mid": [mid_btn_normal, mid_btn_hover, mid_btn_active],
        }[btn_color]
        self.triggered = False
        self.active = False
        self.evt_code = -1
        self.evt = f"{name.upper()}_CLICK"
        self.states = {
            "normal": pg.image.load(self.type[0]).convert_alpha(),
            "hover": pg.image.load(self.type[1]).convert_alpha(),
            "active": pg.image.load(self.type[2]).convert_alpha(),
        }
        self.image = self.states["normal"]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.text_index = -1

    def destroy(self):
        self.kill()
