# -*- coding: utf-8 -*-
"""
Created on Mon May  7 18:46:16 2018

"""

import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as plot

net = nw.mv_oberrhein(scenario="generation")

net.sgen.p_kw = net.sgen.p_kw*3.4
pp.runpp(net)

print("Überlastete Leitungen vor der Änderung")
print(net.res_line[net.res_line.loading_percent > 100])
print()
print(net.line.std_type[net.res_line.loading_percent > 100])

pp.change_std_type(net, 54, "243-AL1/39-ST1A 20.0", element="line")
pp.change_std_type(net, 179, "243-AL1/39-ST1A 20.0", element="line")
pp.change_std_type(net, 192, "243-AL1/39-ST1A 20.0", element="line")

pp.runpp(net)
#Leitungen
cmap_list=[(0, "green"), (100, "yellow"), (100.5, "red"), (105, "red")]
cmap, norm = plot.cmap_continous(cmap_list)
lc = plot.create_line_collection(net, net.line.index, zorder=1, cmap=cmap, norm=norm, linewidths=2)
#plot.draw_collections([lc], figsize=(10,8))

#Busse
cmap_list=[(0.95, "blue"), (1.0, "green"), (1.05, "red")]
cmap, norm = plot.cmap_continous(cmap_list)
bc = plot.create_bus_collection(net, net.bus.index, size=80, zorder=2, cmap=cmap, norm=norm)
plot.draw_collections([lc, bc], figsize=(10,8))

print()
print()
print("Überlastete Leitungen nach der Änderung")
print(net.res_line[net.res_line.loading_percent > 100])
print()
print(net.line.std_type[net.res_line.loading_percent > 100])