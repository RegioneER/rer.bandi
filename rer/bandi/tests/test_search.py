# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from Products.CMFCore.utils import getToolByName
from rer.bandi.testing import RER_BANDI_API_FUNCTIONAL_TESTING


import requests
import transaction
import unittest


class SearchBandiTest(unittest.TestCase):

    layer = RER_BANDI_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.catalog = getToolByName(self.portal, "portal_catalog")

        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Object creation
        self.bando = api.content.create(
            container=self.portal, type="Bando", title="Bando foo"
        )
        self.document = api.content.create(
            container=self.portal, type="Document", title="Empty page"
        )

        transaction.commit()

    def test_route_exists(self):
        response = self.api_session.get("/@search_bandi_rest")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

    def test_search_only_bandi(self):
        response = self.api_session.get("/@search_bandi_rest")

        results = response.json()
        self.assertEqual(
            results[u"items_total"], 1,
        )

    # def test_search_bando_all(self):
    #     pass
