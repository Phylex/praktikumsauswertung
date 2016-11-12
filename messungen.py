#!/usr/bin/python

###############################################################################
# Use:  This file is a objectifying the code allready written. It uses Objects
#       to make using the software easieer
# Author: Alexander Becker
###############################################################################

################################## imports ####################################
import json
import numpy as np
import matplotlib.pyplot as plt
import collections as col
###############################################################################
einheitenpraefixe = {-15:'f',-12:'p',-9:'n',-6:'micro',-5:'10^-5',-3:'m',-2:'c',-1:'d',0:'',2:'h',3:'k',6:'M',9:'G',12:'T',15:'Ex'}

def Create_Messdaten_tabellen(tabellenname,*arguments, vertline=False,horline=False,alignment='center'):
    """Creates a LaTeX table from the collected data and scales the table automatically
    horline produces horizontal lines between the different fields
    Vertline produces vertical lines between the columns"""
    alignmenttable = {'center':'c','left':'l','right':'r'}
    # first we need to calculate the neccesary formatstrings for the table
    if vertline:
        columnformatstring = '|'
    else:
        columnformatstring = ''
    for elem in arguments:
        if type(elem) is messung:
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
    for elem in arguments:
        if type(elem) is messung:
            if elem is arguments[-1]:
                tablefile.write(' '+str(elem.messgroesse)+' \\\\\n')
            else:
                tablefile.write(' '+str(elem.messgroesse)+' &')


    # In the second Row we Specify the the units
    for elem in arguments:
        if type(elem) is messung:
            if elem is arguments[-1]:
                tablefile.write(' ('+einheitenpraefixe[elem.groessenordnung]+elem.einheit+') \\\\\n' )
            else:
                tablefile.write(' ('+einheitenpraefixe[elem.groessenordnung]+elem.einheit+') &')

    # add a plitting line between head and body of the table
    tablefile.write(' \\hline\n')

    maxlength = 0
    for elem in arguments:
        if type(elem) is messung:
            if len(elem.messreihe) > maxlength:
                maxlength = len(elem.messreihe)

    # print the rest of the table
    for i in range(maxlength):
        for elem in arguments:
            if type(elem) is messung:
                if elem is arguments[-1]:
                    try:
                        tablefile.write(' '+str(elem.messreihe[i])+' \\\\\n') # TODO this could use expanding to feature Horizontal lines
                    except IndexError:
                        tablefile.write(' - \\\\\n')
                else:
                    try:
                        tablefile.write(' '+str(elem.messreihe[i])+' &')  # TODO this could use expanding to feature Horizontal lines
                    except IndexError:
                        tablefile.write(' - &')

    # we create the lower horizontal line
    if horline:
        tablefile.write(' \\hline\n')
    #write the last line of the file closing it of
    tablefile.write('\\end{tabular}')
    #now just close it
    tablefile.close()


class messung:
    """Represents a messreihe and its associated data such as statisticaly relevant data. It also provides Funktions to output that data and transform it into appropriate formats"""
    @staticmethod
    def calculate_gaussian_data(messreihe):
        """Calculates the mean, variance and std. deviation of a list of numbers"""
        std_dev = np.std(messreihe,ddof=1)
        var = np.var(messreihe)
        mean = np.mean(messreihe)
        return std_dev, var, mean

    @staticmethod
    def graph_width(measurement,overshute=0.2):
        """Determines the Interval generated to plot over from the given data"""
        span = max(measurement) - min(measurement)
        minimum = min(measurement) - overshute*span
        maximum = max(measurement) + overshute*span
        return np.linspace(minimum,maximum,2000)

    @staticmethod
    def gauss_funktion(x_werte,mittelwert,standardabweichung):
        """calculates the values of a gauss curve characterized by the deviation and mean for every value given in x_werte. returns an array"""
        return (1/(standardabweichung*2*np.pi)*np.exp(-(1/2)*((x_werte-mittelwert)/standardabweichung)**2))

    def __init__(self, messgroesse, messreihe, Formelzeichen, einheit, messgeraet=None, messfehler=None, groessenordnung=0):
        """Constructor; besides taking given arguments, it allso builds all the necessary stuff for a plotting and a table"""
        self.messreihe = messreihe
        self.messgroesse = messgroesse
        self.Formelzeichen = Formelzeichen
        self.messgeraet = messgeraet
        self.messfehler = messfehler
        self.groessenordnung = groessenordnung
        self.einheit = einheit
        self.std_dev, self.var, self.mean = self.calculate_gaussian_data(self.messreihe)
        self.plot = col.namedtuple('plot', 'gauss, hist')
        self.plot.gauss = col.namedtuple('gauss' ,'function, x_values, color, label, linestyle')
        self.plot.gauss.x_values = self.graph_width(self.messreihe)
        self.plot.gauss.function= self.gauss_funktion(self.plot.gauss.x_values, self.mean, self.std_dev)
        self.plot.gauss.color = 'blue'
        self.plot.linestyle = '-'
        self.plot.hist = col.namedtuple('hist', 'bins, align, log, color, label')
        self.plot.hist.bins = 20
        self.plot.hist.align = 'mid'
        self.plot.hist.log = False
        self.plot.hist.color = 'green'
        if type(messgroesse) == str:
            self.plot.hist.label = messgroesse
            self.plot.gauss.label = 'Gaussian curve of '+messgroesse
        else:
            self.plot.hist.label = None
            self.plot.gauss.label = None

    # Seters and getters from here on
    @classmethod
    def set_messung_properties(**kwargs):
        """Sets the general properties of the messung"""
        for kw in kwargs.keys():
            if str(kw) == 'messreihe':
                self.messreihe = kwargs[kw]
            elif str(kw) == 'messgroesse':
                self.messreihe = kwargs[kw]
            elif str(kw) == 'color':
                self.messgeraet = kwargs[kw]
            elif str(kw) == 'label':
                self.messfehler = kwargs[kw]
            elif str(kw) == 'Formelzeichen':
                self.Formelzeichen = kwargs[kw]
            elif str(kw) == 'groessenordnung':
                self.groessenordnung = kwargs[kw]

    @classmethod
    def set_hist_parameter(**kwargs):
        """Sets the parameters for the histogram of the measurement"""
        for kw in kwargs.keys():
            if str(kw) == 'bins':
                self.plot.hist.bins = kwargs[kw]
            elif str(kw) == 'align':
                self.plot.hist.align = kwargs[kw]
            elif str(kw) == 'color':
                self.plot.hist.log = kwargs[kw]
            elif str(kw) == 'label':
                self.plot.hist.label = kwargs[kw]
            elif str(kw) == 'log':
                self.plot.hist.log = kwargs[kw]

    @classmethod
    def set_gauss_parameter(**kwargs):
        """Set the parameters for the plot of the gauss-funktion"""
        for kw in kwargs.keys():
            if str(kw) == 'relwidth':
                self.plot.gauss.x_values = graph_width(self.messreihe,kwargs[kw])
            elif str(kw) == 'linestyle':
                self.plot.gauss.linestyle = kwargs[kw]
            elif str(kw) == 'color':
                self.plot.gauss.color = kwargs[kw]
            elif str(kw) == 'label':
                self.plot.gauss.label = kwargs[kw]

