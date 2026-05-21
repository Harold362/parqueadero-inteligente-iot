import cv2
import numpy as np

cam = cv2.VideoCapture(1)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.resize(frame, (900, 600))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape

    col = w // 3

    alto_modulo = 250
    alto_carril = 100

    y1 = alto_modulo
    y2 = alto_modulo + alto_carril

    # ----- Dibujar módulos -----

    # líneas verticales arriba
    cv2.line(frame, (col, 0), (col, y1), (0,255,0), 2)
    cv2.line(frame, (2*col, 0), (2*col, y1), (0,255,0), 2)

    # líneas verticales abajo
    cv2.line(frame, (col, y2), (col, h), (0,255,0), 2)
    cv2.line(frame, (2*col, y2), (2*col, h), (0,255,0), 2)

    # líneas horizontales
    cv2.line(frame, (0, y1), (w, y1), (255,0,0), 2)
    cv2.line(frame, (0, y2), (w, y2), (255,0,0), 2)

    # Etiquetas superiores
    cv2.putText(frame,"M1",(40,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.putText(frame,"M2",(col+40,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.putText(frame,"M3",(2*col+40,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    # Carril
    cv2.putText(frame,"CARRIL INGRESO",(260,y1+60),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)

    # Etiquetas inferiores
    cv2.putText(frame,"M4",(40,y2+80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.putText(frame,"M5",(col+40,y2+80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.putText(frame,"M6",(2*col+40,y2+80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow("Parqueadero Profesional", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
