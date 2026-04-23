import pygame
import random
pygame.init()

wd = 800
ht = 600
screen = pygame.display.set_mode((wd,ht),pygame.RESIZABLE)          # enables window maximization
font = pygame.font.Font(None,38)
clock = pygame.time.Clock()
running = True
lines = [""]
cursor_visible = True
cursor_timer = 0
cursor_line = 0
cursor_pos = 0
last_click = 0
double_click = 400
bgc = (0,20,50)       # default background color

while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:               # closes the window
            running = False
        if event.type==pygame.KEYDOWN:              
            if event.key==pygame.K_BACKSPACE:          # for erasing characters one at a time
                if cursor_pos > 0:
                    line = lines[cursor_line]
                    lines[cursor_line] = line[:cursor_pos-1] + line[cursor_pos:]
                    cursor_pos -= 1
                elif cursor_line > 0:
                    prev_line_len = len(lines[cursor_line-1])
                    lines[cursor_line-1] += lines[cursor_line]
                    lines.pop(cursor_line)
                    cursor_line -= 1
                    cursor_pos = prev_line_len
            elif event.key==pygame.K_RETURN:        # skips to next line by pressing Enter
                line = lines[cursor_line]
                new_line = line[cursor_pos:]
                lines[cursor_line] = line[:cursor_pos]
                lines.insert(cursor_line+1, new_line)

                cursor_line += 1
                cursor_pos = 0
            elif event.key==pygame.K_LEFT:           # Left arrow
                if cursor_pos > 0:
                    cursor_pos -= 1
                elif cursor_line > 0:
                    cursor_line -= 1
                    cursor_pos = len(lines[cursor_line])
            elif event.key==pygame.K_RIGHT:              # Right arrow
                if cursor_pos < len(lines[cursor_line]):
                    cursor_pos += 1
                elif cursor_line < len(lines) - 1:
                    cursor_line += 1
                    cursor_pos = 0
            elif event.key==pygame.K_UP:                  # Up arrow
                curr = len(lines[cursor_line][:cursor_pos])
                cursor_pos = curr
                cursor_line-=1
            elif event.key==pygame.K_DOWN:              # Down arrow
                curr = len(lines[cursor_line][:cursor_pos])
                cursor_pos = curr
                cursor_line+=1
            elif event.unicode:
                lines[cursor_line]=lines[cursor_line][:cursor_pos]+event.unicode+lines[cursor_line][cursor_pos:]
                cursor_pos+=1
        
        if event.type==pygame.MOUSEBUTTONDOWN:             # changes color on double clicking
            color = [(0,0,0),(250,0,0),(0,230,0),(0,20,50),(214,190,189),(128, 128, 128),(204, 119, 34),(80, 200, 120),(15, 82, 186)]
            current_click = pygame.time.get_ticks()
            if current_click-last_click < double_click:
                bgc = random.choice(color)
            last_click = current_click
    screen.fill(bgc)
    
    y = 50
    for line in lines:
        rendered_text = font.render(line,True,(250,250,250))
        screen.blit(rendered_text,(100,y))
        y+=43

    curs_line = lines[cursor_line][:cursor_pos]
    rendered_cursor = font.render(curs_line,True,(245,245,245))
    cursor_x = 100+rendered_cursor.get_width()
    cursor_y = 49+cursor_line*43

    cursor_timer+=clock.get_time()
    if cursor_timer>500:                # blinking cursor
        cursor_visible = not cursor_visible
        cursor_timer = 0

    if cursor_visible:
        pygame.draw.rect(screen,(255,254,254),(cursor_x,cursor_y,1.5,25))

    pygame.display.update()
    clock.tick(60)
pygame.quit()
