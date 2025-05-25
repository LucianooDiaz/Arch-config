import os, locale
os.environ['LC_TIME'] = 'es_AR.UTF-8'
locale.setlocale(locale.LC_TIME, 'es_AR.UTF-8')


from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from pathlib import Path
import subprocess
import json



wal_colors_path= Path.home() / ".cache" /"wal" /"colors.json"

with open(wal_colors_path) as f:
    wal = json.load(f)

    colors = {
        "background": wal["special"]["background"],
        "foreground": wal["special"]["foreground"],
        "border": wal["colors"]["color10"],
        "active": wal["colors"]["color10"],
        "inactive": wal["colors"]["color8"],
    }



mod = "mod4"
terminal = guess_terminal()

keys = [
    Key([mod], "m", lazy.window.toggle_minimize(), desc="Minimize focus"),
    Key([mod], "u", lazy.group.unminimize_all(), desc="Unminimize all"),
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [
    Group("1", label= ""),
    Group("2", label= ""),
    Group("3", label= ""),
    Group("4", label= ""),
]

for i, group in enumerate(groups):
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                group.name,
                lazy.group[group.name].toscreen(),
                desc=f"Switch to group {group.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                group.name,
                lazy.window.togroup(group.name, switch_group=True),
                desc=f"Switch to & move focused window to group {group.name} and switch",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus='#81a1c1',
        border_focus_stack=["#1e1e2e", "#88c0d0"],
        border_normal='#3b4252',
        border_width=3,
        margin=8,
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()



# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
has_battery = os.path.exists("/sys/class/power_supply/BAT0")

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(        #Escritorios
                    name="groupbox",
                    highlight_method='text',
                    this_current_screen_border=colors["border"],
                    background=colors["background"],
                    active=colors["active"],
                    inactive=colors["inactive"],
                    fontsize=14,
                ),

                #widget.Spacer(length=8),
                widget.TextBox(    #Explorador
                    text= "",
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn ("nemo")
                    },
                    fontsize= 18,
                    padding=8,
                    #background= '#00000000',
                    foreground=colors["foreground"],
                ),
                widget.Spacer(length=1),
                widget.TextBox(    #Menu cambio wallpaper
                    text= "",
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn ("/home/luciano/.config/utiles/rofi_menu.sh")
                    },
                    fontsize= 18,
                    padding=8,
                    #background= '#00000000',
                    foreground=colors["foreground"],
                ),




                widget.Spacer(length=4), #Reproductor
                widget.GenPollText(
                    update_interval = 1,
                    func= lambda:(
                        out if "No players found" not in (out :=  subprocess.getoutput(
                            "playerctl metadata --format '󰎆   {{ artist }} - {{ title }}'"
                         ).strip()) else ""
                    ),
                    padding=13,
                    fontsize=13,
                    foreground= '#ffffff',
                    #background= '#00000000',
                    name = 'media',
                    ),




                widget.Spacer(),

                widget.Image(            #Icono central
                    filename = '/home/luciano/.config/qtile/icons/archlinux.svg',
                    mouse_callbacks= {
                       'Button1': lambda: qtile.cmd_spawn ("/home/luciano/.config/utiles/powermenu.sh"),
                        #'Button3': lambda: qtile.cmd_spawn ("shutdown now")
                    },
                        
                    margin = 3,
                    scale = True,

                ),

                widget.Spacer(),

                widget.GenPollText(     #Logo ethernet, wifi o desconectado
                    update_interval=5,
                    func=lambda: subprocess.check_output (
                        ["/home/luciano/.config/utiles/network_icon.sh"],
                        universal_newlines=True,
                        shell=True
                    ).strip(),
                    fontsize=18,
                    foreground=colors["foreground"],
                ),
                #widget.Net(
                #    interface='enp0s3',  # ethernet.  #wlp2s0, wlan0 para wifi
                 #   format=' ↓ {down:.1f} ↑ {up:.1f}',
                  #  background=colors["background"],
                   # foreground=colors["foreground"],
                    #prefix='M',
                #),

                widget.Spacer(length=4),
                widget.GenPollText( #Volumen
                    update_interval=0.5,
                    func=lambda: subprocess.getoutput(
                    "pamixer --get-volume-human | awk '{ if ($1 == \"muted\") print \"󰝟  Muted\"; else print \"󰕾  \"$1 }'"
                    ),
                    foreground=colors["foreground"],
                    background=colors["background"],
                    padding=6,
                    fontsize=13,
),
                *(
                    [widget.Battery( #Bateria
                        format='  {percent:10.0%}',
                        charge_char='',
                        discharge_char='',
                        empty_char='',
                        full_char='',
                        show_short_text=False,
                    background=colors["background"],
                    foreground=colors["foreground"],
                    )] if has_battery else []
                ),
                widget.Spacer(length=2),
                widget.Clock( #Reloj
                    format='󰥔   %H:%M %a',
                    background=colors["background"],
                    foreground=colors["foreground"],
                ),
                widget.Spacer(length=8)
            ],
            24,
            background=colors["background"],
            margin=[4, 8, 0, 8],
            opacity=0.8,
            rounded=True,
        ),
    ),
]
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

autostart = [
   # "feh --bg-fill /home/luciano/.config/utiles/wallpaper.jpg",
    "picom -b",
    "wal -R",
]

for x in autostart:
    os.system(x)

#Escritorios
@hook.subscribe.setgroup 
def update_group_icons():
        for group in qtile.groups:
            group.label = "" if group.name == qtile.current_group.name else ""

        qtile.call_soon(lambda: qtile.widgets_map["groupbox"].bar.draw())
