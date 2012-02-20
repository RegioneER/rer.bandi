from plone.indexer.decorator import indexer
from rer.bandi.interfaces import IBando
from DateTime import DateTime

@indexer(IBando)
def destinatari_bando(object, **kw):
     return object.getDestinatari()
 
@indexer(IBando)
def getChiusura_procedimento_bando(object, **kw):
    if object.getChiusura_procedimento_bando():
        return object.getChiusura_procedimento_bando()
    return DateTime("2100/12/31")

@indexer(IBando)
def getScadenza_bando(object, **kw):
    if object.getScadenza_bando():
        return object.getScadenza_bando()
    return DateTime("2100/12/31")