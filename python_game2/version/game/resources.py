import pyglet

def center_image(image):
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2


player_image = pyglet.image.load("../resources/player.png")
center_image(player_image)

bullet_image = pyglet.image.load("../resources/bullet.png")
center_image(bullet_image)

star_image = pyglet.image.load("../resources/star.png")
center_image(star_image)

meteorite_image = pyglet.image.load("../resources/meteorite.png")
center_image(meteorite_image)

engine_image = pyglet.image.load("../resources/engine_flame.png")
engine_image.anchor_x = engine_image.width * 2
engine_image.anchor_y = engine_image.height // 2
# 为了将火焰绘制在飞船尾部，需要修改火焰图片的anchor_x 和anchor_y属性

bullet_sound = pyglet.media.load("../resources/bullet.wav", streaming=False)