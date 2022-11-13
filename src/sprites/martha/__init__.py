from pathlib import Path

from robingame.image import SpriteDict

from src import conf

folder = Path(__file__).parent

SIZE = (64, 64)

martha_sprites = SpriteDict(
    folder=folder,
    size=SIZE,
    scale=conf.SCALE_SPRITES,
    create_flipped_versions=True,
)
martha_sprites.register(crouch="crouch.png")
martha_sprites.register(run="run.png")
martha_sprites.register(stand="stand.png")
martha_sprites.register(fall="fall.png")
martha_sprites.register(special_fall="run.png")
martha_sprites.register(air_dodge="run.png")
# martha_sprites.register(nair="nair.png")
# martha_sprites.register(dair="dair.png")
# martha_sprites.register(bair="bair.png")
# martha_sprites.register(fair="fair.png")
# martha_sprites.register(uair="uair.png")
martha_sprites.register(dash_attack="run.png")
martha_sprites.register(jab="jab.png")
martha_sprites.register(aerial_laser="run.png")
# martha_sprites.register(dtilt="dtilt.png")
# martha_sprites.register(utilt="utilt.png")
# martha_sprites.register(ftilt="ftilt.png")
