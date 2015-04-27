__author__ = 'mark'
""" Storing project wide variables """
import os
import sys, pygame
from pygame.locals import *
import time

__production = False

# Setting up touch screen, set if statement to true on Raspberry Pi
if __production:
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
    os.environ["SDL_MOUSEDRV"] = "TSLIB"

# Display settings
pygame.init() 	# Pygame initialization
display_size = screen_width, screen_height = 320, 240

if __production: # If started on Raspberry Pi
    display_flags = FULLSCREEN | DOUBLEBUF                          # Turn on video acceleration
    screen = pygame.display.set_mode(display_size, display_flags)
    pygame.mouse.set_visible(False)                                 # Hide mouse cursor
else:
    screen = pygame.display.set_mode(display_size)


RESOURCES = "resources/"


# Standard font type
FONT = pygame.font.Font(RESOURCES + "UbuntuMono-B.ttf", 14)

# Define colours
BLUE = 0, 148, 255
CREAM = 206, 206, 206
BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
# Scheme aqua (currently not in use)
AQUA_TEAL = 18, 151, 147
AQUA_CHARCOAL = 80, 80, 80
AQUA_YELLOW = 255, 245, 195
AQUA_BLUE = 155, 215, 213
AQUA_PINK = 255, 114, 96
# Scheme FIFTIES
FIFTIES_CHARCOAL = 124, 120, 106
FIFTIES_TEAL = 141, 205, 193
FIFTIES_GREEN = 211, 227, 151
FIFTIES_YELLOW = 255, 245, 195
FIFTIES_ORANGE = 235, 110, 68

# Mouse related variables
MIN_SWIPE = 50  # Minimum movement in pixels to call it a swipe
MAX_CLICK = 15  # Maximum movement in pixels to call it a click
LONG_PRESS_TIME = 500   # Minimum time to call a click a long press
SWIPE_CLICK = 0
SWIPE_LEFT = 1
SWIPE_RIGHT = 2
SWIPE_UP = 3
SWIPE_DOWN = 4
SWIPE_LONG_PRESS = 5

""" Used icons """
# General
ICO_PLAYER = RESOURCES + "home_48x32.png"
ICO_PLAYER_ACTIVE = RESOURCES + "home_active_48x32.png"
ICO_LIBRARY = RESOURCES + "library_48x32.png"
ICO_LIBRARY_ACTIVE = RESOURCES + "library_active_48x32.png"
ICO_SETTINGS = RESOURCES + "settings_48x32.png"
ICO_SETTINGS_ACTIVE = RESOURCES + "settings_active_48x32.png"
ICO_EXIT = RESOURCES + "exit_48x32.png"

# Player
ICO_PLAY = RESOURCES + "play_48x32.png"
ICO_PAUSE = RESOURCES + "pause_48x32.png"
ICO_NEXT = RESOURCES + "next_48x32.png"
ICO_PREVIOUS = RESOURCES + "prev_48x32.png"
ICO_VOLUME_UP = RESOURCES + "vol_up_48x32.png"
ICO_VOLUME_DOWN = RESOURCES + "vol_down_48x32.png"

# Library
ICO_SEARCH = RESOURCES + "search_48x32.png"
ICO_SEARCH_ACTIVE = RESOURCES + "search_active_48x32.png"
ICO_SEARCH_ARTIST = RESOURCES + "artists_48x32.png"
ICO_SEARCH_ARTIST_ACTIVE = RESOURCES + "artists_active_48x32.png"
ICO_SEARCH_ALBUM = RESOURCES + "albums_48x32.png"
ICO_SEARCH_ALBUM_ACTIVE = RESOURCES + "albums_active_48x32.png"
ICO_SEARCH_SONG = RESOURCES + "songs_48x32.png"
ICO_SEARCH_SONG_ACTIVE = RESOURCES + "songs_active_48x32.png"

