
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 3 Behavioral Finance MYST                                                      -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: lizette98                                                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/lizette98/myst_equipo8_lab3                                          -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import numpy as np
import data as dt
import pandas as pd                                       # procesamiento de datos
from datetime import timedelta                            # para incrementos de fechas
from oandapyV20 import API                                # conexion con broker OANDA
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos
import requests

from os import listdir, path


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
            Dataframe de historial con informacion del trading ya limpio
    """
    abspath = path.abspath(param_archivo)
    param_archivo = pd.read_csv(abspath)
    # Quitar el "-e" de la columna Item
    param_archivo['Item'] = param_archivo['Item'].str.replace('-e', '')
    # Poner los activos en minuscula
    param_archivo['Item'] = param_archivo['Item'].str.lower()

    return param_archivo


def f_instrument():
    # Leer excel con todos los pips de Oanda
    from os import path

    abspath = path.abspath('files/Oanda_Instruments.xlsx')
    pips_oanda = pd.read_excel(abspath)
    instrument = pips_oanda['Item']

    return instrument


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
    # Leer el archivo de Oanda con la informacion de pips
    pips_oanda = dt.pips_oanda
    pips_oanda = pips_oanda.set_index('Item')
    pips_oanda = pips_oanda['PipLocation']
    # Formula para obtener el multiplicador de cada activo
    # En param_ins en main se escribe el activo deaseado
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
    # Quitar espacios de columna de Profit
    #param_data['Profit'] = param_data['Profit'].str.replace(' ', '')
    # Convertir columna de Profit a int
    param_data['Profit'] = pd.to_numeric(param_data['Profit'])
    # Convertir a datetime las columnas de tiempo
    param_data['Close Time'] = pd.to_datetime(param_data['Close Time'])
    param_data['Open Time'] = pd.to_datetime(param_data['Open Time'])
    # Renombrar las columnas de tiempo
    param_data = param_data.rename(columns={'Close Time': 'CloseTime', 'Open Time': 'OpenTime'})
    #Nueva columna de tiempo transcurrido en segundos
    param_data['tiempo'] = [(param_data.loc[i, 'CloseTime'] - param_data.loc[i, 'OpenTime']).delta / 1e9
                            for i in range(0, len(param_data['CloseTime']))]
    #Renombrar las columnas de precio de apertura y de cierre
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
    # Inicializar columna de pips
    param_data['pips'] = 0
    # Ciclo para obtener los pips de cada operacion
    for i in range(len(param_data)):
        n = f_pip_size(param_data['Item'].iloc[i])
        if param_data['Type'][i] == 'sell':
            param_data['pips'][i] = (param_data['OpenPrice'][i] - param_data['ClosePrice'][i]) * n
        else:
            param_data['pips'][i] = (param_data['ClosePrice'][i] - param_data['OpenPrice'][i]) * n
    # Convertir columna de Profit a int
    #param_data['Profit'] = pd.to_numeric(param_data['Profit'])
    # Columna de pips acumulados
    param_data['pips_acm'] = param_data['pips'].cumsum()
    # Columna de Profit acumulada
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
    # Creacion del primer df del diccionario
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
    # Convertir a diccionario
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

    # Columna inicializada en $100,000 donde se le suma/resta el profit acumulado
    param_data['profit_acm_d'] = 100000 + param_data.profit_acm

    return param_data.copy()


def f_evolucion_capital(param_data):
    """
    Funcion para analizar la evolucion del capital.

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

    # Agregar normalize a Closetime
    CT_norm = pd.date_range(param_data.CloseTime.min(), param_data.CloseTime.max()).normalize()

    # Convertir a df las fechas diarias
    dates = pd.DataFrame({'timestamp': CT_norm})

    # Normalizar
    groups = param_data.groupby(pd.DatetimeIndex(param_data['CloseTime']).normalize())
    # Profit
    profit = groups['Profit'].sum()
    # Convertir las ganancias diarias a df
    profit_diario = pd.DataFrame({'profit_d': [profit[i] if i in profit.index else 0 for i in CT_norm]})
    profit_acm = np.cumsum(profit_diario) + 100000
    # Combinar los df anteriores de fechas y profit diario
    date_prof = pd.merge(dates, profit_diario, left_index=True, right_index=True)
    # Juntar el df anterior con los profit acumulados
    date_prof_acm = pd.merge(date_prof, profit_acm, left_index=True, right_index=True)
    # Renombrar las columnas del df final
    df_profit_diario = date_prof_acm.rename(columns={"profit_d_x": "profit_d", "profit_d_y": "profit_acm_d"})

    return df_profit_diario


def f_estadisticas_mad(param_data):
    """
    Funcion para crear un DataFrame  con los resultados de cada Medida de Atribucion al Desempeño
    expresadas en términos diarios: 'sharpe', 'drawdown_capi', 'drawup_capi'.

    Parameters
    ----------
    param_data: DataFrame
            DataFrame del historico de operaciones.

    Returns
    -------
    MAD: DataFrame
            Dataframe con tres columnas:
            1. Sharpe Ratio: Rentabilidad menos la tasa de interés libre de riesgo
            entre la volatilidad o desviación standard de esa rentabilidad en el mismo periodo.
            2. DrawDown (Capital): Minusvalia máxima que se registró en la evolución de los valores (de 'profit_acm_d')
            3. DrawUp (Capital): Plusvalía máxima que se registró en la evolución de los valores (de 'profit_acm_d')
    """

    profit_dia = f_evolucion_capital(param_data)

    # Sharpe
    # Promedio de los rendimientos logaritmicos de profit_acm_d
    rp = np.log(profit_dia.profit_acm_d[1:].values / profit_dia.profit_acm_d[:-1].values)
    # Tasa entre dias bursatiles en un año
    rf = 0.05 / 300
    # Desviacion estandar de los rendimientos
    sdp = np.std(rp)

    # DrawDown Capital
    # Tomar el profit minimo
    fila = profit_dia.loc[profit_dia['profit_acm_d'] == profit_dia.profit_acm_d.min()]
    position = fila.index.tolist()
    prev_where = profit_dia.loc[0:position[0]]
    # Punto maximo y minimo del drawdown
    max_prev = profit_dia.loc[profit_dia['profit_acm_d'] == prev_where.profit_acm_d.max()]
    min_prev = profit_dia.loc[profit_dia['profit_acm_d'] == prev_where.profit_acm_d.min()]
    ddown_max = max_prev.iloc[0]['profit_acm_d']
    ddown_min = min_prev.iloc[0]['profit_acm_d']
    ddown = ddown_max - ddown_min
    # Fechas del Drawdown
    date_max_ddown = max_prev.iloc[0]['timestamp']
    date_min_ddown = min_prev.iloc[0]['timestamp']
    # Drawdown
    drawdown = "{}, {}, ${:.2f}".format(date_max_ddown, date_min_ddown, ddown)

    # DrawUp Capital
    # Tomar el profit maximo
    fila_up = profit_dia.loc[profit_dia['profit_acm_d'] == profit_dia.profit_acm_d.max()]
    position_up = fila_up.index.tolist()
    foll_where = profit_dia.loc[0:position_up[0]]
    # Punto maximo y minimo del DrawUp
    max_foll = profit_dia.loc[profit_dia['profit_acm_d'] == foll_where.profit_acm_d.max()]
    min_foll = profit_dia.loc[profit_dia['profit_acm_d'] == foll_where.profit_acm_d.min()]
    dup_max = max_foll.iloc[0]['profit_acm_d']
    dup_min = min_foll.iloc[0]['profit_acm_d']
    dup = dup_max - dup_min
    # Fechas del DrawUp
    date_max_dup = max_foll.iloc[0]['timestamp']
    date_min_dup = min_foll.iloc[0]['timestamp']
    #DrawUp
    drawup = "{}, {}, ${:.2f}".format(date_min_dup, date_max_dup, dup)


    # Dataframe de Metricas
    metricas = pd.DataFrame({'metrica': ['sharpe', 'drawdown_capi', 'drawdup_capi']})
    valor = pd.DataFrame({'valor': [((rp.mean() - rf) / rp.std()), (drawdown), (drawup)]})
    df_mad = pd.merge(metricas, valor, left_index=True, right_index=True)
    descripcion = pd.DataFrame({'descripcion': ['Sharpe Ratio', 'DrawDown de Capital',
                                                'DrawUp de Capital']})
    df_est_mad = pd.merge(df_mad, descripcion, left_index=True, right_index=True)

    return df_est_mad


# ---------- 3. BEHAVIORAL FINANCE
# -- ------------------------- FUNCION: Descargar precios ---------------------------------- #
# -- --------------------------------------------------------------------------------------- #
# -- Descargar precios historicos con OANDA

def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    Parameters
    ----------
    p0_fini : str : fecha inicial para descargar precios en formato str o pd.to_datetime
    p1_ffin : str : fecha final para descargar precios en formato str o pd.to_datetime
    p2_gran : str : M1, M5, M15, M30, H1, H4, H8, segun formato solicitado por OANDAV20 api
    p3_inst : str : nombre de instrumento, segun formato solicitado por OANDAV20 api
    p4_oatk : str : OANDAV20 API
    p5_ginc : int : cantidad de datos historicos por llamada, obligatorio < 5000
    Returns
    -------
    dc_precios : pd.DataFrame : Data Frame con precios TOHLC
    Debugging
    ---------
    p0_fini = pd.to_datetime("2019-01-01 00:00:00").tz_localize('GMT')
    p1_ffin = pd.to_datetime("2019-12-31 00:00:00").tz_localize('GMT')
    p2_gran = "M1"
    p3_inst = "USD_MXN"
    p4_oatk = Tu token
    p5_ginc = 4900
    """

    def f_datetime_range_fx(p0_start, p1_end, p2_inc, p3_delta):
        """
        Parameters
        ----------
        p0_start : str : fecha inicial
        p1_end : str : fecha final
        p2_inc : int : incremento en cantidad de elementos
        p3_delta : str : intervalo para medir elementos ('minutes', 'hours', 'days')
        Returns
        -------
        ls_result : list : lista con fechas intermedias a frequencia solicitada
        Debugging
        ---------
        p0_start = p0_fini
        p1_end = p1_ffin
        p2_inc = p5_ginc
        p3_delta = 'minutes'
        """

        ls_result = []
        nxt = p0_start

        while nxt <= p1_end:
            ls_result.append(nxt)
            if p3_delta == 'minutes':
                nxt += timedelta(minutes=p2_inc)
            elif p3_delta == 'hours':
                nxt += timedelta(hours=p2_inc)
            elif p3_delta == 'days':
                nxt += timedelta(days=p2_inc)

        return ls_result

    # inicializar api de OANDA

    api = API(access_token=p4_oatk)

    gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60 * 5, 'M15': 60 * 15,
          'M30': 60 * 30, 'H1': 60 * 60, 'H4': 60 * 60 * 4, 'H8': 60 * 60 * 8,
          'D': 60 * 60 * 24, 'W': 60 * 60 * 24 * 7, 'M': 60 * 60 * 24 * 7 * 4}

    # -- para el caso donde con 1 peticion se cubran las 2 fechas
    if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 4990:

        # Fecha inicial y fecha final
        f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
        f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

        # Parametros pra la peticion de precios
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                  "to": f2}

        # Ejecutar la peticion de precios
        a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
        a1_hist = api.request(a1_req1)

        # Para debuging
        # print(f1 + ' y ' + f2)
        lista = list()

        # Acomodar las llaves
        for i in range(len(a1_hist['candles']) - 1):
            lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                          'Open': a1_hist['candles'][i]['mid']['o'],
                          'High': a1_hist['candles'][i]['mid']['h'],
                          'Low': a1_hist['candles'][i]['mid']['l'],
                          'Close': a1_hist['candles'][i]['mid']['c']})

        # Acomodar en un data frame
        r_df_final = pd.DataFrame(lista)
        r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final

    # -- para el caso donde se construyen fechas secuenciales
    else:

        # hacer series de fechas e iteraciones para pedir todos los precios
        fechas = f_datetime_range_fx(p0_start=p0_fini, p1_end=p1_ffin, p2_inc=p5_ginc,
                                     p3_delta='minutes')

        # Lista para ir guardando los data frames
        lista_df = list()

        for n_fecha in range(0, len(fechas) - 1):

            # Fecha inicial y fecha final
            f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
            f2 = fechas[n_fecha + 1].strftime('%Y-%m-%dT%H:%M:%S')

            # Parametros pra la peticion de precios
            params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                      "to": f2}

            # Ejecutar la peticion de precios
            a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
            a1_hist = api.request(a1_req1)

            # Para debuging
            # print(f1 + ' y ' + f2)
            lista = list()

            # Acomodar las llaves
            for i in range(len(a1_hist['candles']) - 1):
                lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                              'Open': a1_hist['candles'][i]['mid']['o'],
                              'High': a1_hist['candles'][i]['mid']['h'],
                              'Low': a1_hist['candles'][i]['mid']['l'],
                              'Close': a1_hist['candles'][i]['mid']['c']})

            # Acomodar en un data frame
            pd_hist = pd.DataFrame(lista)
            pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
            pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

            # Ir guardando resultados en una lista
            lista_df.append(pd_hist)

        # Concatenar todas las listas
        r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

        # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
        r_df_final = r_df_final.reset_index(drop=True)
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final


# --- Sesgos

# Descarga de precios necesarios para los sesgos
def func_precios(param_data):
    # Nueva columna de fechas para descargar precios
    param_data['fechas'] = list(param_data['CloseTime'].astype(str).str[0:10])
    # Ordenar por Close Time
    param_data.sort_values(by='CloseTime', inplace=True, ascending=True)
    param_data.reset_index(inplace=True, drop=True)
    start = str(param_data['CloseTime'].min())[0:10]
    end = str(param_data['CloseTime'].max())[0:10]
    total_days = pd.date_range(start=start, end=end, freq='D')
    param_data['CloseTime'] = list([str(i)[0:10] for i in param_data['CloseTime']])

    # Definir parametros para la funcion de precios masivos
    oa_in = "GBP_USD"  # Instrumento
    oa_gn = "D"  # Granularidad de velas (M1: Minuto, M5: 5 Minutos, M15: 15 Minutos)
    fini = pd.to_datetime(param_data['fechas'].min()).tz_localize('GMT') - timedelta(minutes=800) # Fecha inicial
    fini = fini + timedelta(days=1)
    ffin = pd.to_datetime(param_data['fechas'].max()).tz_localize('GMT') - timedelta(minutes=800) # Fecha final
    ffin = ffin + timedelta(days=3)

    precios = f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=oa_gn, p3_inst=oa_in, p4_oatk=dt.oa_token, p5_ginc=4900)

    return precios


def f_be_de(param_data):
    # Nueva columna de ratio del capital acumulado
    param_data['profit_acm_ratio'] = 0
    for i in range(len(param_data)):
        if i == 0:
            # Calcular el ratio (capital_ganadora/capital_acm)*100
            param_data['profit_acm_ratio'] = (param_data['Profit'][i] / 100000) * 100
        else:
            # (capital_perdedora/capital_acm)*100 para cada operacion
            param_data['profit_acm_ratio'] = (param_data['Profit'][i] / param_data['profit_acm_d'][i - 1]) * 100

    # DataFrame de operaciones ganadoras en la cuenta
    df_ganadoras = param_data[param_data['Profit'] > 0]
    # Fecha de cierre de las ganadoras
    ct_ganadoras = df_ganadoras['CloseTime']
    # DataFrame de operaciones perdedoras en la cuenta
    df_perdedoras = param_data[param_data['Profit'] < 0]
    df_ganadoras.reset_index(inplace=True, drop=True)
    df_perdedoras.reset_index(inplace=True, drop=True)

    # Diccionario para resultado final
    dict = {'ocurrencias': {'timestamp': {}, 'operaciones': {}}, 'resultados': {}}

    # Convertir Close y Open time a str
    df_ganadoras['CloseTime'] = list([str(i)[0:10] for i in df_ganadoras['CloseTime']])
    df_perdedoras['CloseTime'] = list([str(i)[0:10] for i in df_perdedoras['CloseTime']])
    df_perdedoras['OpenTime'] = list([str(i)[0:10] for i in df_perdedoras['OpenTime']])

    for i in range(len(df_ganadoras)):
        for j in range(len(df_perdedoras)):
            # Marcar inicio y final de las operaciones perdedoras
            inicio_op = df_perdedoras['OpenTime'][j]
            fin_op = df_perdedoras['CloseTime'][j]
            # Obtener dias totales
            dias_tot = pd.date_range(start=inicio_op, end=fin_op, freq='D')
            # Ciclo para ver si en el momento que la ganadora cerró estaba abierta la operación perdedora
            if df_ganadoras['CloseTime'][i] in dias_tot:
                # Inicializar contador de ocurrencias
                ocurrencias = 0
                ocurrencias += 1
                # Llenado de operaciones del diccionario
                operaciones = {'operaciones': {'ganadora': {'instrumento': df_ganadoras['Item'][i],
                                                            'volumen': df_ganadoras['Size'][i],
                                                            'sentido': df_ganadoras['Type'][i],
                                                            'profit_ganadora': df_ganadoras['Profit'][i]},
                                      'perdedora': {'instrumento': df_perdedoras['Item'][j], 'volumen': df_perdedoras['Size'][j],
                                                    'sentido': df_perdedoras['Type'][j],
                                                    'profit_perdedora': df_perdedoras['Profit'][j]}},
                      'ratio_cp_profit_acm': df_perdedoras['Profit'][j] / df_ganadoras['profit_acm_d'][i],
                      'ratio_cg_profit_acm': df_ganadoras['Profit'][i] / df_ganadoras['profit_acm_d'][i],
                      'ratio_cp_cg': df_perdedoras['Profit'][j] / df_ganadoras['Profit'][i]}

                # Agregar TimeStamp al Diccionario
                tsmp = 0
                tsmp = {'TimeStamp': df_ganadoras['CloseTime'][i]}
                # Llenado de resultados del diccionario
                # Calculo de Statusquo
                # Inicializar statusquo
                status_quo = 0
                if np.abs(df_perdedoras['Profit'][j] / df_ganadoras['profit_acm_d'][i]) < np.abs(df_ganadoras['Profit'][i] / df_ganadoras['profit_acm_d'][i]):
                    status_quo += 1
                # Inicializar aversion a la perdida
                aversion_perdida = 0
                # Contabilizar si el ratio de profit_perdedora/profit_ganadora es > 1.5
                if np.abs(df_perdedoras['Profit'][j] / df_ganadoras['Profit'][i]) > 1.5:
                    aversion_perdida+= 1
            # Obtener cada numero de ocurrencia
            num_ocurr = 'ocurrencia, %s' % str(ocurrencias)
            # Llenar operaciones y timestamp de las ocurrencias del diccionario
            dict['ocurrencias']['operaciones'][num_ocurr] = operaciones
            dict['ocurrencias']['timestamp'][num_ocurr] = tsmp

    # Cantidad de ocurrencias
    dict['cantidad'] = ocurrencias
    # Statusquo y aversion a la perdida en porcentaje
    status_quo_porc = (status_quo/ocurrencias) * 100
    aversion_perdida_porc = (aversion_perdida / ocurrencias) * 100

    #--- Principip 3 Sensibilidad decreciente a los cambios
    sensibilidad_decr = '-'
    # 1. Si el capital_acm de la cuenta aumentó.
    # 2. Si el capital_ganadora & capital_perdedora aumentaron.
    # 3. Si el ratio capital_perdedora/capital_ganadora sigue siendo > 1.5.
    if df_ganadoras['profit_acm_d'][0] < df_ganadoras['profit_acm_d'].iloc[-1] and df_ganadoras['Profit'][0] < df_ganadoras['Profit'].iloc[-1] or \
            df_perdedoras['Profit'][0] < df_perdedoras['Profit'].iloc[-1] and (df_perdedoras['Profit'].min() / df_ganadoras['Profit'].max()) > 1.5:
        sensibilidad_decr = 'si'
    else:
        sensibilidad_decr = 'no'

    # DataFrame para resultados {}
    df_resultados = {'ocurrencias': [ocurrencias], 'status_quo': [status_quo_porc],
                'aversion_perdida': [aversion_perdida_porc],
                'sensibilidad_decreciente': [sensibilidad_decr]}
    dict['resultados'] = pd.DataFrame(df_resultados)

    return dict
