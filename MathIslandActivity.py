from gettext import gettext as _

import sys
from gi.repository import Gtk
import pygame

import sugar3.activity.activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton


import sugargame.canvas

import MathIsland


class MathIslandActivity(sugar3.activity.activity.Activity):
    def __init__(self, handle):
        super(MathIslandActivity, self).__init__(handle)

        self.paused = False

        # Create the game instance.
        self.game = MathIsland.MathIsland()

        # Build the activity toolbar.
        self.build_toolbar()

        # Build the Pygame canvas.
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)

        # Note that set_canvas implicitly calls read_file when
        # resuming from the Journal.
        self.set_canvas(self._pygamecanvas)

        # Start the game running (self.game.run is called when the
        # activity constructor returns).
        self._pygamecanvas.run_pygame(self.game.run)

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        # Pause/Play button:

        stop_play = ToolButton('media-playback-stop')
        stop_play.set_tooltip(_("Stop"))
        stop_play.set_accelerator(_('<ctrl>space'))
        stop_play.connect('clicked', self._stop_play_cb)
        stop_play.show()

        toolbar_box.toolbar.insert(stop_play, -1)

        # Blank space (separator) and Stop button at the end:

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

    def _stop_play_cb(self, button):
        # Pause or unpause the game.
        self.paused = not self.paused
        self.game.set_paused(self.paused)

        # Update the button to show the next action.
        if self.paused:
            button.set_icon('media-playback-start')
            button.set_tooltip(_("Start"))
        else:
            button.set_icon('media-playback-stop')
            button.set_tooltip(_("Stop"))

    def read_file(self, file_path):
        self.game.read_file(file_path)

    def write_file(self, file_path):
        self.game.write_file(file_path)
