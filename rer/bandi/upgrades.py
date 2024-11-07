# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from rer.bandi import logger

default_profile = "profile-rer.bandi:default"

TIPOLOGIA_BANDO_MAPPING = {
    "agevolazioni": "Agevolazioni, finanziamenti, contributi",
    "beni_servizi": "Manifestazioni di interesse",
    "lavori_pubblici": "Manifestazioni di interesse",
    "altro": "Manifestazioni di interesse",
}

DESTINATARI_BANDO_MAPPING = {
    "Cittadini": ["Cittadini"],
    "Imprese": ["Grandi imprese", "PMI", "Micro imprese"],
    "Enti locali": ["Enti pubblici"],
    "Associazioni": ["Enti del Terzo settore"],
    "Altro": ["Scuole, università, enti di formazione"],
}


def remap_fields(brain):
    bando = brain.getObject()
    tipologia = getattr(bando, "tipologia_bando", "")
    destinatari = getattr(bando, "destinatari", [])

    if tipologia:
        if tipologia not in TIPOLOGIA_BANDO_MAPPING:
            logger.warning(
                '  - Unable to find a match for tipologia "{tipologia}" in "{bando}"'.format(  # noqa
                    tipologia=tipologia, bando=brain.getPath()
                )
            )
        else:
            new_value = TIPOLOGIA_BANDO_MAPPING[tipologia]
            logger.info(
                "  - TIPOLOGIA: {old} => {new}".format(
                    old=tipologia, new=new_value
                )
            )
            bando.tipologia_bando = new_value.decode("utf-8")

    if not destinatari:
        new_value = DESTINATARI_BANDO_MAPPING["Altro"]
        bando.destinatari = new_value
        logger.info("  - DESTINATARIO: VUOTO => {new}".format(new=new_value))
    else:
        new_value = []
        for destinatario in destinatari:
            if destinatario not in DESTINATARI_BANDO_MAPPING:
                logger.warning(
                    '  - Unable to find a match for destinatario "{destinatario}" in "{bando}"'.format(  # noqa
                        destinatario=destinatario, bando=brain.getPath()
                    )
                )
            else:
                new_value.extend(DESTINATARI_BANDO_MAPPING[destinatario])
        if new_value:
            logger.info(
                "  - DESTINATARIO: {old} => {new}".format(
                    old=destinatari, new=new_value
                )
            )
            bando.destinatari = new_value
    bando.reindexObject(idxs=["destinatari", "tipologia_bando"])


def upgrade(upgrade_product, version):
    """Decorator for updating the QuickInstaller of a upgrade"""

    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context, "portal_quickinstaller").get(
                upgrade_product
            )
            setattr(p, "installedversion", version)
            return fn(context, *args)

        return wrap_func_args

    return wrap_func


@upgrade("rer.bandi", "2.1.0")
def to_2(context):
    """ """
    logger.info("Upgrading rer.bandi to version 2.1.0")
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runImportStepFromProfile(default_profile, "catalog")


def migrate_to_2200(context):
    PROFILE_ID = "profile-rer.bandi:migrate_to_2200"
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runAllImportStepsFromProfile(PROFILE_ID)
    setup_tool.runImportStepFromProfile(default_profile, "catalog")
    logger.info("Reindexing catalog indexes")
    catalog = getToolByName(context, "portal_catalog")
    bandi = catalog(portal_type="Bando")
    for bando in bandi:
        bando.getObject().reindexObject(
            idxs=[
                "chiusura_procedimento_bando",
                "destinatari",
                "scadenza_bando",
                "tipologia_bando",
            ]
        )

    setup_tool.runImportStepFromProfile(
        "profile-rer.bandi:default", "plone.app.registry"
    )
    setup_tool.runImportStepFromProfile(
        "profile-rer.bandi:default", "typeinfo"
    )

    logger.info("Migrated to 2.2.0")


def migrate_to_2300(context):
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(default_profile, "plone.app.registry")
    logger.info("Add sortable collection criteria")


def migrate_to_2400(context):
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(default_profile, "typeinfo")
    logger.info("Upgrading to 2400")


def migrate_to_2500(context):
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(default_profile, "typeinfo")
    logger.info("Upgrading to 2500")


def migrate_to_3000(context):
    PROFILE_ID = "profile-rer.bandi:migrate_to_3000"
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runAllImportStepsFromProfile(PROFILE_ID)

    #  update indexes and topics
    setup_tool.runImportStepFromProfile(default_profile, "catalog")
    setup_tool.runImportStepFromProfile(default_profile, "plone.app.registry")

    bandi = api.content.find(portal_type="Bando")
    tot_results = len(bandi)
    logger.info("### There are {tot} Bandi to fix ###".format(tot=tot_results))
    for counter, brain in enumerate(bandi):
        logger.info(
            "[{counter}/{tot}] - {bando}".format(
                counter=counter + 1, tot=tot_results, bando=brain.getPath()
            )
        )
        remap_fields(brain=brain)
    logger.info("Upgrading to 3000")


def migrate_to_3100(context):
    PROFILE_ID = "profile-rer.bandi:migrate_to_3100"
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runAllImportStepsFromProfile(PROFILE_ID)

    #  update indexes and topics
    setup_tool.runImportStepFromProfile(default_profile, "catalog")
    setup_tool.runImportStepFromProfile(default_profile, "plone.app.registry")

    bandi = api.content.find(portal_type="Bando")
    tot_results = len(bandi)
    logger.info("### Fixing {tot} Bandi ###".format(tot=tot_results))
    for counter, brain in enumerate(bandi):
        logger.info(
            "[{counter}/{tot}] - {bando}".format(
                counter=counter + 1, tot=tot_results, bando=brain.getPath()
            )
        )
        bando = brain.getObject()
        bando.reindexObject(
            idxs=[
                "chiusura_procedimento_bando",
                "destinatari",
                "scadenza_bando",
                "tipologia_bando",
                "finanziatori",
                "materie",
            ]
        )

    criteria_mapping = {
        "getTipologia_bando": "tipologia_bando",
        "getChiusura_procedimento_bando": "chiusura_procedimento_bando",
        "getScadenza_bando": "scadenza_bando",
        "getFinanziatori_bando": "finanziatori",
        "getMaterie_bando": "materie",
        "getDestinatariBando": "destinatari",
    }
    collections = api.content.find(portal_type="Collection")
    tot_results = len(collections)
    logger.info("### Fixing {tot} Collections ###".format(tot=tot_results))
    for counter, brain in enumerate(collections):
        collection = brain.getObject()
        query = []
        for criteria in getattr(collection, "query", []):
            criteria["i"] = criteria_mapping.get(criteria["i"], criteria["i"])
            query.append(criteria)
        collection.query = query

        # fix sort_on
        sort_on = getattr(collection, "sort_on", "")
        if sort_on in criteria_mapping:
            collection.sort_on = criteria_mapping[sort_on]

        logger.info(
            "[{counter}/{tot}] - {collection}".format(
                counter=counter + 1,
                tot=tot_results,
                collection=brain.getPath(),
            )
        )
    logger.info("Upgrade to 3100 complete")


def migrate_to_3200(context):
    PROFILE_ID = "profile-rer.bandi:migrate_to_3200"
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runAllImportStepsFromProfile(PROFILE_ID)

    #  update indexes and topics
    setup_tool.runImportStepFromProfile(default_profile, "catalog")
    setup_tool.runImportStepFromProfile(default_profile, "plone.app.registry")

    bandi = api.content.find(portal_type="Bando")
    tot_results = len(bandi)
    logger.info("### Fixing {tot} Bandi ###".format(tot=tot_results))
    for counter, brain in enumerate(bandi):
        logger.info(
            "[{counter}/{tot}] - {bando}".format(
                counter=counter + 1, tot=tot_results, bando=brain.getPath()
            )
        )
        bando = brain.getObject()
        if getattr(bando, "finanziatori", []):
            setattr(bando, "finanziato", True)
            keywords = [k for k in getattr(bando, "finanziatori", []) if k]
            if bando.Subject():
                keywords.extend(bando.Subject())
            if keywords:
                setattr(bando, "subject", tuple(set(keywords)))
            delattr(bando, "finanziatori")

    bando.reindexObject(
        idxs=[
            "finanziatori",
            "finanziato",
        ]
    )

    criteria_mapping = {
        "finanziatori": "finanziato",
    }
    collections = api.content.find(portal_type="Collection")
    tot_results = len(collections)
    logger.info("### Fixing {tot} Collections ###".format(tot=tot_results))
    for counter, brain in enumerate(collections):
        collection = brain.getObject()

        crit_list = collection.query
        filtered_crit = [x for x in crit_list if x['i'] == "finanziatori"]
        if not filtered_crit:
            continue
    
        query = []
        for criteria in getattr(collection, "query", []):
            if criteria["i"] == "finanziatori":
                criteria["o"] = 'plone.app.querystring.operation.boolean.isTrue'
                criteria["v"] = ""
            criteria["i"] = criteria_mapping.get(criteria["i"], criteria["i"])

            if criteria not in query:
                query.append(criteria)
        collection.query = query

        # fix sort_on
        #sort_on = getattr(collection, "sort_on", "")
        #if sort_on in criteria_mapping:
        #    collection.sort_on = criteria_mapping[sort_on]

        logger.info(
            "[{counter}/{tot}] - {collection}".format(
                counter=counter + 1,
                tot=tot_results,
                collection=brain.getPath(),
            )
        )
    logger.info("Upgrade to 3200 complete")
