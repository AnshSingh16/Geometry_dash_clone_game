# obstacles.py
from pygame import Rect, draw
from settings import GROUND_Y

class Obstacle:
    def __init__(self, x, w, h, kind='block', y=None):
        # Clamp size to reasonable values
        w = max(20, min(80, w))
        h = max(20, min(80, h))
        self.x = x
        self.w = w
        self.h = h
        self.kind = kind
        self.y = (GROUND_Y - h) if y is None else y
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.color = (0, 0, 0)  # Black fill

    def update(self, speed):
        self.x -= speed
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        if self.kind == 'spike':
            for i in range(0, self.w, 12):
                points = [
                    (self.x + i, self.y + self.h),
                    (self.x + i + 6, self.y),
                    (self.x + i + 12, self.y + self.h)
                ]
                draw.polygon(surf, (0, 0, 0), points)         # Black fill
                draw.polygon(surf, (255, 255, 255), points, 2)  # White border
        else:
            draw.rect(surf, (0, 0, 0), self.rect)              # Black fill
            draw.rect(surf, (255, 255, 255), self.rect, 2)     # White border

class ObstacleManager:
    def __init__(self):
        self.items = []

    def spawn(self, x, w, h, kind='block'):
        ob = Obstacle(x, w, h, kind)
        self.items.append(ob)

    def update(self, speed):
        for ob in self.items:
            ob.update(speed)
        self.items = [o for o in self.items if o.x + o.w > -200]

    def draw(self, surf):
        for ob in self.items:
            ob.draw(surf)

    def clear(self):
        self.items.clear()