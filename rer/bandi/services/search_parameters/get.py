# -*- coding: utf-8 -*-
from plone.api.portal import translate
from plone.restapi.services import Service
from zope.component import getUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.schema.interfaces import IVocabularyFactory


@implementer(IPublishTraverse)
class SearchParametersGet(Service):
    def __init__(self, context, request):
        super(SearchParametersGet, self).__init__(context, request)

    def reply(self):
        return [
            {
                'id': 'SearchableText',
                'label': translate(
                    msgid='bandi_search_text_label', domain='rer.bandi'
                ),
                'help': translate(
                    msgid='bandi_search_text_help', domain='rer.bandi'
                ),
                'type': 'text',
            },
            {
                'id': 'stato_bandi',
                'label': translate(
                    msgid='bandi_search_state_label', domain='rer.bandi'
                ),
                'help': translate(
                    msgid='bandi_search_state_help', domain='rer.bandi'
                ),
                'type': 'select',
                'values': [
                    {
                        'label': translate(
                            msgid='bandi_search_state_all', domain='rer.bandi'
                        ),
                        'value': '',
                    },
                    {
                        'label': translate(
                            msgid='bandi_search_state_open', domain='rer.bandi'
                        ),
                        'value': 'open',
                    },
                    {
                        'label': translate(
                            msgid='bandi_search_state_inprogress',
                            domain='rer.bandi',
                        ),
                        'value': 'inProgress',
                    },
                    {
                        'label': translate(
                            msgid='bandi_search_state_closed',
                            domain='rer.bandi',
                        ),
                        'value': 'closed',
                    },
                ],
            },
            {
                'id': 'getTipoligia_bando',
                'label': translate(
                    msgid='bandi_search_type_label', domain='rer.bandi'
                ),
                'help': '',
                'type': 'checkbox',
                'values': self.getVocabularyTermsForForm(
                    'rer.bandi.tipologie.vocabulary'
                ),
            },
            {
                'id': 'getTipoligia_bando',
                'label': translate(
                    msgid='bandi_search_type_label', domain='rer.bandi'
                ),
                'help': 'bandi_multiselect_help',
                'type': 'checkbox',
                'values': self.getVocabularyTermsForForm(
                    'rer.bandi.tipologie.vocabulary'
                ),
            },
        ]

    def getVocabularyTermsForForm(self, vocab_name):
        """
        Return the values of vocabulary
        """
        utility = getUtility(IVocabularyFactory, vocab_name)

        values = []

        vocab = utility(self.context)

        for entry in vocab:
            if entry.title != u'select_label':
                values.append(entry.value)
        return values
