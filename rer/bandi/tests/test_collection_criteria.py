# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from rer.bandi.testing import RER_BANDI_FUNCTIONAL_TESTING

import unittest


class TestCollectionCriteria(unittest.TestCase):

    layer = RER_BANDI_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        login(self.portal, TEST_USER_NAME)
        self.collection = api.content.create(
            container=self.portal, type="Collection", title="Collection"
        )
        self.bando1 = api.content.create(
            container=self.portal,
            type="Bando",
            title="Bando with destinatari",
            destinatari=["d1", "d2", "dà"],
        )

        self.bando2 = api.content.create(
            container=self.portal,
            type="Bando",
            title="Bando with finanziatori",
            finanziato=True,
        )

        self.bando3 = api.content.create(
            container=self.portal,
            type="Bando",
            title="Bando with materie",
            materie=["m1", "m2"],
        )

    def test_query_destinatari(self):
        query = [
            {
                "i": "destinatari",
                "o": "plone.app.querystring.operation.string.is",
                "v": ["d1"],
            }
        ]
        self.collection.setQuery(query)
        results = self.collection.results()
        self.assertEqual(results.sequence_length, 1)
        self.assertEqual(results[0].Title(), self.bando1.Title())

    def test_query_destinatari_with_accent(self):
        query = [
            {
                "i": "destinatari",
                "o": "plone.app.querystring.operation.string.is",
                "v": ["dà"],
            }
        ]
        self.collection.setQuery(query)
        results = self.collection.results()
        self.assertEqual(results.sequence_length, 1)
        self.assertEqual(results[0].Title(), self.bando1.Title())

    def test_query_finanziatori(self):
        query = [
            {
                "i": "finanziato",
                "o": "plone.app.querystring.operation.boolean.isTrue",
                "v": "",
            }
        ]
        self.collection.setQuery(query)
        results = self.collection.results()
        self.assertEqual(results.sequence_length, 1)
        self.assertEqual(results[0].Title(), self.bando2.Title())

    def test_query_materie(self):
        query = [
            {
                "i": "materie",
                "o": "plone.app.querystring.operation.string.is",
                "v": ["m1"],
            }
        ]
        self.collection.setQuery(query)
        results = self.collection.results()
        self.assertEqual(results.sequence_length, 1)
        self.assertEqual(results[0].Title(), self.bando3.Title())
