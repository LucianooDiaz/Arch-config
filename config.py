from libqtile import bar, widget
from libqtile.config import Screen
import os

has_battery = os.path.exists("/sys/class/power_supply/BAT0")

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method='line',
                    this_current_screen_border='#88c0d0',
                    active='#ffffff',
                    inactive='#555555',
                    background='#1e1e2e',
                    fontsize=14,
                ),
                widget.Spacer(length=8),
                widget.WindowName(
                    format='{name}',
                    max_chars=60,
                    background='#1e1e2e',
                    foreground='#ffffff',
                ),
                widget.Spacer(length=8),
                widget.Net(
                    interface='wlan0',  # Ajustalo a tu interfaz
                    format='  {down} ↓↑ {up}',
                    background='#1e1e2e',
                    foreground='#a3be8c',
                ),
                *(
                    [widget.Battery(
                        format='  {percent:2.0%}',
                        charge_char='',
                        discharge_char='',
                        empty_char='',
                        full_char='',
                        show_short_text=False,
                        background='#1e1e2e',
                        foreground='#ebcb8b',
                    )] if has_battery else []
                ),
                widget.Clock(
                    format='󰥔  %H:%M',
                    background='#1e1e2e',
                    foreground='#81a1c1',
                ),
            ],
            24,
            background='#1e1e2e',
            margin=[4, 8, 0, 8],
        ),
    ),
]
