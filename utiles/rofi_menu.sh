#!/bin/bash
#chmod +x ruta de archivo para ejecutar como admin
echo -e "Perfect Blue\nVaporwave\nVaporwave Rosa" | rofi -dmenu -p " Elegi un tema" | while read -r option; do
    case "$option" in
        "Perfect Blue") /home/luciano/.config/utiles/blue_wallpaper.sh ;;
        "Vaporwave") /home/luciano/.config/utiles/lights.sh ;;
        "Vaporwave Rosa") /home/luciano/.config/utiles/vaporwave_rosa.sh ;;
    esac
done
