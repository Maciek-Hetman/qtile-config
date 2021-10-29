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

from typing import List
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import qtile, hook, extension
import os, subprocess, socket

mod = "mod4"
terminal = "kitty"
WebBrowser = "firefox"
AppLauncher = "rofi -show drun"

margin_size = 4

keys = [
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod, "shift"], "Return", lazy.spawn(WebBrowser)),
    Key([mod], "space", lazy.spawn(AppLauncher)),

    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),

    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

layouts = [
    layout.Columns(border_width=0, margin=margin_size),
    layout.Max(),
    layout.MonadTall(),
    layout.MonadWide(),
    layout.Tile()
]

widget_defaults = dict(
    font='Ubuntu',
    fontsize=13,
    padding=3,
)

extenstion_defaults = widget_defaults.copy()

colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]] # background for inactive screens

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    foreground=colors[2],
                    background=colors[0],
                ),
                widget.GroupBox(
                    font = "Ubuntu Bold",
                    fontsize = 10,
                    margin_y = 5,
                    margin_x = 0,
                    padding_y = 5,
                    padding_x = 3,
                    borderwidth = 3,
                    active = colors[2],
                    inactive = colors[7],
                    rounded = False,
                    highlight_color = colors[1],
                    highlight_method = "line",
                    this_current_screen_border = colors[6],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[6],
                    other_screen_border = colors[4],
                    foreground = colors[2],
                    background = colors[0]
                ),
                widget.Prompt(
                    prompt = prompt,
                    padding = 10,
                    foreground = colors[3],
                    background = colors[1]
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    foreground=colors[2],
                    background=colors[0],
                ),
                widget.WindowName(
                    foreground = colors[6],
                    background = colors[0]
                ),
                widget.Systray(
                    background = colors [0],
                    padding = 5
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    foreground=colors[2],
                    background=colors[0],
                ),
                widget.Memory(
                    foreground = colors[6],
                    background = colors[0],
                    padding = 0
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    foreground=colors[2],
                    background=colors[0],
                ),
                widget.Volume(
                    foreground = colors[6],
                    background = colors[0],
                    padding = 0
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    foreground=colors[2],
                    background=colors[0],
                ),
                widget.Clock(
                    format='%I:%M:%S %p',
                    foreground = colors[6]
                ),
            ],
            24,
            opacity=0.75,
            background=colors[0],
            margin = [4, 4, 0, 4],
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

droups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='ssh-askpass'),
    Match(title='branchdialog'),
    Match(title='pinentry'),
])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wmname = "qtile"

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

