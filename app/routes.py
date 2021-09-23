from flask import render_template, flash, redirect, url_for
from app import app
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.layouts import gridplot
import datetime as dt
from .utils.plot_map import plot_map
import os
import rasterio as rio
import geopandas as gpd


@app.route('/')
@app.route('/index')
def index():
    raster = rio.open('/Users/colinbrust/projects/droughtcast-viz/data/template.tif')
    r2 = rio.open('/Users/colinbrust/projects/DroughtCast/data/models/all_results/median/20070619_preds_None.tif')
    states = gpd.read_file('/Users/colinbrust/projects/droughtcast-viz/data/states.shp')
    date = dt.date(2015, 1, 1)

    p1 = plot_map(raster, states, date, False)
    p2 = plot_map(r2, states, date, True)

    p2.x_range = p1.x_range
    p2.y_range = p1.y_range
    out = gridplot([[p1, p2]])

    plot_script, plot_div = components(out)
    cdn_js = CDN.js_files[0]
    return render_template('base.html', title='egg', plot_script=plot_script, plot_div=plot_div, cdn_js=cdn_js)
