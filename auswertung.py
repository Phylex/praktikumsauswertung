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
import dateutil.parser as dateparser
#================================= Statical Stuff =============================

#================================= Funktionen =================================
#------------------------------------------------------------------------------
# This funktion trys to decode a file given as first argument on the commandline and of that fails it 
# prompts for a valid filepath
def open_json_file(filepath):
    try:
        Experimentfile = open(filepath, 'r')
    except FileNotFoundError:
        file = None
        while (file != 'open'):
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

#------------------------------------------------------------------------------
# This Funktion turns a list of lists where the inner list is a row into a list of lists where the inner lists 
# is the column
def pivot_table(table):
    return [[row[i[0]] for row in table] for i in enumerate(table[0])]

#------------------------------------------------------------------------------
def transformcolumns_to_numpy_array(table):
    transformed_table = np.array([])
    for column in table:
        try:
            np.array(column,dtype=np.float64)
            np.append(transformed_table,colums)
        except:
            np.append(transformed_table,np.array([]))
    return transformed_table
#------------------------------------------------------------------------------
def calculate_basicstatistics(table):
    basicstats = np.array([])
    for coulumn in table:
        standardabweichung = np.std(column)
        varianz = np.var(column)
        mittelwert = np.mean(column)
        np.append([mittelwert,varianz,standardabweichung],basicstats)

#------------------------------------------------------------------------------
################################## Main Code ##################################
# this can also be used as a module so we have to put the main code in here 
if __name__ == "__main__":
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
    #now we heve the local variables we will split the messungen tabelle into the columns
    # we will have to pivot the table to do simple statistical methods on it 
    messdatenpivoted = pivot_table(messungen)
    # now the messdaten are pivoted we have to convert the time from a string into something useful
    # we split the list of Messungen into the data and the timestamp so we can convert the rest of the
    # values into a numpy array so now messzeiten and messdatenpivoted exist
    messzeiten = []
    for timestamp in messdatenpivoted[-1]:
        timeobject = dateparser.parse(timestamp)
        messzeiten.append(timeobject)
    del messdatenpivoted[-1]
    #DEBUG
    print (messzeiten)
    print (messdatenpivoted)
    # we rename the messungen and 
    messungen = transformcolumns_to_numpy_array(messdatenpivoted)
    print (messungen)