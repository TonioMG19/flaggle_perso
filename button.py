import pygame

def contains(rect, pos):
    if pos.x >= rect.x and pos.x <= rect.x + rect.width and pos.y >= rect.y and pos.y <= rect.height + rect.y:
        return True
    return False

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_list(self):
        return [self.x, self.y, self.width, self.height]

    def to_list_pos(self):
        return [self.x, self.y]

class Button:
    def __init__(self, pos, text, size, color, func):
        self.pos = pos
        self.text = text
        self.size = size
        self.color = color
        self.color_uh = color
        self.color_h = (int(color[0] * 0.8), int(color[1] * 0.8), int(color[2] * 0.8))
        self.func = func
        self.is_hover = False

    def draw(self, display):
        pygame.draw.rect(display, self.color, [self.pos[0], self.pos[1], self.size[0], self.size[1]])
        display.blit(self.text.get_render(), self.pos)

    def on_click(self, pos_m, args):
        if pos_m[0] >= self.pos[0] and pos_m[0] <= self.pos[0] + self.size[0] and pos_m[1] >= self.pos[1] and pos_m[1] <= self.pos[1] + self.size[1]:
            return self.func(args)
        else:
            return None

class Text:
    def __init__(self, text, font = None, size = 16, color = (0, 0, 0)):
        self.text = text
        self.font = font
        self.render = self.font.render(self.text, True, color)

    def get_render(self):
        return self.render

class Input:
    def __init__(self, rect, color = (55, 55, 55), font = None, back_color = (30, 30, 30)):
        self.rect = rect
        self.back_rect = Rect(rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20)
        self.back_color = back_color
        self.color = color
        self.font = font
        self.text = ""
        self.is_selected = False
        self.text_buf = Text(self.text, self.font)
    def handle_select(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and contains(self.rect, Pos(*pygame.mouse.get_pos())):
            self.is_selected = True

    def add_text(self, event):
        if event.type == pygame.KEYDOWN and self.is_selected == True:
            if event.key == pygame.K_RETURN:
                self.is_selected = False
                return
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.text_buf = Text(self.text, self.font)
                return
            print(event.key)
            self.text += event.unicode
            self.text_buf = Text(self.text, self.font)
            print(self.text)

    def draw(self, display):
        pygame.draw.rect(display, self.back_color, self.back_rect.to_list())
        pygame.draw.rect(display, self.color, self.rect.to_list())
        display.blit(self.text_buf.get_render(), self.rect.to_list_pos())


class MoveBox:
    def __init__(self, rect, color, font):
        self.rect = rect
        self.color = color
        self.content = []
        self.font = font

    def draw(self, display):
        text = Text('\n'.join(self.content), self.font)
        render = text.get_render()
        screen.blit(render, self.rect.to_list_pos())