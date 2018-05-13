# -*- coding: utf-8 -*-
"""
Created on Sat May  5 16:01:27 2018


"""

import pandapower as pp

net = pp.from_pickle("net_uebung_2.p")

pp.create_line(net, from_bus=37, to_bus=44, 
                        length_km=1.50, std_type="NA2XS2Y 1x185 RM/25 12/20 kV",
                        name="MV Line8")
pp.create_line(net, from_bus=51, to_bus=52, 
                        length_km=0.12, std_type="NAYY 4x120 SE",
                        name="LV Line2.2")

#net.switch.closed.loc[57] = True

net.load.p_kw.loc[18] = 10
net.load.p_kw.loc[4] = 38000

net.trafo.hv_bus.loc[1] = 41
net.trafo.lv_bus.loc[1] = 45

pp.runpp(net)