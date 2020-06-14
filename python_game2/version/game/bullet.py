import pyglet
from game import physicalobject, resources
'''
考虑两点
1.子弹只与部分物体发生碰撞(只与小行星)
2.子弹会在一定的时间内消息，否则的话如果它不碰上小行星将会导致满屏都是子弹。
'''

class Bullet(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(resources.bullet_image, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, 0.5)  #告诉pyglet在子弹创建后大约0.5秒调用上面的函数

        self.is_bullet = True

    def die(self, dt):
        self.dead = True
    "一个在子弹消亡时调用的函数"