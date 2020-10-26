
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

