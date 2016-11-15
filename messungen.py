#!/usr/bin/python
###############################################################################
# Use:  This file is a objectification of the code already written. It uses Objects
#       to make using the software easier
# Author: Alexander Becker
###############################################################################

################################## imports ####################################
import matplotlib.pyplot as plt
import numpy as np
import collections as col

################################## Static stuff ###############################
einheitenpraefixe = {-15: 'f', -12: 'p', -9: 'n', -6: 'micro', -5: '10^-5', -3: 'm', -2: 'c', -1: 'd', 0: '', 2: 'h',
                     3: 'k', 6: 'M', 9: 'G', 12: 'T', 15: 'Ex'}
###############################################################################

def create_messdaten_tabellen(tabellenname: str, *arguments, vertline=False, horline=False, alignment='center'):
    """Creates a LaTeX table from the collected data and scales the table automatically
    horline produces horizontal lines between the different fields
    Vertline produces vertical lines between the columns"""
    alignmenttable = {'center': 'c', 'left': 'l', 'right': 'r'}
    # first we need to calculate the neccesary formatstrings for the table
    if vertline:
        columnformatstring = '|'
    else:
        columnformatstring = ''
    for elem in arguments:
        if type(elem) is Messung:
            columnformatstring += ' ' + alignmenttable[alignment]
            if vertline:
                columnformatstring += ' |'

    # now we open the file start printing to it.
    tablefile = open(tabellenname + '.tex', 'w')

    # we write the first line specifing the table environment and setting the format
    tablefile.write('\\begin{tabular}{' + columnformatstring + '}\n')
    if horline:
        tablefile.write(' \\hline\n')

    # print the first row of the table
    for elem in arguments:
        if type(elem) is Messung:
            if elem is arguments[-1]:
                tablefile.write(' ' + str(elem.messgroesse) + ' \\\\\n')
            else:
                tablefile.write(' ' + str(elem.messgroesse) + ' &')

    # In the second Row we Specify the the units
    for elem in arguments:
        if type(elem) is Messung:
            if elem is arguments[-1]:
                tablefile.write(' (' + einheitenpraefixe[elem.groessenordnung] + elem.einheit + ') \\\\\n')
            else:
                tablefile.write(' (' + einheitenpraefixe[elem.groessenordnung] + elem.einheit + ') &')

    # add a plitting line between head and body of the table
    tablefile.write(' \\hline\n')

    maxlength = 0
    for elem in arguments:
        if type(elem) is Messung:
            if len(elem.messreihe) > maxlength:
                maxlength = len(elem.messreihe)

    # print the rest of the table
    for i in range(maxlength):
        for elem in arguments:
            if type(elem) is Messung:
                if elem is arguments[-1]:
                    try:
                        tablefile.write(' ' + str(elem.messreihe[i]) + ' \\\\\n')
                    except IndexError:
                        tablefile.write(' - \\\\\n')
                else:
                    try:
                        tablefile.write(' ' + str(elem.messreihe[i]) + ' &')
                    except IndexError:
                        tablefile.write(' - &')
        if horline:
            tablefile.write(' \\hline\n')
    # write the last line of the file ending it
    tablefile.write('\\end{tabular}')
    tablefile.close()


class Messung:
    """Represents a Messreihe and its associated data such as statistically relevant data. It also provides Function to\
    output that data and transform it into appropriate formats"""

    def __init__(self, experiment: str, messgroesse: str, messreihe: list, formelzeichen: str, einheit: str, messgeraet: str = None, messfehler: float = None,
                 groessenordnung: int = 0):
        """Constructor; besides taking given arguments, it allso builds all the necessary stuff for a plotting and \
        a table"""
        # we first costruct the named tuples we need for the object
        # the names of the fields are not allowed to be renamed, for they are used as keywords when passing the data to
        # the matplotlib funktions
        self.gaussstruct = col.namedtuple('gauss', ['ydata', 'xdata', 'color', 'label', 'linestyle'])
        self.histstruct = col.namedtuple('hist', ['bins', 'align', 'log', 'color', 'label'])
        self.plotstruct = col.namedtuple('plot', ['gauss', 'hist'])
        # now we add the relevant metadata to the object
        self.experiment = experiment
        self.messreihe = messreihe
        self.messgroesse = messgroesse
        self.formelzeichen = formelzeichen
        self.messgeraet = messgeraet
        self.messfehler = messfehler
        self.groessenordnung = groessenordnung
        self.einheit = einheit
        self.std_dev, self.var, self.mean = self.calculate_gaussian_data()
        # now the structs are filled and inserted into oneanother
        plotwidth = self.graph_width(self.messreihe, 0.3)
        gaussfunction = self.gauss_funktion(plotwidth, self.mean, self.std_dev)
        if type(messgroesse) == str:
            gauss = self.gaussstruct(gaussfunction, plotwidth, 'blue', 'Gaussian curve of ' + messgroesse, '-')
            hist = self.histstruct(20, 'mid', False, 'green', messgroesse)
        else:
            gauss = self.gaussstruct(gaussfunction, plotwidth, 'blue', '', '-')
            hist = self.histstruct(20, 'mid', False, 'green', '')
        self.plot = self.plotstruct(gauss, hist)

    @staticmethod
    def graph_width(measurement: list, overshoot: float = 0.2) -> np.array:
        """Determines the Interval generated to plot over from the given data"""
        span = max(measurement) - min(measurement)
        minimum = min(measurement) - overshoot * span
        maximum = max(measurement) + overshoot * span
        return np.linspace(minimum, maximum, 2000)

    def calculate_gaussian_data(self) -> tuple:
        """Calculates the mean, variance and std. deviation of a list of numbers"""
        std_dev = np.std(self.messreihe, ddof=1)
        var = np.var(self.messreihe)
        mean = np.mean(self.messreihe)
        return std_dev, var, mean

    @staticmethod
    def gauss_funktion(xwerte: np.array, mean: float, std_dev: float) -> np.array:
        """calculates the values of a gauss curve characterized by the deviation and mean for every value given in \
        x_werte. returns an array"""
        return 1 / (std_dev * 2 * np.pi) * np.exp(-(1 / 2) * ((xwerte - mean) / std_dev) ** 2)

    # Setters and getters from here on
    def set_messung_properties(self, **kwargs):
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
                self.formelzeichen = kwargs[kw]
            elif str(kw) == 'groessenordnung':
                self.groessenordnung = kwargs[kw]

    def set_hist_parameter(self, **kwargs):
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

    def set_gauss_parameter(self, **kwargs):
        """Set the parameters for the plot of the gauss-function"""
        for kw in kwargs.keys():
            if str(kw) == 'relwidth':
                self.plot.gauss.x_values = self.graph_width(self.messreihe, kwargs[kw])
            elif str(kw) == 'linestyle':
                self.plot.gauss.linestyle = kwargs[kw]
            elif str(kw) == 'color':
                self.plot.gauss.color = kwargs[kw]
            elif str(kw) == 'label':
                self.plot.gauss.label = kwargs[kw]

    # encoder and decoder for json
    def encodejson(self):
        """Encodes all the parts of the object into a dict, so it can be written into a JSON file by the json library"""
        gauss = []
        for i,value in enumerate(self.plot.gauss):
           gauss.append((self.plot.gauss._fields[i], value))
        hist = []
        for i,value in enumerate(self.plot.hist):
            hist.append((self.plot.hist._fields[i], value))
        gauss = dict(gauss)
        hist = dict(hist)
        object_serialisation = {'object': 'messung', 'experiment': self.experiment, 'messreihe': self.messreihe,
                                'messgroesse': self.messgroesse,
                                'formelzeichen': self.formelzeichen, 'messgeraet': self.messgeraet,
                                'messfehler': self.messfehler, 'groessenordnung': self.groessenordnung,
                                'einheit': self.einheit, 'gauss': gauss,
                                'hist': hist}
        return object_serialisation

    # plots the messung into the
    def plot_messung(self) -> plt.figure:
        figure = plt.figure()
        axis1 = figure.add_axes([0, 0, 1, 1])
        axis1.set_ylabel()
        axis1.hist(self.messreihe, self.plot.hist._asdict())
        axis1.set_xlabel(self.messgroesse+' ('+einheitenpraefixe[self.groessenordnung]+')')
        plt.title(self.experiment)
        for ti in axis1.get_yticklabels():
            ti.set_color(self.plot.hist.color)

        axis2 = axis1.twinx()
        axis2.plot(**self.plot.gauss._asdict())
        axis2.set_ylabel('Gaussian Curve')
        axis2.grid()
        for ti in axis2.get_yticklabels():
            ti.set_color(self.plot.gauss.color)
        return figure


def decodemessungenfromjson(messungsdict: dict) -> Messung:
    try:
        if messungsdict['object'] == 'messung':
            messungsobject = Messung(messungsdict['experiment'], messungsdict['messgroesse'], messungsdict['messreihe'],
                                     messungsdict['formelzeichen'], messungsdict['einheit'], messungsdict['messgeraet'],
                                     messungsdict['messfehler'], messungsdict['groessenordnung'])
            messungsobject.set_gauss_parameter(**messungsdict['gauss'])
            messungsobject.set_hist_parameter(**messungsdict['hist'])
            return messungsobject
        else:
            return None
    except KeyError:
        return None


def create_fit_from_messungen(xmessung: Messung ,ymessung: Messung = None) -> list:
    if ymessung != None:
        # We now do some checking for of the compatibility of the objects
        if len(xmessung.messreihe) != len(ymessung.messreihe):
            raise IndexError('Amount of measurements don\'t match in length')
        elif xmessung.experiment == ymessung.experiment:
            raise NameError('The measurements dont belung to the same Experiment')
        messreihenlist = []
        for i,value in enumerate(xmessung.messreihe):
           messreihenlist.append((value, ymessung.messreihe[i]))
        errortype = []
        if type(xmessung.messfehler) == float or xmessung.messfehler is None:
            errortype.append('simple')
        else:
            errortype.append('matrix')
        if type(ymessung.messfehler) == float or ymessung.messfehler is None:
            errortype.append('simple')
        else:
            errortype.append('matrix')
        return [{'data':[elem for elem in messreihenlist], 'axis_labels':[xmessung.messgroesse,ymessung.messgroesse],
                'axis_units': [einheitenpraefixe[xmessung.groessenordnung] + xmessung.messgroesse,
                               einheitenpraefixe[ymessung.groessenordnung] + ymessung.messgroesse],
                'title': xmessung.experiment}, {'error': [xmessung.messfehler,ymessung.messfehler],
                                                'errortype': errortype}]
    else:
        pass #TODO still need to code the variant of a single measurement encoding