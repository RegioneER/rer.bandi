# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.i18n import translate

from rer.bandi import bandiMessageFactory as _
from rer.bandi import logger

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory

from zope.component import getUtility, queryUtility

try:
    from collective.solr.interfaces import ISolrConnectionConfig
    HAS_SOLR = True
except ImportError:
    HAS_SOLR = False

try:
    from collective.solr_collection.solr import solrUniqueValuesFor as basesolrUniqueValuesFor
    HAS_SOLR_COLLECTION = True
except ImportError:
    HAS_SOLR_COLLECTION = False


class SearchBandiForm(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        voc_tipologia = getUtility(IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)
        self.terms_tipologia = list(voc_tipologia)
        voc_destinatari = getUtility(IVocabularyFactory, name='rer.bandi.destinatari.vocabulary')(self.context)
        self.terms_destinatari = list(voc_destinatari)
        self.solr_enabled = self.isSolrEnabled()

    def isSolrEnabled(self):
        """
        """
        if not HAS_SOLR:
            return False
        util = queryUtility(ISolrConnectionConfig)
        if util:
            return getattr(util, 'active', False)
        return False

    def getUniqueValuesForIndex(self, index):
        """
        """
        if not self.solr_enabled or not HAS_SOLR_COLLECTION:
            pc = getToolByName(self, 'portal_catalog')
            return pc.uniqueValuesFor(index)
        else:
            return self.solrUniqueValuesFor(index, "Bando")

    def solrUniqueValuesFor(self, index, portal_type=""):
        """
        * http://wiki.apache.org/solr/TermsComponent
        """
        from time import time
        from collective.solr.interfaces import ISolrConnectionManager
        from collective.solr.exceptions import SolrInactiveException
        from urllib import urlencode
        from collective.solr.parser import SolrResponse
        start = time()
        config = queryUtility(ISolrConnectionConfig)
        # search = queryUtility(ISearch)
        manager = getUtility(ISolrConnectionManager)
        # manager = search.getManager()
        manager.setSearchTimeout()
        connection = manager.getConnection()
        if connection is None:
            raise SolrInactiveException
        if not portal_type:
            response = connection.doPost(
                connection.solrBase + '/terms',
                urlencode({'terms.fl': index, 'terms.limit': -1}, doseq=True),
                connection.formheaders)
        else:
            response = connection.doPost(
                connection.solrBase + '/select',
                urlencode({'portal_type': portal_type, 'facet': 'on', 'facet.field': index},
                          doseq=True),
                connection.formheaders)
        results = SolrResponse(response)
        response.close()
        manager.setTimeout(None)
        elapsed = (time() - start) * 1000
        slow = config.slow_query_threshold
        if slow and elapsed >= slow:
            logger.info(
                'slow query: %d/%d ms for uniqueValuesFor (%r)',
                results.responseHeader['QTime'], elapsed, index)
        if portal_type:
            faceted = getattr(results, 'facet_counts')
            if faceted:
                terms = faceted.get('facet_felds').keys()
                logger.debug('terms info: %s' % terms)
                return tuple(sorted(terms))
        else:
            terms = getattr(results, 'terms', {})
            logger.debug('terms info: %s' % terms)
            return tuple(terms.get(index, {}).keys())

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
        if "SearchableText" in self.request.form and not SearchableText:
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
