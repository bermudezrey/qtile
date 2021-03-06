# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from typing import List  # noqa: F401

mod = "mod4"


#### KEY BINDINGS ####
keys = [

	# Essentials

		# Open terminal
		    Key(
		    	[mod], "Return", 
		    	lazy.spawn("terminator"),
		    	desc = 'Terminal run launcher'
		    ),
	
		# Launch dmenu
			Key(
				["control"], "space",
				lazy.spawn("dmenu_run -p 'Run: '"),
				desc='Dmenu run launcher'
			),

		# Launch Firefox
			Key(
				[mod, "control"], "f",
				lazy.spawn("firefox"),
				desc='Launches Firefox'
			),

		# Launch Min (browser for Roam)
			Key(
				[mod, "shift"], "r",
				lazy.spawn("min"),
				desc='Launches Min browser'
			),

	# Window management
	
	    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod, "shift"], "Tab", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]


#### GROUPS ####

group_names = [("SYS", {'layout': 'monadtall'}),
               ("WWW", {'layout': 'max'}),
               ("ROAM", {'layout': 'max'}),
               ("DOC", {'layout': 'monadtall'}),
               ("PDF", {'layout': 'monadtall'}),
               ("DEV", {'layout': 'monadtall'}),
               ("EMAIL", {'layout': 'monadtall'}),
               ("ETC1", {'layout': 'monadtall'}),
               ("ETC2", {'layout': 'monadtall'})
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group	



#### LAYOUTS ####
layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

#### COLORS: TEST ####
#colors = {red:


##### COLORS: DT's version #####
#colors = [["#282a36", "#282a36"], # panel background
#          ["#434758", "#434758"], # background for current screen tab
#          ["#ffffff", "#ffffff"], # font color for group names
#          ["#ff5555", "#ff5555"], # border line color for current tab
#          ["#8d62a9", "#8d62a9"], # border line color for other tab and odd widgets
#          ["#668bd7", "#668bd7"], # color for the even widgets
#          ["#e1acff", "#e1acff"]] # window name


#### DEFAULT WIDGET SETTINGS ####
widget_defaults = dict(
    font='sans',
    fontsize=24,
    padding=3,
)
extension_defaults = widget_defaults.copy()


#### BAR & WIDGETS ####

screens = [
    Screen(
        top=bar.Bar(
            [
			widget.Sep(
				linewidth = 0,
				padding = 30),
			widget.GroupBox(
				#font = "Ubuntu Bold",
				#margin_y = 6,
				#borderwidth = 3
				#,
				#active = colors[?],
				#inactive = colors[?],
				#highlight_color = colors[?],
				#highlight_method = "line"),
				),
			#widget.Prompt(),
			#widget.TaskList(),
			widget.WindowName(),
			widget.Systray(),
			widget.CurrentLayout(),
			widget.Sep(
				linewidth = 0,
				padding = 15),
			widget.CPUGraph(),
			widget.Sep(
				linewidth = 0,
				padding = 15),
			widget.MemoryGraph(),
			widget.Sep(
				linewidth = 0,
				padding = 15),
			widget.BatteryIcon(),
			widget.Sep(
				linewidth = 0,
				padding = 15),
			widget.Clock(format='%a, %B %d [ %I:%M ]'),
			#widget.Wallpaper(
				#directory='~/Documents/MEGA/system_files/wallpapers/',
				#random_selection=True
				#)
            #widget.QuickExit(),
            ],
            32,
        ),
		wallpaper='~/Documents/MEGA/system_files/wallpapers/Stripes.jpg',
            wallpaper_mode='fill'
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

##### STARTUP APPLICATIONS #####
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
