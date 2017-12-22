# -*- coding: utf-8 -*-
import logging
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.app.layout.icons.interfaces import IContentIcon
from rer.bandi.interfaces import IBandoFolderDeepening
from datetime import datetime
from DateTime import DateTime

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory

from zope.component import getMultiAdapter, getUtility
from zope.interface import implements, Interface
logger = logging.getLogger('rer.bandi')

class IBandoView(Interface):
    pass


class BandoView(BrowserView):
    implements(IBandoView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.voc_tipologia = getUtility(IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)

    def titleTipologiaBando(self):
        try:
            term = self.voc_tipologia.getTermByToken(self.context.tipologia_bando)
            return term.title
        except LookupError:
            logger.error('tipologia_bando %s not found in vocabulary', self.context.tipologia_bando)
            return self.context.tipologia_bando


    def retrieveFolderDeepening(self):
        """Retrieves all Folder Deppening objects contained in Structured Document
        """
        struct_doc = self.context
        values = []
        dfolders = struct_doc.getFolderContents(contentFilter={'object_provides': IBandoFolderDeepening.__identifier__})
        for df in dfolders:
            if not df.exclude_from_nav:
                values.append(dict(title=df.Title,
                                   description=df.Description,
                                   url=df.getURL(),
                                   path=df.getPath()
                                   ))
        return values

    def retrieveContentsOfFolderDeepening(self, path_dfolder):
        """Retrieves all objects contained in Folder Deppening
        """

        values = []
        objs = self.context.portal_catalog(
            path={'query': path_dfolder, 'depth': 1},
            sort_on='getObjPositionInParent'
        )
        pp = getToolByName(self.context, 'portal_properties')

        for obj in objs:
            if not obj.getPath()== path_dfolder and not obj.exclude_from_nav:
                dictfields=dict(title=obj.Title,
                                description=obj.Description,
                                url=obj.getURL(),
                                path=obj.getPath(),
                                )
                if obj.Type=='Link':
                    dictfields['url']=obj.getRemoteUrl
                if obj.Type=='File':
                    _obj = obj.getObject()
                    if hasattr(_obj, 'file'):
                        # DX
                        dictfields['url']=obj.getURL() + "/download/file"
                        obj_size=_obj.file.size
                    else:
                        # AT
                        dictfields['url']=obj.getURL() + "/at_download/file"
                        obj_file=_obj.getFile()
                        if obj_file.meta_type=='ATBlob':
                            obj_size=obj_file.get_size()
                        else:
                            obj_size=obj_file.getSize()
                    dictfields['filesize']= self.getSizeString(obj_size)
                else:
                    dictfields['url']=obj.getURL() + "/view"

                # icon = getMultiAdapter((self.context, self.request, obj), IContentIcon)
                # dictfields['icon'] = icon.html_tag()
                dictfields['type'] = obj.Type
                values.append(dictfields)

        return values

    def getSizeString(self,size):
        const = {'kB':1024,
                 'MB':1024*1024,
                 'GB':1024*1024*1024}
        order = ('GB', 'MB', 'kB')
        smaller = order[-1]
        if not size:
            return '0 %s' % smaller

        if size < const[smaller]:
            return '1 %s' % smaller
        for c in order:
            if size/const[c] > 0:
                break
        return '%.2f %s' % (float(size/float(const[c])), c)

    def getDestinatariNames(self):
        """
        Return the values of destinatari vocabulary
        """
        dest_utility = getUtility(IVocabularyFactory, 'rer.bandi.destinatari.vocabulary')
        destinatari = self.context.destinatari
        if not dest_utility:
            return destinatari
        dest_values = []
        dest_vocab = dest_utility(self.context)
        for dest in destinatari:
            try:
                dest_title = dest_vocab.getTerm(dest).title
            except LookupError:
                dest_title = dest
            dest_values.append(dest_title)
        return dest_values

    def getEffectiveDate(self):
        """
        Return effectiveDate
        """
        plone = getMultiAdapter((self.context, self.request), name="plone")
        #da sistemare meglio questa parte
        #restituisce la prima data possibile quando questa non è presente
        time = self.context.effective()

        #controllo che EffectiveDate torni il valore stringa None, se cosi significa che non e stata settata la data di pubblicazione
        #se cosi allora torna None
        if self.context.EffectiveDate() == "None":
            return None
        else:
            return plone.toLocalizedTime(time)


    def getDeadLinePartecipationDate(self):
        """
        Return deadline partecipation date
        """
        plone = getMultiAdapter((self.context, self.request), name="plone")
        time = self.context.scadenza_bando
        return plone.toLocalizedTime(time, long_format=True)

    def getAnnouncementCloseDate(self):
        """
        Return Annoucement close date
        """
        plone = getMultiAdapter((self.context, self.request), name="plone")
        time = self.context.chiusura_procedimento_bando
        return time.strftime('%d/%m/%Y')
