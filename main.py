
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

# --- 3.2 Pruebas de sesgos



# ---------- 4. VISUALIZACIONES

# --- 4.1 Grafica 1: Ranking
ranking = vn.ranking(estadisticas_ba=df_data)

# --- 4.1 Grafica 2: DrawDown y DrawUp
drawd_drawup = vn.drawd_drawup(profit_d=df_data)
