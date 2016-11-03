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
import time
import csv
#================================= Statical Stuff =============================
einheitenpraefixe = {-15:'f',-12:'p',-9:'n',-6:'micro',-3:'m',-2:'c',-1:'d',0:'',2:'h',3:'k',6:'M',9:'G',12:'T',15:'Ex'}

# TODO write a dict for various latex commands so it can be printed into a file more easily

#================================= Funktionen =================================
#------------------------------------------------------------------------------
def open_picoscope_csv(filepath):
    '''opens the file given as argument, trys to read it and if it is valid it returns the data and metadata.
       else it returns None. if the filepath is wrong it asks for a valid one'''
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
    #from here on out we will regard the file as open
    #we now try to open the file and read it
    try:
        csvdata = csv.reader(Experimentfile)
        data = []
        for i,row in enumerate(csvdata):
            for j,column in enumerate(row):
                if i == 0:
                    data.append([])
                    data[j].append(column)
                elif i == 1:
                    data[j].append(column[1:-1]) 
                elif i == 2:
                    pass
                else:
                    data[j].append(float(column))
        Experimentfile.close()
        return data
    except:
        print ('Das angegebene File ist kein CSV encoded File')
        Experimentfile.close()
        return None

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
# calculates basic statistics (mittelwert varianz standardabweichung)
def calculate_basicstatistics(table):
    '''This funktion produces a list os lists with [[mittelwert,varianz,Standardabweichung]]'''
    basicstats = []
    for column in table:
        standardabweichung = np.std(column,ddof=1)
        varianz = np.var(column)
        mittelwert = np.mean(column)
        basicstats.append([mittelwert,varianz,standardabweichung])
    return basicstats

#------------------------------------------------------------------------------
# here the funktion plots a gaussian curve for the produced data
def gauss_funktion(x_werte,mittelwert,varianz):
        return (1/(np.sqrt(varianz)*2*np.pi)*np.exp(-(1/2)*((x_werte-mittelwert)/np.sqrt(varianz))**2))

#------------------------------------------------------------------------------
# this funktion adapts the left and right edge of the plotted area to the relavant of the data
def graph_width(measurement,overshute=0.2):
    span = max(measurement) - min(measurement)
    minimum = min(measurement) - overshute*span
    maximum = max(measurement) + overshute*span
    return np.linspace(minimum,maximum,2000)

#------------------------------------------------------------------------------
# this funktion creates a table from the data input
def Create_Messdaten_tabellen(tabellenname,messgroessen,messungen,vertline=False,horline=False,alignment='center'):
    alignmenttable = {'center':'c','left':'l','right':'r'}
    # first we need to calculate the neccesary formatstrings for the table
    if vertline:
        columnformatstring = '| '
    else:
        columnformatstring = ''
    for elem in messgroessen:
        columnformatstring += ' '+alignmenttable[alignment]
        if vertline:
            columnformatstring +=' |'
    # now we open the file start printing to it.
    tablefile = open(tabellenname+'.tex', 'w')
    # we write the first line specifing the table environment and setting the format
    tablefile.write('\\begin{tabular}{'+columnformatstring+'}\n')
    if horline:
        tablefile.write(' \\hline\n')
    # print the first row of the table
    for messgroesse in messgroessen:
        if messgroesse is messgroessen[-1]:
            tablefile.write(' '+str(messgroesse[0])+' \\\\\n') # TODO this could use expanding to feature Horizontal lines
        else:
            tablefile.write(' '+str(messgroesse[0])+' &')  # TODO this could use expanding to feature Horizontal lines
    # add a plitting line between head and body of the table
    tablefile.write(' \\hline\n')
    # print the rest of the table
    for messung in messungen:
        for elem in messung:
            if elem is messung[-1]:
                tablefile.write(' '+str(elem)+' \\\\\n') # TODO this could use expanding to feature Horizontal lines
            else:
                tablefile.write(' '+str(elem)+' &')  # TODO this could use expanding to feature Horizontal lines
    # we create the lower horizontal line
    if horline:
        tablefile.write(' \\hline\n')
    #write the last line of the file closing it of
    tablefile.write('\\end{tabular}')
    #now just close it
    tablefile.close()


#------------------------------------------------------------------------------


################################## Main Code ##################################
# this can also be used as a module so we have to put the main code in here
if __name__ == "__main__":
#================================= file input =================================
    data_from_experiment = open_json_file(sys.argv[1])
    # here if the file returned is not a json we terminate the program
    if data_from_experiment is None:
        print ("The given file isnot valid.")
        quit()
#================================= formating foo ==============================
    # we now have parsed a valid JSON file and are going to add the variables to the locals()
    locals().update(data_from_experiment)
    transformed_measurements = transform_data_into_usable_format(messungen)
    # now we overwrite the old variables with the transformed ones
    locals().update(transformed_measurements)

#================================= statistical analysis =======================
    basicstats = calculate_basicstatistics(messungen)
    filename = time.strftime('%Y-%m-%d-%H%M-'+sys.argv[1]+'-Auswertung')
    with open(filename,'w') as file:
        json.dump({'statistical_data':basicstats},file)
