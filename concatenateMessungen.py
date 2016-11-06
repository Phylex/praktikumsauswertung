#!/usr/bin/python2

import __future__
import sys
import auswertung as au
import numpy as np
import matplotlib.pyplot as plt
import json


if __name__ == '__main__':
    data_from_experiment1 = au.open_json_file(sys.argv[1])
    if data_from_experiment1 is None:
        print ("The given file isnot valid.")
        quit()
    data_from_experiment2 = au.open_json_file(sys.argv[2])
    if data_from_experiment2 is None:
        print ("The given file isnot valid.")
        quit()
    messungen1 = data_from_experiment1['messungen']
    messungen2 = data_from_experiment2['messungen']
    messgroessen = data_from_experiment1['messgroessen']
    metadaten = data_from_experiment1['metadaten']
    Name_of_experiment = data_from_experiment1['Name_of_experiment']
   
    for elem in messungen2:
        messungen1.append(elem)

    filename = sys.argv[1]+'modified'
    with open(filename,'w') as file:
        json.dump({'Name_of_experiment':Name_of_experiment,'messungen':messungen1,'messgroessen':messgroessen,'metadaten':metadaten},file)
