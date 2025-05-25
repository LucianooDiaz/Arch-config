#!/bin/bash
#chmod +x ruta de archivo para ejecutar como admin
echo -e "Perfect Blue\nVaporwave\nVaporwave Rosa\nArchPool\nAquarium\nHIRAETH" | rofi -dmenu -p " Elegi un tema" | while read -r option; do
    case "$option" in
        "Perfect Blue") /home/luciano/.config/utiles/blue_wallpaper.sh ;;
        "Vaporwave") /home/luciano/.config/utiles/lights.sh ;;
        "Vaporwave Rosa") /home/luciano/.config/utiles/vaporwave_rosa.sh ;;
        "ArchPool") /home/luciano/.config/utiles/ArchPool.sh ;;
        "Aquarium") /home/luciano/.config/utiles/aquarium.sh ;;
        "HIRAETH") /home/luciano/.config/utiles/HIRAETH.sh ;;
    esac
done
