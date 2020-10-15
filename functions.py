
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

def f_leer_archivo(param_archivo):
    param_archivo['Item'] = param_archivo['Item'].map(lambda x: str(x)[:-2])
    param_archivo['Item'] = param_archivo['Item'].str.upper()

    return param_archivo

