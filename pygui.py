import pygame

class static_object():
    def __init__(self, x, y, w, h, screen_x, screen_y, color = None, text = '', font = 'freesansbold.ttf', font_size = 10, font_color = (0,0,0), image = None, border_px = None, border_color = (0,0,0), scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        self.x = (round(screen_x*x/100),x)
        self.y = (round(screen_y*y/100),y)
        self.w = (round(screen_x*w/100),w)
        self.h = (round(screen_y*h/100),h)
        self.color = color
        self.minimized=False

        self.FONT = pygame.font.Font(font, font_size)
        self.raw_text = text
        self.text = self.FONT.render(text, True, font_color)

        if image != None:
            self.orig_image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.orig_image, (self.w[0], self.h[0]))
        else:
            self.image = None

        if border_px != None:
            self.border_px = border_px
            self.border_color = border_color
        else:
            self.border_px = None

    def process(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        if self.minimized:
            return
        self.x = (round(screen_x*self.x[1]/100*scale_x+offset_x),self.x[1])
        #screen*scale/100=pixel
        #scale=pixel*100/screen
        self.y = (round(screen_y*self.y[1]/100*scale_y+offset_y),self.y[1])
        self.w = (round(screen_x*self.w[1]/100*scale_x),self.w[1])
        self.h = (round(screen_y*self.h[1]/100*scale_y),self.h[1])
        self.rect = pygame.Rect(self.x[0], self.y[0], self.w[0], self.h[0])

        self.textrect = self.text.get_rect()
        self.textrect.center = (self.x[0]+self.w[0]//2,self.y[0]+self.h[0]//2)

        if self.color != None:
            pygame.draw.rect(surface, self.color, self.rect)
            surface.blit(self.text, self.textrect)

        if self.image != None:
            self.image = pygame.transform.scale(self.orig_image, (self.w[0], self.h[0]))
            self.image_rect = self.image.get_rect()

            self.image_rect.center = (self.x[0]+self.w[0]//2,self.y[0]+self.h[0]//2)
            surface.blit(self.image, self.image_rect)

        if self.border_px != None:
            self.borders = []
            
            self.border_boxes = ((self.x[0],self.y[0],self.w[0],self.border_px),(self.x[0],self.y[0]+self.h[0]-self.border_px,self.w[0],self.border_px),(self.x[0],self.y[0],self.border_px,self.h[0]),(self.x[0]+self.w[0]-self.border_px,self.y[0],self.border_px,self.h[0]))

            for values in (self.border_boxes):
                self.borders.append(pygame.Rect(values[0],values[1],values[2],values[3]))
            for border in self.borders:
                pygame.draw.rect(surface, self.border_color, border)

    def change_text(self, text = '', font = 'freesansbold.ttf', font_size = 10, font_color = (0,0,0)):
        self.FONT = pygame.font.Font(font, font_size)
        self.raw_text = text
        self.text = self.FONT.render(text, True, font_color)

    def change_image(self, image):
        self.orig_image = pygame.image.load(image)

    def set_pos(self, x,y,screen_x,screen_y):
        self.x = (x,round(x*100/screen_x))
        self.y = (y,round(y*100/screen_y))
        #screen*scale/100=pixel
        #scale=pixel*100/screen

    def set_relative_pos(self, x,y,screen_x,screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        self.x = (round(screen_x*x[1]/100*scale_x+offset_x),x[1])
        self.y = (round(screen_y*y[1]/100*scale_y+offset_y),y[1])

    def get_pos(self):
        return (self.x[0],self.y[0])

    def onClick(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        return
    
    def get_self(self):
        return self
    
    def hide(self):
        self.minimized=True

    def show(self):
        self.minimized=False

class click_object(static_object):
    def process(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        if self.minimized:
            return
        super().process(surface, screen_x, screen_y, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x[0] and pos[0] < self.x[0] + self.w[0] and pos[1] > self.y[0] and pos[1] < self.y[0] + self.h[0]:
            data = [True]
        else:
            data = [False]

        data.append(pygame.mouse.get_pressed())

        return data
    
    def onClick(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        if self.minimized:
            return
        return self.process(surface, screen_x, screen_y, scale_x,scale_y,offset_x,offset_y)

class variable_object(click_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, text, font, font_size, font_color, value,scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, text, font, font_size, font_color, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)
        self.value = value

    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value

class base_toggle_button(variable_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, toggle_color, value, text = '', font = 'freesansbold.ttf', font_size = 10, font_color = (0,0,0), scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, text, font, font_size, font_color, value, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)
        self.toggle_color = toggle_color
        self.base_color = color
        self.value = value

    def onClick(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        if self.minimized:
            return
        data = super().process(surface, screen_x, screen_y, scale_x,scale_y,offset_x,offset_y)
        if data[0]:
            self.value = not self.value

        if self.value:
            self.color = self.toggle_color
        else:
            self.color = self.base_color
        return data

class hover_toggle_button(base_toggle_button):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, toggle_color, value, false_hover_color, true_hover_color, text = '', font = 'freesansbold.ttf', font_size = 10, font_color = (0,0,0), scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, toggle_color, value, text, font, font_size, font_color, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)
        self.false_hover_color = false_hover_color
        self.true_hover_color = true_hover_color

    def process(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        if self.minimized:
            return
        data = super().process(surface, screen_x, screen_y, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)

        if self.value:
            if data[0]:
                self.color = self.true_hover_color
            else:
                self.color = self.toggle_color
        else:
            if data[0]:
                self.color = self.false_hover_color
            else:
                self.color = self.base_color

        return data
    
class momentary_button(base_toggle_button):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, toggle_color, function=None, text = '', font = 'freesansbold.ttf', font_size = 10, font_color = (0,0,0), scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, toggle_color, False, text, font, font_size, font_color, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)
        self.function = function

    def process(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        if self.minimized:
            return
        data = super().process(surface, screen_x, screen_y, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)

        if not data[0] or not data[1][0]:
            self.value = False
            self.color = self.base_color

        return data

    def onClick(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0, args=None):
        if self.minimized:
            return
        data = super().process(surface, screen_x, screen_y, scale_x,scale_y,offset_x,offset_y)

        if data[0]:
            self.value = True
            self.color = self.toggle_color
            if self.function!=None and args == None:
                return self.function()
            elif self.function!=None:
                return self.function(args)

class label(static_object):
    def __init__(self,x, y, w, h, screen_x, screen_y, text, font_size, font_color, font = 'freesansbold.ttf', scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, text = text, font = font, font_size=font_size, font_color=font_color, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)

class image(static_object):
    def __init__(self,x, y, w, h, screen_x, screen_y, image, border_px = None, border_color=(0,0,0), scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, image=image, border_px=border_px,border_color=border_color, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)

class rectangle(static_object):
    def __init__(self,x, y, w, h, screen_x, screen_y, color, border_px = None, border_color=(0,0,0), scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, border_px=border_px,border_color=border_color, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)

class textbox(variable_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, border_px=None, border_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, border_px, border_color, scale_x, scale_y, offset_x, offset_y)

class Container(rectangle):
    def __init__(self,x, y, w, h, screen_x, screen_y, color = None, border_px = None, border_color=(0,0,0), scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, border_px=border_px,border_color=border_color, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)
        self.objects = {}

    def process(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        if self.minimized:
            return
        super().process(surface, screen_x, screen_y, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)
        for object in self.objects:
            self.objects[object].process(surface, self.w[0], self.h[0],offset_x=self.x[0],offset_y=self.y[0])

    def onClick(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        if self.minimized:
            return
        for object in self.objects:
            #temp = self.objects[object]
            #temp.onClick(surface, self.w[0], self.h[0],offset_x=self.x[0],offset_y=self.y[0])
            self.objects[object].onClick(surface, self.w[0], self.h[0],offset_x=self.x[0],offset_y=self.y[0])

    def add_object(self, name, object):
        self.objects[name] = object

    def delete_object(self, name):
        del self.objects[name]

class movable_container(Container):
    def __init__(self,x, y, w, h, screen_x, screen_y, top_border_size, top_border_color = None, top_border_title = '', color = None, border_px = None, border_color=(0,0,0), scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, border_px=border_px,border_color=border_color, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)
        self.moving=False
        self.top_border = momentary_button(x, y, w, top_border_size, screen_x, screen_y, top_border_color, top_border_color, None, top_border_title)

    def process(self, surface, screen_x, screen_y, scale_x=1,scale_y=1,offset_x=0,offset_y=0):
        if self.minimized:
            return
        super().process(surface, screen_x, screen_y, scale_x=scale_x,scale_y=scale_y,offset_x=offset_x,offset_y=offset_y)

        data = self.top_border.process(surface, screen_x, screen_y)

        if data[0] and data[1][0] and not self.moving:
            self.moving=True
            mouse_pos=pygame.mouse.get_pos()
            self.move_x_offset=mouse_pos[0]-self.x[0]
            self.move_y_offset=mouse_pos[1]-self.y[0]

        elif data[1][0] and self.moving:
            #self.moving=False
            mouse_pos = pygame.mouse.get_pos()
            self.set_pos(mouse_pos[0]-self.move_x_offset,mouse_pos[1]-self.move_y_offset,screen_x,screen_y)
            self.top_border.set_pos(mouse_pos[0]-self.move_x_offset,mouse_pos[1]-self.move_y_offset,screen_x,screen_y)

        elif not data[1][0] and self.moving:
            self.moving=False