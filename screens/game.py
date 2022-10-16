from core.base import BaseScreen
import pygame as pg


def play():
    play = BaseScreen("Play", "black", 1.5)
    play.create()

    return play


def leaderboard():
    lead = BaseScreen("Leaderboard", "black", 1.5)
    lead.create()

    return lead
