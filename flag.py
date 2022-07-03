import pygame
from io import BytesIO
import requests
from PIL import Image, ImageOps
from random import choice
from button import Button, Text, Rect, Pos, Input, MoveBox

pygame.font.init()

flag = None

font = pygame.font.SysFont('freesansbold.ttf', 32)

data = requests.get("https://flagcdn.com/fr/codes.json").json()

data_keys = list(data.keys())

def invert(data):
    return (255 - data[0], 255 - data[1], 255 - data[2])

def invert_pic(pilimage):
    return ImageOps.invert(pilimage)

def get_rand_flag(data_keys):
    code = choice(data_keys)
    rsp = requests.get("https://flagcdn.com/w320/{}.png".format(code))
    pilimage = Image.open(BytesIO(rsp.content)).convert("RGB")
    pgimg = pygame.image.fromstring(pilimage.tobytes(), pilimage.size, pilimage.mode)
    return pgimg

my_button = Button([0, 300], Text("Random", font), [180, 80], (55,55,55), get_rand_flag)

button_validate = Button((0, 500), Text("validate", font), [100, 100], (0, 55, 0), None)

def clear_data(data):
    clean_data = {}
    for i in data.keys():
        if "us-" not in i:
            clean_data[i] = data[i]
    return clean_data

data = clear_data(data)

data_keys = list(data.keys())
flag = get_rand_flag(data_keys)
# show image
pygame.init()
display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

text_box = Input(Rect(150,150,450,50), font=font)
possibilities = MoveBox()
def get_possible(text):
    text_mod = text.lower()
    possible = []
    for i in data_keys:
        if data[i].lower().startswith(text_mod):
            possible.append(data[i])
    if len(possible) < 5:
        for i in data_keys:
            if text_mod in data[i].lower() and data[i] not in possible:
                possible.append(data[i])
    return possible if len(possible) <= 5 else possible[:5]

possible_rect = Rect(300, 300, 300, 300)



def get_mid_pos(image):
    pos = [1920 / 2 - image.get_width() / 2, 1080 / 2 - image.get_height() / 2]
    return pos

while True:
    for event in pygame.event.get():
        text_box.handle_select(event)
        text_box.add_text(event)
        if event.type == pygame.KEYDOWN:
            print(get_possible(text_box.text))
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit(); exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            tmp = my_button.on_click(pygame.mouse.get_pos(), data_keys)
            if tmp != None:
                flag = tmp
    display.fill((155,155,155))
    display.blit(flag, get_mid_pos(flag))
    my_button.draw(display)
    button_validate.draw(display)
    text_box.draw(display)
    if len(text_box.text) > 0:
        draw_possible(get_possible(text_box.text), possible_rect)
    pygame.display.update()