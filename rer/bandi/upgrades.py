# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from rer.bandi import logger
from rer.bandi.setuphandlers import addKeyToCatalog, addPropertySheet

default_profile = 'profile-rer.bandi:default'


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context, 'portal_quickinstaller').get(upgrade_product)
            setattr(p, 'installedversion', version)
            return fn(context, *args)
        return wrap_func_args
    return wrap_func


@upgrade('rer.bandi', '2.1.0')
def to_2(context):
    """
    """
    logger.info('Upgrading rer.bandi to version 2.1.0')
    portal = context.portal_url.getPortalObject()
    addKeyToCatalog(portal)
    addPropertySheet(portal)
