# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.restapi.search.handler import SearchHandler
from plone.restapi.search.utils import unflatten_dotted_dict
from plone.restapi.services.search.get import SearchGet
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class SearchBandiGet(SearchGet):
    def __init__(self, context, request):
        super(SearchBandiGet, self).__init__(context, request)

    @property
    def query(self):
        query = self.request.form.copy()
        query = unflatten_dotted_dict(query)

        # Questi parametri vengono aggiunti di base a tutte le query
        base_query_parameters = {"portal_type": "Bando"}

        query.update(base_query_parameters)

        stato = query.get("stato_bandi")
        if stato:
            stato_query = self.query_stato(stato)
            del query['stato_bandi']
            query.update(stato_query)
        return query

    def query_stato(self, stato):
        """ In base allo stato che ci viene passato in ingresso generiamo
        la query corretta da passare poi al catalogo.

        Valori possibili per stato: [open, inProgress, closed]
        """

        query = {}

        if stato:
            now = DateTime()
            if stato == "open":
                query["getScadenza_bando"] = {"query": now, "range": "min"}
                query["getChiusura_procedimento_bando"] = {
                    "query": now,
                    "range": "min",
                }
            if stato == "inProgress":
                query["getScadenza_bando"] = {"query": now, "range": "max"}
                query["getChiusura_procedimento_bando"] = {
                    "query": now,
                    "range": "min",
                }
            if stato == "closed":
                query["getChiusura_procedimento_bando"] = {
                    "query": now,
                    "range": "max",
                }
            return query
        else:
            return {}

    def reply(self):
        return SearchHandler(self.context, self.request).search(self.query)
