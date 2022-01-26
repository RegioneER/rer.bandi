# -*- coding: utf-8 -*-
from plone import api
from Products.Five import BrowserView
from rer.bandi import _
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory


class ICollectionBandiView(Interface):
    pass


@implementer(ICollectionBandiView)
class CollectionBandiView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.voc_tipologia = getUtility(
            IVocabularyFactory, name='rer.bandi.tipologie.vocabulary'
        )(self.context)

    def getTipologiaTitle(self, key):
        """
        """
        try:
            value = self.voc_tipologia.getTermByToken(key)
            return value.title
        except LookupError:
            return key

    def isValidDeadline(self, date):
        """
        """
        if not date:
            return False
        if date.Date() == '2100/12/31':
            # a default date for bandi that don't have a defined deadline
            return False
        return True

    def getScadenzaDate(self, brain):
        date = brain.scadenza_bando
        long_format = True
        if brain.scadenza_bando.Time() == '00:00:00':
            # indexer add 1 day to this date, to make a bando ends at midnight
            # of the day-after, if time is not provided
            date = date - 1
            long_format = False
        return api.portal.get_localized_time(
            datetime=date, long_format=long_format
        )

    def getBandoState(self, bando):
        """
        return corretc bando state
        """
        scadenza_bando = bando.scadenza_bando
        chiusura_procedimento_bando = bando.chiusura_procedimento_bando
        state = ('open', translate(_(u'Open'), context=self.request))
        if scadenza_bando and scadenza_bando.isPast():
            if (
                chiusura_procedimento_bando
                and chiusura_procedimento_bando.isPast()
            ):
                state = (
                    'closed',
                    translate(_(u'Closed'), context=self.request),
                )
            else:
                state = (
                    'inProgress',
                    translate(_(u'In progress'), context=self.request),
                )
        else:
            if (
                chiusura_procedimento_bando
                and chiusura_procedimento_bando.isPast()
            ):
                state = (
                    'closed',
                    translate(_(u'Closed'), context=self.request),
                )
        return state
