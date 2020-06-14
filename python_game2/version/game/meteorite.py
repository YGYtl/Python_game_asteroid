import random
from game import physicalobject, resources, star

class Meteorite(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Meteorite, self).__init__(resources.meteorite_image, *args, **kwargs)
        '''让类继承physicalobject类并让他具有PhysicalObject属性'''
        self.rotate_speed = random.random() * 100.0 - 50 #为每个陨石加上些旋转速度

    "update()将旋转应用到第一帧"
    def update(self, dt):
        super(Meteorite, self).update(dt)
        self.rotation += self.rotate_speed * dt

    '''
    handle_collision_with()函数的作用，陨石被击中时， 会产生随机数目的、随机速度的更小的陨石。
    而且一个陨石最多变小2次， 即从Large到Middle再到Small，每次变为原来大小的1/2。
    '''
    def handle_collision_with(self, other_object):
        super(Meteorite, self).handle_collision_with(other_object)
        if other_object.__class__ is self.__class__:
            self.dead = False
        elif other_object.__class__ is star.Star:
            self.dead = False

        if self.dead and self.scale > 0.25:
            num_meteorites = random.randint(3, 4)  # 产生2个或3个陨石
            for i in range(num_meteorites):
                new_meteorite = Meteorite(x=self.x, y=self.y, batch=self.batch)
                new_meteorite.rotation = random.randint(0, 360)
                new_meteorite.velocity_x = random.random() * 80 + self.velocity_x
                new_meteorite.velocity_y = random.random() * 80 + self.velocity_y
                new_meteorite.scale = self.scale * 0.5
                self.new_objects.append(new_meteorite)