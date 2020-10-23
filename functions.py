
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

# ---------- 1. ESTADISTICA DESCRIPTIVA


def f_leer_archivo(param_archivo):
    """
    Funcion para leer el archivo de historial de cada cuenta.

    Parameters
    ----------
    param_archivo: DataFrame
            Dataframe de historial con informacion del trading

    Returns
    -------
    param_archivo: DataFrame
            Dataframe de historial con informacion del trading
    """
    param_archivo['Item'] = param_archivo['Item'].map(lambda x: str(x)[:-2])
    param_archivo['Item'] = param_archivo['Item'].str.lower()

    return param_archivo


def f_pip_size(param_ins):
    """
    Funcion para obtener el número multiplicador para expresar la diferencia de precios en pips.

    Parameters
    ----------
    param_ins: str
            Instrumento para asociarse al multiplicador de pips que le corresponde

    Returns
    -------
    n: int
            Multiplicador de pips que le corresponde al instrumento.
    """
    pips_oanda = dt.pips_oanda
    pips_oanda = pips_oanda.set_index('Item')
    pips_oanda = pips_oanda['PipLocation']
    n = pow(10 / 1, np.abs(pips_oanda[param_ins]))

    return n


def f_columnas_tiempos(param_data):
    """
    Funcion para agregar mas columnas de transformaciones de tiempo.

    Parameters
    ----------
    param_data: DataFrame
            DataFrame que contiene la informacion de las operaciones en oanda.

    Returns
    -------
    param_data: DataFrame
            Dataframe inicial, ahora con la columna del tiempo que duro la transaccion en segundos.
    """
    param_data['Profit'] = param_data['Profit'].str.replace(' ', '')
    param_data['Close Time'] = pd.to_datetime(param_data['Close Time'])
    param_data['Open Time'] = pd.to_datetime(param_data['Open Time'])
    param_data = param_data.rename(columns={'Close Time': 'CloseTime', 'Open Time': 'OpenTime'})
    #Nueva columna de tiempo transcurrido en segundos
    param_data['tiempo'] = (param_data['CloseTime'] - param_data['OpenTime']).dt.seconds
    param_data = param_data.rename(columns={'Price': 'OpenPrice', 'Price.1': 'ClosePrice'})
    return param_data


def f_columnas_pips(param_data):
    """
    Funcion para agregar mas columnas de transformaciones de pips.

    Parameters
    ----------
    param_data: DataFrame
            DataFrame que contiene la informacion de las operaciones en oanda.

    Returns
    -------
    param_data: DataFrame
            Dataframe anterior, ahora con las columnas de pips resultantes de cada operacion,
            valor acumulado de pips y valor acumulado de la columna profit.
    """
    param_data['pips'] = 0
    for i in range(len(param_data)):
        n = f_pip_size(param_data['Item'].iloc[i])
        if param_data['Type'][i] == 'sell':
            param_data['pips'][i] = (param_data['OpenPrice'][i] - param_data['ClosePrice'][i]) * n

        else:
            param_data['pips'][i] = (param_data['ClosePrice'][i] - param_data['OpenPrice'][i]) * n
    param_data['pips_acm'] = param_data['pips'].cumsum()
    param_data['Profit'] = pd.to_numeric(param_data['Profit'])
    param_data['profit_acm'] = param_data['Profit'].cumsum()
    return param_data


def f_estadisticas_ba(param_data):
    """
    Funcion para calcular estadisticas basicas y ranking por instrumentos.

    Parameters
    ----------
    param_data: DataFrame
            DataFrame que contiene la informacion de las operaciones en oanda actualizado.

    Returns
    -------
    evolucion_capital: dict
            Diccionario con las llaves 'df_1_tabla' y 'df_1_ranking'. Ambas son DataFrame.

    df_1_tabla:
            Dataframe con medida, valor y descripcion de las operaciones registadas.

    df_1_ranking:
            Dataframe con el instrumento y el ratio de efectividad de las operaciones realizadas.
    """

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


# ---------- 2. METRICAS DE ATRIBUCION AL DESEMPEÑO

# 2.1 Evolucion de capital en la cuenta de trading
def f_profit_acm_d(param_data):
    """
    Funcion para agregar columna de evolución de capital.

    Parameters
    ----------
    param_data: DataFrame
            DataFrame que contiene la informacion de las operaciones en oanda actualizado.

    Returns
    -------
    param_data: DataFrame
            Dataframe actualizado con columna de evolución de capital inicializada con $100,000 Usd
            y se suma las ganancias o perdidas de la columna 'profit_acm'.
    """

    # Se forma una nueva columna inicializada en $100,000 donde se le suma/resta el profit acumulado
    param_data['profit_acm_d'] = 100000 + param_data.profit_acm

    return param_data.copy()

def f_evolucion_capital(param_data):
    """
    Funcion para agregar mas columnas de transformaciones de tiempo.

    Parameters
    ----------
    param_data: DataFrame
            DataFrame del historico de operaciones.

    Returns
    -------
    df_profit_diario: DataFrame
            Dataframe con tres columnas:
            1. timestamp: contiene las fechas dia a dia durante el priodo que se hizo trading.
            2. profit_d: profit por dia por cada dia de todos los contenidos en el periodo que se hizo trading.
            3. profit_acm_d: profit acumulado diario de la cuenta de capital.
    """

    # Agregar normalize a closetime
    diario = pd.date_range(param_data.CloseTime.min(), param_data.CloseTime.max()).normalize()

    # convertir a dataframe las fechas diarias
    fechas = pd.DataFrame({'timestamp': diario})

    # Agregar normalize a groupby
    groups = param_data.groupby(pd.DatetimeIndex(param_data['CloseTime']).normalize())

    profit = groups['Profit'].sum()
    # convertir los profits diarios a dataframe
    profit_diario = pd.DataFrame({'profit_d': [profit[i] if i in profit.index else 0 for i in diario]})
    profit_acm = np.cumsum(profit_diario) + 100000
    # juntar en un solo dataframe los dos dataframes anteriores fechas y profits diarios
    f_p1 = pd.merge(fechas, profit_diario, left_index=True, right_index=True)
    # juntar el dataframe anterior de los dos df con los profits acumulados
    df_profit_diario1 = pd.merge(f_p1, profit_acm, left_index=True, right_index=True)
    # renombrar las columnas del nuevo dataframe
    df_profit_diario = df_profit_diario1.rename(columns={"profit_d_x": "profit_d", "profit_d_y": "profit_acm_d"})

    return df_profit_diario

