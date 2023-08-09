# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 19:22:02 2019

@author: jz1476
"""
import numpy as np
from pyproj import Transformer, transform
import pandas as pd

# Specify the coordinate system: EPSG: 4326 = WGS84
transformer = Transformer.from_proj(4326, 3628)

data = pd.read_csv('TransitAgenda.csv',header=None)
data.columns = ['ID', 'OTAZ','DTAZ','O_x','O_y','D_x','D_y','Time']

#Specify the dataframe columns that contain the coordinate data.
#homex = data['homey'].values
#homey = data['homex'].values

o_x = data['O_y'].values
o_y = data['O_x'].values

d_x = data['D_y'].values
d_y = data['D_x'].values


#homex_new, homey_new = transform(4326, 3628, homey, homex)

o_x_new, o_y_new = transform(4326, 3628, o_y, o_x)

d_x_new, d_y_new = transform(4326, 3628, d_y, d_x)


#new = {"homex_new":homex_new, "homey_new":homey_new,"o_x_new":o_x_new,"o_y_new":o_y_new,"d_x_new":d_x_new,"d_y_new":d_y_new}

new = {"o_x_new":o_x_new,"o_y_new":o_y_new,"d_x_new":d_x_new,"d_y_new":d_y_new}
new_coord = pd.DataFrame(new)

new_data = data.join(new_coord)

# new_data = new_data[['unique_person_id',
#  'geo',
#  'unique_id_in_geo',
#  'pid',
#  'sample_geo',
#  'page',
#  'pschool',
#  'rpsex',
#  'rpworker',
#  'pworker',
#  'rpdisability',
#  'pworker1',
#  'prace',
#  'trip_purp',
#  'trip_purp_o',
#  'hid',
#  'persontype',
#  'person',
#  'homex',
#  'homey',
#  'homex_new',
#  'homey_new',
#  'plsam',
#  'person_tour',
#  'pertype',
#  'orig_home',
#  'dest_home',
#  'tour_purp',
#  'htaz',
#  'otaz',
#  'dtaz',
#  'trp_dep_hr',
#  'trp_dep_min',
#  'trp_arr_hr',
#  'trp_arr_min',
#  'trpdur',
#  'actdur',
#  'wht_fac3',
#  'pmode',
#  'pmode1',
#  'pmode_r2',
#  'o_x',
#  'o_y',
#  'd_x',
#  'd_y',
#  'o_x_new',
#  'o_y_new',
#  'd_x_new',
#  'd_y_new',
#  'trip_id',
#  'man_nonman']]

new_data = new_data[[
'ID',
'OTAZ',
'DTAZ',
'O_x',
'O_y',
'D_x',
'D_y',
'o_x_new',
'o_y_new',
'd_x_new',
'd_y_new',
'Time'

]]
 
new_data.to_csv('ModeUpdatedNew_newCoord.csv',index = False, header = True)