#!/usr/bin/env python
import cymetric as cym
from cymetric import graphs as cgr
from cymetric import timeseries as tm
import pandas as pd


def Trans(file, rec=(), send=(), nucs_=(), coms=()):
    ''' Return the transactions between senders (send) and receivers (rec),
    filtered by nuclide (nucs) and commodities (coms)
    '''
    db = cym.dbopen(file)
    ev = cym.Evaluator(db=db, write=False)
    df1 = tm.transactions(ev, receivers=rec, senders=send,
                          nucs=nucs_, commodities=coms)
    return df1


def InvFrac(file, facility, nucs1=(), nucs2=(), factor1=1, factor2=1):
    ''' Return the fraction nucs1 / (nucs1+nucs2) the inventory of the
    facilities (fac), weighting factor can be added on nucs1 and nucs2
    '''
    db = cym.dbopen(file)
    ev = cym.Evaluator(db=db, write=False)
    df1 = tm.inventories(ev, facilities=facility, nucs=nucs1)
    df2 = tm.inventories(ev, facilities=facility, nucs=nucs2)
    df_r = df2
    df_r[df_r.columns[1]] = (df2[df2.columns[1]] / factor2) / \
        (df1[df1.columns[1]] / factor1 + df2[df2.columns[1]] / factor2)
    return df_r


def TransFrac(file='', ev=None, rec=(), send=(), nucs1=(), nucs2=(), factor1=1, factor2=1):
    ''' Return the fraction nucs1 / (nucs1+nucs2) in the transaction between
    senders and receivers, weighting factor can be added on nucs1 and nucs2
    '''
    if(file != ''):
        db = cym.dbopen(file)
        ev = cym.Evaluator(db=db, write=False)
    elif (ev == None):
        print('Need either a Filename or a cymetric evaler....')
        return None
    df1 = tm.transactions(ev, receivers=rec, senders=send, nucs=nucs1)
    df2 = tm.transactions(ev, receivers=rec, senders=send, nucs=nucs2)
    df_r = df2
    df_r[df_r.columns[1]] = (df2[df2.columns[1]] / factor2) / \
        (df1[df1.columns[1]] / factor1 + df2[df2.columns[1]] / factor2)
    return df_r


def MakeFlowGraph(file, label=''):
    ''' Generate the transaction flow graph between facilities
    '''
    db_ = cym.dbopen(file)
    ev_ = cym.Evaluator(db=db_, write=False)
    return cgr.flow_graph(evaler=ev_, label=label)


# mode 0 non cumulative
# mode 1 cumul
# mode 2 mean
def month2year(df, mode=0, division=12):
    ''' Convert Month timestep into X timestep (default is year)
        different mode corresponds to way to assess the quantity conversion:
        0: keep only the first value of the year
        1: mean value 
        2: cumulativ value 
    '''
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
    ''' Only keep the max value accross the time periode
    '''
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


def cumul(df):
    ''' Compute the cumulative of the panda dataframe 
    '''
    dfn = pd.DataFrame(columns=['Time', 'Mass'])
    val = 0
    for index, row in df.iterrows():
            val += row['Mass']
            dfn.loc[row['Time']] = row['Time']
            dfn.loc[row['Time']]['Mass'] = val
    return dfn


def increaseonly(df):
    ''' only keep increasing value 
    '''
    dfn = pd.DataFrame(columns=['Time', 'Mass'])
    val = 0
    for index, row in df.iterrows():
        if val < row['Mass']:
            val = row['Mass']
            dfn.loc[int(row['Time'])] = int(row['Time'])
            dfn.loc[int(row['Time'])]['Mass'] = row['Mass']
            val = row['Mass']
    return dfn
