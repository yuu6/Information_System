#!/usr/env/bin python3
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
# ch_font = font_manager.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
from SIR.SIR import SIR
from  manage.nx import get_graph,delDegreeOne

def run_SI_simulation(G, beta, seeds, iterations=500):
    number_of_index = G.order()
    total_i, total_t = np.zeros(number_of_index), np.zeros(number_of_index)
    for i in range(iterations):
        sim = SIR(G, infection_rate=beta, recovery_rate =0, infection_seeds=seeds)
        sim.simulate()
        i, t = sim.get_i_of_t()
        total_i += i
        total_t += t
    average_i = total_i/iterations
    average_t = total_t/iterations
    return np.array([average_i, average_t])

G = delDegreeOne(get_graph())

i_1, i_t_1 = run_SI_simulation(G, 0.004, 'BARABASI, A')
i_2, i_t_2 = run_SI_simulation(G, 0.004, 'NEWMAN, M')
i_3, i_t_3 = run_SI_simulation(G, 0.004, 'CAGNEY, G')

# plot
plt.plot(i_t_1, i_1, 'r', label='度数前10节点')
plt.plot(i_t_2, i_2, 'b', label='介数前10节点')
plt.plot(i_t_3, i_3, 'g', label='传播功率前10节点')
plt.xlabel("感染天数")
plt.ylabel("感染比例")
plt.title("悲惨世界人物关系网络SI仿真")
plt.legend(loc=0)
# plt.savefig('SI_LM_1.png')
plt.show()



