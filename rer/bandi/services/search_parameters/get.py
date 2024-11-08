# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.services import Service
from rer.bandi import _
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.schema.interfaces import IVocabularyFactory


def getVocabularyTermsForForm(vocab_name, context):
    """
    Return the values of vocabulary
    """
    utility = getUtility(IVocabularyFactory, vocab_name)

    values = []

    vocab = utility(context)

    for entry in vocab:
        if entry.title != "select_label":
            values.append({"value": entry.value, "label": entry.title})
    return values


def getSearchFields():
    request = getRequest()
    portal = api.portal.get()
    return [
        {
            "id": "SearchableText",
            "label": translate(
                _("bandi_search_text_label", default="Search text"),
                context=request,
            ),
            "help": "",
            "type": "text",
        },
        {
            "id": "stato_bandi",
            "label": translate(
                _("bandi_search_state_label", default="State"),
                context=request,
            ),
            "help": "",
            "type": "select",
            "multivalued": False,
            "options": [
                {
                    "label": translate(
                        _("bando_state_all_select_label", default="All"),
                        context=request,
                    ),
                    "value": "",
                },
                {
                    "label": translate(
                        _("bando_state_open_select_label", default="Open"),
                        context=request,
                    ),
                    "value": "open",
                },
                {
                    "label": translate(
                        _(
                            "bando_state_inProgress_select_label",
                            default="In progress",
                        ),
                        context=request,
                    ),
                    "value": "inProgress",
                },
                {
                    "label": translate(
                        _(
                            "bando_state_closed_select_label",
                            default="Closed",
                        ),
                        context=request,
                    ),
                    "value": "closed",
                },
            ],
        },
        {
            "id": "tipologia_bando",
            "label": translate(
                _("bandi_search_type_label", default="Type"),
                context=request,
            ),
            "help": "",
            "type": "checkbox",
            "options": getVocabularyTermsForForm(
                context=portal, vocab_name="rer.bandi.tipologie.vocabulary"
            ),
        },
        {
            "id": "destinatari",
            "label": translate(
                _("destinatari_label", default="Who can apply"),
                context=request,
            ),
            "help": "",
            "type": "select",
            "multivalued": True,
            "options": getVocabularyTermsForForm(
                context=portal, vocab_name="rer.bandi.destinatari.vocabulary"
            ),
        },
        {
            "id": "finanziato",
            "label": translate(
                _(
                    "finanziatori_label",
                    default="Financed by EU programmes",
                ),
                context=request,
            ),
            "help": "",
            "type": "checkbox",
            "multivalued": False,
            "options": [
                {
                    "value": "Si",
                },
                {
                    "value": "No",
                },
            ],
        },
        {
            "id": "materie",
            "label": translate(
                _("materie_label", default="Topic"), context=request
            ),
            "help": "",
            "type": "select",
            "multivalued": True,
            "options": getVocabularyTermsForForm(
                context=portal, vocab_name="rer.bandi.materie.vocabulary"
            ),
        },
        {
            "id": "Subject",
            "label": translate(
                _("subject_label", default="Subjects"),
                context=request,
            ),
            "help": "",
            "type": "select",
            "multivalued": True,
            "options": getVocabularyTermsForForm(
                context=portal, vocab_name="plone.app.vocabularies.Keywords"
            ),
        },
    ]


@implementer(IPublishTraverse)
class SearchParametersGet(Service):
    def __init__(self, context, request):
        super(SearchParametersGet, self).__init__(context, request)

    def reply(self):
        return getSearchFields()
