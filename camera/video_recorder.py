import cv2 as cv

# Aqui pega as informações do vídeo (capturados no camera.py) e salva o vídeo em um arquivo

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