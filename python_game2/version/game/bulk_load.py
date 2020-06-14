import pyglet, random
from game import star, meteorite, math_compute, resources

'''
player_lives函数显示小飞船图标，窗口的右上角绘制一行小图标
产生小图标的函数与产生小行星的函数基本是一样的
飞船大小是50*50的，小图标的大小是25*25
从窗口的右端起，每隔30个像素绘制一个图标
'''
def player_lives(num_icons, batch=None):
    player_lives = []
    for i in range(num_icons):
        # 创建一个sprite对象，给它一个位置及缩放尺度
        new_sprite = pyglet.sprite.Sprite(img=resources.player_image, x=785-i*30, y=585, batch=batch)
        new_sprite.scale = 0.5
        player_lives.append(new_sprite)
    return player_lives

'''
随机地加载多个小行星在不同的位置上， 而且一开始不能与飞船发生碰撞。
'''
def stars(num_stars, player_position, batch=None):
    stars = []
    for i in range(num_stars):
        star_x, star_y = player_position
        '''
        一开始让小行星的位置等于飞创(player_position)的位置，然后找到距离飞船足够远才退出循环
        pyglet sprites记录它们的位置有两种方法：元组(Sprite.position)和x,y属性， (Sprite.x和Sprite.y)
        '''
        while math_compute.distance((star_x, star_y), player_position) < 100:
            star_x = random.randint(0, 800)
            star_y = random.randint(0, 600)

        new_star = star.Star(x=star_x, y=star_y, batch=batch)
        "小行星运动"
        new_star.rotation = random.randint(0, 360)  #给它一个随机的旋转角度
        new_star.velocity_x, new_star.velocity_y = random.random()*30, random.random()*30
        stars.append(new_star)  #每个小行星都被加入到列表中
    return stars

'''
'''
def meteorites(num_meteorites, player_position, batch=None):
    meteorites = []
    for i in range(num_meteorites):
        meteorite_x, meteorite_y = player_position
        '''
        一开始让陨石的位置等于飞创(player_position)的位置，然后找到距离飞船足够远才退出循环
        pyglet sprites记录它们的位置有两种方法：元组(Sprite.position)和x,y属性， (Sprite.x和Sprite.y)
        '''
        while math_compute.distance((meteorite_x, meteorite_y), player_position) < 100:
            meteorite_x = random.randint(0, 800)
            meteorite_y = random.randint(0, 600)

        new_meteorite = meteorite.Meteorite(x=meteorite_x, y=meteorite_y, batch=batch)
        "陨石运动"
        new_meteorite.rotation = random.randint(0, 360)  #给它一个随机的旋转角度
        new_meteorite.velocity_x, new_meteorite.velocity_y = random.random()*50, random.random()*50
        meteorites.append(new_meteorite)  #每个小行星都被加入到列表中
    return meteorites