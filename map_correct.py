# -*- coding: utf-8 -*-
"""
Created on Sun May 29 23:13:58 2022

@author: marti
"""

import geopandas as gpd
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure
from bokeh.tile_providers import CARTODBPOSITRON, get_provider # CARTODBPOSITRON_RETINA
from bokeh.io import output_notebook
#output_notebook()
from bokeh.resources import INLINE
output_notebook(INLINE)
#from connection import insert_df
from connection import engine
#from connection import trees
#from prova import trees

"""IMPORTING DATA"""
# import geo data
#engine = insert_df()
trees = gpd.GeoDataFrame.from_postgis('trees', engine, geom_col='geometry')
trees = trees.drop('geometry', axis=1).copy()


"""MAP"""
#Use the dataframe as Bokeh ColumnDataSource
psource = ColumnDataSource(trees)
#Specify feature of the Hover tool
TOOLTIPS = [
    ("name", "@commonName"),
    ("height", "@height")
]
#range bounds supplied in web mercator coordinates epsg=3857
p1 = figure(x_range=((trees.x.min()-20), (trees.x.max()+20)), y_range=((trees.y.min()-20), (trees.y.max()+20)),
          plot_width=700, plot_height=700, tooltips=TOOLTIPS
           ,x_axis_type="mercator", y_axis_type="mercator"
           )   
#Add basemap tile
p1.add_tile(get_provider(CARTODBPOSITRON)) #(get_provider(Vendors.CARTODBPOSITRON_RETINA)) 
#Add Glyphs
p1.circle('x', 'y', source=psource, color='blue', radius=10) #('x', 'y', source=psource, color='blue', radius=20) #size=10
#Add Labels and add to the plot layout
labels = LabelSet(x='x', y='y', text='ID', level="glyph",
              x_offset=5, y_offset=5, source=psource, render_mode='css')
p1.add_layout(labels)

# Save the plot
#output_file(r"C:\Users\marti\OneDrive\Polimi\1 ANNO MAGISTRALE\SOFTWARE ENGINEERING FOR GEOINFORMATICS\map.html")
#plot the map
#show(p1)