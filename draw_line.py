import os
import sys
import numpy as np

stdout = sys.stdout.fileno()
def put_byte(output):
    written_n = os.write(stdout, bytes((output,)))
    if written_n != 1:
        print('error writing to output stream', file=sys.stderr)
        sys.exit(1)

def put_string(output):
    output = output.encode('ascii') if isinstance(output, str) else output
    written_n = os.write(stdout, output)
    if written_n != len(output):
        print('error writing to output stream', file=sys.stderr)
        sys.exit(1)


def draw_line(image, x_init, y_init, x_fin, y_fin, color):
    if(x_fin < x_init):
        stepX = -1
    else:
        stepX = 1
    if(y_fin < y_init):
        stepY = -1
    else:
        stepY = 1
    height, width = image.shape
    #Setting values for the midpoint algorithm
    dx = abs(x_fin - x_init)
    dy = abs(y_fin - y_init)
    y_fin = height - y_fin - 1
    y_init = height - y_init - 1
    #slope < 1
    if (abs(dy) <= abs(dx)):
        delta_E = 2*dy
        delta_NE = 2*(dy - dx)
        d_step = 2*dy - dx
        x = x_init
        y = y_init
        for iterate in range(dx + 1):
            image[y][x] = color
            if (d_step <= 0):
                x += stepX
                d_step += delta_E
            else:
                x += stepX
                y -= stepY
                d_step += delta_NE
    #slope > 1
    elif (abs(dy) > abs(dx)):
        delta_E = 2*dx
        delta_NE = 2*(dx - dy)
        d_step = 2*dx - dy
        x = x_init
        y = y_init
        for iterate in range(dy + 1):
            image[y][x] = color
            if (d_step <= 0):
                y -= stepY
                d_step += delta_E
            else:
                y -= stepY
                x += stepX
                d_step += delta_NE

# Parses and checks command-line arguments
MAX_SIZE = 8192
max_val = 255

w = h = x0 = y0 = x1 = y1 = color = -1
if len(sys.argv) > 7:
    w = int(sys.argv[1])
    h = int(sys.argv[2])
    x0 = int(sys.argv[3])
    y0 = int(sys.argv[4])
    x1 = int(sys.argv[5])
    y1 = int(sys.argv[6])
    color = int(sys.argv[7])

if len(sys.argv)<=7 or w<0 or w>MAX_SIZE or h<0 or h>=MAX_SIZE or x0<0 or x0>=w or x1<0 or x1>=w or y0<0 or y0>=h or \
        y1<0 or y1>=h or color<0 or color>max_val:
    print("usage: draw_line <W> <H> <X0> <Y0> <X1> <Y1> <COLOR> > output.pgm\n"
          "creates a PGM image with a line from (X0, Y0) to (X1, Y1) drawin in it\n"
          "W => image width, from 1 to %d\n"
          "H => image height, from 1 to %d\n"
          "<X0> <Y0> <X1> <Y1> => line coordinates, with 0 <= X < W and 0 <= Y < H\n"
          "COLOR => \"color\" of the line in grayscale, from 0 to %d.\n" %
          (MAX_SIZE, MAX_SIZE, max_val), file=sys.stderr)
    sys.exit(1)

# Defines image header
magic_number_1 = 'P'
magic_number_2 = '5'
width  = w
height = h
end_of_header = '\n'

# Writes header
put_string(magic_number_1)
put_string(magic_number_2)
put_string('\n')
put_string('%d %d\n' % (width, height))
put_string('%d' % max_val)
put_string(end_of_header)

# Creates image...
background = 255
image = np.full((height, width), fill_value=background, dtype=np.uint8)

# Draws line
draw_line(image, x0, y0, x1, y1, color)

# Outputs image
put_string(image.tobytes())
