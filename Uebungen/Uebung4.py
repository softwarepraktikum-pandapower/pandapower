# -*- coding: utf-8 -*-
"""
Created on Sat May 12 15:22:05 2018

"""
import pandapower as pp
import pandapower.networks as nw
import pandas as pd
from numpy.random import choice
import copy


def load_network():
    return nw.mv_oberrhein(scenario="generation")

def violations(net):
    pp.runpp(net)
    if net.res_line.loading_percent.max() > 50:
        return (True, "Line \n Overloading")
    elif net.res_trafo.loading_percent.max() > 50:
        return (True, "Transformer \n Overloading")
    elif net.res_bus.vm_pu.max() > 1.04:
        return (True, "Voltage \n Violation")
    else:
        return (False, None)


def chose_bus(net):
    return choice(net.load.bus.values)

from numpy.random import normal

def get_plant_size_kw():
    return normal(loc=500, scale=50)

iterations = 50
results = pd.DataFrame(columns=["installed", "violation"])

for i in range(iterations):
    net = load_network()
    installed_kw = 0
    while 1:
#        net_copy = copy.deepcopy(net)
        violated, violation_type = violations(net)
        if violated:
            results.loc[i] = [installed_kw, violation_type]
            break
        else:
            plant_size = get_plant_size_kw()
            pp.create_sgen(net, chose_bus(net), p_kw=-plant_size, q_kvar=0)
            installed_kw += plant_size
