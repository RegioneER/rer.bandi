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
    ptypes = api.portal.get_tool('portal_types')
    del ptypes['Bando']
    del ptypes['Bando Folder Deepening']
    setup_tool.runImportStepFromProfile(default_profile, 'typeinfo')
    setup_tool.runImportStepFromProfile(default_profile, 'plone.app.registry')
    logger.info('Add sortable collection criteria')


def migrate_to_2400(context):
    setup_tool = api.portal.get_tool('portal_setup')
    logger.info('Upgrading to 2400')
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
from Products.Archetypes.BaseUnit import BaseUnit
from plone.app.textfield.value import RichTextValue
from DateTime import DateTime

def annotation_migration(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """
    migrate title and description value
    """
    fieldkey = 'Archetypes.storage.AnnotationStorage-{}'.format(src_fieldname)
    value = src_obj.__annotations__[fieldkey]
    if isinstance(value, BaseUnit):
        if src_fieldname  in ('text', 'riferimenti_bando'):
            value = RichTextValue(value.getRaw().decode('utf-8'))
        else:
            value = value.getRaw()
    if isinstance(value, DateTime):
        value = value.asdatetime().replace(tzinfo=None)
    setattr(dst_obj, dst_fieldname, value)

def attribute_migration(src_obj, dst_obj, src_fieldname, dst_fieldname):
    value = getattr(src_obj, src_fieldname)
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
        },
        {
            'AT_field_name': 'destinatari',
            'DX_field_name': 'destinatari',
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
        {
            'AT_field_name': 'text',
            'DX_field_name': 'text',
            'field_migrator': annotation_migration,
        },
        {
            'AT_field_name': 'subject',
            'DX_field_name': 'subjects',
        },
        {
            'AT_field_name': 'allow_discussion',
            'DX_field_name': 'allow_discussion',
        },
        {
            'AT_field_name': 'contributors',
            'DX_field_name': 'contributors',
        },
        {
            'AT_field_name': 'creators',
            'DX_field_name': 'creators',
        },
        {
            'AT_field_name': 'effectiveDate',
            'DX_field_name': 'effective_date',
        },
        {
            'AT_field_name': 'expirationDate',
            'DX_field_name': 'expiration_date',
        },
        {
            'AT_field_name': 'language',
            'DX_field_name': 'language',
        },
        {
            'AT_field_name': 'rights',
            'DX_field_name': 'rights',
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
        src_type='Bando Folder Deepening',
        dst_type='Bando Folder Deepening'
    )
