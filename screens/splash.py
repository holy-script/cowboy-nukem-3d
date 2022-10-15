import os
from core.base import BaseScreen

pg_logo = os.path.join(os.path.dirname(__file__), "..", "assets", "pygame_logo.png")


def logos():
    logos = BaseScreen("Logos", "orange", 1)
    logos.create()
    logos.add_sprite(pg_logo, logos.screen.get_rect().center)
    return logos


def banner():
    banner = BaseScreen("Banner", "pink", 1)
    banner.create()
    (x, y) = banner.screen.get_rect().center
    banner.add_text(
        36,
        (x, y - 36),
        "That was the trouble with explaining with words.",
        "black",
    )
    banner.add_text(
        36, (x, y), "If you explained with gunpowder, people listened.", "black"
    )
    banner.add_text(
        36,
        (x, y + 36),
        "-Dean F. Wilson",
        "black",
    )
    return banner
