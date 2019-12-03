# -*- coding: utf-8 -*-
from plone.restapi.services import Service
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.schema.interfaces import IVocabularyFactory
from rer.bandi import _


@implementer(IPublishTraverse)
class SearchParametersGet(Service):
    def __init__(self, context, request):
        super(SearchParametersGet, self).__init__(context, request)

    def reply(self):
        return [
            {
                'id': 'SearchableText',
                'label': translate(
                    _('bandi_search_text_label', default=u'Search text'),
                    context=self.request,
                ),
                'help': '',
                'type': 'text',
            },
            {
                'id': 'stato_bandi',
                'label': translate(
                    _('bandi_search_state_label', default=u'State'),
                    context=self.request,
                ),
                'help': '',
                'type': 'select',
                'multivalued': False,
                'options': [
                    {
                        'label': translate(
                            _('bando_state_all_select_label', default='All'),
                            context=self.request,
                        ),
                        'value': '',
                    },
                    {
                        'label': translate(
                            _('bando_state_open_select_label', default='Open'),
                            context=self.request,
                        ),
                        'value': 'open',
                    },
                    {
                        'label': translate(
                            _(
                                'bando_state_inProgress_select_label',
                                default='In progress',
                            ),
                            context=self.request,
                        ),
                        'value': 'inProgress',
                    },
                    {
                        'label': translate(
                            _(
                                'bando_state_closed_select_label',
                                default='Closed',
                            ),
                            context=self.request,
                        ),
                        'value': 'closed',
                    },
                ],
            },
            {
                'id': 'getTipologia_bando',
                'label': translate(
                    _('bandi_search_type_label', default='Type'),
                    context=self.request,
                ),
                'help': '',
                'type': 'checkbox',
                'options': self.getVocabularyTermsForForm(
                    'rer.bandi.tipologie.vocabulary'
                ),
            },
            {
                'id': 'getDestinatariBando',
                'label': translate(
                    _('destinatari_label', default='Who can apply'),
                    context=self.request,
                ),
                'help': '',
                'type': 'select',
                'multivalued': True,
                'options': self.getVocabularyTermsForForm(
                    'rer.bandi.destinatari.vocabulary'
                ),
            },
            {
                'id': 'getFinanziatori_bando',
                'label': translate(
                    _(
                        'finanziatori_label',
                        default='Financed by EU programmes',
                    ),
                    context=self.request,
                ),
                'help': '',
                'type': 'select',
                'multivalued': True,
                'options': self.getVocabularyTermsForForm(
                    'rer.bandi.finanziatori.vocabulary'
                ),
            },
            {
                'id': 'getMaterie_bando',
                'label': translate(
                    _('materie_label', default='Topic'), context=self.request
                ),
                'help': '',
                'type': 'select',
                'multivalued': True,
                'options': self.getVocabularyTermsForForm(
                    'rer.bandi.materie.vocabulary'
                ),
            },
            {
                'id': 'Subject',
                'label': translate(
                    _('subject_label', default='Subjects'),
                    context=self.request,
                ),
                'help': '',
                'type': 'select',
                'multivalued': True,
                'options': self.getVocabularyTermsForForm(
                    'plone.app.vocabularies.Keywords'
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
                values.append({'value': entry.value, 'label': entry.title})
        return values
