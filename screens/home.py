from core.base import BaseScreen
import pygame as pg


def menu(data):
    menu = BaseScreen("Menu", "brown", 1.5)
    menu.create()

    (x, y) = menu.screen.get_rect().center

    menu.create_btn("Start!", 36, "brown", x, y - 54, "standard")
    menu.create_btn("Options", 36, "brown", x, y + 18, "standard")
    menu.create_btn("Credits", 36, "brown", x, y + 90, "standard")
    menu.create_btn("Exit", 36, "brown", x, y + 162, "standard")
    menu.add_text(
        32,
        (x, y + 226),
        "A pseudo-3D FPS with cowboys!",
        "dodgerblue3",
    )
    msg = data['message']
    menu.add_text(
        32, (x, y +
             258), f'{msg}', "dodgerblue3"
    )

    return menu


def connect():
    connect = BaseScreen("Connect", "black", 1.5)
    connect.create()

    (x, y) = connect.screen.get_rect().center

    connect.add_text(
        36,
        (x, y - 36),
        "Connect to the game server?",
        "white",
    )
    connect.create_btn("Yes", 36, "brown", x - 80, y + 36, "large")
    connect.create_btn("No", 36, "brown", x + 80, y + 36, "large")

    return connect


def auth(data):
    auth = BaseScreen("Auth", "black", 1.5)
    auth.create()

    (x, y) = auth.screen.get_rect().center

    auth.add_text(
        36,
        (x, y - 54),
        "Please input email address:",
        "white",
    )

    auth.add_text(
        36,
        (x, y),
        "",
        "white",
        'brown',
        True
    )

    auth.input_config = {
        'size': 36,
        'pos': (x, y),
        'color': 'white',
        'bg': 'brown',
    }

    auth.create_btn("Signup", 36, "brown", x - 160, y + 54, "mid")
    auth.create_btn("Login", 36, "brown", x, y + 54, "mid")
    auth.create_btn("Verify", 36, "brown", x + 160, y + 54, "mid")
    msg = data['message']

    return auth
