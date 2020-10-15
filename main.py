
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import functions as fn
import pandas as pd
from os import listdir, path

abspath = path.abspath('files/Historial csv.csv')
arch = pd.read_csv(abspath)

archivo = fn.f_leer_archivo(param_archivo=arch)
