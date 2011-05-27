from plone.indexer.decorator import indexer
from rer.bandi.interfaces import IBando

@indexer(IBando)
def destinatari_bando(object, **kw):
     return object.getDestinatari()