import cv2 as cv

# Aqui fica a ligação com a câmera, captando informações como resolução (width e height) e FPS

class Camera:

    def __init__(self, camera_id):
        self.cap = cv.VideoCapture(camera_id)
        
        self.width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv.CAP_PROP_FPS)

    def read(self):
        return self.cap.read()

    def get_fps(self):
        return int(self.fps) if self.fps > 0 else 30

    def get_frame_size(self):
        return (self.width, self.height)

    def release(self):
        self.cap.release()