import cv2 as cv
from datetime import datetime
from camera.master_cam import MasterCam

# Aqui ocorre a inicialização do sistema

cam = MasterCam(0)  # 0 para webcam, troque pelo IP (no formato: http://ip_da_câmera/video ou rtsp://usuario:senha@ip_da_câmera/porta) que a câmera estiver transmitindo

while True:
    cam.update()
    frame = cam.update()

    if frame is not None:
        cv.imshow("Camera", frame)

    key = cv.waitKey(1)

    if key == ord('s'):
        filetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = f"replay_{filetime}.mp4"

        cam.save_replay(filename)
        cam.send_replay(filename)
    elif key == 27:  # ESC
        break

cam.camera.release()
cv.destroyAllWindows()