from camera.video_recorder import VideoRecorder
from camera.cam_capture import Camera
from camera.replay_buffer import ReplaysBuffer
from camera.uploader import Uploader

# Aqui ocorre a junção de todas as classes (camera, video e replaysbuffer)

class MasterCam:
    def __init__(self, camera_id): 
        self.camera = Camera(camera_id)

        fps = self.camera.get_fps()
        size = self.camera.get_frame_size()

        self.buffer = ReplaysBuffer(fps, 30)
        self.recorder = VideoRecorder(fps, size)
        self.uploader = Uploader("http://192.168.0.7:8000")  # Colocar a URL do servidor aqui (sempre no formato http://IP:PORTA)

    def update(self):
        frame = self.camera.read()

        if frame is not None:
            self.buffer.add(frame)
        return frame

    def save_replay(self, filename):
        frames = self.buffer.get_frames()
        self.recorder.save(frames, filename)

    def send_replay(self, filename):
        self.uploader.upload(filename)