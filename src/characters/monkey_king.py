import pygame
from pygame import Color, Surface

from src import sounds
from src.characters import Character, AerialMove, Move
from src.hitboxes import Hitbox
from src.inputs import FightingGameInput
from src.projectiles.falco_laser import FalcoLaser
from src.sprites.monkey_king import monkey_king_sprites


class MonkeyKing(Character):
    mass = 20
    width = 90
    height = 100
    color = Color("cyan")
    ground_acceleration = 6
    walk_speed = 5
    run_speed = 9
    initial_dash_duration = 16
    run_turnaround_duration = 10
    air_acceleration = 0.75
    air_speed = 5.5
    gravity = 0.6
    jump_speed = 13
    aerial_jump_speed = 13
    shorthop_speed = 7.5
    air_resistance = 0.01
    friction = 0.8
    fall_speed = 10
    fast_fall_speed = 18
    jumpsquat_frames = 7
    max_aerial_jumps = 1
    max_air_dodges = 1
    max_wall_jumps = 1
    sprites = monkey_king_sprites

    def __init__(self, x, y, input=FightingGameInput, facing_right=True):
        super().__init__(x, y, input, facing_right)
        self.state = self.state_fall
        self.damage = 0

    @property
    def image_rect(self):
        """Default is to align the image with the center of the object"""
        if self.image:
            image_rect = self.image.get_rect()
            image_rect.midbottom = self.rect.midbottom
            return image_rect
        else:
            return None

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        if not debug:
            return

        def tprint(surface, x, y, textString):
            font = pygame.font.Font(None, 30)
            textBitmap = font.render(textString, True, Color("black"))
            surface.blit(textBitmap, (x, y))

        colliding = pygame.sprite.spritecollide(self, self.level.platforms, dokill=False)
        touching = [plat for plat in self.level.platforms if self.touching(plat)]
        try:
            state_name = self.state.__name__
        except AttributeError:
            state_name = self.state.__class__.__name__
        things_to_print = [
            f"u = {self.u}",
            f"v = {self.v}",
            f"airborne = {self.airborne}",
            f"touching: {touching}",
            f"colliding: {colliding}",
            f"state: {state_name}",
            f"damage: {self.damage}%",
            f"fast_fall: {self.fast_fall}",
            f"aerial_jumps: {self.aerial_jumps}",
            f"wall_jumps: {self.wall_jumps}",
            # f"hitpause_duration: {self.hitpause_duration}",
            # f"hitstun_duration: {self.hitstun_duration}",
        ]
        line_spacing = 20
        for ii, thing in enumerate(things_to_print):
            tprint(
                surface,
                self.rect.left,
                self.rect.top + ii * line_spacing - line_spacing * len(things_to_print),
                thing,
            )

    class ForwardAir(AerialMove):
        landing_lag = 15

        def __init__(self, character: Character):
            wap = Hitbox(
                owner=character,
                x_offset=15,
                y_offset=-65,
                width=110,
                height=50,
                rotation=15,
                base_knockback=10,
                knockback_angle=45,
                knockback_growth=10,
                damage=15,
            )
            spike = Hitbox(
                owner=character,
                y_offset=30,
                x_offset=40,
                width=80,
                height=40,
                rotation=0,
                base_knockback=20,
                knockback_angle=-80,
                knockback_growth=15,
                damage=15,
                higher_priority_sibling=wap,
            )
            wap2 = Hitbox(
                owner=character,
                x_offset=65,
                y_offset=-10,
                width=60,
                height=110,
                rotation=0,
                base_knockback=20,
                knockback_angle=10,
                knockback_growth=10,
                damage=15,
                higher_priority_sibling=spike,
            )
            sprite = character.sprites[f"fair_{character.facing}"]
            images = sprite.images

            self.frame_mapping = [
                {"image": images[0], "hitboxes": []},
                {"image": images[1], "hitboxes": []},
                {"image": images[2], "hitboxes": []},
                {"image": images[2], "hitboxes": []},
                {"image": images[2], "hitboxes": []},
                {"image": images[3], "hitboxes": [wap]},
                {"image": images[4], "hitboxes": [wap2, spike]},
                {"image": images[5], "hitboxes": [spike]},
                {"image": images[6], "hitboxes": []},
                {"image": images[7], "hitboxes": []},
                {"image": images[8], "hitboxes": []},
            ]
            super().__init__(character)

    class BackAir(AerialMove):
        landing_lag = 5

        def __init__(self, character: Character):
            sweet_spot = Hitbox(
                owner=character,
                x_offset=-50,
                y_offset=10,
                width=80,
                height=40,
                rotation=0,
                base_knockback=10,
                knockback_angle=170,
                knockback_growth=10,
                damage=10,
            )
            sour_spot = Hitbox(
                owner=character,
                x_offset=-50,
                y_offset=10,
                width=60,
                height=30,
                rotation=0,
                base_knockback=5,
                knockback_angle=135,
                knockback_growth=5,
                damage=5,
                higher_priority_sibling=sweet_spot,
            )
            weak_front = Hitbox(
                owner=character,
                x_offset=20,
                y_offset=25,
                width=30,
                height=40,
                rotation=0,
                base_knockback=3,
                knockback_angle=45,
                knockback_growth=2,
                damage=5,
                higher_priority_sibling=sour_spot,
            )
            sprite = character.sprites[f"bair_{character.facing}"]
            images = sprite.images

            self.frame_mapping = [
                {"image": images[0], "hitboxes": []},
                {"image": images[1], "hitboxes": []},
                {"image": images[2], "hitboxes": [sweet_spot, weak_front]},
                {"image": images[2], "hitboxes": [sour_spot, weak_front]},
                {"image": images[2], "hitboxes": [sour_spot, weak_front]},
                {"image": images[2], "hitboxes": [sour_spot, weak_front]},
                {"image": images[1], "hitboxes": []},
            ]
            super().__init__(character)

    class UpAir(AerialMove):
        landing_lag = 2

        def __init__(self, character: Character):
            zeroth_hit = Hitbox(
                owner=character,
                x_offset=-45,
                y_offset=-40,
                width=40,
                height=50,
                rotation=0,
                base_knockback=10,
                knockback_angle=80,
                knockback_growth=15,
                damage=10,
                sound=sounds.smack,
            )
            first_hit = Hitbox(
                owner=character,
                x_offset=5,
                y_offset=-55,
                width=100,
                height=50,
                rotation=0,
                base_knockback=10,
                knockback_angle=90,
                knockback_growth=15,
                damage=10,
                sound=sounds.smack,
                higher_priority_sibling=zeroth_hit,
            )
            second_hit = Hitbox(
                owner=character,
                x_offset=40,
                y_offset=-10,
                width=60,
                height=70,
                rotation=0,
                base_knockback=10,
                knockback_angle=90,
                knockback_growth=15,
                damage=10,
                sound=sounds.smack,
                higher_priority_sibling=first_hit,
            )
            sprite = character.sprites[f"uair_{character.facing}"]
            images = sprite.images

            self.frame_mapping = [
                {"image": images[0], "hitboxes": []},
                {"image": images[1], "hitboxes": []},
                {"image": images[1], "hitboxes": [zeroth_hit]},
                {"image": images[2], "hitboxes": [first_hit]},
                {"image": images[3], "hitboxes": [second_hit]},
                {"image": images[3], "hitboxes": []},
                {"image": images[3], "hitboxes": []},
                {"image": images[3], "hitboxes": []},
            ]
            super().__init__(character)

    class DownAir(AerialMove):
        landing_lag = 15

        def __init__(self, character: Character):
            sweet_spot = Hitbox(
                owner=character,
                x_offset=10,
                y_offset=30,
                width=60,
                height=60,
                rotation=0,
                base_knockback=10,
                knockback_angle=270,
                knockback_growth=15,
                damage=20,
                sound=sounds.bighit,
            )
            sweet_spot2 = Hitbox(
                owner=character,
                x_offset=5,
                y_offset=40,
                width=60,
                height=70,
                rotation=0,
                base_knockback=10,
                knockback_angle=270,
                knockback_growth=15,
                damage=20,
                sound=sounds.bighit,
                higher_priority_sibling=sweet_spot,
            )
            sour_spot = Hitbox(
                owner=character,
                x_offset=5,
                y_offset=40,
                width=40,
                height=50,
                rotation=0,
                base_knockback=5,
                knockback_angle=270,
                knockback_growth=7,
                damage=10,
                sound=sounds.bighit,
                higher_priority_sibling=sweet_spot2,
            )
            sprite = character.sprites[f"dair_{character.facing}"]
            images = sprite.images

            self.frame_mapping = [
                {"image": images[0], "hitboxes": []},
                {"image": images[1], "hitboxes": []},
                {"image": images[1], "hitboxes": []},
                {"image": images[1], "hitboxes": []},
                {"image": images[2], "hitboxes": [sweet_spot]},
                {"image": images[3], "hitboxes": [sweet_spot2]},
                {"image": images[3], "hitboxes": [sweet_spot2]},
                {"image": images[3], "hitboxes": [sweet_spot2]},
                {"image": images[3], "hitboxes": [sweet_spot2]},
                {"image": images[3], "hitboxes": [sour_spot]},
                {"image": images[3], "hitboxes": [sour_spot]},
                {"image": images[3], "hitboxes": []},
                {"image": images[3], "hitboxes": []},
                {"image": images[3], "hitboxes": []},
            ]
            super().__init__(character)

    class NeutralAir(AerialMove):
        landing_lag = 2

        def __init__(self, character: Character):
            front1 = Hitbox(
                owner=character,
                x_offset=30,
                y_offset=0,
                width=90,
                height=30,
                rotation=-10,
                base_knockback=10,
                knockback_angle=45,
                knockback_growth=10,
                damage=10,
            )
            back1 = Hitbox(
                owner=character,
                x_offset=-45,
                y_offset=-35,
                width=50,
                height=30,
                rotation=-25,
                base_knockback=5,
                knockback_angle=90 + 45,
                knockback_growth=5,
                damage=5,
                higher_priority_sibling=front1,
            )
            front2 = Hitbox(
                owner=character,
                x_offset=50,
                y_offset=-5,
                width=70,
                height=30,
                rotation=-15,
                base_knockback=5,
                knockback_angle=45,
                knockback_growth=5,
                damage=5,
                # higher_priority_sibling=back1,
            )
            back2 = Hitbox(
                owner=character,
                x_offset=-45,
                y_offset=-35,
                width=50,
                height=30,
                rotation=-25,
                base_knockback=5,
                knockback_angle=90 + 45,
                knockback_growth=5,
                damage=5,
                higher_priority_sibling=front2,
            )
            sprite = character.sprites[f"nair_{character.facing}"]
            images = sprite.images

            self.frame_mapping = [
                dict(image=images[0], hitboxes=[]),
                dict(image=images[1], hitboxes=[front1, back1]),
                dict(image=images[2], hitboxes=[]),
                dict(image=images[3], hitboxes=[]),
                dict(image=images[4]),
                dict(image=images[5], hitboxes=[front2, back2]),
            ]
            super().__init__(character)

    class UpTilt(Move):
        def __init__(self, character: Character):
            low = Hitbox(
                owner=character,
                x_offset=-15,
                y_offset=10,
                width=60,
                height=40,
                rotation=-30,
                base_knockback=15,
                knockback_angle=95,
                knockback_growth=8,
                damage=8,
            )
            high = Hitbox(
                owner=character,
                x_offset=0,
                y_offset=-15,
                width=50,
                height=60,
                rotation=0,
                base_knockback=15,
                knockback_angle=95,
                knockback_growth=8,
                damage=8,
                higher_priority_sibling=low,
            )
            sprite = character.sprites[f"utilt_{character.facing}"]
            images = sprite.images

            self.frame_mapping = [
                {"image": images[0], "hitboxes": []},
                {"image": images[2], "hitboxes": [low]},
                {"image": images[4], "hitboxes": [high]},
                {"image": images[5], "hitboxes": []},
                {"image": images[6], "hitboxes": []},
                {"image": images[7], "hitboxes": []},
            ]
            super().__init__(character)

    class Jab(Move):
        sound = sounds.swing3

        def __init__(self, character: Character):
            sweet_spot = Hitbox(
                owner=character,
                x_offset=65,
                y_offset=15,
                width=40,
                height=30,
                rotation=0,
                base_knockback=15,
                knockback_angle=45,
                knockback_growth=1,
                damage=3,
                sound=sounds.smack2,
            )
            sprite = character.sprites[f"jab_{character.facing}"]
            images = sprite.images

            self.frame_mapping = [
                {"image": images[0], "hitboxes": [sweet_spot]},
                {"image": images[1]},
                {"image": images[1]},
                {"image": images[1]},
                {"image": images[1]},
            ]
            super().__init__(character)

    class DownSmash(Move):
        def __init__(self, character: Character):
            self.frame_mapping = []
            super().__init__(character)

    class UpSmash(Move):
        def __init__(self, character: Character):
            self.frame_mapping = []
            super().__init__(character)

    class ForwardSmash(Move):
        def __init__(self, character: Character):
            self.frame_mapping = []
            super().__init__(character)

    class DashAttack(Move):
        def __init__(self, character: Character):
            sweet_spot = Hitbox(
                owner=character,
                x_offset=30,
                y_offset=20,
                width=60,
                height=30,
                rotation=0,
                base_knockback=70,
                knockback_angle=80,
                knockback_growth=0,
                damage=20,
                sound=sounds.sword_hit,
            )
            sour_spot = Hitbox(
                owner=character,
                x_offset=30,
                y_offset=20,
                width=60,
                height=30,
                rotation=0,
                base_knockback=30,
                knockback_angle=45,
                knockback_growth=0,
                damage=10,
                higher_priority_sibling=sweet_spot,
                sound=sounds.sword_hit2,
            )
            sprite = character.sprites[f"dash_attack_{character.facing}"]
            images = sprite.images
            image_hit = images[0]

            self.frame_mapping = [
                {"image": image_hit, "hitboxes": [sweet_spot]},
                {"image": image_hit, "hitboxes": [sour_spot]},
                {"image": image_hit},
                {"image": image_hit},
                {"image": image_hit},
                {"image": image_hit},
            ]
            character.u = 13 if character.facing_right else -13
            super().__init__(character)

    class DownTilt(Move):
        def __init__(self, character: Character):
            sweet_spot = Hitbox(
                owner=character,
                x_offset=65,
                y_offset=27,
                width=50,
                height=25,
                rotation=0,
                base_knockback=10,
                knockback_angle=10,
                knockback_growth=13,
                damage=10,
                sound=sounds.smack,
            )
            sour_spot = Hitbox(
                owner=character,
                x_offset=10,
                y_offset=30,
                width=60,
                height=30,
                rotation=0,
                base_knockback=5,
                knockback_angle=80,
                knockback_growth=8,
                damage=4,
                higher_priority_sibling=sweet_spot,
                sound=sounds.smack,
            )
            sprite = character.sprites[f"dtilt_{character.facing}"]
            images = sprite.images

            self.frame_mapping = [
                dict(image=images[0]),
                dict(image=images[1]),
                dict(image=images[2], hitboxes=[sweet_spot, sour_spot]),
                dict(image=images[3], hitboxes=[sweet_spot, sour_spot]),
                dict(image=images[4]),
                dict(image=images[4]),
            ]
            super().__init__(character)

        def get_next_state(self):
            return self.character.state_crouch

    class ForwardTilt(Move):
        def __init__(self, character: Character):
            sweet_spot = Hitbox(
                owner=character,
                x_offset=35,
                y_offset=10,
                width=130,
                height=40,
                rotation=5,
                base_knockback=8,
                knockback_angle=10,
                knockback_growth=8,
                damage=10,
            )
            sour_spot = Hitbox(
                owner=character,
                x_offset=-15,
                y_offset=-40,
                width=120,
                height=40,
                rotation=0,
                base_knockback=4,
                knockback_angle=140,
                knockback_growth=3,
                damage=6,
                higher_priority_sibling=sweet_spot,
            )
            sprite = character.sprites[f"ftilt_{character.facing}"]
            images = sprite.images

            self.frame_mapping = [
                {"image": images[0], "hitboxes": []},
                {"image": images[1], "hitboxes": []},
                {"image": images[2], "hitboxes": [sweet_spot]},
                {"image": images[3], "hitboxes": [sour_spot]},
                {"image": images[4], "hitboxes": []},
                {"image": images[4], "hitboxes": []},
            ]
            super().__init__(character)

    class AerialNeutralB(AerialMove):
        landing_lag = 0

        def __init__(self, character: Character):
            sprite = character.sprites[f"aerial_laser_{character.facing}"]
            images = sprite.images
            image_hit = images[0]

            self.frame_mapping = [
                {"image": image_hit},
                {"image": image_hit},
                {"image": image_hit},
                {"image": image_hit},
                {"image": image_hit},
                {"image": image_hit},
                {"image": image_hit},
                {"image": image_hit},
                {"image": image_hit},
            ]
            sounds.falco.gun.play()
            super().__init__(character)

        def __call__(self):
            super().__call__()

            character = self.character
            if character.tick == 5:
                character.level.add_projectile(
                    FalcoLaser(
                        x=character.x,
                        y=character.y + 10,
                        facing_right=character.facing_right,
                        owner=character,
                    )
                )
                sounds.falco.laser.play()

    class AerialUpB(AerialMove):
        landing_lag = 0

        def __init__(self, character: Character):
            self.frame_mapping = []
            super().__init__(character)

        def handle_physics(self):
            character = self.character
            if character.animation_frame < 2:
                pass
            elif character.animation_frame == 2:
                character.v = -13
                character.u += 2 if character.facing_right else -2
            else:
                super().handle_physics()

        def get_next_state(self):
            return self.character.state_special_fall
