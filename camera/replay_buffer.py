from collections import deque 

# Essa parte é responsável por armazenar apenas os ultimos frames numa lista, chamado de buffer circular, ótimo para otimizar a memória, pois não precisa armazenar todos os frames, apenas os ultimos, que são os mais importantes para o replay.

class ReplaysBuffer:

    def __init__(self, fps, seconds):
        self.frames = deque(maxlen=fps*seconds)

    def add(self, frame):
        self.frames.append(frame.copy())

    def get_frames(self):
        return list(self.frames)

    def clear(self):
        self.frames.clear()