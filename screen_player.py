# This file is part of pi-jukebox.
#
# pi-jukebox is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pi-jukebox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pi-jukebox. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2015- by Mark Zwart, <mark.zwart@pobox.com>
"""
=======================================================
**screen_player.py**: Playback screen.
=======================================================
"""

import sys, pygame
from pygame.locals import *
import time
import subprocess
import os
import glob
from gui_widgets import *
from gui_screens import *
from pij_screen_navigation import *
from mpd_client import *
from settings import *
from screen_settings import *


class ScreenPlaying(Screen):
    """ Screen cover art

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """

    def __init__(self, screen_surface):
        Screen.__init__(self, screen_surface)
        # Screen navigation buttons
        self.add_component(ScreenNavigation('screen_nav', self.surface, 'btn_player'))
        # Player specific buttons
        self.add_component(ButtonIcon('btn_play', self.surface, ICO_PLAY, SCREEN_WIDTH - 51, 5))
        self.add_component(ButtonIcon('btn_stop', self.surface, ICO_STOP, SCREEN_WIDTH - 51, 45))
        self.add_component(ButtonIcon('btn_prev', self.surface, ICO_PREVIOUS, SCREEN_WIDTH - 51, 85))
        self.add_component(ButtonIcon('btn_next', self.surface, ICO_NEXT, SCREEN_WIDTH - 51, 125))
        self.add_component(ButtonIcon('btn_volume', self.surface, ICO_VOLUME, SCREEN_WIDTH - 51, 165))
        # Cover art
        # self.add_component(Picture('pic_cover_art', self.surface, 79, 40, 162, 162, mpd.get_cover_art()))
        self.draw_cover_art()
        # Player specific labels
        self.add_component(LabelText('lbl_track_artist', self.surface, 54, 3, SCREEN_WIDTH - 110, 18))
        self.components['lbl_track_artist'].set_alignment(HOR_MID, VERT_MID)
        self.add_component(LabelText('lbl_track_album', self.surface, 54, 19, SCREEN_WIDTH - 110, 18))
        self.components['lbl_track_album'].set_alignment(HOR_MID, VERT_MID)
        self.add_component(LabelText('lbl_track_title', self.surface, 55, SCREEN_HEIGHT - 27, SCREEN_WIDTH - 108, 18))
        self.components['lbl_track_title'].set_alignment(HOR_MID, VERT_MID)
        self.add_component(LabelText('lbl_time_current', self.surface, SCREEN_WIDTH - 51, 205, 48, 18))
        self.components['lbl_time_current'].set_alignment(HOR_MID, VERT_MID)
        self.add_component(LabelText('lbl_time_total', self.surface, SCREEN_WIDTH - 51, SCREEN_WIDTH - 99, 48, 18))
        self.components['lbl_time_total'].set_alignment(HOR_MID, VERT_MID)
        self.add_component(Slider2('slide_time', self.surface, 55, SCREEN_HEIGHT - 35, SCREEN_WIDTH - 108, 3))

    def show(self):
        """ Displays the screen. """
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        self.components['lbl_time_current'].text_set(mpd.now_playing.time_current)
        self.components['lbl_time_total'].text_set(mpd.now_playing.time_total)
        if mpd.player_control_get() == 'play':
            self.components['btn_play'].set_image_file(ICO_PAUSE)
        else:
            self.components['btn_play'].set_image_file(ICO_PLAY)
        self.components['btn_play'].draw()
        self.components['lbl_track_title'].text_set(mpd.now_playing.title)
        self.components['lbl_track_artist'].text_set(mpd.now_playing.artist)
        self.components['lbl_track_album'].text_set(mpd.now_playing.album)
        if mpd.radio_mode_get():
            self.components['lbl_track_artist'].visible = False
            self.components['lbl_track_album'].position_set(54, 3, SCREEN_WIDTH - 105, 39)
            self.components['pic_cover_art'].picture_set(COVER_ART_RADIO)
        else:
            self.components['lbl_track_artist'].visible = True
            self.components['lbl_track_artist'].text_set(mpd.now_playing.artist)
            self.components['lbl_track_album'].position_set(54, 19, SCREEN_WIDTH - 105, 18)
            self.components['pic_cover_art'].picture_set(mpd.now_playing.cover_art_get())
        return super(ScreenPlaying, self).show()  # Draw screen

    def update(self):
        while True:
            try:
                event = mpd.events.popleft()
                self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
                playing = mpd.now_playing
                if event == 'time_elapsed':
                    self.components['lbl_time_current'].text_set(playing.time_current)
                    self.components['slide_time'].draw(playing.time_percentage)
                elif event == 'playing_file':
                    self.components['lbl_track_title'].text_set(playing.title)
                    if mpd.radio_mode_get():
                        self.components['lbl_track_artist'].visible = False
                        self.components['lbl_track_album'].position_set(54, 3, SCREEN_WIDTH - 105, 39)
                        self.components['pic_cover_art'].picture_set(COVER_ART_RADIO)
                    else:
                        self.components['lbl_track_artist'].visible = True
                        self.components['lbl_track_artist'].text_set(playing.artist)
                        self.components['lbl_track_album'].position_set(54, 19, SCREEN_WIDTH - 105, 18)
                        self.components['pic_cover_art'].picture_set(mpd.now_playing.cover_art_get())
                    self.components['lbl_track_album'].text_set(playing.album)
                    self.components['lbl_time_total'].text_set(playing.time_total)
                elif event == 'state':
                    if self.components['btn_play'].image_file != ICO_PAUSE and mpd.player_control_get() == 'play':
                        self.components['btn_play'].draw(ICO_PAUSE)
                    elif self.components['btn_play'].image_file == ICO_PAUSE and mpd.player_control_get() != 'play':
                        self.components['btn_play'].draw(ICO_PLAY)
            except IndexError:
                break

    def on_click(self, x, y):
        tag_name = super(ScreenPlaying, self).on_click(x, y)
        if tag_name == 'btn_player':
            self.return_object = 0
            self.close()
        elif tag_name == 'btn_playlist':
            self.return_object = 1
            self.close()
        elif tag_name == 'btn_library':
            self.return_object = 2
            self.close()
        elif tag_name == 'btn_directory':
            self.return_object = 3
            self.close()
        elif tag_name == 'btn_radio':
            self.return_object = 4
            self.close()
        elif tag_name == 'btn_settings':
            setting_screen = ScreenSettings(self)
            setting_screen.show()
            self.show()
        elif tag_name == 'btn_play':
            if mpd.player_control_get() == 'play':
                mpd.player_control_set('pause')
                self.components['btn_play'].set_image_file(ICO_PLAY)
            else:
                mpd.player_control_set('play')
                self.components['btn_play'].set_image_file(ICO_PAUSE)
            self.components['btn_play'].draw()
        elif tag_name == 'btn_stop':
            self.components['btn_play'].set_image_file(ICO_PLAY)
            mpd.player_control_set('stop')
        elif tag_name == 'btn_prev':
            mpd.player_control_set('previous')
        elif tag_name == 'btn_next':
            mpd.player_control_set('next')
        elif tag_name == 'btn_volume':
            screen_volume = ScreenVolume(self)
            screen_volume.show()
            self.show()

    def draw_cover_art(self):
        left_position = 79
        hor_length = SCREEN_WIDTH - 2 * 79
        top_position = 40
        vert_length = SCREEN_HEIGHT - 2 * 40
        if hor_length > vert_length:
            cover_size = vert_length
            top_position = 40
            left_position = (SCREEN_WIDTH - cover_size) / 2
        else:
            cover_size = hor_length
            top_position = (SCREEN_HEIGHT - cover_size) / 2
            left_position = 79

        self.add_component(Picture('pic_cover_art', self.surface, left_position, top_position, cover_size, cover_size,
                                   mpd.get_cover_art()))

class ScreenPlaylist(Screen):
    """ The screen containing everything to control playback.
    """
    def __init__(self, screen_rect):
        Screen.__init__(self, screen_rect)
        # Screen navigation buttons
        self.add_component(ScreenNavigation('screen_nav', self.surface, 'btn_playlist'))
        # Player specific buttons
        self.add_component(ButtonIcon('btn_play', self.surface, ICO_PLAY, SCREEN_WIDTH - 51, 45))
        self.add_component(ButtonIcon('btn_stop', self.surface, ICO_STOP, SCREEN_WIDTH - 51, 85))
        self.add_component(ButtonIcon('btn_prev', self.surface, ICO_PREVIOUS, SCREEN_WIDTH - 51, 125))
        self.add_component(ButtonIcon('btn_next', self.surface, ICO_NEXT, SCREEN_WIDTH - 51, 165))
        self.add_component(ButtonIcon('btn_volume', self.surface, ICO_VOLUME, SCREEN_WIDTH - 51, 205))
        # Player specific labels
        self.add_component(LabelText('lbl_track_title', self.surface, 55, 5, SCREEN_WIDTH - 130, 18))
        self.add_component(LabelText('lbl_track_artist', self.surface, 55, 23, SCREEN_WIDTH - 130, 18))
        self.add_component(LabelText('lbl_time', self.surface, SCREEN_WIDTH - 67, 5, 67, 18))
        self.add_component(LabelText('lbl_volume', self.surface, SCREEN_WIDTH - 70, 23, 70, 18))
        # Splits labels from playlist
        self.add_component(Rectangle('rct_split', self.surface, 55, 43, SCREEN_WIDTH - 112, 1))
        # Playlist
        self.add_component(Playlist(self.surface))
        self.components['list_playing'].active_item_index = mpd.playlist_current_playing_index_get()

    def show(self):
        """ Displays the screen. """
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        now_playing = mpd.now_playing
        self.components['lbl_time'].text_set(now_playing.time_current + '/' + now_playing.time_total)
        self.components['lbl_volume'].text_set('Vol: ' + str(mpd.volume) + '%')
        if mpd.player_control_get() == 'play':
            self.components['btn_play'].set_image_file(ICO_PAUSE)
        else:
            self.components['btn_play'].set_image_file(ICO_PLAY)
        self.components['btn_play'].draw()
        self.components['lbl_track_title'].text_set(now_playing.title)
        self.components['lbl_track_artist'].text_set(now_playing.artist)
        self.components['list_playing'].show_playlist()
        self.components['list_playing'].show_item_active()  # Makes sure currently playing playlist item is on screen
        return super(ScreenPlaylist, self).show()

    def update(self):
        now_playing = mpd.now_playing
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        while True:
            try:
                event = mpd.events.popleft()
                if event == 'volume':
                    self.components['lbl_volume'].text_set('Vol: ' + str(mpd.volume) + '%')
                elif event == 'playing_index':
                    self.components['list_playing'].show_playlist()
                elif event == 'time_elapsed' or event == 'playing_time_total':
                    self.components['lbl_time'].text_set(now_playing.time_current + '/' + now_playing.time_total)
                elif event == 'playing_file':
                    self.components['lbl_track_title'].text_set(now_playing.title)
                    self.components['lbl_track_artist'].text_set(now_playing.artist)
                elif event == 'state':
                    state = mpd.player_control_get()
                    if self.components['btn_play'].image_file != ICO_PAUSE and state == 'play':
                        self.components['btn_play'].draw(ICO_PAUSE)
                    elif self.components['btn_play'].image_file == ICO_PAUSE and state != 'play':
                        self.components['btn_play'].draw(ICO_PLAY)
            except IndexError:
                break

    def on_click(self, x, y):
        """
        :param x: The horizontal click position.
        :param y: The vertical click position.

        :return: Possibly returns a screen index number to switch to.
        """
        tag_name = super(ScreenPlaylist, self).on_click(x, y)
        if tag_name == 'btn_player':
            self.return_object = 0
            self.close()
        elif tag_name == 'btn_playlist':
            self.return_object = 1
            self.close()
        elif tag_name == 'btn_library':
            self.return_object = 2
            self.close()
        elif tag_name == 'btn_directory':
            self.return_object = 3
            self.close()
        elif tag_name == 'btn_radio':
            self.return_object = 4
            self.close()
        elif tag_name == 'btn_settings':
            setting_screen = ScreenSettings(self)
            setting_screen.show()
            self.show()
        elif tag_name == 'btn_play':
            if mpd.player_control_get() == 'play':
                mpd.player_control_set('pause')
                self.components['btn_play'].set_image_file(ICO_PLAY)
            else:
                mpd.player_control_set('play')
                self.components['btn_play'].set_image_file(ICO_PAUSE)
            self.components['btn_play'].draw()
        elif tag_name == 'btn_stop':
            self.components['btn_play'].set_image_file(ICO_PLAY)
            mpd.player_control_set('stop')
        elif tag_name == 'btn_prev':
            mpd.player_control_set('previous')
        elif tag_name == 'btn_next':
            mpd.player_control_set('next')
        elif tag_name == 'btn_volume':
            screen_volume = ScreenVolume(self)
            screen_volume.show()
            self.show()
        elif tag_name == 'list_playing':
            selected_index = self.components['list_playing'].item_selected_index
            if selected_index >= 0:
                mpd.play_playlist_item(selected_index + 1)
                self.components['list_playing'].active_item_index = selected_index
                self.components['list_playing'].draw()


class Playlist(ItemList):
    """ Displays playlist information.

        :param screen_rect: The display's rect where the library browser is drawn on.
    """

    def __init__(self, surface):
        ItemList.__init__(self, 'list_playing', surface, 52, 46, SCREEN_WIDTH - 104, SCREEN_HEIGHT - 51)
        self.item_height = 27
        self.item_active_color = FIFTIES_ORANGE
        self.outline_color = FIFTIES_CHARCOAL
        self.font_color = FIFTIES_YELLOW
        self.outline_visible = False

    def show_playlist(self):
        """ Display the playlist. """
        updated = False
        playing_nr = mpd.playlist_current_playing_index_get()
        if self.list != mpd.playlist_current_get():
            self.list = mpd.playlist_current_get()
            updated = True
        if self.active_item_index != mpd.playlist_current_playing_index_get():
            self.active_item_index = mpd.playlist_current_playing_index_get()
            updated = True
        if updated:
            self.draw()


class ScreenVolume(ScreenModal):
    """ Screen setting volume

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """

    def __init__(self, screen):
        ScreenModal.__init__(self, screen, "Volume")
        self.window_x = 15
        self.window_y = 52
        self.window_width -= 2 * self.window_x
        self.window_height -= 2 * self.window_y
        self.outline_shown = True
        self.title_color = FIFTIES_GREEN
        self.outline_color = FIFTIES_GREEN

        self.add_component(ButtonIcon('btn_mute', self.surface, ICO_VOLUME_MUTE, self.window_x + 5, self.window_y + 25))
        self.components['btn_mute'].x_pos = self.window_x + self.window_width / 2 - self.components[
                                                                                        'btn_mute'].width / 2
        self.add_component(
            ButtonIcon('btn_volume_down', self.surface, ICO_VOLUME_DOWN, self.window_x + 5, self.window_y + 25))
        self.add_component(
            ButtonIcon('btn_volume_up', self.surface, ICO_VOLUME_UP, self.window_width - 40, self.window_y + 25))
        self.add_component(
            Slider('slide_volume', self.surface, self.window_x + 8, self.window_y + 63, self.window_width - 18, 30))
        self.components['slide_volume'].progress_percentage_set(mpd.volume)
        self.add_component(
            ButtonText('btn_back', self.surface, self.window_x + self.window_width / 2 - 23, self.window_y + 98, 46, 32,
                       "Back"))
        self.components['btn_back'].button_color = FIFTIES_TEAL

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_mute':
            mpd.volume_mute_switch()
            self.components['slide_volume'].progress_percentage_set(mpd.volume)
        elif tag_name == 'btn_volume_down':
            mpd.volume_set_relative(-10)
            self.components['slide_volume'].progress_percentage_set(mpd.volume)
        elif tag_name == 'btn_volume_up':
            mpd.volume_set_relative(10)
            self.components['slide_volume'].progress_percentage_set(mpd.volume)
        elif tag_name == 'slide_volume':
            mpd.volume_set(self.components['slide_volume'].progress_percentage)
        elif tag_name == 'btn_back':
            self.close()
        if mpd.volume == 0 or mpd.volume_mute_get():
            self.components['btn_mute'].set_image_file(ICO_VOLUME_MUTE_ACTIVE)
        else:
            self.components['btn_mute'].set_image_file(ICO_VOLUME_MUTE)
        self.components['btn_mute'].draw()
