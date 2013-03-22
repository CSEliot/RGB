# class Ring(pygame.sprite.Sprite):
#
#    def __init__(self):
#        pygame.sprite.Sprite.__init__(self)
#        self.image, self.rect = load_image('ring.png', -1)
#        self.MAX_COLLIDE_SIZE = 290
#        self.MIN_COLLIDE_SIZE = 280
#        self.angle = 0.0
#        self.rotate_by = 0.0
#        self.rotation_speed = 2
#
#    def set_direction(self, direction):  # 1 for left, -1 for right
#        if direction == -1:
#            self.rotate_by += self.rotation_speed
#
#
#
#    def spin(self):  # Will change ring angle, based on direction
#        # --Spin the Ring//--
#        if self.direction == -1:
#            self.angle += -self.rotate_by * 2
#        else:
#            self.angle += self.rotate_by * 2
#        ring_rectNew = ring_imgNew.get_rect(center=(CENTER_X, CENTER_Y))