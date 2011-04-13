# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES


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
    portal = context.getSite()
    setup_tool = portal.portal_setup
    setup_tool.runImportStepFromProfile('profile-rer.bandi:default', 'catalog')

    catalog = getToolByName(portal, 'portal_catalog')
    indexes = catalog.indexes()

    wanted = [
            ('getChiusura_procedimento_bando', 'DateIndex'),
            ('getDestinatari', 'KeywordIndex'),
            ('getScadenza_bando', 'DateIndex'),
            ('getTipologia_bando', 'FieldIndex'),
            ]

    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            portal.plone_log('Added %s for field %s.' % (meta_type, name))
    if len(indexables) > 0:
        portal.plone_log('Indexing new indexes %s.' % ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


