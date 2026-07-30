import cv2 as cv

# Aqui fica ligação com a câmera

class Camera:

    def __init__(self, camera_id):
        self.cap = cv.VideoCapture(camera_id)
        
        self.width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))

    def read(self):
        validation, frame = self.cap.read()
        if validation:
            return frame
        return None  

    def get_fps(self):
        return int(self.fps) if self.fps > 0 else 30

    def get_frame_size(self):
        return (self.width, self.height)

    def release(self):
        self.cap.release()