#!/bin/bash

# Descomente estas linhas se estiver desenvolvendo em C
# gcc draw_2d_model.c -o draw_2d_model -std=c99 -lm -Wall
# ./draw_2d_model test_all_commands.dat test_all_commands.ppm
# ./draw_2d_model test_defaults.dat     test_defaults.ppm
# ./draw_2d_model test_transforms.dat   test_transforms.ppm

# Descomente estas linhas se estiver desenvolvendo em Python
# python3 draw_2d_model.py test_all_commands.dat test_all_commands.ppm
# python3 draw_2d_model.py test_defaults.dat     test_defaults.ppm
# python3 draw_2d_model.py test_transforms.dat   test_transforms.ppm

for file in test_all_commands test_defaults test_transforms; do
    if [ -s "${file}.ppm" ]; then
        diff -q "${file}.ppm" "${file}-ref.ppm"
        if [ "$?" == "0" ]; then
            rm -f "${file}-diff.ppm"
        else
            # In systems that have no pamarith, change for:
            # pnmarith -difference "${file}.ppm" "${file}-ref.ppm" > "${file}-diff.ppm"
            pamarith -xor "${file}.ppm" "${file}-ref.ppm" > "${file}-diff.ppm"
        fi
    fi
done
