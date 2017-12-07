# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from collective.tiles.collection.interfaces import ICollectionTileRenderer
from zope.interface import implements
from rer.bandi import bandiMessageFactory as _
from zope.i18n import translate
from zope.component import getUtility
try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory


class HelpersView(BrowserView):

    def getBandoState(self, bando):
        """
        return corretc bando state
        """

        scadenza_bando = bando.getScadenza_bando
        chiusura_procedimento_bando = bando.getChiusura_procedimento_bando
        state = ('open', translate(_(u'Open'), context=self.request))
        if scadenza_bando and scadenza_bando.isPast():
            if (chiusura_procedimento_bando and
                    chiusura_procedimento_bando.isPast()):
                state = (
                    'closed', translate(_(u'Closed'), context=self.request))
            else:
                state = (
                    'inProgress',
                    translate(_(u'In progress'), context=self.request)
                )
        else:
            if (chiusura_procedimento_bando and
                    chiusura_procedimento_bando.isPast()):
                state = (
                    'closed', translate(_(u'Closed'), context=self.request))

        return state

    def voc_tipologia(self):
        return getUtility(
            IVocabularyFactory, name='rer.bandi.tipologia.vocabulary'
        )(self.context)

    def has_effective_date(self, bando):
        if bando.EffectiveDate() == 'None':
            return False
        else:
            effective_date = bando.effective.Date()
            return effective_date != 'None' and effective_date != "1000/01/01"

    def isValidDeadline(self, date):
        """
        """
        if not date:
            return False
        if date.Date() == '2100/12/31':
            # a default date for bandi that don't have a defined deadline
            return False
        return True


class View(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("bandi_layout", default="Layout Bandi")
