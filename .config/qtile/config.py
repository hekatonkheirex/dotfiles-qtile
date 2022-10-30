import os
import socket
import subprocess
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord,hook
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook, qtile
from typing import List  # noqa: F401


# Defaults
mod = "mod4"
myTerm = "wezterm"


# Autostart programs
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])



def focus_previous_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)
    previous_group = group.get_previous_group(skip_empty=True)
    previous_group_index = qtile.groups.index(previous_group)
    if previous_group_index < group_index:
        qtile.current_screen.set_group(previous_group)


def focus_next_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)
    next_group = group.get_next_group(skip_empty=True)
    next_group_index = qtile.groups.index(next_group)
    if next_group_index > group_index:
        qtile.current_screen.set_group(next_group)


def window_to_prev_group(qtile):
    i = qtile.groups.index(qtile.current_group)
    if qtile.current_window is not None and i != 0:
        qtile.current_window.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    i = qtile.groups.index(qtile.current_group)
    if qtile.current_window is not None and i != 6:
        qtile.current_window.togroup(qtile.groups[i + 1].name)


def toggle_minimize_all(qtile):
    group = qtile.current_screen.group
    for win in group.windows:
        win.minimized = not win.minimized
        if win.minimized is False:
            group.layout_all()


keys = [
        # The essentials
        Key(
            [mod], "Return", lazy.spawn(myTerm),
            desc="Launch terminal"
            ),
        Key(
            [mod, "shift"], "r", lazy.restart(),
            desc="Restart Qtile"
            ),
        Key(
            [mod, "shift"], "q", lazy.shutdown(),
            desc="Shutdown Qtile"
            ),
        Key(
            [mod], "w", lazy.window.kill(),
            desc="Kill focused window"
            ),
        Key(
            [mod], "Tab", lazy.next_layout(),
            desc="Toggle between layouts"
            ),

        # Windows management
        Key(
            [mod], "h", lazy.layout.left(),
            desc="Move focus to left"
            ),
        Key(
            [mod], "l", lazy.layout.right(),
            desc="Move focus to right"
            ),
        Key(
            [mod], "j", lazy.layout.down(),
            desc="Move focus down"
            ),
        Key(
            [mod], "k", lazy.layout.up(),
            desc="Move focus up"
            ),
        Key(
            [mod], "space", lazy.layout.next(),
            desc="Move window focus to other window"
            ),
        Key(
            [mod, "shift"], "h", lazy.layout.shuffle_left(),
            desc="Move window to the left"
            ),
        Key(
            [mod, "shift"], "l", lazy.layout.shuffle_right(),
            desc="Move window to the right"
            ),
        Key(
                [mod, "shift"], "j", lazy.layout.shuffle_down(),
                desc="Move window down"
                ),
        Key(
                [mod, "shift"], "k", lazy.layout.shuffle_up(),
                desc="Move window up"
                ),
        Key(
                [mod, "control"], "h", lazy.layout.grow_left(),
                desc="Grow window to the left"
                ),
        Key(
                [mod, "control"], "l", lazy.layout.grow_right(),
                desc="Grow window to the right"
                ),
        Key(
                [mod, "control"], "j", lazy.layout.grow_down(),
                desc="Grow window down"
                ),
        Key(
                [mod, "control"], "k", lazy.layout.grow_up(),
                desc="Grow window up"
                ),
        Key(
                [mod], "n", lazy.layout.normalize(),
                desc="Reset all window sizes"
                ),
        Key(
                [mod, "shift"], "Return", lazy.layout.toggle_split(),
                desc="Toggle between split and unsplit sides of stack"
                ),
        Key(
                [mod], "f", lazy.window.toggle_fullscreen(),
                desc="Toggle fullscreen"
                ),
        Key(
                ["mod1"], "Tab", lazy.layout.next(),
                desc="Microsoft Windows alt+tab windows management"
                ),

        # Custom keybinds
        Key(
                ["control", "mod1"], "l", lazy.spawn('betterlockscreen -l dumblur'),
                desc="Lock the screen"
                ),
        Key(
                [mod], "b", lazy.spawn('firefox'),
                desc="Launch Firefox"
                ),
        Key(
                [mod], "t", lazy.spawn('Thunar'),
                desc="Launch Thunar"
                ),
        Key(
                [mod], "d", lazy.spawn('rofi -show drun'),
                desc="Spawn rofi"
                ),
        Key(
                [mod], "p", lazy.spawn('rofi -show power'),
                desc="Spawn powermenu"
                ),

        # Audio keybindings
        Key(
                [], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle"),
                lazy.spawn("dunstify -i ~/.config/dunst/vmute.png 'Audio muted'"),
                desc="Mute audio"
                ),
        Key(
                [], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%"),
                lazy.spawn("dunstify -i ~/.config/dunst/vdown.png 'Volume down'"),
                desc="Lower audio"
                ),
        Key(
                [], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%"),
                lazy.spawn("dunstify -i ~/.config/dunst/vup.png 'Volume up'"),
                desc="Raise audio"
                ),

        # Screenshots
        Key(
                [], "Print", lazy.spawn("scrot 'screenshot_%Y%m%d_%H%M%S.png' -e \
                        'mkdir -p ~/Pictures/Screenshots && mv $f \
                        ~/Pictures/Screenshots && xclip -selection clipboard \
                        -t image/png -i ~/Pictures/Screenshots/`ls \
                        -1 -t ~/Pictures/Screenshots | head -1`'"),
                lazy.spawn("dunstify -i ~/.config/dunst/screenshot.png \
                        'Screenshot captured'"),
                desc="Take screenshot"
                )
        ]

groups = []
group_names = 'www term file share mus'.split()
group_labels = ["󱓼", "󱓼", "󱓼", "󱓼", "󱓼"]
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

for i in range(len(group_names)):
    groups.append(
            Group(
                name=group_names[i],
                layout=group_layouts[i].lower(),
                label=group_labels[i]
                ))


@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
    d[group_names[0]] = [
            "firefox",
            "Firefox",
            "Navigator",
            "google-chrome",
            "Google-chrome"
            ]
    d[group_names[1]] = [
            "org.wezfurlong.wezterm"
            ]
    d[group_names[2]] = [
            "thunar"
            ]
    d[group_names[3]] = [
            "qBittorrent",
            "discord"
            ]
    d[group_names[4]] = [
            "Spotify"
            ]

    wm_class = client.window.get_wm_class()[0]

    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen(toggle=False)

for i, name in enumerate(group_names, 1):
    keys.extend([
        Key([mod], str(i), lazy.group[name].toscreen()),
        Key([mod, 'shift'], str(i), lazy.window.togroup(name))])

# layouts
# Catppuccin
layout_theme = {
        "border_width": 2,
        "margin": 15,
        "border_focus": "cba6f7",
        "border_normal": "1e1e2e"
        }

layouts = [
        layout.MonadTall(
            border_focus='89b4fa',
            border_normal='1e1e2e',
            border_width=4,
            margin=15,
            ratio=0.52
            ),
        layout.Floating(
            border_focus='f5c2e7',
            border_normal='1e1e2e',
            border_width=4,
            fullscreen_border_width=0
            ),
        layout.Spiral(
            border_focus='89b4fa',
            border_normal='1e1e2e',
            margin=15,
            border_width=4
            )
        ]

# Colors definitions
# Catppuccin
colors = [
        ["#1e1e2e", "#1e1e2e"],  # 0 Background 0
        ["#313244", "#313244"],  # 1 Background 1
        ["#cdd6f4", "#cdd6f4"],  # 2 Foreground 0
        ["#bac2de", "#bac2de"],  # 3 Foreground 1
        ["#f38ba8", "#f38ba8"],  # 4 Red
        ["#a6e3a1", "#a6e3a1"],  # 5 Green
        ["#f9e2af", "#f9e2af"],  # 6 Yellow
        ["#89b4fa", "#89b4fa"],  # 7 Blue
        ["#f5c2e7", "#f5c2e7"],  # 8 Magenta
        ["#89dceb", "#89dceb"],  # 9 Cyan
        ["#fab387", "#fab387"],  # 10 Orange
        ["#cba6f7", "#cba6f7"]  # 11 Violet
        ]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

# Widgets definitions
widget_defaults = dict(
        font='Inter',
        fontsize=18,
        padding=4,
        background='#1e1e2e',
        foreground='#cdd6f4'
        )

extension_defaults = widget_defaults.copy()

screens = [
        Screen(
            top=bar.Bar(
                [
                    widget.Spacer(
                        length=10
                        ),
                    widget.Image(
                        filename='~/.config/qtile/assets/bar/qtile.png',
                        margin=7
                        ),
                    widget.Spacer(
                        length=20
                        ),
                    widget.GroupBox(
                        active=colors[4],
                        block_highlight_text_color=colors[7],
                        borderwidth=0,
                        disable_drag=True,
                        font='Material Design Icons',
                        fontsize=18,
                        inactive=colors[5],
                        rounded=True
                        ),
                    widget.Spacer(
                        length=bar.STRETCH
                        ),
                    widget.Mpris2(
                        name="Spotify",
                        objname="org.mpris.MediaPlayer2.spotify",
                        display_metadata=['xesam:title', 'xesam:artist'],
                        max_chars=50,
                        width=150,
                        fontsize=12,
                        foreground=colors[5]
                        ),
                    widget.Spacer(
                        lenght=bar.STRETCH
                        ),
                    # widget.Image(
                    #     filename='~/.config/qtile/assets/bar/sun.png',
                    #     margin=8
                    #     ),
                    # widget.Backlight(
                    #     foreground=colors[6],
                    #     brightness_file='/sys/class/backlight/amdgpu_bl0/actual_brightness',
                    #     max_brightness_file='/sys/class/backlight/amdgpu_bl0/max_brightness',
                    #     fontsize=12,
                    #     padding=0
                    #     ),
                    # widget.Spacer(
                    #     length=16
                    #     ),
                    # widget.Image(
                    #         filename='~/.config/qtile/assets/bar/vol.png',
                    #         margin=8
                    #         ),
                    # widget.PulseVolume(
                    #         foregroun=colors[8],
                    #         fontsize=12,
                    #         padding=0
                    #         ),
                    # widget.Spacer(
                    #         length=16,
                    #         ),
                    # widget.Image(
                    #         filename='~/.config/qtile/assets/bar/bat.png',
                    #         margin=7,
                    #         ),
                    # widget.Battery(
                    #         format=' {percent:2.0%}',
                    #         foreground = colors[5],
                    #         fontsize=12,
                    #         padding=0,
                    #         ),
                    widget.Wttr(
                            location={'Asuncion': 'Asuncion'},
                            padding=4,
                            format=1,
                            fontsize=12
                            ),
                    widget.Spacer(
                            length=30
                            ),
                    widget.Spacer(
                            length=10,
                            background=colors[1]
                            ),
                    widget.Systray(
                            icon_size=24,
                            padding=0,
                            background=colors[1]
                            ),
                    widget.Spacer(
                            length=10,
                            background=colors[1]
                            ),
                    widget.Spacer(
                            length=20
                            ),
                    widget.Clock(
                            format='%H:%M',
                            font='Inter Bold'
                            ),
                    widget.Spacer(
                            length=10
                            ),
                    widget.CurrentLayoutIcon(
                            padding=0,
                            scale=0.6
                            ),
                    widget.Image(
                            filename='~/.config/qtile/assets/bar/power.png',
                            margin=8,
                            mouse_callbacks={
                                'Button1': lambda: qtile.cmd_spawn('rofi -show power')
                                }
                            ),
                    widget.Spacer(
                            length=10
                            ),
                    ],
                    34,
                    margin=[5, 5, 0, 5],
                    background=colors[0],
                    ),
                    )
                    ]

# Drag floating layouts
mouse = [
        Drag(
            [mod], "Button1", lazy.window.set_position_floating(),
            start=lazy.window.get_position()
            ),
        Drag(
            [mod], "Button3", lazy.window.set_size_floating(),
            start=lazy.window.get_size()
            ),
        Click(
            [mod], "Button2", lazy.window.bring_to_front()
            )
        ]

# General configurations
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
        border_focus='ebbcba',
        border_normal='191724',
        border_width=4,
        fullscreen_border_width=0,
        float_rules=[
            # Run the utility `xprop` to see the wm class and name of an X client
            *layout.Floating.default_float_rules,
            Match(wm_class='confirmreset'),  # gitk
            Match(wm_class='makebranch'),  # gitk
            Match(wm_class='maketag'),  # gitk
            Match(wm_class='ssh-askpass'),  # ssh-askpass
            Match(title='branchdialog'),  # gitk
            Match(title='pinentry'),  # GPG key password entry
            Match(wm_class='Galculator'),
            ]
        )
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
# wmname = "LG3D"
wmname = "Qtile"
