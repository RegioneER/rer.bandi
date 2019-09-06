# -*- coding: utf-8 -*-
from plone import api
from rer.bandi.filevocabulary import XMLFileVocabulary
from six.moves import range
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


TipologiaBandoVocabularyFactory = XMLFileVocabulary(
    envvar='PLONE_RER_BANDI_VOCAB',
    vocabulary_name='rer.bandi.tipologia.vocabulary',
    default_terms=[
        ('beni_servizi', 'Acquisizione beni e servizi'),
        ('agevolazioni', 'Agevolazioni, finanziamenti, contributi'),
        ('altro', 'Altro'),
    ],
)


@implementer(IVocabularyFactory)
class DestinatariVocabularyFactory(object):
    def __call__(self, context):
        values = api.portal.get_registry_record(
            'rer.bandi.interfaces.settings.IBandoSettings.default_destinatari'
        )

        l = []
        for i in range(len(values)):
            l.append(tuple(values[i].split('|')))

        terms = [
            SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
            for pair in l
        ]
        return SimpleVocabulary(terms)


DestinatariVocabulary = DestinatariVocabularyFactory()


@implementer(IVocabularyFactory)
class EnteVocabularyFactory(object):
    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        enti = list(catalog._catalog.uniqueValuesFor('getEnte_bando'))

        terms = [
            SimpleTerm(value=ente, token=ente, title=ente) for ente in enti
        ]

        return SimpleVocabulary(terms)


EnteVocabulary = EnteVocabularyFactory()
