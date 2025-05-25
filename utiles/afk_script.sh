#!/bin/bash

IDLE_TIME_LIMIT= 5000  # 5 minutos en milisegundos

while true; do
    idle_time=$(xprintidle)
    if [ "$idle_time" -ge "$IDLE_TIME_LIMIT" ]; then
        clear
        asciiquarium
        # Después de salir de asciiquarium espera para que no se ejecute de nuevo inmediatamente
        sleep 10
    fi
    sleep 5
done