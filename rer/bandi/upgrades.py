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



# https://github.com/plone/plone.app.contenttypes/blob/master/plone/app/contenttypes/migration/migration.py
from Products.contentmigration.basemigrator.migrator import CMFFolderMigrator
from Products.contentmigration.basemigrator.walker import CatalogWalker
import os
from Products.GenericSetup.context import DirectoryImportContext
from Products.GenericSetup.utils import importObjects
from plone.dexterity.interfaces import IDexterityFTI
# from plone.app.contenttypes.migration.utils import installTypeIfNeeded
# from plone.app.contenttypes.utils import DEFAULT_TYPES
# DEFAULT_TYPES.append('Bando')




class BandoMigrator(CMFFolderMigrator):
    """Base for folderish ATCT
    """
    src_portal_type = 'Bando'
    src_meta_type = 'Bando'
    dst_portal_type = 'Bando'
    dst_meta_type = None # not used

    def __init__(self, *args, **kwargs):
        super(BandoMigrator, self).__init__(*args, **kwargs)
        logger.info(
            'Migrating {0} {1}'.format(
                self.old.portal_type,
                '/'.join(self.old.getPhysicalPath())))


def migrate_to_3000(context):
    # TODO: installare tutti i genericstep modificati/aggiunti/eliminati dalla 2200 alla 3000
    setup_tool = getToolByName(context, 'portal_setup')
    portal = api.portal.get()

    # setup_tool.runImportStepFromProfile(default_profile, 'typeinfo')
    from plone.app.blob.content import ATBlob

    def getIndexValue(self, mimetype='text/plain'):
        return ''

    ATBlob.getIndexValue = getIndexValue

    for type_name in ['Bando', 'Bando Folder Deepening']:
        # installTypeIfNeeded(type_name)
        tt = getToolByName(portal, 'portal_types')
        fti = tt.getTypeInfo(type_name)
        if IDexterityFTI.providedBy(fti):
            continue
        if fti:
            tt.manage_delObjects(type_name)
        tt.manage_addTypeInformation('Dexterity FTI', id=type_name)
        dx_fti = tt.getTypeInfo(type_name)
        profile_info = setup_tool.getProfileInfo(default_profile)
        profile_path = os.path.join(profile_info['path'])
        environ = DirectoryImportContext(setup_tool, profile_path)
        parent_path = 'types/'
        importObjects(dx_fti, parent_path, environ)

    setup_tool.runImportStepFromProfile(default_profile, 'plone.app.registry')

    # migrazione dei vocabolari

    migrate_at_to_dx()

#    catalog = getToolByName(context, 'portal_catalog')
#    bandi = catalog(portal_type="Bando")
#    for bando in bandi:
#        logger.info('migrate bando %s', bando.getURL())
#        obj = bando.getObject()
#    # import pdb; pdb.set_trace()
#    walker = CatalogWalker(portal, BandoMigrator)()
#    # migrate(context, BandoMigrator)
#    bandi = catalog(portal_type="Bando")
#    for bando in bandi:
#        logger.info('migrate bando %s', bando.getURL())
#        obj = bando.getObject()
#    logger.info("Migrated to 3.0.0")

from plone.app.contenttypes.migration.migration import migrateCustomAT

def annotation_migration(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """
    migrate title and description value
    """
    fieldkey = 'Archetypes.storage.AnnotationStorage-{}'.format(src_fieldname)
    value = src_obj.__annotations__[fieldkey]
    if isinstance(value, BaseUnit):
        value = value.getRaw()
    setattr(dst_obj, dst_fieldname, value)


def migrate_at_to_dx():
    """
    migrate links
    """
    fields_mapping = (
        {   
            'AT_field_name': 'title',
            'DX_field_name': 'title',
            'field_migrator': annotation_migration,
        },
        {   
            'AT_field_name': 'description',
            'DX_field_name': 'description',
            'field_migrator': annotation_migration,
        },
        {   
            'AT_field_name': 'tipologia_bando',
            'DX_field_name': 'tipologia_bando',
            'field_migrator': annotation_migration,
        },
        {   
            'AT_field_name': 'destinatari',
            'DX_field_name': 'destinatari',
            'field_migrator': annotation_migration,
        },
        {   
            'AT_field_name': 'ente_bando',
            'DX_field_name': 'ente_bando',
        },
        {   
            'AT_field_name': 'scadenza_bando',
            'DX_field_name': 'scadenza_bando',
            'field_migrator': annotation_migration,
        },
        {   
            'AT_field_name': 'chiusura_procedimento_bando',
            'DX_field_name': 'chiusura_procedimento_bando',
            'field_migrator': annotation_migration,
        },
        {   
            'AT_field_name': 'riferimenti_bando',
            'DX_field_name': 'riferimenti_bando',
            'field_migrator': annotation_migration,
        },

    )
    migrateCustomAT(
        fields_mapping,
        src_type='Bando',
        dst_type='Bando'
    )

    fields_mapping = (
        {   
            'AT_field_name': 'title',
            'DX_field_name': 'title',
            'field_migrator': annotation_migration,
        },
        {   
            'AT_field_name': 'description',
            'DX_field_name': 'description',
            'field_migrator': annotation_migration,
        },
    )
    migrateCustomAT(
        fields_mapping,
        src_type='BandoFolderDeepening',
        dst_type='BandoFolderDeepening'
    )
