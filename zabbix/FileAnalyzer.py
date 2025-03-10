#!/usr/bin/env python3

import os
import glob
from datetime import datetime, date

def start_scandirs(folder):
    filestrings = []
    filestrings = scandirs(folder, filestrings)
    return filestrings

def scandirs(folder, filestrings):
    needpass = 0 #Необходимо пропустить чтение файлов.
    for f in os.scandir(folder):
        if f.is_file() & needpass == 0:
            needpass = 1
            #filestrings.append(f.path)
            #print(size)#Размер файла
        if f.is_dir():
            needpass = 0
            if f.name == 'Archives':
                continue
            if f.name[0] != '.':
                list_of_files = glob.glob(f.path + '/*.zip')  # * means all if need specific format then *.csv
                if list_of_files:
                    latest_file = max(list_of_files, key = os.path.getctime)  # get latest file created in folder
                    shortfilename = os.path.basename(latest_file)
                    size = os.path.getsize(latest_file)
                    timec = os.path.getctime(latest_file)
                    time = datetime.fromtimestamp(timec).strftime('%Y-%m-%d %H:%M:%S')
                    timedifference = datetime.now() - datetime.fromtimestamp(timec)
                    hours = timedifference.total_seconds() / 3600
                    hours = int(hours)
                    days = str(int(hours / 24))
                    count_mark_files = glob.glob(f.path + '/count.txt')
                    if len(count_mark_files) > 0:
                        #print('count file fount')
                        count_mark_file = count_mark_files[0]
                        with open(count_mark_file, 'r') as file:
                            try:
                                first_line = file.readline().rstrip()
                                m = first_line.index('=')
                                count = int(first_line[m+1:])
                            except:
                                count = 2
                    else:
                        count = 2
                        # time - реальное время файла
                        # days - количество дней с даты файла
                        # count - количество запрограммированных дней (периодичность). Получаем из файла count.txt
                    foldername = f.path.split('/')
                    if len(foldername) > 6:
                        foldername = foldername[-2] + '/' + foldername[-1]
                    else:
                        foldername = foldername[-1]
                    stringtext = foldername+'%'+shortfilename + '%' + str(size) + '%' + time + '%' + days + '%' + str(count) + '\n'
                    filestrings.append(stringtext)

                scandirs(f.path, filestrings)

    return filestrings

backup_folder = '/mnt/DBOWN//Backups'
folder = os.path.dirname(os.path.realpath(__file__))
BackupDataFile = folder + '/BackupData.txt'
#print(os.path.realpath(__file__))

filestrings = start_scandirs(backup_folder)
#print(filestrings)

with open(BackupDataFile, 'w+') as file:
    file.writelines(filestrings)
