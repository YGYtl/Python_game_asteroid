import pyglet
from game import util
'''让物体动起来'''
class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)
        '''让类继承Object类并让他具有sprite属性'''

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.reacts_to_bullets = True  # 这个属性表明是否需要对子弹做出响应(飞船不用响应)
        self.is_bullet = False  # 表示一个物体是否是子弹
        self.dead = False
        self.new_objects = []
        '''
        如果要加入新物体，需要将它添加到new_objects。
        在主循环中它会被添加到game_objects列表，而new_objects会被清空。
        '''
        self.event_handlers = []

    def update(self, dt):
        self.x += self.velocity_x * dt
        '''dt是时间间隔'''
        self.y += self.velocity_y * dt
        self.check_bounds()  #如果物体从屏幕的一侧消失， 就让它从屏幕的另一侧出来

    def check_bounds(self):
        min_x = -self.image.width // 2
        min_y = -self.image.height // 2
        max_x = 800 + self.image.width // 2
        max_y = 600 + self.image.height // 2
        if self.x < min_x:
            self.x = max_x
        if self.y < min_y:
            self.y = max_y
        if self.x > max_x:
            self.x = min_x
        if self.y > max_y:
            self.y = min_y

    def collides_with(self, other_object):
        '''使其在适当的情况下忽略子弹'''
        if not self.reacts_to_bullets and other_object.is_bullet:
            return False
        if self.is_bullet and not other_object.reacts_to_bullets:
            return False
        collision_distance = self.image.width * 0.5 * self.scale + other_object.image.width * 0.5 * other_object.scale

        actual_distance = util.distance(self.position, other_object.position)
        return (actual_distance <= collision_distance)

    def handle_collision_with(self, other_object):
        '''忽略同类间的碰撞，并且忽视小行星与陨石的碰撞'''
        self.dead = True