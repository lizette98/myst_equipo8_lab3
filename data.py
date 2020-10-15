
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
# Importar librerias
import pandas as pd
from os import listdir, path
from os.path import isfile, join

pd.set_option('display.expand_frame_rep', False)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Leer archivos
#Ruta absoluta para archivos
abspath = path.abspath('files/Historial csv.csv')
archivo = pd.read_csv(abspath)


