import geopandas as gpd
import numpy as np
import rasterio as rio
from bokeh.plotting import figure
from xyzservices import TileProvider
from bokeh.tile_providers import get_provider
from bokeh.models.mappers import CategoricalColorMapper, LinearColorMapper
from bokeh.models import HoverTool, ColorBar, GeoJSONDataSource



def plot_map(raster, states, date, forecast=True, band=1):
    arr = raster.read(band)
    arr[arr == raster.nodata] = 0
    arr = arr - 1
    arr = arr.astype(np.int8)

    geosource = GeoJSONDataSource(geojson=states.to_json())

    google_tiles = get_provider(TileProvider(
        name='Google Satellite',
        url='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attribution='Google'
    ))

    p = figure(title=f"{'Model Forecasted' if forecast else 'USDM'} Drought for {date}",
            x_axis_label='X [m]',
            y_axis_label='Y [m]',
            match_aspect=True,
            plot_width=650,
            plot_height=450,
            x_range=(-13877352, -7462261),
            y_range=(2900000, 6350000))

    p.add_tile(google_tiles)

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    drought_image = p.image(
        image=[np.flipud(arr)],
        x=raster.bounds[0],
        y=raster.bounds[1],
        dw=raster.bounds[2]-raster.bounds[0],
        dh=raster.bounds[3]-raster.bounds[1]
    )

    p.patches(
        'xs', 'ys', source=geosource, 
        line_color='black',
        line_width = 0.5,
        line_alpha=1,
        fill_alpha=0
    )

    drought_image.glyph.color_mapper = LinearColorMapper(
        low=-1, high=4,
        palette=['rgba(0, 0, 0, 0)', '#FFFF00', '#FCD37F', '#FFAA00', '#E60000', '#730000']
    )

    legend_mapper = CategoricalColorMapper(
        factors=['No Drought', 'D0', 'D1', 'D2', 'D3', 'D4'],
        palette=['rgba(0, 0, 0, 0)', '#FFFF00', '#FCD37F', '#FFAA00', '#E60000', '#730000'] 
    )

    color_bar = ColorBar(color_mapper=legend_mapper, label_standoff=12)

    drought_hover = HoverTool(tooltips=[('Category', 'D@image{0}')],
                        renderers=[drought_image])

    p.add_tools(drought_hover)
    p.add_layout(color_bar, 'above')
    return p
