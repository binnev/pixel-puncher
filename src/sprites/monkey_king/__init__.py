from pathlib import Path

from robingame.image import SpriteDict

from src import conf

folder = Path(__file__).parent

SIZE = (64, 64)

monkey_king_sprites = SpriteDict(
    folder=folder,
    size=SIZE,
    scale=conf.SCALE_SPRITES,
    create_flipped_versions=True,
)
monkey_king_sprites.register(crouch="crouch.png")
monkey_king_sprites.register(run="run.png")
monkey_king_sprites.register(stand="stand.png")
monkey_king_sprites.register(fall="fall.png")
monkey_king_sprites.register(special_fall="run.png")
monkey_king_sprites.register(air_dodge="run.png")
monkey_king_sprites.register(nair="nair.png")
monkey_king_sprites.register(dair="dair.png")
monkey_king_sprites.register(bair="bair.png")
monkey_king_sprites.register(fair="fair.png")
monkey_king_sprites.register(uair="uair.png")
monkey_king_sprites.register(dash_attack="run.png")
monkey_king_sprites.register(jab="jab.png")
monkey_king_sprites.register(aerial_laser="run.png")
monkey_king_sprites.register(dtilt="dtilt.png")
monkey_king_sprites.register(utilt="run.png")
monkey_king_sprites.register(ftilt="ftilt.png")
