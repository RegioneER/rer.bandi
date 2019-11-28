# -*- coding: utf-8 -*-
from plone.app.vocabularies.catalog import KeywordsVocabulary


class TipologieBandoKeywordsVocabularyFactory(KeywordsVocabulary):

    keyword_index = 'getTipologia_bando'


class MaterieBandoKeywordsVocabularyFactory(KeywordsVocabulary):

    keyword_index = 'getMaterie_bando'


class FinanziatoriBandoKeywordsVocabularyFactory(KeywordsVocabulary):

    keyword_index = 'getFinanziatori_bando'


class DestinatariBandoKeywordsVocabularyFactory(KeywordsVocabulary):

    keyword_index = 'getDestinatariBando'


TipologieBandoKeywordsVocabulary = TipologieBandoKeywordsVocabularyFactory()
DestinatariBandoKeywordsVocabulary = (
    DestinatariBandoKeywordsVocabularyFactory()
)
FinanziatoriBandoKeywordsVocabulary = (
    FinanziatoriBandoKeywordsVocabularyFactory()
)
MaterieBandoKeywordsVocabulary = MaterieBandoKeywordsVocabularyFactory()
