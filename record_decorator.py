import functools
import glob
import os
import subprocess
import sys
from collections import deque
from pathlib import Path

import pygame
from pygame import Surface
from robingame.objects import Game


def clean_empty_recordings_dir(output_dir: Path):
    try:
        os.mkdir(output_dir.as_posix())
    except FileExistsError:
        pass

    # clear old files
    files = glob.glob((output_dir / "*").as_posix())
    for file in files:
        os.remove(file)


def save_screenshots(screenshots: deque[Surface], output_dir: Path):
    for ii, image in enumerate(screenshots):
        pygame.image.save(image, str(output_dir / f"{ii}.png"))


def create_videos(output_dir):
    subprocess.run(
        [
            "ffmpeg",
            "-r",
            "60",
            "-i",
            str(output_dir / "%d.png"),
            "-r",
            "60",
            str(output_dir / "out.mp4"),
        ]
    )
    subprocess.run(
        [
            "ffmpeg",
            "-r",
            "60",
            "-i",
            str(output_dir / "%d.png"),
            "-filter_complex",
            # credit: https://superuser.com/questions/1049606/reduce-generated-gif-size-using-ffmpeg
            (
                "fps=30,"
                "scale=1080:-1:flags=lanczos,"
                "split[s0][s1];[s0]"
                "palettegen=max_colors=32[p];[s1][p]"
                "paletteuse=dither=bayer"
            ),
            str(output_dir / "out.gif"),
        ]
    )


def decorate_draw(func, screenshots):
    @functools.wraps(func)
    def wrapped(self, surface: Surface, debug: bool = False):
        # normal _draw call
        func(self, surface, debug)

        # also do _draw onto a new screenshot surface which we store
        screenshot = Surface(surface.get_size()).convert_alpha()
        func(self, screenshot, debug)
        screenshots.append(screenshot)

    return wrapped


def decorate_main(func, screenshots: deque, output_dir: Path):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        """Run the game as normal, but intercept the quit signal and save all the screenshots to
        file."""
        try:
            func(*args, **kwargs)
        except SystemExit:
            clean_empty_recordings_dir(output_dir)
            save_screenshots(screenshots, output_dir)
            create_videos(output_dir)
        pygame.quit()
        sys.exit()

    return wrapped


def record(cls: Game = None, *, n_frames: int, output_dir: Path):
    """
    Patch the Game's ._draw() and .main() methods so that we keep a screenshot of every frame,
    which we later stitch into videos.
    """
    output_dir = output_dir or Path(__file__).parent / "recordings"
    screenshots = deque(maxlen=n_frames)

    def decorate(cls):
        cls._draw = decorate_draw(cls._draw, screenshots=screenshots)
        cls.main = decorate_main(cls.main, screenshots=screenshots, output_dir=output_dir)
        return cls

    return decorate(cls) if cls else decorate
