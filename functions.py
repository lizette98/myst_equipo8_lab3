
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
    n = pow(10 / 1, np.abs(pips_oanda[param_ins]))

    return n


def f_columnas_tiempos(param_data):
    param_data = dt.archivo
    param_data['Profit'] = param_data['Profit'].str.replace(' ', '')
    param_data['Close Time'] = pd.to_datetime(param_data['Close Time'])
    param_data['Open Time'] = pd.to_datetime(param_data['Open Time'])
    #Nueva columna de tiempo transcurrido en segundos
    param_data['tiempo'] = (param_data['Close Time'] - param_data['Open Time']).dt.seconds
    param_data = param_data.rename(columns={'Price': 'Open Price', 'Price.1': 'Close Price'})
    return param_data


def f_columnas_pips(param_data):
    param_data['pips'] = 0
    for i in range(len(param_data)):
        n = f_pip_size(param_data['Item'].iloc[i])
        if param_data['Type'][i] == 'sell':
            param_data['pips'][i] = (param_data['Open Price'][i] - param_data['Close Price'][i]) * n

        else:
            param_data['pips'][i] = (param_data['Close Price'][i] - param_data['Open Price'][i]) * n
    param_data['pips_acm'] = param_data['pips'].cumsum()
    param_data['Profit'] = pd.to_numeric(param_data['Profit'])
    param_data['profit_acm'] = param_data['Profit'].cumsum()
    return param_data


def f_estadisticas_ba(param_data):

    df_1_tabla = pd.DataFrame({'Ops totales': [len(param_data['Ticket']), 'Operaciones totales'],
                               'Ganadoras': [len(param_data[param_data['Profit'] >= 0]), 'Operaciones ganadoras'],
                               'Ganadoras_c': [len(param_data[(param_data['Type'] == 'buy') & (param_data['Profit'] >= 0)]),
                                                   'Operaciones ganadoras de compra'],
                               'Ganadoras_v': [len(param_data[(param_data['Type'] == 'sell') & (param_data['Profit'] >= 0)]),
                                                   'Operaciones ganadoras de venta'],
                               'Perdedoras': [len(param_data[param_data['Profit'] < 0]), 'Operaciones perdedoras'],
                               'Perdedoras_c': [len(param_data[(param_data['Type'] == 'buy') & (param_data['Profit'] < 0)]),
                                                    'Operaciones perdedoras de compra'],
                               'Perdedoras_v': [len(param_data[(param_data['Type'] == 'sell') & (param_data['Profit'] < 0)]),
                                                    'Operaciones perdedoras de venta'],
                               'Mediana (Profit)': [param_data['Profit'].median(), 'Mediana de profit de operaciones'],
                               'Mediana (Pips)': [param_data['pips'].median(), 'Mediana de pips de operaciones'],
                               'r_efectividad': [len(param_data[param_data['Profit'] >= 0]) / len(param_data['Ticket']),
                                                 'Ganadoras Totales/Operaciones Totales'],
                               'r_proporcion': [len(param_data[param_data['Profit'] >= 0]) / len(param_data[param_data['Profit'] < 0]),
                                                'Ganadoras Totales/Perdedoras Totales'],
                               'r_efectividad_c': [len(param_data[(param_data['Type'] == 'buy') & (param_data['Profit'] >= 0)]) / len(param_data['Ticket']),
                                   'Ganadoras Compras/Operaciones Totales'],
                               'r_efectividad_v': [len(param_data[(param_data['Type'] == 'sell') & (param_data['Profit'] >= 0)]) / len(param_data['Ticket']),
                                   'Ganadoras Ventas/Operaciones Totales'],
                               }, index=['valor', 'descripcion']).transpose()

    tb1 = pd.DataFrame({i: len(param_data[param_data.Profit > 0][param_data.Item == i]) / len(param_data[param_data.Item == i])
                        for i in param_data.Item.unique()}, index=['rank']).transpose()

    convert_dict = {'valor': float}
    df_1_tabla = df_1_tabla.astype(convert_dict)

    df_1_ranking = (tb1 * 100).sort_values(by='rank', ascending=False).T.transpose()

    return {'df_1_tabla': df_1_tabla.copy(), 'df_1_ranking': df_1_ranking.copy()}
