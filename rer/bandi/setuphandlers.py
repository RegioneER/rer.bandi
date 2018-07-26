# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

import logging
logger = logging.getLogger('rer.bandi')


def import_various(context):
    if context.readDataFile('rer.bandi_various.txt') is None:
        return

    portal = context.getSite()
    addKeyToCatalog(portal)
    addDefaultValueToRegistry()


def addKeyToCatalog(portal):
    # inizializzazione degli indici

    setup_tool = portal.portal_setup
    setup_tool.runImportStepFromProfile('profile-rer.bandi:default', 'catalog')
    catalog = getToolByName(portal, 'portal_catalog')
    indexes = catalog.indexes()

    wanted = [
        ('getChiusura_procedimento_bando', 'DateIndex', {
         'indexed_attrs': 'getChiusura_procedimento_bando', }),
        ('getDestinatariBando', 'KeywordIndex', {
            'indexed_attrs': 'getDestinatariBando', }),
        ('getScadenza_bando', 'DateIndex', {
            'indexed_attrs': 'getScadenza_bando', }),
        ('getTipologia_bando', 'FieldIndex', {
            'indexed_attrs': 'getTipologia_bando', }),
        ('getEnte_bando', 'KeywordIndex', {
            'indexed_attrs': 'getEnte_bando', }),
    ]

    indexables = []
    for idx in wanted:
        if idx[0] in indexes:
            logger.info(
                "Found the '%s' index in the catalog, nothing changed.\n" % idx[0])
        else:
            catalog.addIndex(name=idx[0], type=idx[1], extra=idx[2])
            logger.info("Added '%s' (%s) to the catalog.\n" % (idx[0], idx[1]))
            indexables.append(idx[0])
    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.' % ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def addDefaultValueToRegistry():

    DEST = (u'Cittadini|Cittadini',
            u'Imprese|Imprese',
            u'Enti locali|Enti locali',
            u'Associazioni|Associazioni',
            u'Altro|Altro')

    registry = getUtility(IRegistry)
    registry['rer.bandi.interfaces.settings.IBandoSettings.default_destinatari'] = DEST

    enti = (u'Regione Emilia-Romagna', )
    registry['rer.bandi.interfaces.settings.IBandoSettings.default_ente'] = enti
