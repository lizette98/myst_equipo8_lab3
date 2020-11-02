
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 3 Behavioral Finance MYST                                                      -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: lizette98                                                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/lizette98/myst_equipo8_lab3                                          -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# ---------- 4. Visualizations
import functions as fn
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as py
py.offline.init_notebook_mode(connected = False)

df_data = fn.f_leer_archivo(param_archivo='files/historicos_alcg.csv')

pip_size = fn.f_pip_size(param_ins='eurusd')

df_data = fn.f_columnas_tiempos(param_data=df_data)

df_data = fn.f_columnas_pips(param_data=df_data)

profit_acum_d = fn.f_profit_acm_d(param_data=df_data)

evolucion_capital = fn.f_evolucion_capital(param_data=df_data)

MAD = fn.f_estadisticas_mad(param_data=df_data)


# --- 4.1 Grafica de ranking
estadisticas_ba = fn.f_estadisticas_ba(df_data)

def ranking(estadisticas_ba):
    """
    Funcion para graficar el ranking de los activos obtenidos en functions.

    Parameters
    ----------
    estadisticas_ba: Function
            Función utilizada para calcular el ranking de asertividad de divisas.

    Returns
    -------
    PieChart_Rank: Pie Chart Graph
            Grafica de pastel que muestra el porcentaje que representa la asertividad
            del total de CFDs usados en la cuenta.
    """

    # Llamamos la funcion de ranking calculada en functions
    estadisticas_ba = fn.f_estadisticas_ba(df_data)
    # Obtenemos solo el df de ranking
    df_ranking = pd.DataFrame(estadisticas_ba['df_1_ranking'])
    df_1_ranking = df_ranking.reset_index()
    # Renombrar columnas del df
    df_ranking = df_1_ranking.rename(columns={"index": "pares", "rank": "rank"})

    # Grafica de pastel
    PieChart_Rank = go.Figure()
    labels = df_ranking['pares']
    values = df_ranking['rank']
    PieChart_Rank = go.Figure(data=[go.Pie(labels=labels, values=values,
                                      pull=[0.2, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                            0])])
    PieChart_Rank.update_layout(title="Ranking", font=dict(size=16))
    #pie_rank.update_traces(textposition='inside', textinfo='percent+label')
    py.iplot(PieChart_Rank)


# --- 4.2 Gráfica drawdown y drawup
profit_d = fn.f_evolucion_capital(df_data)

def drawd_drawup(profit_d):
    """
    Funcion para graficar el drawdown y drawup de la cuenta de trading.

    Parameters
    ----------
    profit_d: Function
            Función utilizada para obtener el dataframe con los datos necesarios.

    Returns
    -------
    profits: Graph
            Grafica de linea que muestra el profit acumulado en la cuenta y su respectivo
            drawdown y drawup.
    """
    # Llamamos la funcion con el dataframe de evolucion de capital
    profit_d = fn.f_evolucion_capital(df_data)

    profits = go.Figure()
    profits.add_trace(go.Scatter(x=profit_d.timestamp,
                               y=[None, None, None, None, None, None, None, 99775.28, None, None, 134035.28, None, None, None,
                                  None], name='drawup',
                               connectgaps=True, mode='lines', line={'dash': 'dash', 'color': 'green'}))
    profits.add_trace(go.Scatter(x=profit_d.timestamp,
                               y=[100027.15, None, None, None, None, None, None, 99775.28, None, None, None, None, None, None,
                                  None], name='drawdown',
                               connectgaps=True, mode='lines', line={'dash': 'dash', 'color': 'red'}))
    profits.add_trace(go.Scatter(x=profit_d.timestamp, y=profit_d.profit_acm_d, name='profit acumulado', mode='lines',
                               marker=dict(color='Black')))

    profits.update_layout(title="Evolución del Capital Acumulado Diario", xaxis_title="Tiempo (fechas)", yaxis_title="Profit ($)")

    # profs.show()
    py.iplot(profits)




































































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


