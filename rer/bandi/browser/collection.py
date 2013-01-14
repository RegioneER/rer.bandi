# -*- coding: utf-8 -*-
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

    def getBandoState(self, bando):
        """
        return corretc bando state
        """
        scadenza_bando = bando.scadenza_bando
        chiusura_procedimento_bando = bando.chiusura_procedimento_bando
        state = ('open', translate(_(u'Open'), context=self.request))
        if scadenza_bando and scadenza_bando.isPast():
            if chiusura_procedimento_bando and chiusura_procedimento_bando.isPast():
                state = ('closed', translate(_(u'Closed'), context=self.request))
            else:
                state = ('inProgress', translate(_(u'In progress'), context=self.request))
        else:
            if chiusura_procedimento_bando and chiusura_procedimento_bando.isPast():
                state = ('closed', translate(_(u'Closed'), context=self.request))
        return state
