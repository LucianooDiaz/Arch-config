#!/bin/bash

# Archivo de colores generado por pywal
WAL_COLORS="$HOME/.cache/wal/colors"

# Extraer color de fondo
BACKGROUND=$(sed -n 1p "$WAL_COLORS")

# Reemplazar en dunstrc usando sed
sed -i "s/^background = .*/background = \"$BACKGROUND\"/" ~/.config/dunst/dunstrc
sed -i "s/^frame_color = .*/frame_color = \"$BACKGROUND\"/" ~/.config/dunst/dunstrc

# Reiniciar dunst para aplicar
pkill dunst && dunst &
