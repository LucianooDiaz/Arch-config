#!/bin/sh

# Power menu script using rofi

CHOSEN=$(printf "Bloquear\nSuspender\nReiniciar\nApagar\nCerrar sesion" | rofi -dmenu -p "Inicio/apagado" -theme "/home/luciano/.config/utiles/powermenu.rasi")

case "$CHOSEN" in
    "Bloquear") lockscreen ;;
    "Suspender") systemctl suspend-then-hibernate ;;
    "Reiniciar") reboot ;;
    "Apagar") poweroff ;;
    "Cerrar sesion") hyprctl dispatch exit ;;
    *) exit 1 ;;
esac