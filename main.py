
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 3 Behavioral Finance MYST                                                      -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: lizette98                                                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/lizette98/myst_equipo8_lab3                                          -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# BEHAVIORAL FINANCE

import functions as fn
import data as dt
import visualizations as vn

# ---------- 1. ESTADISTICA DESCRIPTIVA

# --- 1.1 Funcion para leer el archivo ya limpio.
df_data = fn.f_leer_archivo(param_archivo='files/historicos_alcg.csv')

# --- 1.2 Funcion para obtener el multiplicador para diferencia de pips
ins = dt.ins
# En param_ins se escribe el activo deseado
pip_size = fn.f_pip_size(param_ins='eurusd')

# --- 1.3 Funcion de transformaciones de tiempo en segundos
df_data = fn.f_columnas_tiempos(param_data=df_data)

# --- 1.4 Funcion de transformaciones de pips
df_data = fn.f_columnas_pips(param_data=df_data)

# --- 1.5 Funcion para calcular estadisticas basicas y ranking por instrumentos
est_ba = fn.f_estadisticas_ba(param_data=df_data)


# ---------- 2. METRICAS DE ATRIBUCION AL DESEMPEÑO

# --- 2.1 Columna de evolucion de capital
profit_acum_d = fn.f_profit_acm_d(param_data=df_data)

# --- 2.2 DataFrame de evolucion de capital
evolucion_capital = fn.f_evolucion_capital(param_data=df_data)

# --- 2.3 DataFrame de Medidas de Atribucion al Desempeño
MAD = fn.f_estadisticas_mad(param_data=df_data)


# ---------- 3. BEHAVIORAL FINANCE

# --- 3.1 Descarga de precios
import pandas as pd
from datetime import timedelta
oa_in = "SPX500_USD"  # Instrumento
oa_gn = "D"       # Granularidad de velas (M1: Minuto, M5: 5 Minutos, M15: 15 Minutos)

df_data['fechas'] = list(df_data['CloseTime'].astype(str).str[0:10])
fini = pd.to_datetime(df_data['fechas'].min()).tz_localize('GMT') - timedelta(minutes=800) # Fecha inicial
fini = fini + timedelta(days=1)
ffin = pd.to_datetime(df_data['fechas'].max()).tz_localize('GMT') - timedelta(minutes=800) # Fecha final
ffin = ffin + timedelta(days=3)

precios = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=oa_gn,
                          p3_inst=oa_in, p4_oatk=dt.oa_token, p5_ginc=4900)

# --- 3.2 Pruebas de sesgos

df_data['ratio_capital_acm'] = 0
for i in range(len(df_data)):
    if i == 0:
        df_data['ratio_capital_acm'] = (df_data['Profit'][i]/100000)*100
    else:
        df_data['ratio_capital_acm'] = (df_data['Profit'][i]/df_data['profit_acm_d'][i-1]) * 100

# Separamos las operaciones en perdedoras y ganadoras para posteriormente usar las ganadoras como ancla
ganadoras = df_data[df_data['Profit'] > 0]
# Y guardamos el cierre de operaciones de las ganadoras
ganadoras_ct = ganadoras['CloseTime']
# Tambien sacamos las perdedoras por si las necesitamos más adelante
perdedoras = df_data[df_data['Profit'] < 0]
# Como sabemos que nuestra ancla van a ser las operaciones ganadoras las separamos del resto y creamos un DF
# Pero primero reseteamos el índice para futuros problemas de indexación
ganadoras.reset_index(inplace=True, drop=True)
perdedoras.reset_index(inplace=True, drop=True)

# Creamos el diccionario
diccionario = {'Ocurrencias': {'TimeStamp': {}, 'Operaciones': {}}, 'Resultados': {}}
# Iniciamos todas las variables en 0
oc = 0
op = 0
gn = 0
# Tenemos que iniciar un contador en cero para status quo y aversion a la pérdida
# me base en apuntes de métodos númericos
s_q = 0
ave_per = 0
# Decidí ponerle un nombre más pequeño a ganadoras y perdedoras por practicidad
# Además de que convierto a str closetime y opentime de ambas para poder comparar más adelante
g = ganadoras
g['CloseTime'] = list([str(i)[0:10] for i in g['CloseTime']])
p = perdedoras
p['CloseTime'] = list([str(i)[0:10] for i in p['CloseTime']])
# Tuve que agregar esta linea para que en mi archivo tuviera ocurrencias, quitando las horas, de lo contrario
# Obtenia 0 ocurrencias y me daba error en status quo, eso aumentó las ocurrencias en el del profesor, si
# no la hubiera puesto me hubiera dado 25 en la del profesor
p['OpenTime'] = list([str(i)[0:10] for i in p['OpenTime']])

import numpy as np
for i in range(len(g)):
    for j in range(len(p)):
        # hacemos las dos variables de la misma longitud para poder comparar
        # Asi que nos basamos en la operacion perdedora y su tiempo de ejercicio
        start = p['OpenTime'][j]
        end = p['CloseTime'][j]
        total_days = pd.date_range(start=start, end=end, freq='D')
        # Tenemos que ver si en el momento que la ganadora cerró estaba abierta la operación perdedora en cuestión
        if g['CloseTime'][i] in total_days:
            # Le agregamos al contador que nos va a ir midiendo el número de ocurrencias
            oc += 1
            # Generamos el diccionario con los valores indicados por el profesor en operaciones
            op = {'Operaciones': {'Ganadora': {'instrumento': g['Item'][i], 'volumen': g['Size'][i],
                                               'sentido': g['Type'][i],
                                               'capital_ganadora': g['Profit'][i]},
                                  'Perdedora': {'instrumento': p['Item'][j], 'volumen': p['Size'][j],
                                                'sentido': p['Type'][j],
                                                'capital_perdedora': p['Profit'][j]}},
                  'ratio_cp_capital_acm': p['Profit'][j] / g['profit_acm_d'][i],
                  'ratio_cg_capital_acm': g['Profit'][i] / g['profit_acm_d'][i],
                  'ratio_cp_cg': p['Profit'][j] / g['Profit'][i]}
            # Ahora tenemos que agregarle el parámetro TimeStamp al diccionario
            gn = {'TimeStamp': g['CloseTime'][i]}
            # Ahora pasamos a calcular los datos necesarios para la asignación de la otra rama central
            # del diccionario, "Resultados"
            # Primero calculamos status quo tomando en cuenta el capital acm del ancla en el momento de la ocurrencia
            if np.abs(p['Profit'][j] / g['profit_acm_d'][i]) < np.abs(g['Profit'][i] / g['profit_acm_d'][i]):
                s_q += 1
            if np.abs(p['Profit'][j] / g['Profit'][i]) > 1.5:
                ave_per += 1
        # Me apoye en este punto en videos de Youtube explicativos de como usar diccionarios en Python
        # Aqui concatene la palabra Ocurrencia con el número de ocurrencia en cuestión, ya que así lo pedía el
        # profesor, además de que tuve que convertirlo en str
        n_oc = 'Ocurrencia, %s' % str(oc)
        # Asigno los valores encontrados al diccionario anteriormente encontrado
        diccionario['Ocurrencias']['Operaciones'][n_oc] = op
        diccionario['Ocurrencias']['TimeStamp'][n_oc] = gn

diccionario['Cantidad'] = oc
# Sacamos el porcentaje de cada métrica calculada respecto a ocurrencias en %
status_quo = (s_q/oc)*100
ave_per = (ave_per/oc)*100

sen_dec = '-'
if g['profit_acm_d'][0] < g['profit_acm_d'].iloc[-1] and g['Profit'][0] < g['Profit'].iloc[-1] or p['Profit'][0] < p['Profit'].iloc[-1] and (p['Profit'].min()/g['Profit'].max()) > 1.5:
    sen_dec = 'Sí'
else:
    sen_dec = 'No'

# Asignamos valores a un nuevo DataFrame que asignamos a la rama de 'Resultados'
mad_data = {'Ocurrencias': [oc], 'Status Quo': [status_quo],
            'Aversión a la pérdida': [ave_per],
            'Sensibilidad Decreciente': [sen_dec]}
diccionario['Resultados'] = pd.DataFrame(mad_data)
diccionario


# Sesgos
# sesgos = fn.f_be_de(param_data=df_data)


# ---------- 4. VISUALIZACIONES

# --- 4.1 Grafica 1: Ranking
ranking = vn.ranking(estadisticas_ba=df_data)

# --- 4.1 Grafica 2: DrawDown y DrawUp
drawd_drawup = vn.drawd_drawup(profit_d=df_data)
