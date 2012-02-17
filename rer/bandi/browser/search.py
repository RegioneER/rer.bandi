# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.i18n import translate
from rer.bandi import bandiMessageFactory as _
try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory

from zope.component import getUtility

class SearchBandiForm(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        voc_tipologia = getUtility(IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)
        self.terms_tipologia = list(voc_tipologia)

        voc_destinatari = getUtility(IVocabularyFactory, name='rer.bandi.destinatari.vocabulary')(self.context)
        self.terms_destinatari = list(voc_destinatari)

class SearchBandi(BrowserView):
    """
    A view for search bandi results
    """
    def searchBandi(self):
        """
        return a list of bandi
        """
        pc=getToolByName(self.context,'portal_catalog')
        stato = self.request.form.get('stato_bandi','')
        if stato:
            now=DateTime()
            if stato=="open":
                self.request.form['getScadenza_bando']={'query':now,'range':'min'}
            if stato=="inProgress":
                self.request.form['getScadenza_bando']={'query':now,'range':'max'}
                self.request.form['getChiusura_procedimento_bando']={'query':now,'range':'min'}
            if stato=="closed":
                self.request.form['getChiusura_procedimento_bando']={'query':now,'range':'max'}
        return pc(**self.request.form)
    
    def getBandoState(self,bando):
        """
        """
        scadenza_bando=bando.scadenza_bando
        chiusura_procedimento_bando=bando.chiusura_procedimento_bando
        state=('open',translate(_(u'Open'),context=self.request))
        if scadenza_bando and scadenza_bando.isPast():
            if chiusura_procedimento_bando and chiusura_procedimento_bando.isPast():
                state= ('closed',translate(_(u'Closed'),context=self.request))
            else:
                state= ('inProgress',translate(_(u'In progress'),context=self.request))
        else:
            if chiusura_procedimento_bando and chiusura_procedimento_bando.isPast():
                state= ('closed',translate(_(u'Closed'),context=self.request))
        return state
        