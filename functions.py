
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
from os import listdir, path
import data as dt



def f_leer_archivo(param_archivo):
    param_archivo['Item'] = param_archivo['Item'].map(lambda x: str(x)[:-2])
    param_archivo['Item'] = param_archivo['Item'].str.upper()

    return param_archivo


def f_pip_size(param_ins):
    pips_oanda = dt.pips_oanda
    pips_oanda = pips_oanda.set_index('Item')
    pips_oanda = pips_oanda['PipLocation']
    int = pow(10 / 1, np.abs(pips_oanda[param_ins]))

    return int

def f_columnas_tiempos(param_data):
    param_data = dt.archivo
    param_data['Close Time'] = pd.to_datetime(param_data['Close Time'])
    param_data['Open Time'] = pd.to_datetime(param_data['Open Time'])
    param_data['tiempo'] = (param_data['Close Time'] - param_data['Open Time']).dt.seconds

    return param_data