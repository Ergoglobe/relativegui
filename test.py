import pygame, pygui

pygame.init()

SIZE = (900, 500)
TPS = 60

WINDOW = pygame.display.set_mode(SIZE, pygame.RESIZABLE)

FONT = pygame.font.Font('freesansbold.ttf', 10)

COLOR = {
    'BLACK':(0,0,0),
    'WHITE':(255,255,255),
    'GREY':(127,127,127),
    'RED':(255,0,0),
    'GREEN':(0,255,0),
    'BLUE':(0,0,255),
    'YELLOW':(255,255,0),
    'CYAN':(0,255,255),
    'MAGENTA':(255,0,255),
    'DARKGREY':(80,80,80),
    'PINK':(255,192,203),
    'LIGHTPINK':(255,182,193),
    'HOTPINK':(255,105,180),
    'DEEPPINK':(255,20,147),
    'ORANGE':(255,165,0),
    'DARKORANGE':(255,140,0),
    'ORANGERED':(255,69,0),
    'GOLD':(255,215,0),
    'INDIGO':(75,0,130),
    'LIMEGREEN':(50,205,50),
    'MAROON':(128,0,0),
    'BABYBLUE':(137,207,240),
    'SILVER':(192,192,192),
    'PEACH':(255,218,185),
    'CORAL':(255, 127, 80),
    'CRIMSON':(157,34,53),

}

def test():
    if momentarytest.raw_text == 'Moment':
        momentarytest.change_text('Changed')
    else:
        momentarytest.change_text('Moment')

    imagetest.flip_image(False,True)

imagetest = pygui.image(20, 20, 20, 20, SIZE[0],SIZE[1], 'satispower.png',2,COLOR['RED'])
toggletest = pygui.base_toggle_button(1,0,5,5,SIZE[0],SIZE[1],COLOR['RED'], COLOR['GREEN'], False, 'Toggle',font_size=20)
hovertest = pygui.hover_toggle_button(1,6,5,5,SIZE[0],SIZE[1],COLOR['RED'], COLOR['GREEN'], False,COLOR['MAROON'],COLOR['CYAN'], 'Hover',font_size=20)
momentarytest = pygui.momentary_button(1,12,5,5,SIZE[0],SIZE[1],COLOR['RED'],COLOR['GREEN'],test, 'Moment',font_size=20)
circletest= pygui.circle(10,50,.5,SIZE[0],SIZE[1],COLOR['RED'])

textboxtest = pygui.single_line_text_box(1,20,15,5,SIZE[0],SIZE[1],COLOR['RED'],font_size=20)

containertest = pygui.movable_container(50,50,50,50,SIZE[0],SIZE[1],5,COLOR['BLUE'],'Container',COLOR['GREY'],top_border_font_size=20)
containertest.add_object('hover',pygui.hover_toggle_button(1,12,5,5,SIZE[0],SIZE[1],COLOR['RED'], COLOR['GREEN'], False,COLOR['MAROON'],COLOR['CYAN'], 'Hover',font_size=20))
containertest.add_object('image',pygui.image(20, 20, 20, 20, SIZE[0],SIZE[1], 'satispower.png',5,COLOR['RED']))
containertest.add_object('one__line',pygui.single_line_text_box(1,50,15,5,SIZE[0],SIZE[1],COLOR['RED']))

objects = [toggletest, hovertest, momentarytest, imagetest, textboxtest,circletest,containertest]

def draw_window():
    WINDOW.fill(COLOR['BLACK'])

def main():
    global SIZE

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(TPS)

        if WINDOW.get_size() != SIZE:
            SIZE = WINDOW.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for object in objects:
                    object.onClick()
            elif event.type == pygame.KEYDOWN:
                for object in objects:
                    object.onPress(event.key,event.unicode)

        if toggletest.get_value():
            containertest.hide()
        else:
            containertest.show()

        draw_window()

        for object in objects:
            object.process(WINDOW,SIZE[0],SIZE[1])

        pygame.display.flip()


if __name__ == '__main__':
    main()

pygame.quit()
quit()