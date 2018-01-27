#!/usr/bin/env python
import numpy as np
import pandas as pd

###################
# STOLEN from https://github.com/CNERG/enrich_calcs/blob/master/calc_enrich.py

# Determines the total feed flow rates required at each stage
# of the cascade for steady-state flow
def calc_feed_flows(n_stages_enrich, n_stages_strip, cascade_feed, cut):
    n_stages = n_stages_strip + n_stages_enrich

    eqn_answers = np.zeros(n_stages)
    if len(cut) != n_stages_enrich+n_stages_strip:
        print("oupsy bad dimension")
        return 0

    for i in range(-1 * n_stages_strip, n_stages_enrich):
        eqn = np.zeros(n_stages)
        position = n_stages_strip + i
        eqn[position] = -1
        if (position != 0):
            eqn[position - 1] = cut[position-1]
        if (position != n_stages - 1):
            eqn[position + 1] = (1 - cut[position-1])
        if (position == 0):
            eqn_array = eqn
        else:
            eqn_array = np.vstack((eqn_array, eqn))
        if (i == 0):
            eqn_answers[position] = -1 * cascade_feed

    return np.linalg.solve(eqn_array, eqn_answers)

def calc_feed_flows_no_back(n_stages_enrich, n_stages_strip, cascade_feed, cut):
    n_stages = n_stages_strip + n_stages_enrich

    eqn_answers = np.zeros(n_stages)
    if len(cut) != n_stages_enrich+n_stages_strip:
        print("oupsy bad dimension")
        return 0

    for i in range(-1 * n_stages_strip, n_stages_enrich):
        eqn = np.zeros(n_stages)
        position = n_stages_strip + i
        eqn[position] = -1
        if (position != 0):
            eqn[position - 1] = cut[position-1]
        if (position != n_stages - 1):
            eqn[position + 1] = 0
        if (position == 0):
            eqn_array = eqn
        else:
            eqn_array = np.vstack((eqn_array, eqn))
        if (i == 0):
            eqn_answers[position] = -1 * cascade_feed

    return np.linalg.solve(eqn_array, eqn_answers)
