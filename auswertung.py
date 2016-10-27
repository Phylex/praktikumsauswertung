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
         data = json.load(Experimentfile)
         Experimentfile.close()
         return data
    except JSONDecodeError:
        print ('Das angegebene File ist kein JSON encoded File')
        Experimentfile.close()
        return None

#------------------------------------------------------------------------------
# This Funktion turns a list of lists where the inner list is a row into a list of lists where the inner lists 
# is the column
def pivot_table(table):
    return [[row[i[0]] for row in table] for i in enumerate(table[0])]

#------------------------------------------------------------------------------
def transformcolumns_to_numpy_array(table):
    for column in table:
        try:
            transformed_table = np.array(table)
        except ValueError:
            return None
    return transformed_table

#------------------------------------------------------------------------------

# Here we pivot the table, Split the table into measured data and timestamps and then transform the measured data into 
# numpy array format to use the ascociated funktions later on
def transform_data_into_usable_format(table):
    table_pivoted = pivot_table(table)
    timestamps = []
    for timestamp in table_pivoted[-1]:
        timestamps.append(dateparser.parse(timestamp))
    del table_pivoted[-1]
    new_table = transformcolumns_to_numpy_array(table_pivoted)
    return {'messungen':new_table,'timestamps':timestamps}

#------------------------------------------------------------------------------
def calculate_basicstatistics(table):
    basicstats = np.array([])
    for column in table:
        standardabweichung = np.std(column)
        varianz = np.var(column)
        mittelwert = np.mean(column)
        basicstats = np.append([mittelwert,varianz,standardabweichung],basicstats,axis=0)
    return basicstats

#------------------------------------------------------------------------------
################################## Main Code ##################################
# this can also be used as a module so we have to put the main code in here 
if __name__ == "__main__":
    data_from_experiment = open_json_file(sys.argv[1])
    # here if the file returned is not a json we terminate the program
    if data_from_experiment is None:
        quit()
    # we now have parsed a valid JSON file and are going to add the variables to the locals()
    # if the file imported is a file built by the Messung.py we where will be following variables
        #messungen
        #messgroessen
        #metadaten
    locals().update(data_from_experiment)
    transformed_measurements = transform_data_into_usable_format(messungen)
    basicstats = calculate_basicstatistics(transformed_measurements)
    print (transformed_measurements)
    print (basicstats)
