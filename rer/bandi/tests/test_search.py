# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from Products.CMFCore.utils import getToolByName
from rer.bandi.testing import RER_BANDI_INTEGRATION_TESTING

import unittest
import requests


class SearchBandiTest(unittest.TestCase):

    layer = RER_BANDI_INTEGRATION_TESTING

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
        self.bando = api.content.create(
            container=self.portal, type="Bando", title="Bando foo"
        )

    def test_overall_response_format(self):
        response = self.api_session.get("/@search_bandi_rest")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

        results = response.json()
        self.assertEqual(
            results[u"items_total"],
            len(results[u"items"]),
            "items_total property should match actual item count.",
        )

    # def test_search_bando_all(self):
    #     pass
