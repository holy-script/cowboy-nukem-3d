import pygame as pg
import sys
from pygame.locals import *
from core.director import Director
from config import *
from server import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.director = Director(self.clock)
        self.director.startup()
        self.connected = False
        self.message = ''
        self.pinged = False

    def new_game(self):
        pass

    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        self.screen.fill("black")
        self.director.direct()
        [
            pg.display.get_surface().blit(sprite.image, sprite.rect)
            for sprite in self.director.current.sprites()
        ]
        [
            pg.display.get_surface().blit(
                text[0], text[0].get_rect(center=text[1]))
            for text in self.director.current.texts
        ]

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()
            if (
                event.type == self.director.events["FADE_OUT_LOGOS"]
                or event.type == self.director.events["FADE_OUT_BANNER"]
            ):
                self.director.end_screen()
            if event.type == self.director.events["FADE_IN_LOGOS"]:
                self.director.start_screen("logos")
            if event.type == self.director.events["FADE_IN_BANNER"]:
                self.director.start_screen("banner")
            if event.type == self.director.events["FADE_IN_CONNECT"]:
                self.director.start_screen("connect")
            if self.director.current:
                if self.director.current.evts_added:
                    if self.director.current.name == "Connect":
                        if not self.pinged:
                            print("sending...")
                            try:
                                res = ping()
                                if res['response'] == 'OK':
                                    self.connected = True
                            except:
                                self.message = 'Cannot connect to server at the moment...'
                            finally:
                                self.pinged = True
                        if event.type == self.director.events["YES_CLICK"]:
                            self.director.end_screen()
                            if self.connected:
                                self.message = 'You are online - do subscribe to the leaderboard for live updates!'
                            pg.time.set_timer(
                                self.director.events["FADE_IN_YES"], 1500, 1)
                        if event.type == self.director.events["NO_CLICK"]:
                            if self.connected:
                                self.message = 'Have fun playing offline, but feel free to switch!'
                                self.connected = False
                            self.director.end_screen()
                            pg.time.set_timer(
                                self.director.events["FADE_IN_NO"], 1500, 1)
                        if event.type == self.director.events["FADE_IN_YES"] or event.type == self.director.events["FADE_IN_NO"]:
                            self.director.start_screen(
                                'auth', {
                                    'message': self.message,
                                    'input': 'email',
                                })
                    if self.director.current.name == 'Auth':
                        if event.type == self.director.events["SIGNUP_CLICK"]:
                            self.director.end_screen()
                            pg.time.set_timer(
                                self.director.events["FADE_IN_SIGNUP"], 1500, 1)
                        if event.type == self.director.events["LOGIN_CLICK"]:
                            self.director.end_screen()
                            pg.time.set_timer(
                                self.director.events["FADE_IN_LOGIN"], 1500, 1)
                        if event.type == self.director.events["VERIFY_CLICK"]:
                            self.director.end_screen()
                            pg.time.set_timer(
                                self.director.events["FADE_IN_VERIFY"], 1500, 1)
                        if event.type == self.director.events["FADE_IN_LOGIN"]:
                            pass
                        if event.type == self.director.events["FADE_IN_SIGNUP"]:
                            pass
                        if event.type == self.director.events["FADE_IN_VERIFY"]:
                            pass
                        self.director.current.taking_input = True
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_BACKSPACE:
                                self.director.current.input = self.director.current.input[:-1]
                            else:
                                self.director.current.input += event.unicode
                            inputs['email'] = self.director.current.input

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
