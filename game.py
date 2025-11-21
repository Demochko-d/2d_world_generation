import pygame
import random

# начальная позиция и состояние
start_y = 7
min_y = -40
seam_mode = (1, 0)
button_green = True
button_green_2 = True
button_green_3 = True
to_nigth = True
rain = False
biom = 'Поле'
time_counter = 0

# иниализация и настройки экрана
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Game")
font = pygame.font.SysFont("arial", 24)
font_plus = pygame.font.SysFont("arial", 24)
clock = pygame.time.Clock()
FPS = 120
run = True

# настройки камеры
land = []
camera_x = 15
camera_y = 0
end_d, start_d = 0, 0
camera_speed_x_std = 20
camera_speed_y_std = 12
camera_speed_x = camera_speed_x_std
camera_speed_y = camera_speed_y_std
speed_2 = 2
speed_3 = 5

ne_trogat = 38

# настройки размера
p_d_x = 15
display_x = p_d_x * 2
display_y = 18
x_generete = display_x + camera_x
pixel_size = (WIDTH / display_x)
size_draw = pixel_size + 1

# цвета
green = (20, 180, 0)
dark_green = (20, 130, 0)
brown = (90, 40, 0)
grey = (85, 75, 70)
dark_grey = (60, 60, 70)
super_dark_grey = (30, 30, 40)
gold = (220, 220, 0)
diamond = (0, 190, 240)
emirald = (0, 190, 120)
rubi = (190, 10, 10)
coald = (20, 10, 0)
iron = (105, 105, 105)
color_ore_list = (gold, diamond, emirald, rubi, coald, iron)
text_color = (255, 255, 255)
red = (200, 0, 0)
black = (0, 0, 0)
pesoc = (250, 220, 110)
dark_pesoc = (200, 180, 80)
snow = (210, 200, 210)
ice_snow = (190, 180, 240)
pink  = (255, 140, 130)
yellow = (255, 255, 0)
brown_gray = (75, 60, 50)
color_flower = (red, pesoc, pink)
sky_color = [140, 140, 235]
mushroom_color_st = (150, 90, 30)
mushroom_color_p = (120, 40, 0)
mushroom_color_m = (230, 50, 30)

# настройки генерации
day_time = 30  # скорость смены дня и ночи (больше - дольше)
nerownost = 0.25
obriv = 0.01
tree_shans = 0.05
ore_shans = 0.35
ore_stak = 1.6 # чем больше тем кучнее руда
flower_shans = 0.06
mushroom_shans = 0.012
new_biome_shans = 0.011
rain_shans = 0.0004
drop_leave_shans = 0.0017
rain_drops = []  # список капель дождя
rain_intensity = (2, 6, 7, 8, 9, 20)  # сколько капель генерируемое за фпс
intensity = 8
rain_speed = 13  # скорость падения и размер капель
biom_config = {
    'Поле': (0.25, 0.045, 1, 0.06, brown, 0.011, 0.01),
    'Пустыня': (0.1, 0.012, 1, 0.017, brown, 0.002, 0.022),
    'Скалы': (0.85, 0.006, 3, 0.005, brown_gray, 0.003, 0.09),
    'Тайга': (0.35, 0.019, 1, 0.007, brown, 0.005, 0.008),
    'Лес': (0.3, 0.175, 1, 0.053, brown, 0.105, 0.015),
} # не все параметры указываються в процентах из-за особеностей генерации
# параметры генерации каждого бюиома, сначала неровность, потом кол - во деревьев,
# потом максимальное отличие высоты между соседними блоками, потом количество цветов, потом цвет "земли",
# потом шанс на гриб, потом количество обрывов
''''
{Пример':
 ('неровности', 'шанс на дереве', 'максимальный перепад высот', 'шанс на цветок', 'цвет земли', 'шанс на гриб'
 'шанс на обрыв')}
'''
list_biome = tuple(biom_config.keys())


class Part:

    def __init__(
            self, x=0, y=start_y, tree=None, ore=None, flower=None, dirt_color=brown, mushroom=None, color_ore=None):

        self.x = x
        self.y = y
        self.tree = tree
        self.ore = ore
        self.solor_ore = color_ore
        self.solor_tree = (random.randint(17, 29), random.randint(160, 196), 0)
        self.dual_tree = random.choice((True, False, False, False))
        self.type = biom
        self.flower_color = flower
        self.dirt_color = dirt_color
        self.color_stvol = (random.randint(80, 105), random.randint(30, 62), random.randint(0, 8))
        self.color_mushroom = mushroom
        self.leave_drop = 0

        if self.tree: self.koff = (None, None, None, None, 2, 2.2, 2.5, 2.9, 3.3, 3.7, 4)[self.tree]

        if biom == 'Лес' or biom == 'Поле': self.color_g = (green, dark_green)[x % 2]
        elif biom == 'Пустыня': self.color_g = (pesoc, dark_pesoc)[x % 2]
        elif biom == 'Скалы': self.color_g = grey
        elif biom == 'Тайга': self.color_g = (snow, ice_snow)[x % 2]


    def draw(self):

        real_x = (self.x - camera_x)  * pixel_size
        real_y = (display_y - self.y + camera_y) * pixel_size

        for y_lvl in range(self.y - int(camera_y) - seam_mode[0]):

            if y_lvl < 4:
                color_s = (self.color_g, self.dirt_color, grey, grey)[y_lvl]
            elif y_lvl < 10:
                color_s = dark_grey
            elif y_lvl < ne_trogat + self.y:
                color_s = super_dark_grey
            else:
                color_s = black

            pygame.draw.rect(screen, color_s,
                             (real_x, real_y + (pixel_size * y_lvl), size_draw, size_draw))

            if y_lvl == self.ore:
                self.draw_ore(real_x, real_y, y_lvl)


        if self.tree is not None:
            self.draw_tree(real_x, real_y)

        elif self.flower_color is not None:
            self.draw_flower(real_x, real_y)

        elif self.color_mushroom is not None:
            self.draw_mushroom(real_x, real_y)


    def draw_tree(self, real_x, real_y):

        if self.leave_drop == 0 and random.random() < drop_leave_shans:
            self.leave_drop = 240


        for stvol in range(1, self.tree):
            pygame.draw.rect(screen, self.color_stvol, (real_x, real_y - (pixel_size * stvol), size_draw, size_draw))

        pygame.draw.circle(screen, self.solor_tree,
                           (real_x + pixel_size / 2, real_y - (pixel_size * self.tree)),
                           size_draw * self.koff)
        if self.dual_tree:
            pygame.draw.circle(screen, self.solor_tree,
                               (real_x + pixel_size / 2, real_y - (pixel_size * self.tree) - 2 * pixel_size),
                               size_draw * (self.koff - 0.4))

        if self.leave_drop > 0:
            self.leave_drop -= 1
            pygame.draw.circle(screen, self.solor_tree,
                               (real_x - (pixel_size * (1, -2)[self.x % 2]),
                                real_y - pixel_size * (self.tree * self.leave_drop - 15) / 200), size_draw / 7)


    def draw_flower(self, real_x, real_y):

        pygame.draw.line(screen, self.solor_tree,
                         (real_x + pixel_size / 2, real_y),
                         (real_x + pixel_size / 2, real_y - pixel_size), 6)
        pygame.draw.circle(screen, self.flower_color,
                           (real_x + pixel_size / 2, real_y - pixel_size), pixel_size / 2.5)
        pygame.draw.circle(screen, yellow,
                           (real_x + pixel_size / 2, real_y - pixel_size), pixel_size / 4.8)


    def draw_mushroom(self, real_x, real_y):

        hat_width = pixel_size
        hat_height = pixel_size * 0.45
        stem_width = pixel_size * 0.25
        stem_height = pixel_size * 0.45
        cx = real_x + pixel_size / 2
        cy = real_y

        pygame.draw.rect(screen, mushroom_color_st,
            (cx - stem_width / 2, cy - stem_height, stem_width, stem_height))

        pygame.draw.ellipse(screen, self.color_mushroom,
            (cx - hat_width / 2, cy - stem_height - hat_height + 4, hat_width, hat_height))

        pygame.draw.circle(screen, self.color_mushroom,
                           (real_x + stem_width / 2, real_y - stem_height * 1.15), pixel_size / 5)

        pygame.draw.circle(screen, self.color_mushroom,
                           (real_x + pixel_size - stem_width / 2, real_y - stem_height * 1.15), pixel_size / 5)


    def draw_ore(self, real_x, real_y, y_lvl):

        bx = real_x
        by = real_y + (pixel_size * y_lvl)
        r = max(2, int(pixel_size * 0.27))
        pattern = [
            (0.20, 0.25),
            (0.60, 0.30),
            (0.35, 0.55),
            (0.70, 0.60),
        ]

        for px, py in pattern:
            x = bx + int(px * pixel_size)
            y = by + int(py * pixel_size)
            pygame.draw.rect(screen, self.solor_ore, (x, y, r, r))


def params_to_part(x, y_old):

    global biom, nerownost, tree_shans, flower_shans, obriv, mushroom_shans

    tree = None
    ore = None
    flower = None
    mushroom = None
    color_ore = None

    if random.random() < new_biome_shans:
        biom = random.choice(list_biome)
        nerownost = biom_config[biom][0]
        tree_shans = biom_config[biom][1]
        flower_shans = biom_config[biom][3]
        mushroom_shans = biom_config[biom][5]
        obriv = biom_config[biom][6]

    if random.random() < nerownost:
        if random.random() < obriv:
            y = y_old + (random.randint(4, 7) * random.choice((-1, 1)))
        else:
            y = random.randint(max(y_old - biom_config[biom][2], min_y + 5),
                               max(y_old + biom_config[biom][2], min_y + 6))
    else:
        y = y_old

    if random.random() < tree_shans:
        if biom != 'Лес':
            tree = random.randint(4, 7)
        else:
            tree = random.randint(6, 10)

    elif random.random() < flower_shans:
        flower = random.choice(color_flower)

    elif random.random() < mushroom_shans:
        mushroom = random.choice((mushroom_color_p, mushroom_color_m))

    if land[-1].ore is None:
        if random.random() < ore_shans:
            ore = random.randint(9, -min_y + 4)
            color_ore = random.choice(color_ore_list)
    else:
        if random.random() < ore_shans * ore_stak:
            ore = random.randint(max(9, land[-1].ore - 1), min(-min_y + 4, land[-1].ore + 1))
            color_ore = land[-1].solor_ore

    dirt_color = biom_config[biom][4]

    return x, y, tree, ore, flower, dirt_color, mushroom, color_ore


def new_part():

    x = len(land)
    y_old = land[-1].y
    x, y, tree, ore, flower, dirt_color, mushroom, color_ore = params_to_part(x, y_old)
    land.append(Part(x, y, tree, ore, flower, dirt_color, mushroom, color_ore))


def camere_move():

    global camera_x, camera_y

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        camera_x += camera_speed_x * dt
    elif keys[pygame.K_LEFT]:
        camera_x -= camera_speed_x * dt
    if keys[pygame.K_UP]:
        camera_y += camera_speed_y * dt
    elif keys[pygame.K_DOWN]:
        camera_y -= camera_speed_y * dt
    camera_x, camera_y = max(camera_x, 0), max(camera_y, min_y)


def seam_button(ev):

    global seam_mode, button_green

    rect = pygame.Rect(10, 10, 170, 45)
    color = red if button_green else green
    pygame.draw.rect(screen, color, rect)

    tx = font.render("режим без швов", True, text_color)
    screen.blit(tx, (20, 15))

    for event in ev:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):

                button_green = not button_green
                seam_mode = (0, 1) if not button_green else (1, -1)


def esc_button(ev):
    global run

    rect = pygame.Rect(WIDTH - 40, 10, 30, 30)
    pygame.draw.rect(screen, red, rect)

    tx = font.render("X", True, text_color)
    screen.blit(tx, (WIDTH - 32 , 10))

    for event in ev:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):

                run = False


def speed_button(ev):
    global camera_speed_x, camera_speed_y, button_green_2, button_green_3

    rect = pygame.Rect(10, 60, 170, 45)
    color = red if button_green_2 else green
    pygame.draw.rect(screen, color, rect)

    tx = font.render("ускорение x2", True, text_color)
    screen.blit(tx, (35 , 65))

    for event in ev:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):

                button_green_2 = not button_green_2
                button_green_3 = True
                if not button_green_2:
                    camera_speed_x = speed_2 * camera_speed_x_std
                    camera_speed_y = speed_2 * camera_speed_y_std
                else:
                    camera_speed_x = camera_speed_x_std
                    camera_speed_y = camera_speed_y_std


def speed_button_s(ev):
    global camera_speed_x, camera_speed_y, button_green_2, button_green_3

    rect = pygame.Rect(10, 110, 170, 45)
    color = red if button_green_3 else green
    pygame.draw.rect(screen, color, rect)

    tx = font.render("ускорение x5", True, text_color)
    screen.blit(tx, (35 , 115))

    for event in ev:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):

                button_green_3 = not button_green_3
                button_green_2 = True
                if not button_green_3:
                    camera_speed_x = speed_3 * camera_speed_x_std
                    camera_speed_y = speed_3 * camera_speed_y_std
                else:
                    camera_speed_x = camera_speed_x_std
                    camera_speed_y = camera_speed_y_std


def update_land():

    global land, camera_x, camera_y, end_d, start_d

    start_d = int(camera_x) + seam_mode[0]
    end_d = int(camera_x + display_x) + seam_mode[1]
    for _ in range(end_d - len(land)):
        new_part()


def draw_sky():

    global sky_color, time_counter, to_nigth

    time_counter += 1
    if time_counter == day_time:
        if to_nigth:
            sky_color = list(map(lambda x: x - 1, sky_color))
            time_counter = 0
            if sky_color[0] == -70:
                to_nigth = False
        else:
            sky_color = list(map(lambda x: x + 1, sky_color))
            time_counter = 0
            if sky_color[0] == 140:
                to_nigth = True

    sky_color_b = list(map(lambda x: max(0, x), sky_color))
    screen.fill(sky_color_b)


def all_button():

    seam_button(events)
    esc_button(events)
    speed_button(events)
    speed_button_s(events)

    screen.blit(font_plus.render(f"Блоков прогружено: {len(land)}", True, black), (200, 15))
    screen.blit(font_plus.render(f"Биом: {land[int(camera_x)].type}", True, black), (200, 40))
    screen.blit(font.render(f"Блоков прогружено: {len(land)}", True, text_color), (202, 17))
    screen.blit(font.render(f"Биом: {land[int(camera_x)].type}", True, text_color), (202, 42))


def weather():

    global rain, rain_drops, intensity

    if random.random() < rain_shans:
        rain = not rain
        intensity = random.choice(rain_intensity)
    if rain:
        for _ in range(intensity):
            rain_drops.append([random.randint(0, WIDTH), random.randint(-100, -30)])

    draw_rain()


def draw_rain():

    for i in rain_drops:
        pygame.draw.line(screen, text_color, (i[0], i[1]), (i[0], i[1] + rain_speed))
        i[1] += rain_speed
    rain_drops[:] = [d for d in rain_drops if d[1] < HEIGHT + 50]


def draw_world():

    draw_sky()

    weather()

    update_land()

    for i in land[start_d:end_d]:
        i.draw()

land.append(Part())
for _ in range(x_generete):
    new_part()
print('симуляция запущена.')

while run:

    draw_world()

    dt = clock.tick(FPS) / 1000
    events = pygame.event.get()

    camere_move()

    all_button()

    pygame.display.update()

pygame.quit()
print('симуляция остановлена.')