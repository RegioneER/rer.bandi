# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.Five import BrowserView
from rer.bandi import bandiMessageFactory as _
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implements, Interface
try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory

class ICollectionBandiView(Interface):
    pass


class CollectionBandiView(BrowserView):
    implements(ICollectionBandiView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.voc_tipologia = getUtility(IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)

    def getBandoState(self,bando):
        """
        """
        if not bando.scadenza_bando.isPast():
            return ('open',translate(_(u'Open'),context=self.request))
        else:
            if bando.chiusura_procedimento_bando.isPast():
                return ('closed',translate(_(u'Closed'),context=self.request))
            else:
                return ('inProgress',translate(_(u'In progress'),context=self.request))
        return ()