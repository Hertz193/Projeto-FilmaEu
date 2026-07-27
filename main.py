import cv2 as cv

# Aqui ocorre a junção de todas as classes (camera, video e replaysbuffer)

from camera.video_recorder import VideoRecorder
from camera.cam_capture import Camera
from camera.replay_buffer import ReplaysBuffer

cam = Camera(0) # 0 para webcam, troque pelo IP que a câmera estiver transmitindo
buffer = ReplaysBuffer(cam.get_fps(), 30)
video = VideoRecorder(cam.get_fps(), cam.get_frame_size())

while True:
    validation, frame = cam.read()

    if not validation:
        break

    buffer.add(frame)
    cv.imshow("Replay", frame)
    key = cv.waitKey(1)

    if key == ord("s"):
        video.save(
            buffer.get_frames(),
            "replay.mp4"
        )

    if key == 27:  # 27 == ESC
        break

cam.release()
cv.destroyAllWindows()