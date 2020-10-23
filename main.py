
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
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


