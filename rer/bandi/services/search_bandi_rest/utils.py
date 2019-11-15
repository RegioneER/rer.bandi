# -*- coding: utf-8 -*-
from DateTime import DateTime


def query_stato(stato):
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
