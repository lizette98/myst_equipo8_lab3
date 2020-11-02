
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""


def f_stats_mad(param_data):
    profit_dia = f_evolucion_capital(param_data)

    # Sharpe ratio
    rp = np.log(profit_dia.profit_acm_d[1:].values / profit_dia.profit_acm_d[:-1].values)
    rf = 0.05 / 300
    sdp = numpy.std(rp)

    # Drawdown Capital

    where_row = profit_dia.loc[profit_dia['profit_acm_d'] == profit_dia.profit_acm_d.min()]
    where_position = where_row.index.tolist()

    prev_where = profit_dia.loc[0:where_position[0]]
    where_max_prev = profit_dia.loc[profit_dia['profit_acm_d'] == prev_where.profit_acm_d.max()]
    where_min_prev = profit_dia.loc[profit_dia['profit_acm_d'] == prev_where.profit_acm_d.min()]
    max_ddown = where_max_prev.iloc[0]['profit_acm_d']
    min_ddown = where_min_prev.iloc[0]['profit_acm_d']
    ddown = max_ddown - min_ddown

    fecha_i_ddown = where_max_prev.iloc[0]['timestamp']
    fecha_f_ddown= where_min_prev.iloc[0]['timestamp']
    drawdown = "{}, {}, ${:.2f}".format(fecha_i_ddown, fecha_f_ddown, ddown)

    # Drawup Capital

    where_row_up = profit_dia.loc[profit_dia['profit_acm_d'] == profit_dia.profit_acm_d.max()]
    where_position_up = where_row_up.index.tolist()

    foll_where = profit_dia.loc[0:where_position_up[0]]
    where_max_foll = profit_dia.loc[profit_dia['profit_acm_d'] == foll_where.profit_acm_d.max()]
    where_min_foll = profit_dia.loc[profit_dia['profit_acm_d'] == foll_where.profit_acm_d.min()]
    max_dup = where_max_foll.iloc[0]['profit_acm_d']
    min_dup = where_min_foll.iloc[0]['profit_acm_d']
    dup = max_dup - min_dup

    fecha_f_dup = where_max_foll.iloc[0]['timestamp']
    fecha_i_dup = where_min_foll.iloc[0]['timestamp']
    drawup = "{}, {}, ${:.2f}".format(fecha_i_dup, fecha_f_dup, dup)




































































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


