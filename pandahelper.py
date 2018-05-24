#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt




def RemoveNan(df):
    df.fillna(0, inplace=True)
    return df 


def RenameTS(df, x_label, y_label):
    return pd.DataFrame({x_label: df[df.columns[0]], y_label: df[df.columns[1]]})


def MakePlot(dfs, x_name, y_name, figsize = (20,12), mk = 'x', mk_z=14,
        linestyle='-', color=None, mfc='none', loc='best', lw=2.0):
    SMALL_SIZE = 40
    MEDIUM_SIZE = SMALL_SIZE+2
    BIGGER_SIZE = MEDIUM_SIZE +2

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    
    
    
    e1x = dfs[0][0].plot(x=x_name, y=dfs[0][1],
                      marker=mk, markersize=mk_z, linestyle=linestyle[0],
                      mfc=mfc, color=color[0], linewidth=lw, figsize=figsize)
    for i, df in enumerate(dfs[1:]):
        df[0].plot(x=x_name, y=df[1],
                      marker=mk, markersize=mk_z, linestyle=linestyle[i+1],
                      mfc=mfc,color=color[i+1], linewidth=lw, figsize=figsize, ax=e1x)

    plt.xlabel(x_name)
    plt.ylabel(y_name)
    #plt.savefig('trans.png', dpi=326)
    plt.legend(loc=loc)
        
