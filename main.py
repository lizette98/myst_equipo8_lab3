
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 3 Behavioral Finance MYST                                                      -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: lizette98                                                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/lizette98/myst_equipo8_lab3                                          -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# BEHAVIORAL FINANCE

import functions as fn
import data as dt
import visualizations as vn

# ---------- 1. ESTADISTICA DESCRIPTIVA

# --- 1.1 Funcion para leer el archivo ya limpio.
df_data = fn.f_leer_archivo(param_archivo='files/historicos_alcg.csv')

# --- 1.2 Funcion para obtener el multiplicador para diferencia de pips
ins = dt.ins
# En param_ins se escribe el activo deseado
pip_size = fn.f_pip_size(param_ins='eurusd')

# -------------         Funcion de prueba para los instrumentos
# Instrumentos en mayuscula
instruments = fn.f_instrument()

# --- 1.3 Funcion de transformaciones de tiempo en segundos
df_data = fn.f_columnas_tiempos(param_data=df_data)

# --- 1.4 Funcion de transformaciones de pips
df_data = fn.f_columnas_pips(param_data=df_data)

# --- 1.5 Funcion para calcular estadisticas basicas y ranking por instrumentos
est_ba = fn.f_estadisticas_ba(param_data=df_data)


# ---------- 2. METRICAS DE ATRIBUCION AL DESEMPEÑO

# --- 2.1 Columna de evolucion de capital
profit_acum_d = fn.f_profit_acm_d(param_data=df_data)

# --- 2.2 DataFrame de evolucion de capital
evolucion_capital = fn.f_evolucion_capital(param_data=df_data)

# --- 2.3 DataFrame de Medidas de Atribucion al Desempeño
MAD = fn.f_estadisticas_mad(param_data=df_data)


# ---------- 3. BEHAVIORAL FINANCE

# --- 3.1 Descarga de precios
# Funcion que dio Francisco para descargar los precios
precios = fn.func_precios(param_data=df_data)

# --- 3.2 Sesgos

sesgos = fn.f_be_de(param_data=df_data)


# ---------- 4. VISUALIZACIONES

# --- 4.1 Grafica 1: Ranking
ranking = vn.ranking(estadisticas_ba=df_data)

# --- 4.1 Grafica 2: DrawDown y DrawUp
drawd_drawup = vn.drawd_drawup(profit_d=df_data)

# --- 4.3 Disposition Effect
sesgos_graph = vn.sesgos(sesgos)

""" 

# PRUEBA
# Nueva columna de ratio del capital acumulado
param_data = df_data
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

# PRUEBA
import pandas as pd
param_data['CloseTime'] = pd.to_datetime(param_data['CloseTime'])
param_data['OpenTime'] = pd.to_datetime(param_data['OpenTime'])
df_ganadoras['CloseTime'] = pd.to_datetime(df_ganadoras['CloseTime'])
df_ganadoras['OpenTime'] = pd.to_datetime(df_ganadoras['OpenTime'])
# Con las operaciones ya ganadas, buscar las operaciones que pertenecen a los dos escenarios en los que habrían posibles ocurrencias de operaciones abiertas al momento de cierre de las ganadoras
posibles_operaciones = [[param_data.iloc[i, :] for i in range(len(param_data))
                         # Que la operación ganadora haya iniciado antes, y haya cerrado antes que la operación abierta y que la operación abierta haya cerrado después del momento de cierre de la operación ganadora
                         if df_ganadoras['CloseTime'][k] > param_data['OpenTime'][i] > df_ganadoras['OpenTime'][k] and
                         param_data['CloseTime'][i] > df_ganadoras['CloseTime'][k] or
                         # Que la operación haya abierto antes que la ganadora Y cerrado después de la ganadora
                         param_data['OpenTime'][i] < df_ganadoras['OpenTime'][k] and
                         param_data['CloseTime'][i] > df_ganadoras['CloseTime'][k]]
                        for k in range(len(df_ganadoras))]

# Colocar todas las posibles operaciones en formato dataframe en donde la primera, es la operación ancla, y cada dataframe en una lista
pos_ops = [pd.concat([df_ganadoras.iloc[i, :], pd.concat(posibles_operaciones[i], axis=1)],
                     axis=1, sort=False, ignore_index=True).T for i in range(len(posibles_operaciones)) if
           posibles_operaciones[i] != []]

# Se descargan los precios de cierre en una lista de acuerdo a la operación ancla con la función de descarga de precios
# Definir parametros para la funcion de precios masivos
inst_mayus = [i.upper() for i in list(pos_ops[1].Item.unique())]
inst_mayus_ = [i[:-3] + "_"+i[-3:] for i in inst_mayus]

#inst_precios = fn.f_instrument()

# pos_ops[k]['Item'][i+1] for i in range(len(pos_ops[k]) - 1)
    #                                for k in range(len(pos_ops)))
from datetime import timedelta
df_precios = pd.DataFrame(columns=['TimeStamp', 'Open', 'High', 'Low', 'Close'])
df_precios_2 = pd.DataFrame(columns=['TimeStamp', 'Open', 'High', 'Low', 'Close'])
json_precios = {}

for i in inst_mayus_:
    oa_in = i  # Instrumento
    oa_gn = "D"  # Granularidad de velas (M1: Minuto, M5: 5 Minutos, M15: 15 Minutos)
    fini = pd.to_datetime(param_data['fechas'].min()).tz_localize('GMT') - timedelta(minutes=800) # Fecha inicial
    fini = fini + timedelta(days=1)
    ffin = pd.to_datetime(param_data['fechas'].max()).tz_localize('GMT') - timedelta(minutes=800) # Fecha final
    ffin = ffin + timedelta(days=3)

    precios = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=oa_gn, p3_inst=oa_in, p4_oatk=dt.oa_token, p5_ginc=4900)
    json_precios[oa_in] = precios.values

df_precios, df_precios_2 = [pd.DataFrame(json_precios[k], columns=['TimeStamp', 'Open', 'High', 'Low', 'Close']) for k in inst_mayus_]





# prices = [[f_prices(f_instrument(pos_ops[k]['symbol'][i+1]), pos_ops[k]['closetime'][0])
#           for i in range(len(pos_ops[k]) - 1)] for k in range(len(pos_ops))]
"""