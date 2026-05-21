import cv2

cam = cv2.VideoCapture(1)

while True:
    ret, frame = cam.read()

    if not ret:
        print("No se detectó cámara")
        break

    cv2.imshow("Camara USB", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
