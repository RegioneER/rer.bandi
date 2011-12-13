# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
import logging
logger = logging.getLogger('rer.bandi')

def add_catalog_indexes(context):
    """
    Setup handler to add indexes to the portal catalog
    """
    if context.readDataFile('rer.bandi_various.txt') is None:
        return
    portal = context.getSite()
    setup_tool = portal.portal_setup
    setup_tool.runImportStepFromProfile('profile-rer.bandi:default', 'catalog')
    catalog = getToolByName(portal, 'portal_catalog')
    indexes = catalog.indexes()

    wanted = [
            ('getChiusura_procedimento_bando', 'DateIndex',{'indexed_attrs': 'getChiusura_procedimento_bando', }),
            ('getDestinatariBando', 'KeywordIndex',{'indexed_attrs': 'getDestinatariBando', }),
            ('getScadenza_bando', 'DateIndex',{'indexed_attrs': 'getScadenza_bando', }),
            ('getTipologia_bando', 'FieldIndex',{'indexed_attrs': 'getTipologia_bando', }),
            ]

    indexables = []
    for idx in wanted:
        if idx[0] in indexes:
            logger.info("Found the '%s' index in the catalog, nothing changed.\n" % idx[0])
        else:
            catalog.addIndex(name=idx[0], type=idx[1], extra=idx[2])
            logger.info("Added '%s' (%s) to the catalog.\n" % (idx[0], idx[1]))
            indexables.append(idx[0])
    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.' % ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)

def addPropertySheet(context):
    if context.readDataFile('rer.bandi_various.txt') is None:
        return
    portal = context.getSite()
    DEST=('Cittadini|Cittadini',
          'Imprese|Imprese',
          'Enti locali|Enti locali',
          'Associazioni|Associazioni',
          'Altro|Altro')
    portal_properties = getToolByName(portal, 'portal_properties')
    rer_bandi_settings = getattr(portal_properties, 'rer_bandi_settings',None)
    if not rer_bandi_settings:
        portal_properties.addPropertySheet(id='rer_bandi_settings',title='RER Bandi settings')
        logger.info("Added RER Bandi settings property-sheet")
        rer_bandi_settings = getattr(portal_properties, 'rer_bandi_settings',None)
    if not rer_bandi_settings.hasProperty('destinatari_bandi'):
        rer_bandi_settings.manage_addProperty(id='destinatari_bandi',value=DEST,type='lines')

