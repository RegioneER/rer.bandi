# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.indexer.decorator import indexer
from rer.bandi.interfaces.bando import IBando

# importo il datetime di python
from datetime import datetime

# funzione che riceve un date e torna un datetime con l'ora a zero


def dateToDatetime(d):
    return datetime.combine(d, datetime.min.time())


@indexer(IBando)
def destinatari_bando(object, **kw):
    return [x.encode('utf-8') for x in getattr(object, 'destinatari', [])]


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
    return tipologia.encode('utf-8')


@indexer(IBando)
def getFinanziatori_bando(object, **kw):
    return [x.encode('utf-8') for x in getattr(object, 'finanziatori', [])]


@indexer(IBando)
def getMaterie_bando(object, **kw):
    return [x.encode('utf-8') for x in getattr(object, 'materie', [])]
