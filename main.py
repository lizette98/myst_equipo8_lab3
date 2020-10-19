
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
archivo = fn.f_leer_archivo(param_archivo=archivo)

# --- 1.2 Funcion para obtener el multiplicador para diferencia de pips
ins = dt.ins
# En param_ins se escribe el activo deseado
pip_size = fn.f_pip_size(param_ins='XAUUSD')

# --- 1.3 Funcion de transformaciones de tiempo
# FALTA COMPLETAR Y HACER FUNCION
param_data = archivo
param_data['Close Time'] = pd.to_datetime(param_data['Close Time'])
param_data['Open Time'] = pd.to_datetime(param_data['Open Time'])

