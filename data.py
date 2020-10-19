
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
from os import listdir, path

# Leer historial de cada cuenta
abspath = path.abspath('files/Historial Andrea.csv')
archivo = pd.read_csv(abspath)

# Leer excel con todos los pips de Oanda
abspath = path.abspath('files/Oanda_Instruments.xlsx')
pips_oanda = pd.read_excel(abspath)
# Quitar guion bajo en el item
pips_oanda['Item'] = pips_oanda['Item'].str.replace('_', '')
pips_oanda['Item'] = pips_oanda['Item'].str.lower()
ins = pips_oanda['Item']
