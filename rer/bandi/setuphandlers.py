# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
import logging
logger = logging.getLogger('rer.bandi')

TYPES_TO_VERSION = ('Bando',)

def setVersionedTypes(context):
    """
    Setup handler to put under version control the specified portal types
    """
    if context.readDataFile('rer.bandi_various.txt') is None:
        return
    portal=context.getSite()
    portal_repository = getToolByName(portal, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in TYPES_TO_VERSION:
        if type_id not in versionable_types:
            # use append() to make sure we don't overwrite any
            # content-types which may already be under version control
            versionable_types.append(type_id)
            # Add default versioning policies to the versioned type
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)

    portal_repository.setVersionableContentTypes(versionable_types)




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

