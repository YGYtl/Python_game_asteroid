import random
from game import physicalobject, resources, meteorite

class Star(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Star, self).__init__(resources.star_image, *args, **kwargs)
        '''让类继承physicalobject类并让他具有PhysicalObject属性'''
        self.rotate_speed = random.random() * 100.0 - 50 #为每个小行星加上些旋转速度

    "update()将旋转应用到第一帧"
    def update(self, dt):
        super(Star, self).update(dt)
        self.rotation += self.rotate_speed * dt

    '''
    handle_collision_with()函数的作用，小星星被击中时， 会产生随机数目的、随机速度的更小的小星星。
    而且一个小星星最多变小1次， 每次变为原来大小的1/2。
    '''
    def handle_collision_with(self, other_object):
        super(Star, self).handle_collision_with(other_object)
        if other_object.__class__ is self.__class__:
            self.dead = False
        elif other_object.__class__ is meteorite.Meteorite:
            self.dead = False

        if self.dead and self.scale > 0.25:
            num_stars = random.randint(4, 5)  # 产生2个或3个小行星
            for i in range(num_stars):
                new_star = Star(x=self.x, y=self.y, batch=self.batch)
                new_star.rotation = random.randint(0, 360)
                new_star.velocity_x = random.random() * 50 + self.velocity_x
                new_star.velocity_y = random.random() * 50 + self.velocity_y
                new_star.scale = self.scale * 0.5  #scale缩放因子
                self.new_objects.append(new_star)