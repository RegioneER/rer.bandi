# -*- coding: utf-8 -*-

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory
    
from zope.component import getUtility
from zope.interface import implements, Interface

from Products.Five import BrowserView

from rer.bandi import bandiMessageFactory as _

class ICollectionBandiView(Interface):
    pass


class CollectionBandiView(BrowserView):
    implements(ICollectionBandiView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.voc_tipologia = getUtility(IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)

