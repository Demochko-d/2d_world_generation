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

# настройки камеры
camera_x = 15
camera_y = 0
end_d, start_d = 0, 0
camera_speed_x_std = 22
camera_speed_y_std = 13
camera_speed_x = camera_speed_x_std
camera_speed_y = camera_speed_y_std
speed_2 = 2
speed_3 = 5

# настройки размера
p_d_x = 15
display_x = p_d_x * 2
display_y = 18
x_generete = display_x + camera_x

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
fial = (200, 0, 200)
color_flower = (red, pesoc, pink, text_color, diamond, fial)
sky_color = [140, 140, 235]
mushroom_color_st = (150, 90, 30)
mushroom_color_p = (120, 40, 0)
mushroom_color_m = (230, 50, 30)

# настройки генерации
day_time = 30  # скорость смены дня и ночи (больше - дольше)
nerownost = 0.25
obriv = 0.006
params_obriv = (4, 6)  # мин и макс вытоса обрыва
tree_shans = 0.045
ore_shans = 0.35
ore_stak = 1.6 # чем больше тем кучнее руда
flower_shans = 0.06
mushroom_shans = 0.011
new_biome_shans = 0.007
rain_shans = 0.0004
drop_leave_shans = 0.001
dop_obj_shans = 0.08
boost_flower = 0.8 # на сколько цветы на поленя выше чем везде
rain_drops = []  # список капель дождя
rain_intensity = (2, 6, 7, 8, 9, 20)  # сколько капель генерируемое за фпс
intensity = 8
rain_speed = 27  # скорость падения и размер капель
snow_speed = 2
lighting_shans = 0.0008
biom_config = {
    'Поле': (0.25, 0.045, 1, 0.06, brown, 0.007, 0.004, 0.08),
    'Пустыня': (0.1, 0.009, 1, 0.01, brown, 0.001, 0.013, 0.02),
    'Скалы': (0.85, 0.006, 3, 0.005, brown_gray, 0.003, 0.09, 0.13),
    'Тайга': (0.35, 0.012, 1, 0.0008, brown, 0.0025, 0.007, 0.003),
    'Лес': (0.3, 0.175, 1, 0.053, brown, 0.105, 0.006, 0.07),
    'Цветочная поляна': (0.08, 0.018, 1, 0.4, brown, 0.003, 0.001, 0.2),
    'Пустошь': (0.23, 0.0015, 1, 0.0015, grey, 0.0015, 0.011, 0.01)
} # не все параметры указываються в процентах из-за особеностей генерации
# параметры генерации каждого бюиома, сначала неровность, потом кол - во деревьев,
# потом максимальное отличие высоты между соседними блоками, потом количество цветов, потом цвет "земли",
# потом шанс на гриб, потом количество обрывов, потом шанс на особый обьект, у каждого биома он свой.
''''
{Пример':
 ('неровности', 'шанс на дерево', 'максимальный перепад высот', 'шанс на цветок', 'цвет земли', 'шанс на гриб'
 'шанс на обрыв', 'шанс на особый обьект')}
'''
list_biome = tuple(biom_config.keys())
