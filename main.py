import pygame as pg
import sys
from pygame.locals import *
from core.director import Director
from config import *
from server import *
import json
from core.map import Map
from core.player import Player
from core.raycasting import RayCasting
from core.renderer import ObjectRenderer


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
        self.flow = ''
        self.delta_time = 1
        self.started = False

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)

    def update(self):
        if self.started:
            self.player.update()
            self.raycasting.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
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
        if self.started:
            self.object_renderer.draw()
            # self.map.draw()
            # self.player.draw()

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
                if self.director.current.name == "Connect" and self.director.current.evts_added:
                    if not self.pinged:
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
                    if event.type == self.director.events["FADE_IN_YES"]:
                        self.director.start_screen(
                            'email', {
                                'message': self.message,
                            })
                    if event.type == self.director.events["FADE_IN_NO"]:
                        self.director.start_screen(
                            'menu', {
                                'message': self.message,
                            })
                if self.director.current.name == 'Email' and self.director.current.evts_added:
                    self.director.current.taking_input = True
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.director.current.input = self.director.current.input[:-1]
                        else:
                            self.director.current.input += event.unicode
                        inputs['email'] = self.director.current.input
                    if len(inputs['email']) > 0:
                        if event.type == self.director.events["SIGNUP_CLICK"]:
                            self.director.end_screen()
                            self.flow = 'signup'
                            pg.time.set_timer(
                                self.director.events["FADE_IN_SIGNUP"], 1500, 1)
                        if event.type == self.director.events["LOGIN_CLICK"]:
                            self.director.end_screen()
                            self.flow = 'login'
                            pg.time.set_timer(
                                self.director.events["FADE_IN_LOGIN"], 1500, 1)
                        if event.type == self.director.events["VERIFY_CLICK"]:
                            self.director.end_screen()
                            self.flow = 'verify'
                            pg.time.set_timer(
                                self.director.events["FADE_IN_VERIFY"], 1500, 1)
                        if event.type == self.director.events["FADE_IN_LOGIN"]:
                            self.director.start_screen('pwd', {
                                'message': self.message,
                            })
                        if event.type == self.director.events["FADE_IN_SIGNUP"]:
                            self.director.start_screen('pwd', {
                                'message': self.message,
                            })
                        if event.type == self.director.events["FADE_IN_VERIFY"]:
                            self.director.start_screen('otp', {
                                'message': self.message,
                            })
                if self.director.current.name == 'Pwd' and self.director.current.evts_added:
                    self.director.current.taking_input = True
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.director.current.input = self.director.current.input[:-1]
                        else:
                            self.director.current.input += event.unicode
                        inputs['pwd'] = self.director.current.input
                    if len(inputs['pwd']) > 0:
                        if event.type == self.director.events["SUBMIT_CLICK"]:
                            self.director.end_screen()
                            pg.time.set_timer(
                                self.director.events["FADE_IN_SUBMIT"], 1500, 1)
                        if event.type == self.director.events["FADE_IN_SUBMIT"]:
                            if self.flow == 'login' or self.flow == 'verify':
                                try:
                                    res = login()
                                    res = res['response']
                                    res = json.loads(res)
                                    self.message = res['msg']
                                    if res['signin'] == True:
                                        self.director.start_screen('menu', {
                                            'message': self.message,
                                        })
                                    else:
                                        self.director.start_screen('email', {
                                            'message': self.message,
                                        })
                                except:
                                    self.message = 'An error occurred while logging in, try again'
                                    self.director.start_screen('email', {
                                        'message': self.message,
                                    })
                            if self.flow == 'signup':
                                try:
                                    res = signup()
                                    res = res['response']
                                    res = json.loads(res)
                                    self.message = res['msg']
                                    if res['create'] == True:
                                        self.director.start_screen('otp', {
                                            'message': self.message,
                                        })
                                    else:
                                        self.director.start_screen('email', {
                                            'message': self.message,
                                        })
                                except:
                                    self.message = 'An error occurred while logging in, try again'
                                    self.director.start_screen('email', {
                                        'message': self.message,
                                    })
                if self.director.current.name == 'Otp' and self.director.current.evts_added:
                    self.director.current.taking_input = True
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.director.current.input = self.director.current.input[:-1]
                        else:
                            self.director.current.input += event.unicode
                        inputs['otp'] = self.director.current.input
                    if len(inputs['otp']) > 0:
                        if event.type == self.director.events["CHECK_CLICK"]:
                            self.director.end_screen()
                            pg.time.set_timer(
                                self.director.events["FADE_IN_CHECK"], 1500, 1)
                        if event.type == self.director.events["FADE_IN_CHECK"]:
                            if self.flow == 'verify' or self.flow == 'signup':
                                try:
                                    res = otp()
                                    res = res['response']
                                    res = json.loads(res)
                                    self.message = res['msg']
                                    if res['verify'] == True:
                                        if self.flow == 'signup':
                                            self.flow = 'login'
                                        self.director.start_screen('pwd', {
                                            'message': self.message,
                                        })
                                    else:
                                        self.director.start_screen('email', {
                                            'message': self.message,
                                        })
                                except:
                                    self.message = 'An error occurred while verifying, try again'
                                    self.director.start_screen('email', {
                                        'message': self.message,
                                    })
                if self.director.current.name == 'Menu' and self.director.current.evts_added:
                    if event.type == self.director.events["START!_CLICK"]:
                        self.director.end_screen()
                        pg.time.set_timer(
                            self.director.events["FADE_IN_START!"], 1500, 1)
                    if event.type == self.director.events["FADE_IN_START!"]:
                        self.director.start_screen('play')
                if self.director.current.name == 'Play':
                    if not self.started:
                        self.director.to_blit = False
                        self.new_game()
                        self.started = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
