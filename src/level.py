from utils import load_json
from obstacles import ObstacleManager
import random

class Level:
    def __init__(self, filename):
        self.data = load_json(filename)
        self.ob_manager = ObstacleManager()
        self.spawn_index = 0
        self.camera_x = 0
        self.setup_from_data()
        self.last_infinite_spawn_x = 0  # For infinite mode

    def setup_from_data(self):
        self.spawn_list = self.data.get('spawns', [])
        self.bg_color = tuple(self.data.get('bg_color', [30, 30, 35]))
        self.music = self.data.get('music')

    def update(self, speed):
        self.camera_x += speed
        WIDTH = 800  # Or import from settings

        # Spawn obstacles from the level file
        while self.spawn_index < len(self.spawn_list) and self.spawn_list[self.spawn_index]['x'] <= self.camera_x + WIDTH:
            spawn = self.spawn_list[self.spawn_index]
            self.ob_manager.spawn(spawn['x'] - self.camera_x, spawn['w'], spawn['h'], spawn.get('kind', 'block'))
            self.spawn_index += 1

        # Infinite generation after level file is exhausted
        if self.spawn_index >= len(self.spawn_list):
            # Spawn a new obstacle every 400-600 pixels
            if self.camera_x + WIDTH > self.last_infinite_spawn_x + random.randint(400, 600):
                x = self.camera_x + WIDTH
                w = random.choice([40, 50, 60])
                h = random.choice([40, 50, 60])
                kind = random.choice(['block', 'spike'])
                self.ob_manager.spawn(x - self.camera_x, w, h, kind)
                self.last_infinite_spawn_x = x

        self.ob_manager.update(speed)

    def draw(self, surf):
        self.ob_manager.draw(surf)

    def reset_runtime(self, start_x):
        self.spawn_index = 0
        self.ob_manager.clear()
        self.camera_x = 0
        self.spawn_list = self.data.get('spawns', [])
        self.last_infinite_spawn_x = 0

    def prepare(self, start_x=1200):
        self.reset_runtime(start_x)