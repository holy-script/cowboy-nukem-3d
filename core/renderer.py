import pygame as pg
from config import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture(
            'assets/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture(
            'assets/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'assets/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('assets/game_over.png', RES)
        self.win_image = self.get_texture('assets/win.png', RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def win(self):
        self.screen.blit(self.win_image, (0, 0))
        self.game.score = pg.time.get_ticks() - self.game.score
        print(self.game.score)

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 *
                           self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, 'burlywood4',
                     (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(
            self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('assets/1.png'),
            2: self.get_texture('assets/2.png'),
            3: self.get_texture('assets/3.png'),
            4: self.get_texture('assets/4.png'),
            5: self.get_texture('assets/5.png'),
        }
