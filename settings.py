import ctypes
import math
import random

import pygame
import ctypes

user32 = ctypes.windll.user32

WIDTH, HEIGHT = int(user32.GetSystemMetrics(78)), int(user32.GetSystemMetrics(79))
# WIDTH , HEIGHT = 800, 600
TITLE = "Tower Defence"

PLAYER_BULLET_COLOR = (20, 20, 20)
BACKGROUND_COLOR = (255, 255, 255)