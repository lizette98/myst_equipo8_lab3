
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
    param_archivo['Item'] = param_archivo['Item'].str.lower()

    return param_archivo


def f_pip_size(param_ins):
    pips_oanda = dt.pips_oanda
    pips_oanda = pips_oanda.set_index('Item')
    pips_oanda = pips_oanda['PipLocation']
    int = pow(10 / 1, np.abs(pips_oanda[param_ins]))

    return int


def f_columnas_tiempos(param_data):
    param_data = dt.archivo
    #Convertir columnas a datetime
    param_data['Close Time'] = pd.to_datetime(param_data['Close Time'])
    param_data['Open Time'] = pd.to_datetime(param_data['Open Time'])
    #Nueva columna de tiempo transcurrido en segundos
    param_data['tiempo'] = (param_data['Close Time'] - param_data['Open Time']).dt.seconds
    param_data = param_data.rename(columns={'Price': 'Open Price', 'Price.1': 'Close Price'})
    return param_data


def f_columnas_pips(param_data):
    param_data = dt.archivo
    param_data['pips'] = 0
    for i in range(len(param_data)):
        n = f_pip_size(param_data['Item'].iloc[i])
        if param_data['Type'][i] == 'sell':
            param_data['pips'][i] = (param_data['OpenPrice'][i] - param_data['ClosePrice'][i]) * n

        else:
            param_data['pips'][i] = (param_data['ClosePrice'][i] - param_data['OpenPrice'][i]) * n
    param_data['pips_acm'] = param_data['pips'].cumsum()
    param_data['profit_acm'] = param_data['Profit'].cumsum()
    return param_data
