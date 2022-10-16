from core.base import BaseScreen
import pygame as pg


def menu(data):
    menu = BaseScreen("Menu", "brown", 1.5)
    menu.create()

    (x, y) = menu.screen.get_rect().center

    menu.add_text(
        40,
        (x, y - 220),
        "COWBOY NUKEM 3D",
        "black",
    )
    menu.create_btn("Start!", 36, "brown", x, y - 100, "standard")
    menu.create_btn("Leaderboard", 36, "brown", x, y, "standard")
    menu.create_btn("Exit", 36, "brown", x, y + 100, "standard")
    menu.add_text(
        32,
        (x, y - 162),
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


def email(data):
    email = BaseScreen("Email", "black", 1.5)
    email.create()

    (x, y) = email.screen.get_rect().center

    email.add_text(
        36,
        (x, y - 54),
        "Please input email address:",
        "white",
    )

    email.add_text(
        36,
        (x, y),
        "",
        "white",
        'brown',
        True
    )

    email.input_config = {
        'size': 36,
        'pos': (x, y),
        'color': 'white',
        'bg': 'brown',
    }

    email.create_btn("Signup", 36, "brown", x - 160, y + 54, "mid")
    email.create_btn("Login", 36, "brown", x, y + 54, "mid")
    email.create_btn("Verify", 36, "brown", x + 160, y + 54, "mid")

    msg = data['message']
    email.add_text(
        32, (x, y +
             258), f'{msg}', "dodgerblue3"
    )

    return email


def pwd(data):
    pwd = BaseScreen("Pwd", "black", 1.5)
    pwd.create()

    (x, y) = pwd.screen.get_rect().center

    pwd.add_text(
        36,
        (x, y - 54),
        "Please input password:",
        "white",
    )

    pwd.add_text(
        36,
        (x, y),
        "",
        "white",
        'brown',
        True
    )

    pwd.input_config = {
        'size': 36,
        'pos': (x, y),
        'color': 'white',
        'bg': 'brown',
    }

    pwd.create_btn("Submit", 36, "brown", x, y + 54, "mid")

    msg = data['message']
    pwd.add_text(
        32, (x, y +
             258), f'{msg}', "dodgerblue3"
    )

    return pwd


def otp(data):
    otp = BaseScreen("Otp", "black", 1.5)
    otp.create()

    (x, y) = otp.screen.get_rect().center

    otp.add_text(
        36,
        (x, y - 54),
        "Please input OTP:",
        "white",
    )

    otp.add_text(
        36,
        (x, y),
        "",
        "white",
        'brown',
        True
    )

    otp.input_config = {
        'size': 36,
        'pos': (x, y),
        'color': 'white',
        'bg': 'brown',
    }

    otp.create_btn("Check", 36, "brown", x, y + 54, "mid")

    msg = data['message']
    otp.add_text(
        32, (x, y +
             258), f'{msg}', "dodgerblue3"
    )

    return otp
