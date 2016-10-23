metadaten = [['Messgroesse','Bitte geben Sie die Messgroesse (z.B. Spannug, Strom...) an: ','str'],['Einheit','Bitte geben Sie die Einheit der Messgroesse an (Nur SI einheit ohne Vorfaktor) an : ','str'],['Messgeraet','Bitte geben Sie das Messgeraet an: ','str'],['Messbereich','Bitte geben Sie den Messbereich als exponenten der Zehnerpotenz (z.B. \'-3\' fuer milli...) an: ','int'],['Tolleranz','Bitte geben Sie die Tolleranz in Einheiten des Messbereiches (z.B. \'0.1\' fuer eine toleranz von 0.1 mV mit \'-3\' im Messbereich) an: ','float']]

messgroessen = [['Temperatur','V','asdf',0,0.1],['Spannung','V','asdf2',0,0.1]]

messungen = [[1,222,34],[2,55,6],[3,8,99999],[4,150000000000,7]]

eingaberichtig = 'ist die eingabe richtig'

def input_with_type_check(printstring='',input_type='str',errormsg='Error',escape_sequence='ende'):
    read_data = input(printstring)
    if(read_data != escape_sequence):
        if input_type == 'str':
            try:
                return str(read_data)
            except ValueError:
                print (errormsg)
                return None
        elif input_type == 'int':
            try:
                return  int(read_data)
            except ValueError:
                print (errormsg)
                return None
        elif input_type == 'float':
            try:
                return float(read_data)
            except ValueError:
                print (errormsg)
                return None
    else:
        return escape_sequence

def max_length_of_column(table):
    maxlengthlist = []
    for i in range(len(table[0])):          # we take the first row of the table to be the width
        lengthlist = []                     # This list holds the length of all the elements of a column
        for row in table:
            lengthlist.append(len(str(row[i])))
        maxlengthlist.append(max(lengthlist))
    return maxlengthlist
# We now have to print a table that expanfds in both the horizontal and vertical depending on the size of the collected data sets
# first we print the Experiment information every messgroessen - Parameter gets a line.
#print ('\n\nErfasste Daten:')
#print ('================================================================================\n')
## print header for the table from the data in messgroessen:
## for the correct formatting we have to determin the max size of the field:
#maxlengthlist = [7]                  # This list holds the max length of each column
#messgroessenindex = 0               # This is simply for keeping track of the number
## add the length of the fist column 
## we now do the stringlength analysis
#for messgroesse in messgroessen:
#    lengthlist = []                     # This list holds the length of all the elements of a column
#    lengthlist.append(len(messgroesse[0]))
#    for messung in messungen:
#        lengthlist.append(len(str(messung[messgroessenindex])))
#    maxlengthlist.append(max(lengthlist))
#    messgroessenindex += 1
#print (maxlengthlist)
#
## Now we print the first line with delimiters
#print ('Messung'.rjust(maxlengthlist[0]+1),end='|')
#for i in range(len(messgroessen)):
#    print (messgroessen[i][0].rjust(maxlengthlist[i+1]+1),end='|')
#print ('')
## and now the data with fitting delimiters
#for messung in messungen:
#    for i in range(len(messung)):
#        print (str(messung[i]).rjust(maxlengthlist[i]+1),end='|')
#    print ('')
print ('\n\nErfasste Daten:')
print ('================================================================================\n')
# now we build a printable table
tabelle = [['Messung']]
for messgroesse in messgroessen:
    tabelle[0].append(messgroesse[0])
for messung in messungen:
    tabelle.append(messung)
#determin the longeset string in the table for width adjustment
maxlength = max_length_of_column(tabelle)
# print the table
for row in tabelle:
    for i in range(len(messgroessen)+1):
        print (str(row[i]).rjust(maxlength[i]+1),end='|')
    print ('')
