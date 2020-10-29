
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 3 Behavioral Finance MYST                                                      -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: lizette98                                                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/lizette98/myst_equipo8_lab3                                          -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
from os import listdir, path

#BEHAVIORAL FINANCE

import functions as fn
import data as dt

# ---------- 1. ESTADISTICA DESCRIPTIVA


# --- 1.1 Funcion para leer el archivo ya limpio.
archivo = dt.archivo
df_data = fn.f_leer_archivo(param_archivo=archivo)

# --- 1.2 Funcion para obtener el multiplicador para diferencia de pips
ins = dt.ins
# En param_ins se escribe el activo deseado
pip_size = fn.f_pip_size(param_ins='eurusd')

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


# ---------- 4. Visualizations
# Esto va a ir en visualizations

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as py
py.offline.init_notebook_mode(connected = False)
import pandas as pd

archivo = dt.archivo
df_data = fn.f_leer_archivo(param_archivo=archivo)


# Grafica de ranking
estadisticas_ba = fn.f_estadisticas_ba(df_data)
def ranking(estadisticas_ba):
    """
    Parameters
    ----------
    estadisticas_ba : función : Función utilizada para calcular el ranking de asertividad de divisas
    Returns
    -------
    graph : gráfica de pastel con plotly mostrando el porcentaje que representa la asertividad del total de pares usados
    """
    # Llamamos la funcion de ranking calculada en functions
    estadisticas_ba = fn.f_estadisticas_ba(df_data)
    # Obtenemos solo el df de ranking
    df_ranking = pd.DataFrame(estadisticas_ba['df_1_ranking'])
    df_1_ranking = df_ranking.reset_index()
    # Renombrar columnas del df
    df_ranking = df_1_ranking.rename(columns={"index": "pares", "rank": "rank"})

    # Grafica de pastel
    PieChart_Rank = go.Figure()
    labels = df_ranking['pares']
    values = df_ranking['rank']
    PieChart_Rank = go.Figure(data=[go.Pie(labels=labels, values=values,
                                      pull=[0.2, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                            0])])
    PieChart_Rank.update_layout(title="Ranking", font=dict(size=16))
    #pie_rank.update_traces(textposition='inside', textinfo='percent+label')
    py.iplot(PieChart_Rank)


# Gráfica drawdown y drawup
profit_d = fn.f_evolucion_capital(df_data)


def drawd_drawup(profit_d):
    """
    Parameters
    ----------
    profit_d : función : Función utilizada para el dataframe con el pd.DataFrame(datos)
    Returns
    -------
    graph : gráfica de línea con plotly mostrando el profit acumulado
    """
    # Llamamos la funcion con el dataframe de evolucion de capital
    profit_d = fn.f_evolucion_capital(df_data)

    profits = go.Figure()
    profits.add_trace(go.Scatter(x=profit_d.timestamp,
                               y=[None, None, None, None, None, None, None, 99775.28, None, None, 134035.28, None, None, None,
                                  None], name='drawup',
                               connectgaps=True, mode='lines', line={'dash': 'dash', 'color': 'green'}))
    profits.add_trace(go.Scatter(x=profit_d.timestamp,
                               y=[100027.15, None, None, None, None, None, None, 99775.28, None, None, None, None, None, None,
                                  None], name='drawdown',
                               connectgaps=True, mode='lines', line={'dash': 'dash', 'color': 'red'}))
    profits.add_trace(go.Scatter(x=profit_d.timestamp, y=profit_d.profit_acm_d, name='profit acumulado', mode='lines',
                               marker=dict(color='Black')))

    profits.update_layout(title="Evolución del Capital Acumulado Diario", xaxis_title="Tiempo (fechas)", yaxis_title="Profit ($)")

    # profs.show()
    py.iplot(profits)