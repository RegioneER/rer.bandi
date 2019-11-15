# -*- coding: utf-8 -*-
from .utils import query_stato
from plone.restapi.search.handler import SearchHandler
from plone.restapi.search.utils import unflatten_dotted_dict
from plone.restapi.services.search.get import SearchGet
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class SearchBandiGet(SearchGet):
    def __init__(self, context, request):
        super(SearchBandiGet, self).__init__(context, request)

    def reply(self):
        query = self.request.form.copy()
        query = unflatten_dotted_dict(query)

        # Questi parametri vengono aggiunti di base a tutte le query
        base_query_parameters = {
            "portal_type": "Bando",
        }

        stato = query.get("stato_bandi")
        if stato:
            stato_query = query_stato(stato)

        query.update(base_query_parameters)
        query.update(stato_query)

        return SearchHandler(self.context, self.request).search(query)
