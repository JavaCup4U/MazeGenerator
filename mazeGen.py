
import pygame
import time 
import random 

# window set up 
width = 500
height = 600
FPS = 30

# colors 
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
# pygame 
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()

# maze content 
x = 0           # x axis 
y = 0           # y axis 
w = 20          # width of cell 

grid = []
visited = []
stack = []
solution = {}

# create gride 
def create_grid(x, y, w):
    for i in range(1, 21):
        x = 20 
        y = y + 20
        for j in range(1, 21):
            pygame.draw.line(screen, white, [x, y], [x + w, y])          # top of box
            pygame.draw.line(screen, white, [x + w, y], [x + w, y + w])  # right side of box
            pygame.draw.line(screen, white, [x + w, y + w], [x, y + w ]) # bottom of box
            pygame.draw.line(screen, white, [x, y + w], [x, y])          # left side of box
            grid.append((x, y))                                          # add box to grid list 
            x = x + 20                                                   # move box to new position

# draw rectangle twice the width of the box to animate a wall being removed 
def move_up(x, y):
    pygame.draw.rect(screen, red, (x + 1, y - w + 1, 19, 39) , 0)
    pygame.display.update()

def move_down(x, y):
    pygame.draw.rect(screen, red, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()

def move_left(x, y):
    pygame.draw.rect(screen, red, ( x - w + 1, y + 1, 39, 19), 0)
    pygame.display.update()

def move_right(x, y):
    pygame.draw.rect(screen, red, ( x + 1, y + 1, 39, 19), 0)
    pygame.display.update()

def curr_cell(x, y ):
    pygame.draw.rect( screen, green, (x + 1, y + 1, 18, 18), 0) # draw a single cell
    pygame.display.update()

# re - colors path after current cell has been visited 
def backtrack_cell(x, y):
    pygame.draw.rect(screen, red, (x + 1, y + 1, 18, 18), 0)
    pygame.display.update()

# used to output the solution 
def result(x, y):
    pygame.draw.rect(screen, black, (x+8, y+8, 5, 5), 0)
    pygame.display.update()

def create_maze(x, y):
    curr_cell(x, y)                                             # start first positioning of maze
    stack.append((x, y))                                        # place first spot into stack
    visited.append((x, y))                                      # add start spot to visited list 
    while len(stack) > 0:                                       # loop while stack is not empty
        time.sleep(.07)                                         # slow down program
        cells = []                                              # create cell list
        if (x + w, y) not in visited and (x + w, y) in grid:    # is right box available ?
            cells.append("right")                               # if yes add to cells list 
        
        if (x - w, y) not in visited and (x - w, y) in grid:    # check if left box is available?
            cells.append("left")                                
        
        if (x, y + w) not in visited and (x, y + w) in grid:    # check if bottom box is availabe?
            cells.append("down")
        
        if (x, y - w) not in visited and (x, y - w) in grid:    # check if top box is available
            cells.append("up")
        
        if len(cells) > 0:                                      # check cells list to see if its empty
            selected_cell = (random.choice(cells))                 # select a cell randomly from the cells list 


            if selected_cell == "right":                        # if right cell is selected 
                move_right(x, y)                                # call move right function
                solution[(x + w, y)] = x, y                     # solution = dictionary key = new cell, other = current cell 
                x = x + w                                       # make this cell the current one
                visited.append((x, y))                          # add it to visited list
                stack.append((x, y))                            # place current cell on to the stack 

            elif selected_cell == "left":
                move_left(x, y)
                solution[(x - w, y)] = x, y 
                x = x - w
                visited.append((x, y))
                stack.append((x,y))

            elif selected_cell == "down":
                move_down(x, y)
                solution[(x, y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))
            
            elif selected_cell == "up":
                move_up(x, y)
                solution[(x, y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:                                                    
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            curr_cell(x, y)                                       # use current cell function to show backtrack 
            time.sleep(.05)                                       # slow down 
            backtrack_cell(x, y)                                  # change color to green to identify backtrack path
 
def route_back(x, y):
    result(x, y)                                                  # result list contains all coordinates to route back to start
    while (x, y) != 20:                                           # loop until cell position == start position 
        x, y = solution[x, y]                                     # key value now becomes the new key
        result(x, y)                                              # show route back
        time.sleep(.1)




x, y = 20, 20                                                    # Start position
create_grid(40, 0, 20)                                           # 1st arg = x val, 2nd arg = y val, 3rd arg = width of cell
create_maze(x, y)                                                # call create maze function
route_back(400,400)                                              # call route back function


# pygame loop 
running = True 

while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
