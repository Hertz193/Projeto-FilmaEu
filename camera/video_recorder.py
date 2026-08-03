import cv2 as cv
from datetime import datetime

# Aqui pega as informações do vídeo (capturados no cam_capture.py) e salva o vídeo em um arquivo com data e hora no nome do arquivo, para que seja possível identificar o replay posteriormente. Além disso, é responsável por liberar o vídeo quando o programa é finalizado.

class VideoRecorder:

    def __init__(self, fps, frame_size):
        self.fps = fps
        self.size = frame_size

    def save(self, frames, filename):
        writer = cv.VideoWriter(
            filename,
            cv.VideoWriter_fourcc(*'mp4v'),
            self.fps,
            self.size
        )

        for frame in frames:
            writer.write(frame)

        writer.release()