import __future__
import kafe
from kafe import function_library

einheitenpraefixe = {-15:'f',-12:'p',-9:'n',-6:'micro',-5:'10^-5',-3:'m',-2:'c',-1:'d',0:'',2:'h',3:'k',6:'M',9:'G',12:'T',15:'Ex'}

#------------------------------------------------------------------------------
# This funktion prepares the data given by the messen.py program
# we will have the job of Createing a Dataset and then returning it
def transform_data_into_kafe_Dataset_linear_regression(messgroessen, messungen, experiment_Name):
    if len(messgroessen) > 2 or len(messgroessen) > 2:
        return None
    else:
        kafedata = kafe.dataset.Dataset(data=[elem for elem in messungen], axis_labels=[messgroesse[0] for messgroesse in messgroessen], axis_units=[ einheitenpraefixe[messgroesse[3]]+messgroesse[1] for messgroesse in messgroessen],title = experiment_Name)
        print (kafedata)
        for i, elem in enumerate(messgroessen):
            kafedata.add_error_source(i,'simple', elem[-1])
        return kafedata

#------------------------------------------------------------------------------
# This Funktion will generate a fit object from the dataset built by the fun-
# ction above the fitting funktion defaults to a 2 parameter linear fit
def build_kafe_fit_and_plot_object(kafedataset,fitfunktion=kafe.function_library.linear_2par):
    kafefit = kafe.Fit(kafedataset,fitfunktion)
    kafefit.do_fit()
    kafeplot = kafe.Plot(kafefit)
    kafeplot.plot_all()
    return [kafefit,kafeplot]
