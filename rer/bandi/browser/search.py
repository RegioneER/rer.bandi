# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.app.schema.vocabulary import IVocabularyFactory

from Products.Five.browser import BrowserView


class SearchBandiForm(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        voc_tipologia = getUtility(IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)
        self.terms_tipologia = list(voc_tipologia)

        voc_destinatari = getUtility(IVocabularyFactory, name='rer.bandi.destinatari.vocabulary')(self.context)
        self.terms_destinatari = list(voc_destinatari)


