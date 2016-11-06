#!/usr/bin/python2
 
import __future__
import sys
import auswertung as au
import numpy as np
import matplotlib.pyplot as plt
import json


if __name__ == '__main__':
    data_from_experiment = au.open_json_file(sys.argv[1])
    if data_from_experiment is None:
        print ("The given file isnot valid.")
        quit()
    globals().update(data_from_experiment)
    
    messungen = au.pivot_table(messungen)
   
    tmpmessung = [[]]
  
    for i in range(len(messungen[0])-1):
        tmpmessung[0].append((messungen[0][i+1]-messungen[0][i])) 
    for i in range(len(messungen)-1):
        del messungen[i+1][0]
    for i in range(len(messungen)-1):
        tmpmessung.append(messungen[i+1])
    
    messungen = au.pivot_table(tmpmessung)
   
    filename = sys.argv[1]+'modified'
    with open(filename,'w') as file:
        json.dump({'Name_of_experiment':Name_of_experiment,'messungen':messungen,'messgroessen':messgroessen,'metadaten':metadaten},file)
