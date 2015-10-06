# -*- coding: utf-8 -*-
from plone.app.vocabularies.catalog import KeywordsVocabulary
from rer.bandi.filevocabulary import XMLFileVocabulary
from rer.bandi.psheetvocabulary import PropertySheetVocabulary


TipologiaBandoVocabularyFactory = XMLFileVocabulary(envvar='PLONE_RER_BANDI_VOCAB',
                                                    vocabulary_name='rer.bandi.tipologia.vocabulary',
                                                    default_terms=[
                                                        ('beni_servizi',
                                                         'Acquisizione beni e servizi'),
                                                        ('agevolazioni',
                                                         'Agevolazioni, finanziamenti, contributi'),
                                                        ('altro', 'Altro'),
                                                    ])


DestinatariVocabularyFactory = PropertySheetVocabulary(sheet_name='rer_bandi_settings',
                                                       property_name='destinatari_bandi',
                                                       default_terms=[
                                                           ('Cittadini',
                                                            'Cittadini'),
                                                           ('Imprese',
                                                            'Imprese'),
                                                           ('Enti locali',
                                                            'Enti locali'),
                                                           ('Associazioni',
                                                            'Associazioni'),
                                                           ('Altro', 'Altro')
                                                       ])


class DestinatariBandoVocabulary(KeywordsVocabulary):

    """
        Vocabulary factory listing all catalog keywords
        from the "getDestinatariBando" index
    """

    keyword_index = 'getDestinatariBando'


DestinatariBandoVocabularyFactory = DestinatariBandoVocabulary()


class TipologiaBandoVocabulary(KeywordsVocabulary):

    """
        Vocabulary factory listing all catalog keywords
        from the "getTipologia_bando" index
    """

    keyword_index = 'getTipologia_bando'


TipologiaBandoVocabularyFactory = TipologiaBandoVocabulary()
