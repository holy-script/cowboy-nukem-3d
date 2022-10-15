import pygame as pg
from config import *
from core.sprites import GameSprite
from core.buttons import Button


class BaseScreen(pg.sprite.Group):
    def __init__(self, name, bg="white", transition_count=3):
        super().__init__()
        self.size = RES
        self.bg = bg
        self.count = transition_count
        self.texts = []
        self.name = name
        self.btns: list[Button] = []
        self.evts_added = False
        self.taking_input = False
        self.input_index = -1
        self.input_config = {}
        self.input = ''

    def create(self):
        self.screen = pg.Surface(self.size)
        self.screen.fill(pg.Color(self.bg))

    def opacity(self, val):
        self.screen.set_alpha(val)
        [sprite.image.set_alpha(val) for sprite in self.sprites()]
        [text[0].set_alpha(val) for text in self.texts]

    def add_sprite(self, path, point, pos="center"):
        sprite = GameSprite(path, self, point, pos)
        self.add(sprite)
        return sprite

    def add_text(self, size, pos, text, color, bg=None, is_input=False):
        font = pg.font.SysFont(None, size)
        txt = font.render(
            text, True, pg.Color(color), None if bg is None else pg.Color(bg)
        )
        self.texts.append((txt, pos))
        if is_input:
            self.input_index = len(self.texts) - 1
        return (txt, pos, len(self.texts) - 1)

    def change_text(self, size, pos, text, color, bg, index):
        font = pg.font.SysFont(None, size)
        txt = font.render(
            text, True, pg.Color(color), None if bg is None else pg.Color(bg)
        )
        self.texts[index] = (txt, pos)

    def create_btn(self, name, font_size, color, x, y, btn_color):
        btn = Button(name, x, y, btn_color)
        self.add(btn)
        self.btns.append(btn)
        btn.text_index = self.add_text(
            font_size, (x, y), name.upper(), color)[-1]

    def change_textpos(self, index, pos):
        self.texts[index] = (self.texts[index][0], pos)

    def evt_call(self, evts, evt_count):
        for btn in self.btns:
            evt_count += 1
            evts[btn.evt] = evt_count
            btn.evt_code = evt_count
            evt_count += 1
            evts[f"FADE_IN_{btn.name.upper()}"] = evt_count
        return (evts, evt_count)

    def handle_btn_clicks(self):
        for btn in self.btns:
            if btn.rect.collidepoint(pg.mouse.get_pos()):
                if pg.mouse.get_pressed()[0]:
                    btn.image = btn.states["active"]
                    btn.rect.centery = btn.y_active
                    if not btn.triggered:
                        pg.event.post(pg.event.Event(btn.evt_code))
                        btn.triggered = True
                else:
                    btn.image = btn.states["hover"]
                    btn.rect.centery = btn.y_normal
                    if btn.triggered:
                        btn.triggered = False
                self.change_textpos(btn.text_index, btn.rect.center)
            else:
                btn.image = btn.states["normal"]

    @staticmethod
    def translate(value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return round(rightMin + (valueScaled * rightSpan))

    def update(self):
        self.handle_btn_clicks()
        if self.taking_input:
            self.change_text(
                self.input_config['size'], self.input_config['pos'], self.input,
                self.input_config['color'], self.input_config['bg'], self.input_index)
