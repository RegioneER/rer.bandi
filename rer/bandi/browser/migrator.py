# -*- coding: utf-8 -*-
from plone import api
from Products.Five import BrowserView
from plone.app.contenttypes.migration.migration import migrateCustomAT
from Products.CMFCore.utils import getToolByName
from rer.bandi import logger
from rer.bandi.setuphandlers import addKeyToCatalog
# https://github.com/plone/plone.app.contenttypes/blob/master/plone/app/contenttypes/migration/migration.py
from Products.contentmigration.basemigrator.migrator import CMFFolderMigrator
from Products.contentmigration.basemigrator.walker import CatalogWalker
import os
from Products.GenericSetup.context import DirectoryImportContext
from Products.GenericSetup.utils import importObjects
from plone.dexterity.interfaces import IDexterityFTI
from plone.app.blob.content import ATBlob
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
default_profile = 'profile-rer.bandi:default'


class DXMigratorView(BrowserView):

    # TODO: dry run
    # TODO: autocsrf
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        context = self.context

        setup_tool = getToolByName(context, 'portal_setup')
        portal = api.portal.get()

        # setup_tool.runImportStepFromProfile(default_profile, 'typeinfo')

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

        return "OK"



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
