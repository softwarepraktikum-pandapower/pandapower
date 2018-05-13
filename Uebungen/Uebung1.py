# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:32:04 2018

@author: Denise
"""

import pandapower as pp
import pandapower.plotting as plot
#from pandapower.plotting.plotly import pf_res_plotly
#pf_res_plotly(net)

#create empty net
net = pp.create_empty_network()

#create buses
bus0 = pp.create_bus(net, vn_kv=10, name="Bus 0", geodata=[1.5,0])
bus1 = pp.create_bus(net, vn_kv=0.4, name="Bus 1", geodata=[1.5,-1])
bus2 = pp.create_bus(net, vn_kv=0.4, name="Bus 2", geodata=[0,-2])
bus3 = pp.create_bus(net, vn_kv=0.4, name="Bus 3", geodata=[0,-3])
bus4 = pp.create_bus(net, vn_kv=0.4, name="Bus 4", geodata=[1.5,-4])
bus5 = pp.create_bus(net, vn_kv=0.4, name="Bus 5", geodata=[3,-2])
bus6 = pp.create_bus(net, vn_kv=0.4, name="Bus 6", geodata=[3,-3])

#Geodata hinzufügen
#net.bus_geodata.at[0, "x"] = 1.5
#net.bus_geodata.at[0, "y"] = 0

#create bus elements
pp.create_ext_grid(net, bus0)

pp.create_load(net, bus=bus2, p_kw=15, q_kvar=-10, name="Load2")
pp.create_load(net, bus=bus3, p_kw=5, q_kvar=0.1, name="Load3")
pp.create_load(net, bus=bus4, p_kw=25, q_kvar=-5, name="Load4")
pp.create_load(net, bus=bus6, p_kw=13.78, q_kvar=4.53, name="Load6")

pp.create_sgen(net, bus2, p_kw=-2, q_kvar=0.2, name="static generator2")
pp.create_sgen(net, bus3, p_kw=-10, q_kvar=0, name="static generator3")
pp.create_sgen(net, bus6, p_kw=-7, q_kvar=-1, name="static generator6")

pp.create_sgen(net, bus1, p_kw=-35, q_kvar=5, name="sgen WKA")

pp.create_gen(net, bus5, p_kw=-100, vm_pu=1.0, name="generator")

#create branch elements
line1 = pp.create_line(net, from_bus=bus1, to_bus=bus2, length_km=0.72, std_type="NAYY 4x50 SE", name="Line1")
line2 = pp.create_line(net, from_bus=bus2, to_bus=bus3, length_km=1.5, std_type="NAYY 4x50 SE", name="Line2")
line3 = pp.create_line(net, from_bus=bus3, to_bus=bus4, length_km=0.3, std_type="NAYY 4x50 SE", name="Line3")
line4 = pp.create_line(net, from_bus=bus1, to_bus=bus5, length_km=0.14, std_type="NAYY 4x50 SE", name="Line4")
line5 = pp.create_line(net, from_bus=bus5, to_bus=bus6, length_km=0.17, std_type="NAYY 4x50 SE", name="Line5")
line6 = pp.create_line(net, from_bus=bus6, to_bus=bus4, length_km=0.5, std_type="NAYY 4x50 SE", name="Line6")

pp.create_switch(net, bus4, line3, et="l", type="LBS", closed=False)

trafo = pp.create_transformer(net, hv_bus=bus0, lv_bus=bus1, std_type="0.63 MVA 10/0.4 kV", name="Trafo")