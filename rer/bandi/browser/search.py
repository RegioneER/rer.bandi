# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.i18n import translate
from rer.bandi import bandiMessageFactory as _
try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory

from zope.component import getUtility


class SearchBandiForm(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        voc_tipologia = getUtility(IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)
        self.terms_tipologia = list(voc_tipologia)

        voc_destinatari = getUtility(IVocabularyFactory, name='rer.bandi.destinatari.vocabulary')(self.context)
        self.terms_destinatari = list(voc_destinatari)

    def getDefaultEnte(self):
        """
        return the default ente
        """
        portal_properties = getToolByName(self, 'portal_properties')
        rer_bandi_settings = getattr(portal_properties, 'rer_bandi_settings', None)
        if rer_bandi_settings:
            return rer_bandi_settings.getProperty('default_ente', '')
        return ''


class SearchBandi(BrowserView):
    """
    A view for search bandi results
    """
    def searchBandi(self):
        """
        return a list of bandi
        """
        pc = getToolByName(self.context, 'portal_catalog')
        stato = self.request.form.get('stato_bandi', '')
        search_type = self.request.form.get('search_type', '')
        SearchableText = self.request.form.get('SearchableText', '')
        query = self.request.form.copy()
        if stato:
            now = DateTime()
            if stato == "open":
                query['getScadenza_bando'] = {'query': now, 'range': 'min'}
                query['getChiusura_procedimento_bando'] = {'query': now, 'range': 'min'}
            if stato == "inProgress":
                query['getScadenza_bando'] = {'query': now, 'range': 'max'}
                query['getChiusura_procedimento_bando'] = {'query': now, 'range': 'min'}
            if stato == "closed":
                query['getChiusura_procedimento_bando'] = {'query': now, 'range': 'max'}
        if search_type == 'solr':
            query['use_solr'] = True
        if not SearchableText:
            del query['SearchableText']
        return pc(**query)

    def getBandoState(self, bando):
        """
        """
        scadenza_bando = bando.getScadenza_bando
        chiusura_procedimento_bando = bando.getChiusura_procedimento_bando
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

    def isValidDeadline(self, date):
        """
        """
        if not date:
            return False
        if date.Date() == '2100/12/31':
            #a default date for bandi that don't have a defined deadline
            return False
        return True
