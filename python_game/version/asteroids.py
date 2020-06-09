import pyglet
from game import asteroid, load, player, meteorite

game_window = pyglet.window.Window(800, 600)

#pyglet的批量绘制
main_batch = pyglet.graphics.Batch()


#设置文字标签，需要将batch对象传递给物体的构造函数(使用关键字 batch)
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="It's a Game ^。^!", x=400, y=575, anchor_x='center', batch=main_batch)


game_over_label = pyglet.text.Label(text="GAME OVER",
                                    x=400, y=-300, anchor_x='center',
                                    batch=main_batch, font_size=48)


player_ship = None
player_lives = []
score = 0
num_asteroids = 3
num_meteorites = 1
game_objects = []

# 事件栈的size
event_stack_size = 0


def init():
    global score, num_asteroids, num_meteorites

    score = 0
    score_label.text = "Score: " + str(score)

    num_asteroids = 3
    num_meteorites = 1
    reset_level(2)


def reset_level(num_lives=2):
    global player_ship, player_lives, game_objects, event_stack_size

    # 清空事件栈
    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    for life in player_lives:
        life.delete()

    # 创建Player的实例
    player_ship = player.Player(x=400, y=300, batch=main_batch)

    # 加载小飞船图标
    player_lives = load.player_lives(num_lives, main_batch)

    # 加载多个小行星
    asteroids = load.asteroids(num_asteroids, player_ship.position, main_batch)

    # 加载多个陨石
    meteorites = load.meteorites(num_meteorites, player_ship.position, main_batch)

    # 为了调用每一个物体的update函数，需要一个列表来存放这些物体。
    game_objects = [player_ship] + asteroids + meteorites

    '''
    告诉pyglet 哪些实例是事件句柄(event handler)
    用game_window.push_handlers()函数把它压入事件栈中
    '''
    for obj in game_objects:
        for handler in obj.event_handlers:
            game_window.push_handlers(handler)
            event_stack_size += 1


#窗口绘制，在相同名字的函数上使用装饰器
@game_window.event
def on_draw():
    # 绘制前先清屏
    game_window.clear()

    # 绘制
    main_batch.draw()


def update(dt):
    global score, num_asteroids, num_meteorites

    player_dead = False
    victory = False

    '''
    检查所有的物体对，物体两两之间要进行检查，两个for就搞定了
    '''
    for i in range(len(game_objects)):
        for j in range(i + 1, len(game_objects)):

            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):  #若发生 碰撞
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)


    to_add = []

    asteroids_remaining = 0 # 记录还有多少小行星
    meteorites__remaining = 0 # 记录还有多少个陨石

    for obj in game_objects:
        obj.update(dt)
        to_add.extend(obj.new_objects)
        obj.new_objects = []
        if isinstance(obj, asteroid.Asteroid):
            asteroids_remaining += 1
        if isinstance(obj, meteorite.Meteorite):
            meteorites__remaining += 1


    if asteroids_remaining == 0 and meteorites__remaining == 0:
        victory = True

    # 删除死亡的对象
    for to_remove in [obj for obj in game_objects if obj.dead]:
        if to_remove == player_ship:
            player_dead = True
        to_add.extend(to_remove.new_objects)

        to_remove.delete()

        game_objects.remove(to_remove)

        if isinstance(to_remove, asteroid.Asteroid):
            score += 1
            score_label.text = "Score: " + str(score)

        if isinstance(to_remove, meteorite.Meteorite):
            score += 5
            score_label.text = "Score: " + str(score)

    game_objects.extend(to_add)


    if player_dead:
        if len(player_lives) > 0:
            reset_level(len(player_lives) - 1)
        else:
            game_over_label.y = 300
    elif victory:
        num_asteroids += 1
        num_meteorites += 1
        player_ship.delete()
        score += 10
        reset_level(len(player_lives))


if __name__ == "__main__":
    init()

    # 将刷新频率设定为每秒钟120次，pyglet会传递经过的时间dt 作为唯一的参数给update函数
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    pyglet.app.run()