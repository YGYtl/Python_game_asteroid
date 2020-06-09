import random
from game import physicalobject, resources, meteorite

class Asteroid(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Asteroid, self).__init__(resources.asteroid_image, *args, **kwargs)
        '''让类继承physicalobject类并让他具有PhysicalObject属性'''
        self.rotate_speed = random.random() * 100.0 - 50 #为每个小行星加上些旋转速度

    "update()将旋转应用到第一帧"
    def update(self, dt):
        super(Asteroid, self).update(dt)
        self.rotation += self.rotate_speed * dt

    '''
    handle_collision_with()函数的作用，小行星被击中时， 会产生随机数目的、随机速度的更小的小行星。
    而且一个小行星最多变小1次， 每次变为原来大小的1/2。
    '''
    def handle_collision_with(self, other_object):
        super(Asteroid, self).handle_collision_with(other_object)
        if other_object.__class__ is self.__class__:
            self.dead = False
        elif other_object.__class__ is meteorite.Meteorite:
            self.dead = False
        elif self.__class__ is not other_object.__class__:
            self.dead = True
        "忽略两个小行星间的碰撞,调用它超类的方法来处理"
        if self.dead and self.scale > 0.5:
            num_asteroids = random.randint(4, 5)  # 产生2个或3个小行星
            for i in range(num_asteroids):
                new_asteroid = Asteroid(x=self.x, y=self.y, batch=self.batch)
                new_asteroid.rotation = random.randint(0, 360)
                new_asteroid.velocity_x = random.random() * 50 + self.velocity_x
                new_asteroid.velocity_y = random.random() * 50 + self.velocity_y
                new_asteroid.scale = self.scale * 0.5
                self.new_objects.append(new_asteroid)