# coding: utf-8

###############################################################################
# This Program Creates plots form the inputted data
# Author: Alexander Becker
#Creation Date: 01.11.15
###############################################################################

#================================= Imports ====================================
import __future__
import sys
import auswertung as au
import numpy as np
import matplotlib.pyplot as plt

#================================= Formatting help and other static data ======


################################## Main Program ###############################
if __name__ == '__main__':
    # import the data and do a small check
    au.import_experiment_data(sys.argv[1])
    if au.Name_of_experiment in globals():
        print (true)
        Name_of_experiment = au.Name_of_experiment
    else:
        Name_of_experiment = sys.argv[2]

    #we calculate the basical Statistical values
    stats = au.calculate_basicstatistics(au.messungen)

    #we calculate the gaussian Curve from the data
    gaussianXvalues = []
    for i,elem in enumerate(stats):
        gaussianXvalues.append(au.graph_width(au.messungen[i],overshute=0.5))
    gaussianCurve = []
    for i,elem in enumerate(stats):
        print (stats[i])
        gaussianCurve.append(au.gauss_funktion(gaussianXvalues[i],stats[i][0],stats[i][2]))

    # Now we Plot the whole thing out nicely
    for i, elem in enumerate(stats):
        figure, axis1 = plt.subplots()
        axis1.set_ylabel('Quantity of measurements')
        axis1.hist(au.messungen[i],color = 'g')
        axis1.set_xlabel(au.messgroessen[i][0]+' ('+au.einheitenpraefixe[au.messgroessen[i][3]]+au.messgroessen[i][1]+')')
        plt.title(Name_of_experiment)
        for ti in axis1.get_yticklabels():
            ti.set_color('g')

        axis2 = axis1.twinx()
        axis2.plot(gaussianXvalues[i],gaussianCurve[i])
        axis2.set_ylabel('Value of Gauss Curve')
        axis2.grid()
        for ti in axis2.get_yticklabels():
            ti.set_color('b')
        figure.savefig(sys.argv[1]+'plots'+str(i))
################################## ENDE #######################################
