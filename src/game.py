from robingame.input import GamecubeController
from robingame.objects import Game

from src import conf
from src.inputs import Keyboard0, Keyboard1


class PixelPuncher(Game):
    fps = conf.FPS
    window_width = conf.SCREEN_WIDTH
    window_height = conf.SCREEN_HEIGHT
    window_caption = "FIGHTING GAME"
    frame_duration = 3
    font_name = "ubuntu"
    font_size = 50
    parental_name = "game"

    def __init__(self):
        super().__init__()

        # input devices
        # todo; should input devices be entities too?! All they need is an .update() method and a
        #  self.draw() that does nothing...
        self.keyboard0 = Keyboard0()
        self.keyboard1 = Keyboard1()
        self.controller0 = GamecubeController(controller_id=0)
        self.controller1 = GamecubeController(controller_id=1)
        self.input_devices = [
            self.keyboard0,
            self.keyboard1,
            self.controller0,
            self.controller1,
        ]
        from src.scenes import SandBox

        self.add_scene(SandBox())

    def read_inputs(self):
        super().read_inputs()
        for device in self.input_devices:
            device.read_new_inputs()


if __name__ == "__main__":
    PixelPuncher().main()
