import pyglet, math
from pyglet.window import key
from game import bullet, physicalobject, resources

class Player(physicalobject.PhysicalObject):
    "引擎火焰的初始化与Player类的初始化一样(因为它们都是Sprite类)"
    def __init__(self, *args, **kwargs):  #将关键字参数设置为实例属性
        super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
        self.engine_sprite = pyglet.sprite.Sprite(img=resources.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False  # 一开始是不显示的，当按键触发才显示

        self.thrust = 100.0
        self.rotate_speed = 150.0
        self.bullet_speed = 850.0

        self.reacts_to_bullets = False  # 实现当 子弹 击中小星星或陨石时，要发生些什么

        self.key_handler = key.KeyStateHandler()  # Player类的构造函数
        self.event_handlers = [self, self.key_handler]
        '''pyglet使用轮询方法(polling approach) 来处理键盘输入
        发送键被按下与释放的消息来注册事件句柄(event handlers) '''

    def update(self, dt):
        super(Player, self).update(dt)
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt
        if self.key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)  # 正方向定义不同，加负号
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x += force_x
            self.velocity_y += force_y
            self.engine_sprite.rotation = self.rotation
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y

            self.engine_sprite.visible = True
            "火焰只在飞船向前推进时显示"
        else:
            self.engine_sprite.visible = False

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.fire()

    def fire(self):
        "发射子弹"
        angle_radians = -math.radians(self.rotation)  #将角度转换成弧度并逆转方向

        "计算子弹的位置并实例化它"
        ship_radius = self.image.width // 2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = bullet.Bullet(bullet_x, bullet_y, batch=self.batch)

        "子弹速度的计算"
        bullet_vx = self.velocity_x + math.cos(angle_radians) * self.bullet_speed
        bullet_vy = self.velocity_y + math.sin(angle_radians) * self.bullet_speed
        new_bullet.velocity_x, new_bullet.velocity_y = bullet_vx, bullet_vy

        "把子弹加到new_objects列表，主循环会把它加到game_objects中"
        self.new_objects.append(new_bullet)

        resources.bullet_sound.play()

    def delete(self):
        self.engine_sprite.delete()
        super(Player, self).delete()
        "删除Player, 类实例时也需要删除引擎火焰"