# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.restapi.serializer.converters import json_compatible
from rer.bandi import _
from rer.bandi.interfaces import IRerBandiLayer
from rer.bandi.services.search_parameters.get import getSearchFields
from rer.sitesearch.interfaces import ISiteSearchCustomFilters
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, IRerBandiLayer)
@implementer(ISiteSearchCustomFilters)
class BandiAdapter(object):
    """
    """

    label = _("bandi_sitesearch_adapter_label", default=u"Bandi")

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        filters = {}
        for filter_data in getSearchFields():
            index = filter_data.get("id", "")
            if index in ["Subject", "SearchableText"]:
                continue
            if index == "stato_bandi":
                for option in filter_data["options"]:
                    val = option.get("value", "")
                    if not val:
                        continue
                    now = json_compatible(DateTime())
                    query = {}
                    if val == "open":
                        query["scadenza_bando"] = {
                            "query": now,
                            "range": "min",
                        }
                        query["chiusura_procedimento_bando"] = {
                            "query": now,
                            "range": "min",
                        }
                    if val == "inProgress":
                        query["scadenza_bando"] = {
                            "query": now,
                            "range": "max",
                        }
                        query["chiusura_procedimento_bando"] = {
                            "query": now,
                            "range": "min",
                        }
                    if val == "closed":
                        query["chiusura_procedimento_bando"] = {
                            "query": now,
                            "range": "max",
                        }
                    option["value"] = query
            filters[index] = filter_data
        return filters
