#!/usr/bin/env python
import cymetric as cym
from cymetric import graphs as cgr
from cymetric import timeseries as tm
import pandas as pd


def Trans(file, rec=(), send=(), nucs_=(), coms=()):
    db = cym.dbopen(file)
    ev = cym.Evaluator(db=db, write=False)
    df1 = tm.transactions(ev, receivers=rec, senders=send,
                          nucs=nucs_, commodities=coms)
    return df1


def InvFrac(file, facility, nucs1=[''], nucs2=[''], factor1=1, factor2=1):
    db = cym.dbopen(file)
    ev = cym.Evaluator(db=db, write=False)
    df1 = tm.inventories(ev, facilities=facility, nucs=nucs1)
    df2 = tm.inventories(ev, facilities=facility, nucs=nucs2)
    df_r = df2
    df_r[df_r.columns[1]] = (df2[df2.columns[1]] / factor2) / \
        (df1[df1.columns[1]] / factor1 + df2[df2.columns[1]] / factor2)
    return df_r


def TransFrac(file, rec=[''], send=[''], nucs1=[''], nucs2=[''], factor1=1, factor2=1):
    db = cym.dbopen(file)
    ev = cym.Evaluator(db=db, write=False)
    df1 = tm.transactions(ev, receivers=rec, senders=send, nucs=nucs1)
    df2 = tm.transactions(ev, receivers=rec, senders=send, nucs=nucs2)
    df_r = df2
    df_r[df_r.columns[1]] = (df2[df2.columns[1]] / factor2) / \
        (df1[df1.columns[1]] / factor1 + df2[df2.columns[1]] / factor2)
    return df_r


def MakeFlowGraph(file, label=''):
    db_ = cym.dbopen(file)
    ev_ = cym.Evaluator(db=db_, write=False)
    return cgr.flow_graph(evaler=ev_, label=label)


# mode 0 non cumulative
# mode 1 cumul
# mode 2 mean
def month2year(df, mode=0, division=12):
    dfn = pd.DataFrame(columns=['Time', 'Mass'])
    df.rename(index=str, columns={"Quantity": "Mass"})
    val = 0
    for index, row in df.iterrows():
        if mode == 0:
            val = row['Mass']
        else:
            val += row['Mass']
        if row['Time'] % division == 0:
            if mode == 2:
                val *= 1. / float(division)
            dfn.loc[int(row['Time'] / division)] = int(row['Time'] / 12)
            dfn.loc[int(row['Time'] / division)]['Mass'] = val
            val = 0
    return dfn


def maxperdiv(df, division=12):
    dfn = pd.DataFrame(columns=['Time', 'Mass'])
    val = 0
    for index, row in df.iterrows():
        if val < row['Mass']:
            val = row['Mass']
        if row['Time'] % division == 0:
            dfn.loc[int(row['Time'] / division)] = int(row['Time'] / 12)
            dfn.loc[int(row['Time'] / division)]['Mass'] = val
            val = 0
    return dfn


def increaseonly(df):
    dfn = pd.DataFrame(columns=['Time', 'Mass'])
    val = 0
    for index, row in df.iterrows():
        if val < row['Mass']:
            val = row['Mass']
            dfn.loc[int(row['Time'])] = int(row['Time'])
            dfn.loc[int(row['Time'])]['Mass'] = row['Mass']
            val = row['Mass']
    return dfn
