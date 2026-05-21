# Parqueadero Inteligente IoT

Proyecto de parqueadero inteligente desarrollado con:

- Python
- OpenCV
- Arduino Mega
- ESP32
- RFID RC522
- LCD 16x2
- Sensores IR
- Servomotores
- WiFi IoT

## Funciones principales

- Detección de vehículos por cámara
- Detección de mal parqueo
- Monitoreo de módulos libres
- Control automático de barreras
- Acceso RFID
- Visualización web en tiempo real
- Monitoreo desde celular o computador

## Arquitectura

Python procesa la cámara usando OpenCV y envía información serial al Arduino Mega y ESP32.

El Arduino Mega controla:

- LCD
- Servomotores
- Sensores IR

El ESP32 controla:

- RFID
- LEDs
- Servidor web IoT
- WiFi

## Tecnologías utilizadas

- Python
- OpenCV
- PySerial
- Arduino IDE
- ESP32
- C++
- Linux Ubuntu

## Autor

Ing. Harold Bejarano
