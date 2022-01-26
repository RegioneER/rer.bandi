# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from rer.bandi import _
from six.moves.urllib.parse import quote
from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory


class SearchBandiForm(BrowserView):
    def getUniqueValuesForIndex(self, index):
        """
        get uniqueValuesFor a given index
        """
        pc = api.portal.get_tool(name='portal_catalog')
        return pc.uniqueValuesFor(index)

    def getVocabularyTermsForForm(self, vocab_name):
        """
        Return the values of destinatari vocabulary
        """
        dest_utility = getUtility(IVocabularyFactory, vocab_name)

        dest_values = []

        dest_vocab = dest_utility(self.context)

        for dest in dest_vocab:
            if dest.title != u'select_label':
                dest_values.append(dest.value)
        return dest_values


class SearchBandi(BrowserView):
    """
    A view for search bandi results
    """

    def searchBandi(self):
        """
        return a list of bandi
        """
        pc = getToolByName(self.context, "portal_catalog")
        stato = self.request.form.get("stato_bandi", "")
        SearchableText = self.request.form.get("SearchableText", "")
        query = self.request.form.copy()
        if stato:
            now = DateTime()
            if stato == "open":
                query["scadenza_bando"] = {"query": now, "range": "min"}
                query["chiusura_procedimento_bando"] = {
                    "query": now,
                    "range": "min",
                }
            if stato == "inProgress":
                query["scadenza_bando"] = {"query": now, "range": "max"}
                query["chiusura_procedimento_bando"] = {
                    "query": now,
                    "range": "min",
                }
            if stato == "closed":
                query["chiusura_procedimento_bando"] = {
                    "query": now,
                    "range": "max",
                }
        if "SearchableText" in self.request.form and not SearchableText:
            del query["SearchableText"]
        return pc(**query)

    @property
    def rss_query(self):
        """
        set rss query with the right date
        """
        query = self.request.QUERY_STRING
        stato = self.request.form.get("stato_bandi", "")
        if stato:
            now = DateTime().ISO()
            if stato == "open":
                query = (
                    query
                    + "&scadenza_bando.query:record=%s&scadenza_bando.range:record=min"
                    % quote(now)
                )
                query = (
                    query
                    + "&chiusura_procedimento_bando.query:record=%s&chiusura_procedimento_bando.range:record=min"
                    % quote(now)
                )
            if stato == "inProgress":
                query = (
                    query
                    + "&amp;scadenza_bando.query:record=%s&scadenza_bando.range:record=max"
                    % quote(now)
                )
                query = (
                    query
                    + "&amp;chiusura_procedimento_bando.query:record=%s&chiusura_procedimento_bando.range:record=min"
                    % quote(now)
                )
            if stato == "closed":
                query = (
                    query
                    + "&amp;chiusura_procedimento_bando.query:record=%s&chiusura_procedimento_bando.range:record=max"
                    % quote(now)
                )

        return query

    def getBandoState(self, bando):
        """
        """

        scadenza_bando = bando.scadenza_bando
        chiusura_procedimento_bando = bando.chiusura_procedimento_bando
        state = ("open", translate(_(u"Open"), context=self.request))
        if scadenza_bando and scadenza_bando.isPast():
            if (
                chiusura_procedimento_bando
                and chiusura_procedimento_bando.isPast()
            ):
                state = (
                    "closed",
                    translate(_(u"Closed"), context=self.request),
                )
            else:
                state = (
                    "inProgress",
                    translate(_(u"In progress"), context=self.request),
                )
        else:
            if (
                chiusura_procedimento_bando
                and chiusura_procedimento_bando.isPast()
            ):
                state = (
                    "closed",
                    translate(_(u"Closed"), context=self.request),
                )

        return state

    def isValidDeadline(self, date):
        """
        """

        if not date:
            return False
        if date.Date() == "2100/12/31":
            # a default date for bandi that don't have a defined deadline
            return False
        return True

    def getSearchResultsDescriptionLength(self):
        length = api.portal.get_registry_record(
            "plone.search_results_description_length"
        )
        return length

    def getAllowAnonymousViewAbout(self):
        return api.portal.get_registry_record("plone.allow_anon_views_about")

    def getTypesUseViewActionInListings(self):

        return api.portal.get_registry_record(
            "plone.types_use_view_action_in_listings"
        )
