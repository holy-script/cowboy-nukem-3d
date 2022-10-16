from core.sprites import *
from core.npc import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.npc_list = []
        self.npc_path = 'assets/'
        add_npc = self.add_npc
        self.npc_positions = {}
        add_npc(BanditNPC(game, pos=(11.0, 19.0)))
        add_npc(BanditNPC(game, pos=(11.5, 4.5)))
        add_npc(BanditNPC(game, pos=(13.5, 6.5)))
        add_npc(BanditNPC(game, pos=(2.0, 20.0)))
        add_npc(BanditNPC(game, pos=(4.0, 29.0)))
        add_npc(WagabondNPC(game, pos=(5.5, 14.5)))
        add_npc(WagabondNPC(game, pos=(5.5, 16.5)))
        add_npc(BossNPC(game, pos=(14.5, 25.5)))

    def check_win(self):
        if not len(self.npc_positions):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.director.start_screen(
                'menu', {
                    'message': "You won! If you're online, do checkout the leaderboard!",
                })
            self.game.started = False
            self.game.director.to_blit = True
            pg.mouse.set_visible(True)

    def update(self):
        self.npc_positions = {
            npc.map_pos for npc in self.npc_list if npc.alive}
        [npc.update() for npc in self.npc_list]
        self.check_win()

    def add_npc(self, npc):
        self.npc_list.append(npc)
