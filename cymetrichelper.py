#!/usr/bin/env python
import cymetric as cym
from cymetric import graphs as cgr
from cymetric import timeseries as tm



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
