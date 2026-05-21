import cv2

cam = cv2.VideoCapture(1)   # cámara USB externa

while True:
    ret, frame = cam.read()

    if not ret:
        print("No se detectó cámara")
        break

    # Redimensionar para trabajo cómodo
    frame = cv2.resize(frame, (900, 600))

    h, w, _ = frame.shape

    # Medidas columnas y filas
    col = w // 3
    row = h // 2

    # Dibujar líneas verticales
    cv2.line(frame, (col, 0), (col, h), (0,255,0), 2)
    cv2.line(frame, (2*col, 0), (2*col, h), (0,255,0), 2)

    # Dibujar línea horizontal
    cv2.line(frame, (0, row), (w, row), (0,255,0), 2)

    # Etiquetas módulos
    labels = [
        ("M1", (50, 50)),
        ("M2", (col+50, 50)),
        ("M3", (2*col+50, 50)),
        ("M4", (50, row+50)),
        ("M5", (col+50, row+50)),
        ("M6", (2*col+50, row+50)),
    ]

    for text, pos in labels:
        cv2.putText(frame, text, pos,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,0,255), 2)

    cv2.imshow("Parqueadero 6 Modulos", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
