import pygame.image

import LEVEL_3n4.movable_objects as movable_objects


class Sprite:

    def __init__(self, image, x=0, y=0):
        self.image = image
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.gravity = 4

    def load_image(self):
        return pygame.image.load(self.image)

    def get_frame(self, width, height, scale, frame_nr=0):
        frame = pygame.Surface((width, height))
        frame.blit(self.load_image(), (0, 0), ((frame_nr * width), 0, width, height))
        frame = pygame.transform.scale(frame, (width * scale, height * scale))
        frame.set_colorkey((0, 0, 0))
        self.width = width * scale
        self.height = height * scale

        return frame

    def scale(self, width, height):
        return pygame.image.load(pygame.transform.scale(self.image, (width, height)))


class Obstacles:

    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collision = []
        self.flag = False

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class ActionPlace(Sprite):
    def __init__(self, image, x=0, y=0, width=0, height=0):
        Sprite.__init__(self, image, x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collision = []
        self.flag = False
        self.was_pressed = False

    def update(self):
        if self.collision:
            self.flag = True
        else:
            self.flag = False

        # print(self.flagBox)

class MainMenu(Sprite):
    def __init__(self, image, x=0, y=0, width=0, height=0):
        Sprite.__init__(self, image, x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collision = []
        self.flag = False

    def update(self):
        if self.collision:
            self.flag = True
        else:
            self.flag = False




class ActionPlace_2(Obstacles):
    def __init__(self, width, height, x, y):
        Obstacles.__init__(self, width, height, x, y)

    def update(self):
        if self.collision:
            self.flag = True


class ActionPlacePuzzle(Obstacles):
    def __init__(self, x, y, width, height, name=''):
        Obstacles.__init__(self, width, height, x, y)
        self.fingerprint = name

    def update(self):
        if self.collision:
            self.flag = True
        else:
            self.flag = False

    def get_fingerprint(self):
        return self.fingerprint


class Platform(Sprite):
    def __init__(self, x, y, width, height=20):
        Sprite.__init__(self, 'LEVEL_3n4/assets/sprites/unmovable_obj/platform.png', x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Door(Sprite):
    def __init__(self, x, y, width=30, height=180):
        Sprite.__init__(self, 'LEVEL_3n4/assets/sprites/unmovable_obj/doors_4_1.png', x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Laser(Obstacles):
    def __init__(self, width, height, x, y):
        Obstacles.__init__(self, width, height, x, y)
        # # pygame.mixer.init()
        # pygame.mixer.music.load('LEVEL_3n4/assets/sound/laser_sound.mp3')
        # pygame.mixer.Sound.set_volume(1)
        self.sound_fx = pygame.mixer.Sound('LEVEL_3n4/assets/sound/laser_sound_effect.wav')

    def on_off_odd_master(self, delay):
        if delay == 100:
            if self.width == 0:
                self.width = 5
                # self.sound_fx.play()

            elif self.width == 5:
                self.width = 0
                # self.sound_fx.stop()
            return 0

        else:
            return delay + 1

    def on_off_odd_slave(self, delay):
        if delay == 100:
            if self.width == 0:
                self.width = 5

            elif self.width == 5:
                self.width = 0

    def on_off_even_master(self, delay):
        if delay == 50:
            if self.width == 0:
                self.width = 5

            elif self.width == 5:
                self.width = 0
            return 0
        else:
            return delay + 1

    def on_off_even_slave(self, delay):
        if delay == 50:
            if self.width == 0:
                self.width = 5

            elif self.width == 5:
                self.width = 0

    def on_off_even_slave_indi(self, delay):
        if delay == 30:
            if self.width == 0:
                self.width = 5

            elif self.width == 5:
                self.width = 0

    def on_off_odd_slave_indi(self, delay):
        if delay == 80:
            if self.width == 0:
                self.width = 5

            elif self.width == 5:
                self.width = 0

    def update_laser(self):
        if self.sound_fx:
            self.sound()
        if self.collision:
            for obj in self.collision:
                print(isinstance(obj, movable_objects.Player))
                if isinstance(obj, movable_objects.Player):
                    print("died")
                    return 1  # change to 1
                if isinstance(obj, movable_objects.Box):
                    print('box')

    def sound(self):
        if self.width:
            self.sound_fx.play()
            self.sound_fx.set_volume(0.01)
        else:
            self.sound_fx.stop()


class InfoPlate(Sprite):
    def __init__(self, image, x, y, width, height):
        Sprite.__init__(self, image, x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Mouse(Obstacles):
    def __init__(self, width, height):
        Obstacles.__init__(self, width, height, 0, 0)

    def update_rect(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def stop_rect(self):
        self.rect = pygame.Rect(0, self.y, self.width, self.height)
