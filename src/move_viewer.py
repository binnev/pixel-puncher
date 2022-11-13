from importlib import import_module, reload
from unittest.mock import MagicMock

import pygame
from pygame import Surface
from robingame.input import EventQueue
from robingame.objects import Game, Group
from robingame.text.font import fonts

from src import conf, characters


class MoveViewer(Game):
    window_width = 300
    window_height = 300
    window_caption = "MOVE VIEWER"
    frame_duration = 3
    font_name = "ubuntu"
    font_size = 50
    parental_name = "game"
    screen_color = pygame.Color("gray")
    character_class = characters.Martha
    move_class = characters.Martha.Jab

    def __init__(self):
        super().__init__()
        self.frame = 0
        self.hitboxes = Group()
        self.characters = Group()
        self.child_groups += [
            self.hitboxes,
            self.characters,
        ]
        self.setup()

    def draw(self, surface, debug):
        super().draw(surface, debug)
        fonts.cellphone_black.render(surface, f"{self.frame=}", x=0, y=0, scale=3)
        self.hitboxes.draw(surface, debug=True)

    def update(self):
        # super().update()
        self.tick += 1
        for event in EventQueue.filter(type=pygame.KEYDOWN):
            if event.key == pygame.K_RIGHT:
                self.frame += 1
                self.setup()
            if event.key == pygame.K_LEFT:
                self.frame -= 1
                self.setup()
            if event.key == pygame.K_r:
                self.hot_reload()
                self.setup()
        if self.tick % 60 == 0:
            self.hot_reload()
            self.setup()

    def setup(self):
        self.characters.kill()
        self.hitboxes.kill()
        self.character = self.character_class(
            x=self.window_width // 2,
            y=self.window_height // 2,
            input=MagicMock(),
        )
        self.move = self.move_class(character=self.character)
        self.frame %= len(self.move.frame_mapping)
        self.character.state = self.move
        self.character.state.handle_physics = MagicMock()
        self.character.level = self  # hack alert
        self.character.tick = self.frame * self.frame_duration
        self.character.state()
        self.characters.add(self.character)

    def hot_reload(self):
        path_to_character_class = f"{self.character_class.__module__}"
        module = import_module(path_to_character_class)
        module = reload(module)
        self.character_class = getattr(module, self.character_class.__name__)
        self.move_class = getattr(self.character_class, self.move_class.__name__)
        print

    def add_hitbox(self, *hitboxes):
        self.add_to_group(*hitboxes, group=self.hitboxes)


if __name__ == "__main__":
    MoveViewer().main()
