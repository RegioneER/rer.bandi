# -*- coding: utf-8 -*-
from plone import api
from plone.memoize import ram
from Products.Five import BrowserView
from time import time

import pkg_resources

JS_TEMPLATE = '{portal_url}/++plone++rer.bandi.static/dist/{env_mode}/{name}.js?v={version}'
CSS_TEMPLATE = '{portal_url}/++plone++rer.bandi.static/dist/{env_mode}/{name}.css?v={version}'


class View(BrowserView):
    """ """

    @ram.cache(lambda *args: time() // (60 * 60))
    def get_version(self):
        return pkg_resources.get_distribution('rer.bandi').version

    def get_env_mode(self):
        return (
            api.portal.get_registry_record('plone.resources.development')
            and 'dev'
            or 'prod'
        )

    def get_resource_js(self, name='main'):
        return JS_TEMPLATE.format(
            portal_url=api.portal.get().absolute_url(),
            env_mode=self.get_env_mode(),
            name=name,
            version=self.get_version(),
        )

    def get_resource_css(self, name='main'):
        return CSS_TEMPLATE.format(
            portal_url=api.portal.get().absolute_url(),
            env_mode=self.get_env_mode(),
            name=name,
            version=self.get_version(),
        )
