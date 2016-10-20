###############################################################################
# Use:  This program is used when an Experiment is run and the data is collec-
#       ted it lets the user input data and dumps it in a json file for further
#       analysis.
# Author: Alexander Becker (becker(dot)alexander42(at)gmail(dot)com)
# Version: 0.0
################################# Imports #####################################

import pandas as pd
import json
import datetime as time

################################# Version info ################################
version = 0.0

################################# User interface Strings ######################
eingabefehler = 'Keine gueltige eingabe'


################################# Useful static stuff #########################
# Here we can assign Units to the desired measurement that are automatically added if the measurement is found in the following table
bekannte_messgroessen = {'Spannung':'V','Strom':'A','Kraft':'N','Flussdichte':'B','Stromdichte':'A/m^2','Strecke':'m','Flaeche':'m^2','Zeit':'s','Lichtmenge':'lm'}

# Here we store the Metadata type that should be collected and a describing String that is printed to the user when prompted to enter the required data
# the allowed datatypes are specified in the third field and can be 'str' for string, 'int' for integer and 'float' for float
metadaten = [['Messgroesse','Bitte geben Sie die Messgroesse (z.B. Spannug, Strom...) an: ','str'],['Einheit','Bitte geben Sie die Einheit der Messgroesse an (Nur SI einheit ohne Vorfaktor) an : ','str'],['Messgeraet','Bitte geben Sie das Messgeraet an: ','str'],['Messbereich','Bitte geben Sie den Messbereich als exponenten der Zehnerpotenz (z.B. \'-3\' fuer milli...) an: ','int'],['Tolleranz','Bitte geben Sie die Tolleranz in Einheiten des Messbereiches (z.B. \'0.1\' fuer eine toleranz von 0.1 mV mit \'-3\' im Messbereich) an: ','float']]

################################# Functions ###################################
#------------------------------------------------------------------------------
def input_with_type_check(printstring='',type='str',errormsg='Error'):
    if type == 'str':
        try:
            return str(input(printstring))
        except ValueError:
            print (errormsg)
            return None
    elif type == 'int':
        try:
            return  int(input(printstring))
        except ValueError:
            print (errormsg)
            return None
    elif type == 'float':
        try:
            return float(input(printstring))
        except ValueError:
            print (errormsg)
            return None
#------------------------------------------------------------------------------

################################# Main code ###################################
print ("Sie haben ein neues Experiment begonnen.\n")
# TODO We still need to collect data about the experiment such as name of the experimentator date and time and so on

# Now before the exeriment we collect metadata about it and store it in a dict.
print ("Bitte geben Sie nun die zu messenden Groessen ein (z.B. Spannung, Strom ...)\n")
#Here we start to collect metadata (specified in the metadaten table) for the experiment 
# the Messgroessen is a list of lists that store the metadata for each column of mesurements
messgroessen = []
i = 0

# here we ask the user for the metadata specified in the metadaten list. we also Print the descriptive texts and check for type integrity
while i==0 or answer=='y' or answer == 'Y':
    aktuelle_messgroesse = []
    i = 0
    while i < len(metadaten):
        eingabe = input_with_type_check(metadaten[i][1],metadaten[i][2],eingabefehler)
        if eingabe is not None:
            aktuelle_messgroesse.append(eingabe)
            i += 1
        if(i==1):
            if aktuelle_messgroesse[0] in bekannte_messgroessen:
                aktuelle_messgroesse.append(bekannte_messgroessen[aktuelle_messgroesse[0]])
                i+=1
    messgroessen.append(aktuelle_messgroesse)
    del aktuelle_messgroesse
    answer = input("Soll eine weitere Messgroesse eingestellt werden(y/n):")
print (messgroessen)
print ('\n')

#Now we start to collect the data that is measured during the experiment
#herefor we create a numpy array to hold the data in
messungen = np.array(dtype = object)
aktuelle_messung = [None]
i = 0
while aktuelle_messung[-1] is not 'ende':
    # Initialise Variables
    j = 0
    aktuelle_messung = []
    print ('------------------------------')
    print ('%i. Messung: '%i)
    while j < len(metadaten):
        messung = input_with_type_check(messgroessen[j][1]+': ','float',eingabefehler)
        if messung is not None and messung is not 'ende':
            aktuelle_messung.append(messung)
            j += 1
        if messung is 'ende':
            aktuelle_messung.append(messung)
            break
    aktuelle_messung.append(time.datetime())
    messungen.append(aktuelle_messung)
    i += 1





