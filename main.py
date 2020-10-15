
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
from os import listdir, path

#BEHAVIORAL FINANCE

import functions as fn
import data as dt

#----- 1. ESTADISTICA DESCRIPTIVA
archivo = dt.archivo

#--- 1.1 Funcion para leer el archivo ya limpio.
archivo = fn.f_leer_archivo(param_archivo=archivo)

#FATLA COMPLETAR Y PASAR A FUNCION
#--- 1.2 Funcion para obtener el multiplicador para diferencia de pips
#Leer excel con todos los pips
abspath = path.abspath('files/Oanda_Instruments.xlsx')
pips_oanda = pd.read_excel(abspath)

#Cambiar nombre de Items
pips_oanda = pips_oanda.rename(columns={'Symbol':'Item'})
#Quitar puntos en el ticker
pips_oanda['Item'] = pips_oanda['Item'].str.replace('.', '')
df_pips = pd.merge(archivo, pips_oanda, on='Item')
df_pips = df_pips.assign(PipsLocation = pow(10/1,abs(df_pips['PipLocation'])))
df_pips = df_pips.iloc[:, [4,22]]
df_pips = df_pips.set_index('Item')
pip_size = df_pips.to_dict()





