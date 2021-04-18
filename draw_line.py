# Renders a 2D model into a PPM image
import sys
import numpy as np

# ---------- Configuration types and constants ----------

IMAGE_DTYPE = np.uint8
COORD_DTYPE = np.int64
MODEL_DTYPE = np.float64

MAX_SIZE = 1024
MAX_VAL = 255
MAX_LINE_LEN = 10240-1 # 10240 characters minus the \0 terminator
DEFAULT_BACKGROUND = 255
CHANNELS_N = 3
DEFAULT_COLOR = (0, 0, 0,)

# ---------- Output routines ----------

def put_string(output, output_file):
    output = output.encode('ascii') if isinstance(output, str) else output
    written_n = output_file.write(output)
    if written_n != len(output):
        print('error writing to output stream', file=sys.stderr)
        sys.exit(1)

def save_ppm(image, output_file):
    # Defines image header
    magic_number_1 = 'P'
    magic_number_2 = '6'
    width  = image.shape[1]
    height = image.shape[0]
    end_of_header = '\n'

    # Writes header
    put_string(magic_number_1, output_file)
    put_string(magic_number_2, output_file)
    put_string('\n', output_file)
    put_string('%d %d\n' % (width, height), output_file)
    put_string('%d' % MAX_VAL, output_file)
    put_string(end_of_header, output_file)

    # Outputs image
    put_string(image.tobytes(), output_file)

# ---------- Drawing/model routines ----------

def draw_line(image, x_init, y_init, x_fin, y_fin, color):
    if(x_fin < x_init):
        stepX = -1
    else:
        stepX = 1
    if(y_fin < y_init):
        stepY = -1
    else:
        stepY = 1
    height, width, m = image.shape
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

# ---------- Main routine ----------

# Parses and checks command-line arguments
if len(sys.argv)!=3:
    print("usage: python draw_2d_model.py <input.dat> <output.ppm>\n"
          "       interprets the drawing instructions in the input file and renders\n"
          "       the output in the NETPBM PPM format into output.ppm")
    sys.exit(1)

input_file_name  = sys.argv[1]
output_file_name = sys.argv[2]

# Reads input file and parses its header
with open(input_file_name, 'rt', encoding='utf-8') as input_file:
    input_lines = input_file.readlines()

if input_lines[0] != 'EA979V3\n':
    print(f'input file format not recognized!', file=sys.stderr)
    sys.exit(1)

dimensions = input_lines[1].split()
width = int(dimensions[0])
height = int(dimensions[1])

if width<=0 or width>MAX_SIZE or height<=0 or height>MAX_SIZE:
    print(f'input file has invalid image dimensions: must be >0 and <={MAX_SIZE}!', file=sys.stderr)
    sys.exit(1)

# Creates image
image = np.full((height, width, 3), fill_value=DEFAULT_BACKGROUND, dtype=IMAGE_DTYPE)

#
# TODO: Inicialize as demais variaveis
#
M = np.array([[1,0,0], [0,1,0], [0,0,1]])

# Main loop - interprets and renders drawing commands
for line_n,line in enumerate(input_lines[2:], start=3):
    if (line[0] == '#'):
        continue

    if len(line)>MAX_LINE_LEN:
        print(f'line {line_n}: line too long!', file=sys.stderr)
        sys.exit(1)

    if not line.strip():
        # Blank line - skips
        continue

    command = line[0]
    parameters = line[1:].strip().split()
    def check_parameters(n):
        if len(parameters) != n:
            print(f'line {line_n}: command {command} expected {n} parameters but got {len(parameters)}!',
                  file=sys.stderr)
            sys.exit(1)

    if command == 'c':
        # Clears with new background color
        check_parameters(CHANNELS_N)
        background_color = np.array(parameters, dtype=IMAGE_DTYPE)
        image[:, :] = background_color
        DEFAULT_BACKGROUND = background_color

    elif command == 'C':
        check_parameters(CHANNELS_N)
        DEFAULT_COLOR = np.array(parameters, dtype=IMAGE_DTYPE)

    elif command == 'M':
        check_parameters(9)

        M = np.array(parameters, dtype=MODEL_DTYPE).reshape(3,3)

    elif command == 'm':
        check_parameters(9)

        M = np.array(parameters, dtype=MODEL_DTYPE).reshape(3,3).dot(M)

    elif command == 'L':
        # Draws given line
        check_parameters(4)
        draw_line(image, int(parameters[0]), int(parameters[1]), int(parameters[2]), int(parameters[3]), DEFAULT_COLOR)

    elif command == 'P':
        # Draws poliline from given points
        check_parameters(int(parameters[0])*2 + 1)
        b = -1
        for iterate in range(int(parameters[0]) - 1):
            b += 2
            draw_line(image, int(parameters[b]), int(parameters[b+1]), int(parameters[b+2]), int(parameters[b+3]), DEFAULT_COLOR)

    elif command == 'R':
        # Draws a poligon with the given points
        check_parameters(int(parameters[0])*2 + 1)
        b = -1
        for iterate in range(int(parameters[0]) - 1):
            b += 2
            draw_line(image, int(parameters[b]), int(parameters[b+1]), int(parameters[b+2]), int(parameters[b+3]), DEFAULT_COLOR)
        draw_line(image, int(parameters[-2]), int(parameters[-1]), int(parameters[1]), int(parameters[2]), DEFAULT_COLOR)

    else:
        print(f'line {line_n}: unrecognized command "{command}"!', file=sys.stderr)
        sys.exit(1)

# If we reached this point, everything went well - outputs rendered image file
with open(output_file_name, 'wb') as output_file:
    save_ppm(image, output_file)
