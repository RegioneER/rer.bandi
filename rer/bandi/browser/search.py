# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.i18n import translate
from plone import api

from rer.bandi import bandiMessageFactory as _
from urllib2 import quote
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
    from collective.solr_collection.solr import solrUniqueValuesFor
    HAS_SOLR_COLLECTION = True
except ImportError:
    HAS_SOLR_COLLECTION = False


class SearchBandiForm(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        voc_tipologia = getUtility(
            IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)
        self.terms_tipologia = list(voc_tipologia)
        voc_destinatari = getUtility(
            IVocabularyFactory, name='rer.bandi.destinatari.vocabulary')(self.context)
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
        get uniqueValuesFor a given index
        """
        if not self.solr_enabled or not HAS_SOLR_COLLECTION:
            pc = getToolByName(self, 'portal_catalog')
            return pc.uniqueValuesFor(index)
        else:
            return solrUniqueValuesFor(index, portal_type="Bando")

    def getDefaultEnte(self):
        """
        return the default ente
        """
        portal_properties = getToolByName(self, 'portal_properties')
        rer_bandi_settings = getattr(
            portal_properties, 'rer_bandi_settings', None)
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
        SearchableText = self.request.form.get('SearchableText', '')
        query = self.request.form.copy()
        if stato:
            now = DateTime()
            if stato == "open":
                query['getScadenza_bando'] = {'query': now, 'range': 'min'}
                query['getChiusura_procedimento_bando'] = {
                    'query': now, 'range': 'min'}
            if stato == "inProgress":
                query['getScadenza_bando'] = {'query': now, 'range': 'max'}
                query['getChiusura_procedimento_bando'] = {
                    'query': now, 'range': 'min'}
            if stato == "closed":
                query['getChiusura_procedimento_bando'] = {
                    'query': now, 'range': 'max'}
        if "SearchableText" in self.request.form and not SearchableText:
            del query['SearchableText']

        return pc(**query)

    @property
    def rss_query(self):
        """
        set rss query with the right date
        """
        query = self.request.QUERY_STRING
        stato = self.request.form.get('stato_bandi', '')
        if stato:
            now = DateTime().ISO()
            if stato == "open":
                query = query + \
                    "&amp;getScadenza_bando.query:record:date=%s&getScadenza_bando.range:record=min" % quote(
                        now)
                query = query + \
                    "&amp;getChiusura_procedimento_bando.query:record:date=%s&getChiusura_procedimento_bando.range:record=min" % quote(
                        now)
            if stato == "inProgress":
                query = query + \
                    "&amp;getScadenza_bando.query:record:date=%s&getScadenza_bando.range:record=max" % quote(
                        now)
                query = query + \
                    "&amp;getChiusura_procedimento_bando.query:record:date=%s&getChiusura_procedimento_bando.range:record=min" % quote(
                        now)
            if stato == "closed":
                query = query + \
                    "&amp;getChiusura_procedimento_bando.query:record:date=%s&getChiusura_procedimento_bando.range:record=max" % quote(
                        now)

        return query

    def getBandoState(self, bando):
        """
        """

        scadenza_bando = bando.getScadenza_bando
        chiusura_procedimento_bando = bando.getChiusura_procedimento_bando
        state = ('open', translate(_(u'Open'), context=self.request))
        if scadenza_bando and scadenza_bando.isPast():
            if chiusura_procedimento_bando and chiusura_procedimento_bando.isPast():
                state = ('closed', translate(
                    _(u'Closed'), context=self.request))
            else:
                state = ('inProgress', translate(
                    _(u'In progress'), context=self.request))
        else:
            if chiusura_procedimento_bando and chiusura_procedimento_bando.isPast():
                state = ('closed', translate(
                    _(u'Closed'), context=self.request))

        return state

    def isValidDeadline(self, date):
        """
        """

        if not date:
            return False
        if date.Date() == '2100/12/31':
            # a default date for bandi that don't have a defined deadline
            return False
        return True

    def getSearchResultsDescriptionLength(self):
        length = api.portal.get_registry_record(
            'plone.search_results_description_length')
        return length

    def getAllowAnonymousViewAbout(self):
        return api.portal.get_registry_record(
            'plone.allow_anon_views_about'
        )

    def getTypesUseViewActionInListings(self):

        return api.portal.get_registry_record(
            'plone.types_use_view_action_in_listings'
        )
