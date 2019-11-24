# -*- coding: utf-8 -*-
from datetime import datetime
from DateTime import DateTime
from plone.indexer.decorator import indexer
from rer.bandi.interfaces.bando import IBando

import six


def dateToDatetime(d):
    return datetime.combine(d, datetime.min.time())


@indexer(IBando)
def destinatari_bando(object, **kw):
    destinatari = getattr(object, 'destinatari', [])
    if not destinatari:
        return []
    if six.PY2:
        return [x.encode('utf-8') for x in destinatari]
    return destinatari


@indexer(IBando)
def getChiusura_procedimento_bando(object, **kw):

    date_chiusura_procedimento_bando = getattr(
        object, 'chiusura_procedimento_bando', None
    )
    if date_chiusura_procedimento_bando:
        datetime_chiusura_procedimento_bando = dateToDatetime(
            date_chiusura_procedimento_bando
        )
    else:
        return DateTime('2100/12/31')

    if datetime_chiusura_procedimento_bando:
        return DateTime(datetime_chiusura_procedimento_bando)


@indexer(IBando)
def getScadenza_bando(object, **kw):
    datetime_scadenza_bando = getattr(object, 'scadenza_bando', None)
    if not datetime_scadenza_bando:
        return DateTime('2100/12/31')
    zope_dt_scadenza_bando = DateTime(datetime_scadenza_bando)
    if zope_dt_scadenza_bando.Time() == '00:00:00':
        return zope_dt_scadenza_bando + 1
    else:
        return zope_dt_scadenza_bando


@indexer(IBando)
def getTipologia_bando(object, **kw):
    tipologia = getattr(object, 'tipologia_bando', '')
    if six.PY2:
        return tipologia.encode('utf-8')
    return tipologia


@indexer(IBando)
def getFinanziatori_bando(object, **kw):
    finanziatori = getattr(object, 'finanziatori', [])
    if not finanziatori:
        return []
    if six.PY2:
        return [x.encode('utf-8') for x in finanziatori]
    return finanziatori


@indexer(IBando)
def getMaterie_bando(object, **kw):
    materie = getattr(object, 'materie', [])
    if not materie:
        return []
    if six.PY2:
        return [x.encode('utf-8') for x in materie]
    return materie
