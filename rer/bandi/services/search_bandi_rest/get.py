# -*- coding: utf-8 -*-
from plone.api.portal import translate
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

        query.update(base_query_parameters)

        return SearchHandler(self.context, self.request).search(query)
