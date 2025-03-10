#!/usr/bin/env python3

import os
from sys import argv

folder = os.path.dirname(os.path.realpath(__file__))
BackupDataFile = folder + '/BackupData.txt'

param1, param2 = argv

with open(BackupDataFile, 'r') as reader:
    line = reader.readline()
    while line != '':  # The EOF char is an empty string
        lines = line.split(sep='%')
        database = lines[0]
        if database == param2:
            print_line = lines[2]
            print(print_line)
            break
        line = reader.readline()
