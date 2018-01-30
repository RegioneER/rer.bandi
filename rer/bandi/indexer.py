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
    return getattr(object, 'destinatari', None)


@indexer(IBando)
def getChiusura_procedimento_bando(object, **kw):

    date_chiusura_procedimento_bando = getattr(
        object, 'chiusura_procedimento_bando', None)
    if date_chiusura_procedimento_bando:
        datetime_chiusura_procedimento_bando = dateToDatetime(
            date_chiusura_procedimento_bando)
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
def getEnte_bando(object, **kw):
    return getattr(object, 'ente_bando', None)


@indexer(IBando)
def getTipologia_bando(object, **kw):
    return getattr(object, 'tipologia_bando', None)


# @indexer(IBando)
# def SearchableTextBandi(obj):
#     pt = getToolByName(api.portal.get(), 'portal_transforms')
#     stream = pt.convertTo('text/plain', obj.text.output, mimetype='text/html')
#
#     text = []
#     li = []
#     li.append(obj.Title())
#     li.append(obj.Description())
#     li.append(stream.getData().strip())
#
#     for string in li:
#         for word in string.split():
#             if word not in text:
#                 if isinstance(word, unicode):
#                     text.append(word.encode('utf-8'))
#                 else:
#                     text.append(word)
#
#     return ' '.join(text)
