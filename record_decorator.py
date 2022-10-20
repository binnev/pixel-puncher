import functools
import glob
import os
import subprocess
import sys
from collections import deque
from pathlib import Path

import pygame
from pygame import Surface


def clean_empty_recordings_dir(recording_dir: Path):
    try:
        os.mkdir(recording_dir.as_posix())
    except FileExistsError:
        pass

    # clear old files
    files = glob.glob((recording_dir / "*").as_posix())
    for file in files:
        os.remove(file)


def save_screenshots(screenshots: list[Surface], recording_dir: Path):
    for ii, image in enumerate(screenshots):
        pygame.image.save(image, str(recording_dir / f"{ii}.png"))


def create_videos(recording_dir):
    subprocess.run(
        [
            "ffmpeg",
            "-r",
            "60",
            "-i",
            str(recording_dir / "%d.png"),
            "-r",
            "60",
            str(recording_dir / "out.mp4"),
        ]
    )
    subprocess.run(
        [
            "ffmpeg",
            "-r",
            "60",
            "-i",
            str(recording_dir / "%d.png"),
            "-filter_complex",
            # credit: https://superuser.com/questions/1049606/reduce-generated-gif-size-using-ffmpeg
            (
                "fps=30,"
                "scale=1080:-1:flags=lanczos,"
                "split[s0][s1];[s0]"
                "palettegen=max_colors=32[p];[s1][p]"
                "paletteuse=dither=bayer"
            ),
            str(recording_dir / "out.gif"),
        ]
    )


def decorate_draw(func, screenshots):
    @functools.wraps(func)
    def wrapped(surface: Surface, debug: bool = False):
        func(surface, debug)  # normal _draw call

        screenshot = Surface(surface.get_size()).convert_alpha()
        func(screenshot, debug)
        screenshots.append(screenshot)

    return wrapped


def record(func, n_frames=60):
    screenshots = deque(maxlen=n_frames)
    recording_dir = Path(__file__).parent / "recordings"

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        cls = args[0]
        cls._draw = decorate_draw(cls._draw, screenshots)
        try:
            func(*args, **kwargs)
        except SystemExit:
            clean_empty_recordings_dir(recording_dir)
            save_screenshots(screenshots, recording_dir)
            create_videos(recording_dir)
        pygame.quit()
        sys.exit()

    return wrapped
