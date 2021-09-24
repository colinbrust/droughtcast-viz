from flask import render_template, flash, redirect, url_for, request
from app import app
from dateutil.relativedelta import relativedelta
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.layouts import gridplot
import datetime as dt
from .utils.plot_map import plot_map
from .utils.dict_mapper import mapper
from pathlib import Path
import rasterio as rio
import geopandas as gpd
import os


@app.route('/', methods=['GET', 'POST'])
def index():

    stat = request.args.get('stat') or 'median'
    holdout = request.args.get('holdout') or 'None'
    lead_time = request.args.get('lead_time') or 2

    date_options = Path(f'./data/{stat}/').glob(f'*{holdout}.tif')
    date_options = [dt.datetime.strptime(x.stem,f'%Y%m%d_preds_{holdout}').date() for x in date_options]
    date_options = sorted(date_options)
    date = request.args.get('date') or date_options[0]

    stat_options = set(['min', 'median', 'max', 'iqr'])
    stat_options = list(stat_options.intersection([x.stem for x in Path('./data').iterdir()]))

    holdout_options = set(['None', 'pr', 'rmax', 'rmin', 'sm-rootzone', 'sm-surface', 'srad', 'tmmn', 'tmmx', 'vpd', 'vs', 'GPP', 'ET'])
    holdout_options = holdout_options.intersection([x.stem.split('_')[-1] for x in Path('./data/median/').glob('*.tif')])

    if not isinstance(date, dt.date):
        date = dt.datetime.strptime(date, '%Y-%m-%d').date()
    
    print(type(date))
    print(type(lead_time))
    usdm_date = str(date + relativedelta(weeks=int(lead_time))).replace('-', '')

    forecast = rio.open(f"./data/{stat}/{str(date).replace('-', '')}_preds_{holdout}.tif")
    usdm = rio.open(f"./data/usdm/{usdm_date}_USDM.tif")

    states = gpd.read_file('./data/states.shp')

    p1 = plot_map(forecast, states, date, True, int(lead_time))
    p2 = plot_map(usdm, states, date, False, 1)

    p2.x_range = p1.x_range
    p2.y_range = p1.y_range
    out = gridplot([[p1, p2]])

    plot_script, plot_div = components(out)

    return render_template(
        'base.html', 
        title='DroughtCast', 
        dates=date_options,
        holdouts=holdout_options,
        holdout_mapper=mapper['holdouts'],
        stats=stat_options,
        stat_mapper=mapper['stat'],
        lead_times=list(range(1, 13)),
        plot_script=plot_script, 
        plot_div=plot_div, 
        cdn_js=CDN.js_files[0]
    )
