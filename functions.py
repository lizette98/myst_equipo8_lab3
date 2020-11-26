"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: PAP                                                                                        -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: eremarin45                                                                                  -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/IteraCapital/Impacto_social                                          -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import matplotlib.pyplot as plt
from numpy import random
import pandas as pd
from os import path


# ---------- 1. leer archivos

def f_leer_archivo(param_archivo):
    """
    Funcion para leer el archivo de nuestras bases de datos.

    Parameters
    ----------
    param_archivo: DataFrame
            Dataframe de un csv de los datos

    Returns
    -------
    param_archivo: DataFrame
            Dataframe de la base de datos que solicitemos
    """
    abspath = path.abspath(param_archivo)
    param_archivo = pd.read_csv(abspath)

    return param_archivo


# ---------- 2. simulacion montecarlo

def sim_montecarlo(N):
    """
    Funcion para hacer una simulación montecarlo.

    Parameters
    ----------
    x: Media de los rendimientos

    N: número de pasos
    n: cantidad de trayectorias


    Returns
    -------
    param_archivo: DataFrame
            Dataframe de la base de datos que solicitemos
    """
    x = 5.54913
    xx = [x]
    add_el = xx.append
    for i in range(N):
        z = random.choice([-.1, .1])
        x += z
        add_el(x)
    return xx, x


N = 100
n = 50
final = []
for j in range(n):
    xx, x = sim_montecarlo(N)
    final.append(x)
    plt.plot(xx)
plt.title("Simulacion escenarios rend")
plt.show()

# ---------- 3.
