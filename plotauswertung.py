# coding: utf-8

###############################################################################
# This Program Creates plots form the inputted data
# Author: Alexander Becker
#Creation Date: 01.11.15
###############################################################################

#================================= Imports ====================================
import sys
import auswertung as au
import numpy as np
import matplotlib.pyplot as plt

#================================= Formatting help and other static data ======

einheitenpraefixe = {-15:'f',-12:'p',-9:'n',-6:'micro',-3:'m',-2:'c',-1:'d',0:'',2:'h',3:'k',6:'M',9:'G',12:'T',15:'Ex'}

################################## Main Program ###############################
data = au.open_json_file(sys,argv[1])
Name_of_experiment = sys.argv[2]
# here if the file returned is not a json we terminate the program
if data_from_experiment is None:
    print ("The given file isnot valid.")
    quit()

# the variables are made accessable and messungen is transformed so that it is
# easyer to calculate the statistical data
locals().update(data)
messungen = au.transform_data_into_usable_format(messungen)
locals().update(messungen)

#the next lines are only needed in the Elastizitaetsexperiment 
#messungen = messungen[1:]
#tmpmessungen = []
#for messung in messungen:
#    for elem in messung:
#        tmpmessungen.append(elem)
#tmpmessungen = [tmpmessungen]
#messungen = np.array(tmpmessungen)
#messgroessen = [['Periodendauer x 10','s','Stoppuhr',0,0.2]]
##################################

#we calculate the basical Statistical values
stats = au.calculate_basicstatistics(messungen)

#we calculate the gaussian Curve from the data
gaussianXvalues = []
for i,elem in enumerate(stats):
    gaussianXvalues.append(au.graph_width(messungen[i]))
gaussianCurve = []
for i,elem in enumerate(stats):
    gaussianCurve.append(au.gauss_funktion(gaussianXvalues[i],stats[i][0],stats[i][1]))

# Now we Plot the whole thing out nicely
for i, elem in enumerate(stats):
    figure, axis1 = plt.subplots()
    axis1.set_ylabel('Quantity of measurements')
    axis1.hist(messungen[i],color = 'g')
    axis1.set_xlabel(messgroessen[i][0]+' ('+einheitenpraefixe[messgroessen[i][3]]+messgroessen[i][1]+')')
    plt.title(Name_of_experiment)
    for ti in axis1.get_yticklabels():
        ti.set_color('g')
    
    axis2 = axis1.twinx()
    axis2.plot(gaussianXvalues[i],gaussianCurve[i])
    axis2.set_ylabel('Value of Gauss Curve')
    axis2.grid()
    for ti in axis2.get_yticklabels():
        ti.set_color('b')
    figure.savefig(experimentfile+'plots'+str(i))
