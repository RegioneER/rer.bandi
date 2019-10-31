# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from rer.bandi import logger

default_profile = 'profile-rer.bandi:default'

TIPOLOGIA_BANDO_MAPPING = {
    'agevolazioni': u'Agevolazioni, finanziamenti, contributi',
    'beni_servizi': u'Manifestazioni di interesse',
    'lavori_pubblici': u'Manifestazioni di interesse',
    'altro': u'Manifestazioni di interesse',
}

DESTINATARI_BANDO_MAPPING = {
    'Cittadini': [u'Cittadini'],
    'Imprese': [u'Grandi imprese', u'PMI', u'Micro imprese'],
    'Enti locali': [u'Enti pubblici'],
    'Associazioni': [u'Enti del Terzo settore'],
    'Altro': [u'Scuole, università, enti di formazione'],
}


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """

    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context, 'portal_quickinstaller').get(
                upgrade_product
            )
            setattr(p, 'installedversion', version)
            return fn(context, *args)

        return wrap_func_args

    return wrap_func


@upgrade('rer.bandi', '2.1.0')
def to_2(context):
    """
    """
    logger.info('Upgrading rer.bandi to version 2.1.0')
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'catalog')


def migrate_to_2200(context):
    PROFILE_ID = 'profile-rer.bandi:migrate_to_2200'
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(PROFILE_ID)
    setup_tool.runImportStepFromProfile(default_profile, 'catalog')
    logger.info("Reindexing catalog indexes")
    catalog = getToolByName(context, 'portal_catalog')
    bandi = catalog(portal_type="Bando")
    for bando in bandi:
        bando.getObject().reindexObject(
            idxs=[
                "getChiusura_procedimento_bando",
                "getDestinatariBando",
                "getScadenza_bando",
                "getTipologia_bando",
            ]
        )

    setup_tool.runImportStepFromProfile(
        'profile-rer.bandi:default', 'plone.app.registry'
    )
    setup_tool.runImportStepFromProfile(
        'profile-rer.bandi:default', 'typeinfo'
    )

    logger.info("Migrated to 2.2.0")


def migrate_to_2300(context):
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'plone.app.registry')
    logger.info('Add sortable collection criteria')


def migrate_to_2400(context):
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'typeinfo')
    logger.info('Upgrading to 2400')


def migrate_to_2500(context):
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'typeinfo')
    logger.info('Upgrading to 2500')


def migrate_to_3000(context):
    PROFILE_ID = 'profile-rer.bandi:migrate_to_3000'
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(PROFILE_ID)

    #  update indexes and topics
    setup_tool.runImportStepFromProfile(default_profile, 'catalog')
    setup_tool.runImportStepFromProfile(default_profile, 'plone.app.registry')

    bandi = api.content.find(portal_type='Bando')
    tot_results = len(bandi)
    logger.info('### There are {tot} Bandi to fix ###'.format(tot=tot_results))
    for counter, brain in enumerate(bandi):
        logger.info(
            '[{counter}/{tot}] - {bando}'.format(
                counter=counter + 1, tot=tot_results, bando=brain.getPath()
            )
        )
        remap_fields(brain=brain)
    logger.info('Upgrading to 3000')


def remap_fields(brain):
    bando = brain.getObject()
    tipologia = getattr(bando, 'tipologia_bando', '')
    destinatari = getattr(bando, 'destinatari', [])

    if tipologia:
        if tipologia not in TIPOLOGIA_BANDO_MAPPING:
            logger.warning(
                '  - Unable to find a match for tipologia "{tipologia}" in "{bando}"'.format(  # noqa
                    tipologia=tipologia, bando=brain.getPath()
                )
            )
        new_value = TIPOLOGIA_BANDO_MAPPING[tipologia]
        logger.info(
            '  - TIPOLOGIA: {old} => {new}'.format(
                old=tipologia, new=new_value
            )
        )
        bando.tipologia_bando = new_value

    if destinatari:
        new_value = []
        for destinatario in destinatari:
            if destinatario not in DESTINATARI_BANDO_MAPPING:
                logger.warning(
                    '  - Unable to find a match for destinatario "{destinatario}" in "{bando}"'.format(  # noqa
                        destinatario=destinatario, bando=brain.getPath()
                    )
                )
            new_value.extend(DESTINATARI_BANDO_MAPPING[destinatario])
        logger.info(
            '  - DESTINATARIO: {old} => {new}'.format(
                old=destinatari, new=new_value
            )
        )
        bando.destinatari = new_value
    bando.reindexObject(idxs=['getDestinatariBando', 'getTipologia_bando'])
