import pyglet
from game import star, bulk_load, player, meteorite

game_window = pyglet.window.Window(800, 600)

#pyglet的批量绘制
main_batch = pyglet.graphics.Batch()


#设置文字标签，需要将batch对象传递给物体的构造函数(使用关键字 batch)
level_label = pyglet.text.Label(text="It's a star Game ^。^!", x=400, y=575, anchor_x='center', batch=main_batch)
game_over_label = pyglet.text.Label(text="GAME OVER",
                                    x=400, y=-300, anchor_x='center',
                                    batch=main_batch, font_size=48)
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
time_label = pyglet.text.Label(text="Time: ", x=150, y=575, batch=main_batch)


player_airship = None
player_lives = []
score = 0
num_stars = 3
num_meteorites = 1
game_objects = []
time_left = 1200
count = 0
level = 0

# 事件栈的size
event_stack_size = 0


def init():
    global score, num_stars, num_meteorites, time_left, count

    score = 0
    time_left = 1200
    count = 0
    score_label.text = "Score: " + str(score)
    time_label.text = "Time: " + str((time_left-count)//120)

    num_stars = 3
    num_meteorites = 1
    reset_level(2)


def reset_level(num_lives=2):
    global player_airship, player_lives, game_objects, event_stack_size

    # 清空事件栈
    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    for life in player_lives:
        life.delete()

    # 创建Player的实例
    player_airship = player.Player(x=400, y=300, batch=main_batch)
    # 加载小飞船图标
    player_lives = bulk_load.player_lives(num_lives, main_batch)
    # 加载多个星星
    stars = bulk_load.stars(num_stars,player_airship.position, main_batch)
    # 加载多个陨石
    meteorites = bulk_load.meteorites(num_meteorites, player_airship.position, main_batch)
    # 为了调用每一个物体的update函数，需要一个列表来存放这些物体。
    game_objects = [player_airship] + stars + meteorites

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
    global score, num_stars, num_meteorites, count, time_left, level

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

    stars_remaining = 0 # 记录还有多少星星
    meteorites__remaining = 0 # 记录还有多少个陨石

    for obj in game_objects:
        obj.update(dt)
        to_add.extend(obj.new_objects)
        obj.new_objects = []
        if isinstance(obj, star.Star):
            stars_remaining += 1
        if isinstance(obj, meteorite.Meteorite):
            meteorites__remaining += 1


    if stars_remaining == 0 and meteorites__remaining == 0:
        victory = True

    # 删除死亡的对象
    for to_remove in [obj for obj in game_objects if obj.dead]:
        if to_remove == player_airship:
            player_dead = True
        to_add.extend(to_remove.new_objects)

        to_remove.delete()

        game_objects.remove(to_remove)

        if isinstance(to_remove, star.Star):
            score += 1
            score_label.text = "Score: " + str(score)

        if isinstance(to_remove, meteorite.Meteorite):
            score += 5
            score_label.text = "Score: " + str(score)

    if count < time_left:
        count_now = (time_left - count)//120
        time_label.text = "Time: " + str(count_now)

    count += 1

    game_objects.extend(to_add)


    if player_dead or count >= time_left:
        if len(player_lives) > 0 and count <= time_left:
            if count == time_left:
                player_airship.delete()
            count = 0
            reset_level(len(player_lives) - 1)
        else:
            game_over_label.y = 300
    elif victory:
        level += 1
        num_stars += 1
        num_meteorites += 1
        player_airship.delete()
        score += 10
        count = 0
        time_left += level*1440
        reset_level(len(player_lives))



if __name__ == "__main__":
    init()

    # 将刷新频率设定为每秒钟120次，pyglet会传递经过的时间dt 作为唯一的参数给update函数
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    pyglet.app.run()