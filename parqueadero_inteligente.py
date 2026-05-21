# ================= LIBRERIAS ==================

import cv2
# Librería OpenCV
# Se usa para cámara y visión artificial

import numpy as np
# Librería NumPy
# Se usa para matrices y procesamiento de imágenes

import serial
# Comunicación serial con Arduino y ESP32

import time
# Manejo de tiempos y pausas


# ================= CONEXIONES SERIAL ==================

arduino = serial.Serial('/dev/ttyUSB0', 9600)

"""
Conexión con Arduino Mega

/dev/ttyUSB0 = puerto del Arduino
9600 = velocidad serial
"""

esp32 = serial.Serial('/dev/ttyUSB1', 115200)

"""
Conexión con ESP32

/dev/ttyUSB1 = puerto ESP32
115200 = velocidad serial
"""

time.sleep(2)

"""
Espera 2 segundos para estabilizar
las conexiones seriales
"""


# ================= RFID AUTORIZADO ==================

uid_registrado = "AD698F21"

"""
UID permitido del RFID
Si se detecta este UID:
- abre servo
- muestra bienvenida
"""


# ================= MEMORIA ESTADOS ==================

estado_anterior = {}

"""
Diccionario que guarda estados anteriores
de cada módulo

Ejemplo:
M1 -> OCUPADO
M2 -> LIBRE

Sirve para evitar parpadeos
o falsas detecciones
"""


# ================= CAMARA ==================

cam = cv2.VideoCapture(1)

"""
Abre cámara USB

0 = primera cámara

Si falla:
usar 1 o 2
"""


# ================= LOOP PRINCIPAL ==================

while True:

    # Captura imagen cámara
    ret, frame = cam.read()

    # Si no recibe imagen sale
    if not ret:
        break


    # ================= REDIMENSIONAR ==================

    frame = cv2.resize(frame, (900,600))

    """
    Cambia tamaño de ventana cámara
    """


    # ================= ESCALA GRISES ==================

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    """
    Convierte imagen a escala grises
    para facilitar procesamiento
    """


    # ================= SUAVIZAR RUIDO ==================

    gray = cv2.GaussianBlur(gray,(5,5),0)

    """
    Elimina ruido visual
    """


    # ================= TAMAÑO IMAGEN ==================

    h,w = gray.shape

    """
    h = alto
    w = ancho
    """


    # ================= DIVISION COLUMNAS ==================

    col = w // 3

    """
    Divide imagen en 3 columnas
    """


    # ================= ESPACIOS ==================

    gap = 25

    """
    Separación entre módulos
    """

    an = col - gap

    """
    ancho módulo
    """

    offset = gap // 2

    """
    centrar visualmente
    """


    # ================= ALTURAS ==================

    alto_modulo = 250

    """
    altura módulos superiores
    """

    alto_carril = 100

    """
    espacio central circulación
    """

    y1 = alto_modulo

    """
    límite módulos superiores
    """

    y2 = alto_modulo + alto_carril

    """
    inicio módulos inferiores
    """


    # ================= MODULOS ==================

    zonas = [

        ("M1",0*col+offset,0,an,y1),
        ("M2",1*col+offset,0,an,y1),
        ("M3",2*col+offset,0,an,y1),

        ("M4",0*col+offset,y2,an,h-y2),
        ("M5",1*col+offset,y2,an,h-y2),
        ("M6",2*col+offset,y2,an,h-y2),
    ]

    """
    Cada módulo contiene:

    nombre
    x
    y
    ancho
    alto
    """


    # ================= LISTAS ==================

    ocupados = []
    libres = []

    """
    Guardan módulos ocupados y libres
    """


    # ================= PROCESAMIENTO GLOBAL ==================

    th_global = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        5
    )

    """
    Convierte imagen en binaria
    para detectar objetos
    """


    # ================= KERNEL GLOBAL ==================

    kernel_global = np.ones((5,5), np.uint8)

    """
    Matriz usada para limpieza imagen
    """


    # ================= CERRAR HUECOS ==================

    th_global = cv2.morphologyEx(
        th_global,
        cv2.MORPH_CLOSE,
        kernel_global
    )

    """
    Une zonas blancas cercanas
    """


    # ================= CONTORNOS GLOBALES ==================

    contours_globales,_ = cv2.findContours(
        th_global,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    """
    Detecta formas/objetos
    """


    # ================= ANALISIS MODULOS ==================

    for nombre,x,y,an,al in zonas:

        # Extrae región módulo
        roi = gray[y:y+al, x:x+an]


        # Umbral adaptativo
        th = cv2.adaptiveThreshold(
            roi,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            31,
            5
        )


        # Kernel pequeño
        kernel = np.ones((3,3), np.uint8)


        # Limpieza ruido
        th = cv2.morphologyEx(
            th,
            cv2.MORPH_OPEN,
            kernel
        )


        # Buscar contornos
        contours,_ = cv2.findContours(
            th,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )


        # Variable detección
        objeto = False


        # Revisar contornos
        for cnt in contours:

            area = cv2.contourArea(cnt)

            """
            Calcula tamaño objeto
            """

            if area > 800:
                objeto = True

                """
                Si área grande:
                hay vehículo
                """


        # Crear estado inicial
        if nombre not in estado_anterior:
            estado_anterior[nombre] = "LIBRE"


        # Estado actual
        estado_actual = "OCUPADO" if objeto else "LIBRE"


        # Suavizado estados
        estado_final = estado_actual if estado_actual == estado_anterior[nombre] else estado_anterior[nombre]


        # Guardar estado
        estado_anterior[nombre] = estado_actual


        # ================= MODULO OCUPADO ==================

        if estado_final == "OCUPADO":

            color = (0,0,255)

            """
            Rojo
            """

            ocupados.append(nombre)

        # ================= MODULO LIBRE ==================

        else:

            color = (0,255,0)

            """
            Verde
            """

            libres.append(nombre)


        # Dibujar rectángulo módulo
        cv2.rectangle(frame,(x,y),(x+an,y+al),color,3)


        # Texto módulo
        cv2.putText(
            frame,
            f"{nombre} {estado_final}",
            (x+20,y+40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )


    # ================= MAL PARQUEO ==================

    alerta = False

    """
    Variable alerta mal parqueo
    """


    # Revisar contornos globales
    for cnt in contours_globales:

        area = cv2.contourArea(cnt)

        # Ignorar ruido pequeño
        if area < 4000:
            continue


        # Rectángulo objeto
        rx,ry,rw,rh = cv2.boundingRect(cnt)


        # Lista módulos tocados
        modulos = []


        # Revisar si toca varios módulos
        for nombre,x,y,an,al in zonas:

            if (rx < x+an and
                rx+rw > x and
                ry < y+al and
                ry+rh > y):

                modulos.append(nombre)


        # Si toca 2 módulos
        if len(modulos) >= 2:

            alerta = True


            # Texto alerta
            cv2.putText(
                frame,
                "ALERTA MAL PARQUEO",
                (180,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                3
            )


    # ================= LED ROJO ESP32 ==================

    if alerta:

        esp32.write(b"ROJO_ON\n")

        """
        Enciende LED rojo
        """

    else:

        esp32.write(b"ROJO_OFF\n")

        """
        Apaga LED rojo
        """


    # ================= MODULOS LIBRES ==================

    if len(libres) == 0:

        mensaje = "LLENO"

        """
        No hay módulos libres
        """

        esp32.write(b"VERDE_OFF\n")

        """
        Apaga LED verde
        """

    else:

        mensaje = ",".join(libres)

        """
        Une módulos libres

        Ejemplo:
        M1,M3,M5
        """

        esp32.write(b"VERDE_ON\n")

        """
        Enciende LED verde
        """


    # ================= ENVIAR A ARDUINO ==================

    arduino.write((mensaje + "\n").encode())

    """
    Envía módulos libres al Mega
    """


    # ================= ENVIAR A ESP32 WEB ==================

    esp32.write(("LIBRES:" + mensaje + "\n").encode())

    """
    Actualiza página web ESP32
    """


    # ================= RFID ==================

    if esp32.in_waiting:

        """
        Si ESP32 envió datos
        """

        tarjeta = esp32.readline().decode(errors='ignore').strip()

        """
        Lee UID RFID
        """

        if tarjeta == uid_registrado:

            """
            RFID válido
            """

            arduino.write(b"YESID\n")

            """
            Arduino muestra:
            BIENVENIDO YESID PROFE
            """


    # ================= TEXTO PANTALLA ==================

    cv2.putText(
        frame,
        "LIBRES: " + mensaje,
        (20,580),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    """
    Mostrar módulos libres
    en ventana OpenCV
    """


    # ================= MOSTRAR VENTANA ==================

    cv2.imshow("Parqueadero Inteligente", frame)


    # ================= SALIR ==================

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ================= CERRAR ==================

cam.release()

"""
Libera cámara
"""

cv2.destroyAllWindows()

"""
Cierra ventanas OpenCV
"""