#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt




def RemoveNan(df):
    df.fillna(0, inplace=True)
    return df 


def RenameTS(df, x_label, y_label):
    return pd.DataFrame({x_label: df[df.columns[0]], y_label: df[df.columns[1]]})


def MakePlot(dfs, x_name, y_name, figsize = (20,12), mk = 'x', mk_z=14, linestyle='-', mfc='none'):
    e1x = dfs[0][0].plot(x=x_name, y=dfs[0][1],
                      marker=mk, markersize=mk_z, linestyle=linestyle,
                      mfc=mfc, figsize=figsize)
    for df in dfs[1:]:
        df[0].plot(x=x_name, y=df[1],
                      marker=mk, markersize=mk_z, linestyle=linestyle,
                      mfc=mfc, figsize=figsize, ax=e1x)

    plt.xlabel(x_name)
    plt.ylabel(y_name)
    #plt.savefig('trans.png', dpi=326)
    plt.legend()
        
