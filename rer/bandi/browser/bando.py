# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from rer.bandi.interfaces import IBandoFolderDeepening

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory

from zope.component import getMultiAdapter, getUtility
from zope.interface import implements, Interface

class IBandoView(Interface):
    pass


class BandoView(BrowserView):
    implements(IBandoView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.voc_tipologia = getUtility(IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)


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

    def retrieveContentsOfFolderDeepening(self,path_dfolder):
        """Retrieves all objects contained in Folder Deppening
        """
        path = {'query':path_dfolder,'depth':1}

        values = []
        objs = self.context.portal_catalog(
              path = path,
              sort_on = 'getObjPositionInParent'
        )

        pp = getToolByName(self.context, 'portal_properties')
        typesUseViewActionInListings = pp.site_properties.typesUseViewActionInListings

        ploneview = getMultiAdapter((self.context, self.request), name="plone")

        for obj in objs:
            if not obj.getPath()== path_dfolder and not obj.exclude_from_nav:
                dictfields=dict(title=obj.Title,
                                description=obj.Description,
                                url=obj.getURL(),
                                )
                if obj.Type=='Link':
                    dictfields['url']=obj.getRemoteUrl
                if obj.Type in typesUseViewActionInListings and not obj.Type=='File':
                    dictfields['url']=obj.getURL() + "/view"
                if obj.Type=='File':
                    dictfields['url']=obj.getURL() + "/at_download/file"
                    obj_file=obj.getObject().getFile()
                    if obj_file.meta_type=='ATBlob':
                        obj_size=obj_file.get_size()
                    else:
                         obj_size=obj_file.getSize()
                    dictfields['filesize']= self.getSizeString(obj_size)
                icon = ploneview.getIcon(obj)
                dictfields['icon'] = icon.html_tag()
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
        destinatari = self.context.getDestinatari()
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
