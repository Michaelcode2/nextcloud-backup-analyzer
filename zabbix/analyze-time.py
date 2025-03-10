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
        #print(database)
        #print(first)
        if database == param2:
            allowed_days = int(lines[5])
            real_days = int(lines[4])
            if (allowed_days-real_days) < 0:
                print(real_days-allowed_days) # просрочено дней
            else:
                print(0)
            break
        line = reader.readline()
