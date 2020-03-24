import pygame


class Widget(object):

    def __init__(self, screen, size):
        self.surface = pygame.surface.Surface(size)

    def draw(self):
        screen.blit(self.surface, (0, 0))


class ColorSector(Widget):

    def __init__(self, screen, icon_size):
        self.icon_size = icon_size
        self.height = icon_size
        self.width = 360 + icon_size
        self.selected_color = [255, 0, 0]
        self.rect = pygame.Rect([0, 0, self.width, self.height])
        super(ColorSector, self).__init__(screen, [self.width, self.height])

    def setup(self):
        for i in range(360):
            for j in range(100):
                pygame.draw.line(self.surface, from_hsva(i,j,brightness,100), [
                                 i, j],[i, j],1)
        pygame.draw.rect(self.surface, self.selected_color, [360,0,self.icon_size,self.icon_size])

    def run(self):
        index = mouseX
        try:
            self.selected_color = from_hsva(mouseX,mouseY,brightness,100)
            pygame.draw.rect(self.surface, self.selected_color, [360,0,self.icon_size,self.icon_size])
        except ValueError:
            pass

def from_hsva(h,s,v,a):
    color = pygame.Color(0)
    color.hsva = h,s,v,a
    return color

def to_hsva(r,g,b,a=255):
    return pygame.Color(r,g,b,a).hsla

pygame.init()


# Screen Setup

# Model is trained on images of size (450,337)
image_size = (450, 337)

# gives a larger size to work with to give finer control
canvas_size = (image_size[0] * 2, image_size[1] * 2)

# Menu bar size
menu_rect = pygame.Rect([0, 0, 100, 100])
paint_rect = pygame.Rect([0, menu_rect[3], *canvas_size])
processed_rect = pygame.Rect(
    [paint_rect[2], paint_rect[1], paint_rect[2], paint_rect[3]])
width = paint_rect[2] + processed_rect[2]
height = paint_rect[3] + menu_rect[3]

screen = pygame.display.set_mode([width, height])
paint_surface = pygame.surface.Surface([*paint_rect[2:]])
processed_surface = pygame.surface.Surface([*processed_rect[2:]])

brush_size = 100
scroll = 0
brightness = 100

# Class Setup
color_selctor = ColorSector(screen, 100)
color_selctor.setup()



running = True
mouseX, mouseY = pygame.mouse.get_pos()
while running:
    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scroll = 1
            if event.button == 5:
                scroll = -1

    # Logic
    last_mouseX, last_mouseY = mouseX, mouseY
    mouseX, mouseY = pygame.mouse.get_pos()
    left_click, middle_cick, right_click = pygame.mouse.get_pressed()


    # Draw
    screen.fill((255, 255, 255))

    
    if paint_rect.collidepoint(mouseX, mouseY):

        if scroll == 1:
            brush_size += 10
            brush_size = min(brush_size, 200)
        if scroll == -1:
            brush_size -= 10
            brush_size = max(brush_size, 1)
        if left_click:
            pygame.draw.line(paint_surface, color_selctor.selected_color,
                             (mouseX - paint_rect[0], mouseY - paint_rect[1]), [last_mouseX - paint_rect[0], last_mouseY - paint_rect[1]], brush_size)
            pygame.draw.circle(paint_surface, color_selctor.selected_color,
                               (mouseX - paint_rect[0], mouseY - paint_rect[1]), brush_size // 2)
    if color_selctor.rect.collidepoint(mouseX, mouseY):
        print(scroll,brightness)
        if scroll == 1:
            brightness += 1
            brightness = min(brightness, 100)
            color_selctor.setup()
        if scroll == -1:
            brightness -= 1
            brightness = max(brightness, 1)
            color_selctor.setup()
        if left_click:
            color_selctor.run()
            


    screen.blit(paint_surface, (paint_rect))
    screen.blit(paint_surface, (processed_rect))

    color_selctor.draw()
    pygame.display.flip()

    scroll = 0

pygame.quit()
