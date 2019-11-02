# -*- coding: utf-8 -*-
from rer.bandi import bandiMessageFactory as _
from z3c.form.interfaces import NOVALUE
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

TIPOLOGIE_BANDO = [
    u'Agevolazioni, finanziamenti, contributi',
    u'Accreditamenti, albi, elenchi',
    u'Autorizzazioni di attivita',
    u'Manifestazioni di interesse',
]

DESTINATARI_BANDO = [
    u'Cittadini',
    u'Confidi',
    u'Cooperative',
    u'Enti del Terzo settore',
    u'Enti e laboratori di ricerca',
    u'Enti pubblici',
    u'Grandi imprese',
    u'Liberi professionisti',
    u'Micro imprese',
    u'Partenariato pubblico/privato',
    u'PMI',
    u'Scuole, università, enti di formazione',
    u'Soggetti accreditati',
]

FINANZIATORI_BANDO = [u'FESR', u'FSE', u'FEASR', u'FEAMP']

MATERIE_BANDO = [
    u'Agricoltura e sviluppo delle aree rurali',
    u'Ambiente',
    u'Beni immobili e mobili',
    u'Cultura',
    u'Diritti e sociale',
    u'Edilizia e rigenerazione urbana',
    u'Energia',
    u'Estero',
    u'Imprese e commercio',
    u'Innovazione e ICT',
    u'Istruzione e formazione',
    u'Lavoro',
    u'Mobilità e trasporti',
    u'Pesca',
    u'Ricerca',
    u'Riordino istituzionale',
    u'Sport',
]


class BandiBaseVocabularyFactory(object):
    @property
    def terms(self):
        return [
            SimpleTerm(
                value=x.encode('utf-8'), token=x.encode('utf-8'), title=x
            )
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
