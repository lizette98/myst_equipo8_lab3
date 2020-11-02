
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
abspath = path.abspath('files/historicos_alcg.csv')
archivo = pd.read_csv(abspath)

# Leer excel con todos los pips de Oanda
abspath = path.abspath('files/Oanda_Instruments.xlsx')
pips_oanda = pd.read_excel(abspath)
# Quitar guion bajo en el item
pips_oanda['Item'] = pips_oanda['Item'].str.replace('_', '')
pips_oanda['Item'] = pips_oanda['Item'].str.lower()
ins = pips_oanda['Item']

"""
def f_pip_size(param_ins):

    Funcion para obtener el número multiplicador para expresar la diferencia de precios en pips.
    Parameters
    ----------
    param_ins: str
            Instrumento para asociarse al multiplicador de pips que le corresponde
    Returns
    -------
    n: int
            Multiplicador de pips que le corresponde al instrumento.
 
    # Leer el archivo de Oanda con la informacion de pips
    pips_oanda = dt.pips_oanda
    pips_oanda = pips_oanda.set_index('Item')
    pips_oanda = pips_oanda['PipLocation']
    # Formula para obtener el multiplicador de cada activo
    n = pow(10 / 1, np.abs(pips_oanda[param_ins]))

    return n
   """

def f_pip_size(param_data):
    pips_oanda = []
    pips_acum = []
    profit_acum = []
    for i in range(len(archivo)):
        if i == 0:
            if archivo['Type'].iloc[i] == 'buy':
                pips_oanda.append(
                    (archivo['Close Time'].iloc[i] - archivo['Open Time'].iloc[i]) * f_pip_size(
                        archivo['Symbol'].iloc[i]))
            else:
                pips_oanda.append(
                    (archivo['Open Time'].iloc[i] - archivo['Close Time'].iloc[i]) * f_pip_size(
                        archivo['Symbol'].iloc[i]))
            pips_acum.append(pips_oanda[0])
            profit_acum.append(archivo['Profit'].iloc[0])

        else:
            if archivo['Type'].iloc[i] == 'buy':
                pips_oanda.append(
                    (archivo['closePrice'].iloc[i] - archivo['openPrice'].iloc[i]) * f_pip_size(
                        archivo['Symbol'].iloc[i]))

            else:
                pips_oanda.append(
                    (archivo['openPrice'].iloc[i] - archivo['closePrice'].iloc[i]) * f_pip_size(
                        archivo['Symbol'].iloc[i]))

            pips_acum.append(pips_acum[i - 1] + pips[i])
            profit_acum.append(profit_acum[i - 1] + archivo['Profit'].iloc[i])

    archivo['pips'] = pips_oanda
    archivo['pips_acum'] = pips_acum
    archivo['profit_acum'] = profit_acum
    return archivo

'''
sacar pips
df_ancla: ganadora
    por cada uno ver cuales estan abiertas cuando se cerro esa operación time mayor a la hr de cierre
    
buy close-open en pips
sell open-close
checar pip value oanda
todo es $



ops_res= first_row = df.index.get_loc(first[0])
last_row = df.index.get_loc(last[0])
if first_row == last_row:
       result = df.loc[first[0], first[1]: last[1]].min()
elif first_row < last_row:
       first_row_min = df.loc[first[0], first[1]:].min()
       last_row_min = df.loc[last[0], :last[1]].min()
       middle_min = df.iloc[first_row + 1:last_row].min().min()
       result = min(first_row_min, last_row_min, middle_min)
else: 
       raise ValueError('first row must be <= last row')


'''