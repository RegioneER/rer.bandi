# -*- coding: utf-8 -*-
from rer.bandi import bandiMessageFactory as _
from z3c.form.interfaces import NOVALUE
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

TIPOLOGIE_BANDO = [
    'Agevolazioni, finanziamenti, contributi',
    'Accreditamenti, albi, elenchi',
    'Autorizzazioni di attivita',
    'Manifestazioni di interesse',
]

DESTINATARI_BANDO = [
    'Cittadini',
    'Confidi',
    'Cooperative',
    'Enti del Terzo settore',
    'Enti e laboratori di ricerca',
    'Enti pubblici',
    'Grandi imprese',
    'Liberi professionisti',
    'Micro imprese',
    'Partenariato pubblico/privato',
    'PMI',
    'Scuole, università, enti di formazione',
    'Soggetti accreditati',
]

FINANZIATORI_BANDO = ['FESR', 'FSE', 'FEASR', 'FEAMP']

MATERIE_BANDO = [
    'Agricoltura e sviluppo delle aree rurali',
    'Ambiente',
    'Beni immobili e mobili',
    'Cultura',
    'Diritti e sociale',
    'Edilizia e rigenerazione urbana',
    'Energia',
    'Estero',
    'Imprese e commercio',
    'Innovazione e ICT',
    'Istruzione e formazione',
    'Lavoro',
    'Mobilità e trasporti',
    'Pesca',
    'Ricerca',
    'Riordino istituzionale',
    'Sport',
]


class BandiBaseVocabularyFactory(object):
    @property
    def terms(self):
        return [
            SimpleTerm(value=x, token=x, title=x.decode('utf-8'))
            for x in self.vocab_name
        ]

    def __call__(self, context):
        return SimpleVocabulary(self.terms)


@implementer(IVocabularyFactory)
class TipologieBandoVocabularyFactory(BandiBaseVocabularyFactory):

    vocab_name = TIPOLOGIE_BANDO


@implementer(IVocabularyFactory)
class DestinatariBandoVocabularyFactory(BandiBaseVocabularyFactory):

    vocab_name = DESTINATARI_BANDO


@implementer(IVocabularyFactory)
class FinanziatoriBandoVocabularyFactory(BandiBaseVocabularyFactory):

    vocab_name = FINANZIATORI_BANDO


@implementer(IVocabularyFactory)
class MaterieBandoVocabularyFactory(BandiBaseVocabularyFactory):

    vocab_name = MATERIE_BANDO


TipologieBandoVocabulary = TipologieBandoVocabularyFactory()
DestinatariBandoVocabulary = DestinatariBandoVocabularyFactory()
FinanziatoriBandoVocabulary = FinanziatoriBandoVocabularyFactory()
MaterieBandoVocabulary = MaterieBandoVocabularyFactory()
