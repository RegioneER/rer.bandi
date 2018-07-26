# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from rer.bandi import logger
from rer.bandi.setuphandlers import addKeyToCatalog

default_profile = 'profile-rer.bandi:default'


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context, 'portal_quickinstaller').get(
                upgrade_product)
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


def migrate_to_2200(context):
    PROFILE_ID = 'profile-rer.bandi:migrate_to_2200'
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(PROFILE_ID)
    setup_tool.runImportStepFromProfile(default_profile, 'catalog')
    logger.info("Reindexing catalog indexes")
    catalog = getToolByName(context, 'portal_catalog')
    bandi = catalog(portal_type="Bando")
    for bando in bandi:
        bando.getObject().reindexObject(idxs=["getChiusura_procedimento_bando",
                                              "getDestinatariBando",
                                              "getScadenza_bando",
                                              "getTipologia_bando"])

    setup_tool.runImportStepFromProfile(
        'profile-rer.bandi:default', 'plone.app.registry')
    setup_tool.runImportStepFromProfile(
        'profile-rer.bandi:default', 'typeinfo')

    logger.info("Migrated to 2.2.0")


def migrate_to_2300(context):
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'plone.app.registry')
    logger.info('Add sortable collection criteria')


def migrate_to_2400(context):
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'typeinfo')
    logger.info('Upgrading to 2400')