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
    row = h // 2

    zonas = [
        (0,0,col,row), (col,0,col,row), (2*col,0,col,row),
        (0,row,col,row), (col,row,col,row), (2*col,row,col,row)
    ]

    for i, (x,y,an,al) in enumerate(zonas):
        roi = gray[y:y+al, x:x+an]

        promedio = np.mean(roi)

        if promedio < 120:
            color = (0,0,255)   # ocupado rojo
            estado = "OCUPADO"
        else:
            color = (0,255,0)   # libre verde
            estado = "LIBRE"

        cv2.rectangle(frame, (x,y), (x+an,y+al), color, 3)

        cv2.putText(frame, f"M{i+1} {estado}",
                    (x+20, y+40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, color, 2)

    cv2.imshow("Detector Parqueadero", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
