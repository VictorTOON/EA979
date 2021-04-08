/* Renders a 2D model into a PPM image */

#include <assert.h>
#include <inttypes.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ---------- Configuration types and constants ---------- */

typedef uint32_t     pixel_t; // Colors packed __RRGGBB
typedef int_fast16_t coord_t;
typedef double       model_t;

#define PRI_COORD PRIdFAST16

#define MAX_LINE_LEN 10240

const char *parameter_delimiters = " \t\r\n";

const int     max_val      = 255;
const size_t  channels_n   = 3;
const size_t  transforms_n = 9;
const coord_t max_size     = 1024;

const int default_background = 0x00FFFFFF; // White
const pixel_t default_color  = 0x00000000; // Black

/* ---------- Output routines ---------- */

void put_byte(int byte, FILE *output) {
    int status = putc(byte, output);
    if (status == EOF) {
        fprintf(stderr, "error writing to output stream\n");
        exit(EXIT_FAILURE);
    }
}

void put_pixel(pixel_t pixel, FILE *output) {
    put_byte(pixel >> 16       , output); // Red
    put_byte(pixel >>  8 & 0xFF, output); // Green
    put_byte(pixel       & 0xFF, output); // Blue
}

void save_ppm(pixel_t *image, coord_t width, coord_t height, FILE *output) {
    // Defines image header
    const char magic_number_1 = 'P';
    const char magic_number_2 = '6';
    const char end_of_header = '\n';

    // Writes header
    put_byte(magic_number_1, output);
    put_byte(magic_number_2, output);
    put_byte('\n', output);
    fprintf(output, "%"PRI_COORD" %"PRI_COORD"\n", width, height);
    fprintf(output, "%d", max_val);
    put_byte(end_of_header, output);

    size_t pixels_n = width*height;
    for (size_t i=0; i<pixels_n; i++) {
        put_pixel(image[i], output);
    }
}

/* ---------- Input routines ---------- */

// This struct "saves" the entire state about the input
typedef struct {
    FILE *input_file;
    char input_buffer[MAX_LINE_LEN];
    int  input_line_i;
    char *input_tokens;
    char *last_token;
    int  input_token_i;
} input_control_t;

char *get_next_line(input_control_t *ic, bool accept_eof) {
    // Gets the next line into buffer
    ic->input_line_i++;
    char *next_line = fgets(ic->input_buffer, MAX_LINE_LEN, ic->input_file);
    ic->input_tokens = next_line;
    ic->input_token_i = 0;
    // If we got a NULL pointer, it's either an error or the end-of-file
    if (next_line == NULL) {
        if (ferror(ic->input_file) != 0) {
            fprintf(stderr, "error reading from input stream\n");
            exit(EXIT_FAILURE);
        }
        if (accept_eof) {
            return NULL; // We reached the end-of-file
        }
        else {
            fprintf(stderr, "line %d: unexpected end of file!\n", ic->input_line_i);
            exit(EXIT_FAILURE);
        }
    }
    // Checks that the string contains a newline
    if (strchr(ic->input_buffer, '\n') != NULL) {
        return ic->input_buffer;
    }
    // ...if it doesn't, either we reached the end of non-newline terminated file
    if (feof(ic->input_file)) {
        return ic->input_buffer;
    }
    // ...or the line was too long to fit in the buffer
    fprintf(stderr, "line %d: line too long!\n", ic->input_line_i);
    exit(EXIT_FAILURE);
}

char *get_next_token(input_control_t *ic) {
    if (ic->input_token_i == 0) {
        ic->last_token = strtok(ic->input_tokens, parameter_delimiters);
    }
    else {
        ic->last_token = strtok(NULL, parameter_delimiters);
    }
    if (ic->last_token == NULL) {
        fprintf(stderr, "line %d: too few parameters / unexpected end of line!\n", ic->input_line_i);
        exit(EXIT_FAILURE);
    }
    ic->input_token_i++;
    return ic->last_token;
}

void ensure_end_of_line(input_control_t *ic) {
    if (ic->input_token_i == 0) {
        ic->last_token = strtok(ic->input_tokens, parameter_delimiters);
    }
    else {
        ic->last_token = strtok(NULL, parameter_delimiters);
    }
    if (ic->last_token != NULL) {
        fprintf(stderr, "line %d: too many parameters (expected %d)!\n",
                ic->input_line_i, ic->input_token_i);
        exit(EXIT_FAILURE);
    }
}

long to_integer(const char *str, const input_control_t *ic) {
    char *not_number_ptr;
    long result = strtol(str, &not_number_ptr, 10);
    if (*not_number_ptr != '\0') {
        fprintf(stderr, "line %d, parameter %d: expected integer!",
                ic->input_line_i, ic->input_token_i);
        exit(EXIT_FAILURE);
    }
    return result;
}

double to_decimal(const char *str, const input_control_t *ic) {
    char *not_number_ptr;
    double result = strtod(str, &not_number_ptr);
    if (*not_number_ptr != '\0') {
        fprintf(stderr, "line %d, parameter %d: expected decimal!",
                ic->input_line_i, ic->input_token_i);
        exit(EXIT_FAILURE);
    }
    return result;
}

/* ---------- Drawing/model routines ---------- */

void clear_image(pixel_t *image, size_t pixels_n, pixel_t color) {
    //
    // Complete a funcao
    //
}

void draw_line(pixel_t *image, coord_t w, coord_t h, coord_t x0, coord_t y0,
               coord_t x1, coord_t y1, pixel_t color) {
    //
    // Complete a funcao
    //
}

void multiply_matrices(model_t *restrict left, const model_t *restrict right) {
    //
    // Complete a funcao
    //
}

void apply_transform(model_t *restrict points, const size_t points_n,
                     const model_t *restrict transform) {
    //
    // Complete a funcao
    //
}

/* ---------- Main function ---------- */

int main(int argc, char *argv[]) {

    if (argc != 3) {
        fprintf(stderr,
              "usage: draw_2d_model <input.dat> <output.ppm>\n"
              "       interprets the drawing instructions in the input file and renders\n"
              "       the output in the NETPBM PPM format into output.ppm\n");
        return EXIT_FAILURE;
    }

    const char *input_file_name  = argv[1];
    const char *output_file_name = argv[2];

    // Reads input file and parses its header
    input_control_t *ic = calloc(sizeof(input_control_t), 1);
    if (ic == NULL) {
        fprintf(stderr, "not enough memory!");
        return EXIT_FAILURE;
    }
    ic->input_file = fopen(input_file_name, "rt");
    if (ic->input_file == NULL) {
        fprintf(stderr, "error opening '%s'\n", input_file_name);
        return EXIT_FAILURE;
    }

    get_next_line(ic, false);
    if (strcmp(ic->input_buffer,  "EA979V3\n") != 0) {
        fprintf(stderr, "input file format not recognized!");
        return EXIT_FAILURE;
    }

    get_next_line(ic, false);
    const coord_t width  = to_integer(get_next_token(ic), ic);
    const coord_t height = to_integer(get_next_token(ic), ic);

    if (width<=0 || width>max_size || height<=0 || height>max_size) {
        fprintf(stderr, "input file has invalid image dimensions: must be >0 and <={MAX_SIZE}!");
        return EXIT_FAILURE;
    }

    // Creates transformation matrix, starting with identity
    model_t transform[] = { 1., 0., 0., 0., 1., 0., 0., 0., 1. },
            transform_acc[transforms_n];

    pixel_t *image = malloc(sizeof(pixel_t)*width*height);

    //
    // TODO! Inicialize as demais variaveis
    //


    // Main loop - interprets and renders drawing commands
    while (get_next_line(ic, true) != NULL) {

        char command = ic->input_buffer[0];
        ic->input_tokens++;

        switch (command) {

        //
        // TODO! Complete o codigo para os demais comandos
        //

        case 'm':
            for (int i=0; i<transforms_n; i++) {
                transform_acc[i] = to_decimal(get_next_token(ic), ic);
            }
            ensure_end_of_line(ic);
            multiply_matrices(transform, transform_acc);
        break;

        default:
            fprintf(stderr, "line %d: unrecognized command '%c'!", ic->input_line_i, command);
            return EXIT_FAILURE;
        }

    } // while

    // If we reached this point, everything went well - outputs rendered image file
    FILE *output_file = fopen(output_file_name, "wb");
    if (output_file == NULL) {
        fprintf(stderr, "error opening '%s'\n", output_file_name);
        return EXIT_FAILURE;
    }
    save_ppm(image, width, height, output_file);

    return EXIT_SUCCESS;
}
