
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: PAP                                                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: eremarin45                                                                                  -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/IteraCapital/Impacto_social                                          -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
from os import path

# Leer excel Poblacion economicamente activa
abspath = path.abspath('files/PEA.csv')
pea = pd.read_csv(abspath)

# Leer excel Recursos canalizados a las AFORES
abspath = path.abspath('files/Flujos1.csv')
df_pe = pd.read_csv(abspath)

# Leer excel de Rendimiento de las Siefores
abspath = path.abspath('files/Rend.csv')
df_rend = pd.read_csv(abspath)

