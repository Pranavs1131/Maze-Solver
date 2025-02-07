from PIL import Image, ImageDraw
import numpy as np

from maze_solver import make_step

def ConvertImage(ImageName):
    try:
        # Open the maze image and make greyscale, and get its dimensions
        im = Image.open(ImageName).convert('L')
        #im.show()
        w, h = im.size

        # Ensure all black pixels are 0 and all white pixels are 1
        binary = im.point(lambda p: p < 128 and 1)

        # Resize to half its height and width so we can fit on Stack Overflow, get new dimensions
        binary = binary.resize((w//2,h//2),Image.NEAREST)
        w, h = binary.size

        # Convert to Numpy array - because that's how images are best stored and processed in Python
        nim = np.array(binary)

        # Each cell of the maze is represented by 5 numbers. Therefore change scaling FROM (5 number: 1 cell) TO (1 number: 1 cell)
        # initialize maze matrix
        maze = [[0 for i in range(int(w/5))] for j in range(int(h/5))]

        # go through every 5th number in each row and add it sequentially to the new matrix (maze).
        ri = ci = 0
        r = c = 4

        while ri < h/5:
            ci = 0
            c = 4
            while ci < w/5:
                maze[ri][ci] = nim[r][c]
                ci += 1
                c += 5
            ri += 1
            r += 5

        return [maze,int(h/5),int(w/5)]

    except FileNotFoundError:
        print("Error: Input image file not found.")
        return None
    

import time

def draw_matrix(a, m, the_path=[]):
    for u in range(len(the_path) - 1):
        im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        for i in range(len(a)):
            for j in range(len(a[i])):
                color = (255, 255, 255)
                r = 0
                if a[i][j] == 1:
                    color = (0, 0, 0)
                if i == start[0] and j == start[1]:
                    color = (0, 255, 0)
                    r = borders
                if i == end[0] and j == end[1]:
                    color = (0, 255, 0)
                    r = borders
                draw.rectangle((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                               fill=color)
                if m[i][j] > 0:
                    r = borders
                    draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                                 fill=(255, 0, 0))
        y = the_path[u][0] * zoom + int(zoom / 2)
        x = the_path[u][1] * zoom + int(zoom / 2)
        y1 = the_path[u + 1][0] * zoom + int(zoom / 2)
        x1 = the_path[u + 1][1] * zoom + int(zoom / 2)
        draw.line((x, y, x1, y1), fill=(255, 0, 0), width=5)
        draw.rectangle((0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0, 255, 0), width=2)
        images.append(im)
        time.sleep(0.5)  # Adjust the delay as needed

maze_name = input("Enter Image name with file format (eg. 'maze.png'): ")
output_name = input("Save output as (filename alone): ")

# Check if the maze conversion was successful
maze_loc = './inputs/' + maze_name
converted_maze = ConvertImage(maze_loc)
if converted_maze is None:
    exit()

a, rows, columns = converted_maze
zoom = 20
borders = 5
start = 1, 0
end = rows - 2, columns - 1

# Initialize maze solving algorithm
m = []
for i in range(rows):
    m.append([])
    for j in range(columns):
        m[-1].append(0)
i, j = start
m[i][j] = 1

k = 0
images = []
while m[end[0]][end[1]] == 0:
    k += 1
    make_step(k)
    draw_matrix(a, m)

# Trace back the path
i, j = end
k = m[i][j]
the_path = [(i, j)]
while k > 1:
    if i > 0 and m[i - 1][j] == k - 1:
        i, j = i - 1, j
        the_path.append((i, j))
        k -= 1
    elif j > 0 and m[i][j - 1] == k - 1:
        i, j = i, j - 1
        the_path.append((i, j))
        k -= 1
    elif i < len(m) - 1 and m[i + 1][j] == k - 1:
        i, j = i + 1, j
        the_path.append((i, j))
        k -= 1
    elif j < len(m[i]) - 1 and m[i][j + 1] == k - 1:
        i, j = i, j + 1
        the_path.append((i, j))

draw_matrix(a, m, the_path)

# Generate output GIF
saveas = './outputs/' + output_name + '.gif'
images[0].save(saveas,
               save_all=True, append_images=images[1:],
               optimize=False, duration=1, loop=0)

print("Output generated. Close program and check working directory.")


"""
def draw_matrix(a, m, the_path=[]):
    im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(len(a)):
        for j in range(len(a[i])):
            color = (255, 255, 255)
            r = 0
            if a[i][j] == 1:
                color = (0, 0, 0)
            if i == start[0] and j == start[1]:
                color = (0, 255, 0)
                r = borders
            if i == end[0] and j == end[1]:
                color = (0, 255, 0)
                r = borders
            draw.rectangle((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                           fill=color)
            if m[i][j] > 0:
                r = borders
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                             fill=(255, 0, 0))
    for u in range(len(the_path) - 1):
        y = the_path[u][0] * zoom + int(zoom / 2)
        x = the_path[u][1] * zoom + int(zoom / 2)
        y1 = the_path[u + 1][0] * zoom + int(zoom / 2)
        x1 = the_path[u + 1][1] * zoom + int(zoom / 2)
        draw.line((x, y, x1, y1), fill=(255, 0, 0), width=5)
    draw.rectangle((0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0, 255, 0), width=2)
    images.append(im)


def make_step(k):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == k:
                if i > 0 and m[i - 1][j] == 0 and a[i - 1][j] == 0:
                    m[i - 1][j] = k + 1
                if j > 0 and m[i][j - 1] == 0 and a[i][j - 1] == 0:
                    m[i][j - 1] = k + 1
                if i < len(m) - 1 and m[i + 1][j] == 0 and a[i + 1][j] == 0:
                    m[i + 1][j] = k + 1
                if j < len(m[i]) - 1 and m[i][j + 1] == 0 and a[i][j + 1] == 0:
                    m[i][j + 1] = k + 1


maze_name = input("Enter Image name with file format (eg. 'maze.png'): ")
output_name = input("Save output as (filename alone): ")

# Check if the maze conversion was successful
maze_loc = './inputs/' + maze_name
converted_maze = ConvertImage(maze_loc)
if converted_maze is None:
    exit()

a, rows, columns = converted_maze
zoom = 20
borders = 5
start = 1, 0
end = rows - 2, columns - 1

# Initialize maze solving algorithm
m = []
for i in range(rows):
    m.append([])
    for j in range(columns):
        m[-1].append(0)
i, j = start
m[i][j] = 1

k = 0
images = []
while m[end[0]][end[1]] == 0:
    k += 1
    make_step(k)
    draw_matrix(a, m)

# Trace back the path
i, j = end
k = m[i][j]
the_path = [(i, j)]
while k > 1:
    if i > 0 and m[i - 1][j] == k - 1:
        i, j = i - 1, j
        the_path.append((i, j))
        k -= 1
    elif j > 0 and m[i][j - 1] == k - 1:
        i, j = i, j - 1
        the_path.append((i, j))
        k -= 1
    elif i < len(m) - 1 and m[i + 1][j] == k - 1:
        i, j = i + 1, j
        the_path.append((i, j))
        k -= 1
    elif j < len(m[i]) - 1 and m[i][j + 1] == k - 1:
        i, j = i, j + 1
        the_path.append((i, j))
        k -= 1

draw_matrix(a, m, the_path)

# Generate output GIF
saveas = './outputs/' + output_name + '.gif'
images[0].save(saveas,
               save_all=True, append_images=images[1:],
               optimize=False, duration=1, loop=0)

print("Output generated. Close program and check working directory.")
"""