# -*- coding: utf-8 -*-
from plone.app.vocabularies.catalog import KeywordsVocabulary


class TipologieBandoKeywordsVocabularyFactory(KeywordsVocabulary):

    keyword_index = 'tipologia_bando'


class MaterieBandoKeywordsVocabularyFactory(KeywordsVocabulary):

    keyword_index = 'materie'


class FinanziatoriBandoKeywordsVocabularyFactory(KeywordsVocabulary):

    keyword_index = 'finanziatori'


class DestinatariBandoKeywordsVocabularyFactory(KeywordsVocabulary):

    keyword_index = 'destinatari'


TipologieBandoKeywordsVocabulary = TipologieBandoKeywordsVocabularyFactory()
DestinatariBandoKeywordsVocabulary = (
    DestinatariBandoKeywordsVocabularyFactory()
)
FinanziatoriBandoKeywordsVocabulary = (
    FinanziatoriBandoKeywordsVocabularyFactory()
)
MaterieBandoKeywordsVocabulary = MaterieBandoKeywordsVocabularyFactory()
