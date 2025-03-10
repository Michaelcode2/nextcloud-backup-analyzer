#!/usr/bin/env python3

import os
import json
import subprocess

folder = os.path.dirname(os.path.realpath(__file__))
BackupDataFile = folder + '/BackupData.txt'

# Стартуем первый скрипт генерации файла для анализа
os.system(folder+'/FileAnalyzer.py')

with open(BackupDataFile, 'r') as reader:
    line = reader.readline()
    data = {}
    data["data"] = []
    while line != '':  # The EOF char is an empty string
        lines = line.split(sep='%')
        insert_line = lines[0]
        data["data"].append({
            "{#BACKUP}" : insert_line})
        #json.dumps(data)
        line = reader.readline()
    zabbix_data = json.dumps(data, skipkeys = True, ensure_ascii=False)
    print(zabbix_data)
