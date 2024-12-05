# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

TIPOLOGIE_BANDO = [
    u"Agevolazioni, finanziamenti, contributi",
    u"Accreditamenti, albi, elenchi",
    u"Autorizzazioni di attività",
    u"Manifestazioni di interesse",
]

DESTINATARI_BANDO = [
    u"Cittadini",
    u"Confidi",
    u"Cooperative",
    u"Enti del Terzo settore",
    u"Enti e laboratori di ricerca",
    u"Enti pubblici",
    u"Grandi imprese",
    u"Liberi professionisti",
    u"Micro imprese",
    u"Partenariato pubblico/privato",
    u"PMI",
    u"Scuole, università, enti di formazione",
    u"Soggetti accreditati",
]


MATERIE_BANDO = [
    u"Agricoltura e sviluppo delle aree rurali",
    u"Ambiente",
    u"Beni immobili e mobili",
    u"Cultura",
    u"Diritti e sociale",
    u"Edilizia e rigenerazione urbana",
    u"Energia",
    u"Estero",
    u"Fauna, caccia, pesca",
    u"Imprese e commercio",
    u"Innovazione e ICT",
    u"Istruzione e formazione",
    u"Lavoro",
    u"Mobilità e trasporti",
    u"Ricerca",
    u"Riordino istituzionale",
    u"Sport",
]


class BandiBaseVocabularyFactory(object):
    @property
    def terms(self):
        res = []
        return [
            SimpleTerm(value=x, token=x.encode("utf-8"), title=x)
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
class MaterieBandoVocabularyFactory(BandiBaseVocabularyFactory):

    vocab_name = MATERIE_BANDO


TipologieBandoVocabulary = TipologieBandoVocabularyFactory()
DestinatariBandoVocabulary = DestinatariBandoVocabularyFactory()
MaterieBandoVocabulary = MaterieBandoVocabularyFactory()
