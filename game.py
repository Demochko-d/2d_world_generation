import pygame
import random
from config_gen import * # все параметры генерации

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
pixel_size = (WIDTH / display_x)
size_draw = pixel_size + 1
hat_width = pixel_size
hat_height = pixel_size * 0.45
stem_width = size_draw * 0.25
stem_height = size_draw * 0.45

# доп константы
land = []
ne_trogat = 38

class Chunck:

    def __init__(
            self, x=0, y=start_y,
            tree=None, ore=None, flower=None, dirt_color=brown, mushroom=None, color_ore=None, dop_obj=None):

        self.x = x
        self.y = y
        self.tree = tree
        self.ore = ore
        self.solor_ore = color_ore
        if biom != 'Тайга': self.solor_tree = (random.randint(17, 29),
                                               random.randint(160, 196), 0)
        else: self.solor_tree = (random.randint(180, 190)
                                     , random.randint(185, 200), random.randint(225, 240))
        self.dual_tree = random.choice((True, False, False, False))
        self.type = biom
        self.flower_color = flower
        self.dirt_color = dirt_color
        self.color_stvol = (random.randint(80, 98), random.randint(30, 62), random.randint(0, 8))
        self.color_mushroom = mushroom
        self.leave_drop = 0
        self.dop_obj = dop_obj

        if self.tree: self.koff = (None, None, None, None, 2, 2.2, 2.5, 2.9, 3.3, 3.7, 4)[self.tree]

        if biom == 'Лес' or biom == 'Поле' or biom == 'Цветочная поляна': self.color_g = (green, dark_green)[x % 2]
        elif biom == 'Пустыня': self.color_g = (pesoc, dark_pesoc)[x % 2]
        elif biom == 'Скалы': self.color_g = grey
        elif biom == 'Тайга': self.color_g = (snow, ice_snow)[x % 2]
        elif biom == 'Пустошь': self.color_g = (dark_grey, super_dark_grey)[x % 2]


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

        elif self.dop_obj is not None:
            self.draw_dop_obj(real_x, real_y)

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

        if self.type == 'Цветочная поляна':
            plus_h = pixel_size * boost_flower
        else:
            plus_h = 0

        pygame.draw.line(screen, self.solor_tree,
                         (real_x + pixel_size / 2, real_y),
                         (real_x + pixel_size / 2, real_y - pixel_size - plus_h), 6)
        pygame.draw.circle(screen, self.flower_color,
                           (real_x + pixel_size / 2, real_y - pixel_size - plus_h), pixel_size / 2.5)
        pygame.draw.circle(screen, yellow,
                           (real_x + pixel_size / 2, real_y - pixel_size - plus_h), pixel_size / 4.8)


    def draw_mushroom(self, real_x, real_y):

        cx = real_x + pixel_size / 2
        cy = real_y

        pygame.draw.rect(screen, mushroom_color_st,
            (cx - stem_width / 2, cy - stem_height, stem_width, stem_height + 1))

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


    def draw_dop_obj(self, real_x, real_y):

        if self.type == 'Поле' or self.type == 'Лес' or self.type == 'Цветочная поляна':

            pygame.draw.line(screen, self.solor_tree,
                             (real_x + pixel_size / 2, real_y),
                             (real_x + pixel_size / 2, real_y - pixel_size / 1.5), 6)
            pygame.draw.line(screen, self.solor_tree,
                             (real_x + pixel_size / 2, real_y),
                             (real_x + pixel_size / 1.25, real_y - pixel_size / 1.5), 6)
            pygame.draw.line(screen, self.solor_tree,
                             (real_x + pixel_size / 2, real_y),
                             (real_x + pixel_size * 0.2, real_y - pixel_size / 1.5), 6)

        elif self.type == 'Пустыня':

            pygame.draw.line(screen, self.dirt_color,
                (real_x + pixel_size / 2, real_y),
                (real_x + pixel_size / 2, real_y - pixel_size / 1.3), 8)
            pygame.draw.line(screen, self.dirt_color,
                (real_x + pixel_size / 2, real_y - pixel_size / 3),
                (real_x + pixel_size * 0.25, real_y - pixel_size / 1.2), 6)
            pygame.draw.line(screen, self.dirt_color,
                (real_x + pixel_size / 2, real_y - pixel_size / 3),
                (real_x + pixel_size * 0.75, real_y - pixel_size / 1.2), 6)

        elif self.type == 'Скалы':

            p1 = (real_x + pixel_size * 0.25, real_y)
            p2 = (real_x + pixel_size * 0.75, real_y)
            p3 = (real_x + pixel_size * 0.50, real_y - pixel_size * 0.6)
            pygame.draw.polygon(screen, self.dirt_color, (p1, p2, p3))

        elif self.type == 'Тайга':

            pygame.draw.circle(
                screen, self.solor_tree,
                (real_x + pixel_size / 2, real_y - pixel_size * 0.3),
                pixel_size * 0.35)
            pygame.draw.circle(
                screen, self.solor_tree,
                (real_x + pixel_size / 2, real_y - pixel_size * 0.77),
                pixel_size * 0.25)

        elif self.type == 'Пустошь':

            pygame.draw.line(screen, black,
                (real_x + pixel_size * 0.35, real_y),
                (real_x + pixel_size * 0.30, real_y - pixel_size * 0.5), 5)
            pygame.draw.line(screen, black,
                (real_x + pixel_size * 0.50, real_y),
                (real_x + pixel_size * 0.50, real_y - pixel_size * 0.6), 7)
            pygame.draw.line(screen, black,
                (real_x + pixel_size * 0.65, real_y),
                (real_x + pixel_size * 0.70, real_y - pixel_size * 0.5), 5)


def params_to_part(x, y_old):

    global biom, nerownost, tree_shans, flower_shans, obriv, mushroom_shans, dop_obj_shans

    tree = None
    ore = None
    flower = None
    mushroom = None
    color_ore = None
    dop_obj = None

    if random.random() < new_biome_shans:
        biom = random.choice(list_biome)
        nerownost = biom_config[biom][0]
        tree_shans = biom_config[biom][1]
        flower_shans = biom_config[biom][3]
        mushroom_shans = biom_config[biom][5]
        obriv = biom_config[biom][6]
        dop_obj_shans = biom_config[biom][7]

    if random.random() < nerownost:
        if random.random() < obriv:
            y = max(y_old + (random.randint(params_obriv[0], params_obriv[1]) * random.choice((-1, 1))), min_y)
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

    elif random.random() < dop_obj_shans:
        dop_obj = True

    if land[-1].ore is None:
        if random.random() < ore_shans:
            ore = random.randint(9, -min_y + 4)
            color_ore = random.choice(color_ore_list)
    else:
        if random.random() < ore_shans * ore_stak:
            ore = random.randint(max(9, land[-1].ore - 1), min(-min_y + 4, land[-1].ore + 1))
            color_ore = land[-1].solor_ore

    dirt_color = biom_config[biom][4]

    return x, y, tree, ore, flower, dirt_color, mushroom, color_ore, dop_obj


def new_part():

    x = len(land)
    y_old = land[-1].y
    x, y, tree, ore, flower, dirt_color, mushroom, color_ore, dop_obj = params_to_part(x, y_old)
    land.append(Chunck(x, y, tree, ore, flower, dirt_color, mushroom, color_ore, dop_obj))


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


def info_text():

    text_info_list = (f"Биом: {land[int(camera_x)].type}",
                      f"Погода: {('Ясно', 'Осадки')[rain]}",
                      f"Блоков прогружено: {len(land)}",
                      f"x:{int(camera_x)}   y:{int(camera_y+40)}")

    for text in range(len(text_info_list)):
        screen.blit(font_plus.render(text_info_list[text], True, black), (200, 15 + text * 25))
        screen.blit(font.render(text_info_list[text], True, text_color), (202, 17 + text * 25))


def weather():

    global rain, rain_drops, intensity

    if random.random() < rain_shans:
        rain = not rain
        intensity = random.choice(rain_intensity)
    if rain:
        if random.random() < lighting_shans:
            draw_lighting()
        for _ in range(intensity):
            rain_drops.append([random.randint(0, WIDTH), random.randint(-100, -30)])

    draw_rain()


def draw_lighting():

    pygame.draw.polygon(screen, text_color, [(0, 0),
                                             (WIDTH * 0.4, 0), (WIDTH * 0.35, HEIGHT * 0.25),(0, HEIGHT * 0.2)])
    pygame.draw.polygon(
        screen, text_color,
        [(WIDTH * 0.2, HEIGHT * 0.35),(WIDTH * 0.6, HEIGHT * 0.3),
         (WIDTH * 0.55, HEIGHT * 0.45),(WIDTH * 0.15, HEIGHT * 0.5)])


def draw_rain():

    if land[int(camera_x)].type == 'Тайга':
        rain_speed_t = snow_speed
    elif land[int(camera_x)].type == 'Пустыня':
        rain_drops.clear()
        return
    else:
        rain_speed_t = rain_speed

    for i in rain_drops:
        pygame.draw.line(screen, text_color, (i[0], i[1]), (i[0], i[1] + rain_speed_t))
        i[1] += rain_speed_t
    rain_drops[:] = [d for d in rain_drops if d[1] < HEIGHT + 50]


def draw_world():

    draw_sky()

    weather()

    update_land()

    for i in land[start_d:end_d]:
        i.draw()


def start():
    land.append(Chunck())
    for _ in range(x_generete):
        new_part()
    print('симуляция запущена.')


start()

while run:

    draw_world()

    dt = clock.tick(FPS) / 1000
    events = pygame.event.get()

    camere_move()

    all_button()

    info_text()

    pygame.display.update()

pygame.quit()
print('симуляция остановлена.')
