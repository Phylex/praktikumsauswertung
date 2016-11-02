###############################################################################
# This Program is a small utility to generate tables from the data provided
# by the experiments of the P1
# Author: Alexander Becker
# Date of creation 30.10.16
###############################################################################

#================================= imports ====================================
import json

#================================= Funktionen =================================

#------------------------------------------------------------------------------
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
    tablefile = open(tabellenname, 'w')
    # we write the first line specifing the table environment and setting the format
    tablefile.write('\\begin{tabular}{'+columnformatstring+'}\n')
    if horline:
        tablefile.write(' \\hline\n')
    # print the first row of the table
    for elem in messgroessen:
        if elem is messgroessen[-1]:
            tablefile.write(' '+elem[0]+'\\\\\n') # TODO this could use expanding to feature Horizontal lines
        else:
            tablefile.write(elem[0]+' &')  # TODO this could use expanding to feature Horizontal lines
    # print the rest of the table
    for messung in messungen:
        for elem in messung:
            tablefile.write(' '+elem[0]+' &')  # TODO this could use expanding to feature Horizontal lines
            if elem is messung[-1]:
                tablefile.write(' '+elem[0]+'\\\\\n') # TODO this could use expanding to feature Horizontal lines
    # we create the lower horizontal line
    if horline:
        tablefile.write(' \\hline\n')
    #now just close it
    tablefile.close()

