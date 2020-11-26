"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: PAP                                                                                        -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: eremarin45                                                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository:
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# ---------- 4. Visualizations
import functions as fn
import matplotlib.pyplot as plt

df_rend = fn.f_leer_archivo(param_archivo='files/Rend.csv')


def fig(df_rend: object):
    """
    Funcion para graficar el rendimiento de las siefores.

    Parameters
    ----------
    df_rend : Function
            Función utilizada para leer archivo.

    Returns
    -------
    plt.plot(): figura
            Grafica de línea para visualizar todos los rendimientos de cada siefore
    """

    rend = df_rend
    figura = rend.plot()
    plt.show(figura)
