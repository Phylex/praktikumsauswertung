###############################################################################
# Use: Dieses File nimmt ein oeffnet ein Experimentenfile und zerlegt es in 
# Author: Alexander
#
#
#
#
###############################################################################

#================================= Imports ====================================
import json
import numpy as np
import sys

#================================= Statical Stuff =============================

#================================= Funktionen =================================
def open_json_file(filepath):
    try:
        open(filepath, 'r')
    except FileNotFoundError:
        file = None
        while file != 'open':
            try:
                file = input('Bitte geben Sie den Pfad zur Datei an:')
                Experimentfile = open(file, 'r')
                file = 'open'
            except FileNotFoundError:
                file = None
    # from here on we regard the file as open
    # we now will atempt to read the file assuming it is a json file
    try:
         return json.load(Experimentfile)
    except JSONDecodeError:
        print ('Das angegebene File ist kein JSON encoded File')
        return None

################################## Main Code ##################################
# this can also be used as a module so we have to put the main code in here 
if __name__ is '__main__':
    data_from_experiment = open_json_file(sys.argv[1])
    # here if the file returned is not a json we terminate the program
    if data_from_experiment is None:
        quit()
    # we now have parsed a valid JSON file and are going to add the variables to the locals()
    locals().update(data_from_experiment)
    # if the file imported is a file built by the Messung.py we where will be following variables
        #messungen
        #messgroessen
        #metadaten

