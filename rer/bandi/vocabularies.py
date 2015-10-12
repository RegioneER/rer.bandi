# -*- coding: utf-8 -*-
from plone.app.vocabularies.catalog import KeywordsVocabulary
from rer.bandi.filevocabulary import XMLFileVocabulary
from rer.bandi.psheetvocabulary import PropertySheetVocabulary
try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory

from zope.interface.declarations import implements
from zope.interface import implementer
from zope.component.hooks import getSite
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility


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

@implementer(IVocabularyFactory)
class CatalogDestinatarioBandoVocabulary(object):

    """
        Vocabulary factory listing all catalog keywords
        from the "getDestinatariBando" index
    """
    keyword_index = 'getDestinatariBando'
    vocab_id = "rer.bandi.destinatari.vocabulary"

    def __call__(self, context):
        site = getSite()
        catalog = getToolByName(site, "portal_catalog", None)
        index = catalog._catalog.getIndex(self.keyword_index)

        # Vocabulary term tokens *must* be 7 bit values, titles *must* be
        # unicode
        factory = getUtility(
            IVocabularyFactory,
            self.vocab_id,
        )
        vocabulary = factory(site)
        items = []
        for index_name in index._index:
            if isinstance(index_name, unicode):
                # no need to use portal encoding for transitional encoding from
                # unicode to ascii. utf-8 should be fine.
                index_name = index_name.encode('utf-8')
            try:
                title = vocabulary.getTerm(index_name)
            except LookupError:
                title = index_name
            items.append(SimpleTerm(
                value=index_name,
                token=index_name,
                title=title.title
            ))
        return SimpleVocabulary(items)


CatalogDestinatarioBandoVocabularyFactory = CatalogDestinatarioBandoVocabulary()


@implementer(IVocabularyFactory)
class CatalogTipologiaBandoVocabulary(CatalogDestinatarioBandoVocabulary):

    """
        Vocabulary factory listing all catalog keywords
        from the "getTipologia_bando" index
    """

    keyword_index = 'getTipologia_bando'
    vocab_id = "rer.bandi.tipologia.vocabulary"

CatalogTipologiaBandoVocabularyFactory = CatalogTipologiaBandoVocabulary()
