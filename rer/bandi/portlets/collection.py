# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from rer.bandi import bandiMessageFactory as _
from plone.portlet.collection.collection import ICollectionPortlet
from zope import schema
from zope.component import getMultiAdapter, getUtility
from plone.app.portlets.browser import formhelper
from zope.i18n import translate
from plone.app.vocabularies.catalog import CatalogSource
from zope.interface import implements
from plone import api
try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory


class IBandoCollectionPortlet(ICollectionPortlet):
    """A portlet which renders the results of a collection object.
    """

    show_more_text = schema.TextLine(title=_(u"Other text"),
                                     description=_(
                                         u"Alternative text to show in 'other' link."),
                                     required=True,
                                     default=u'Altro\u2026')

    show_more_path = schema.Choice(
                            title=_(u"Internal link"),
                            description=_(u"Insert an internal link. This field override external link field"),
                            required=False,
                            source=CatalogSource())

    show_description = schema.Bool(
        title=u'Mostra descrizione', required=True, default=False)

    show_tipologia_bando = schema.Bool(
        title=u'Mostra tipologia bando', required=True, default=False)

    show_effective = schema.Bool(
        title=u'Mostra data di pubblicazione', required=True, default=False)

    show_scadenza_bando = schema.Bool(
        title=u'Mostra data di scadenza', required=True, default=False)


class Assignment(base.Assignment):

    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IBandoCollectionPortlet)

    header = u""
    target_collection = None
    limit = None
    show_more = True

    # parametri da ripulire
    def __init__(self, header=u"", target_collection=None, limit=None, show_more=True, show_more_text=None, show_more_path=None,
                 show_description=False, show_tipologia_bando=False, show_effective=False, show_scadenza_bando=False,
                 uid=None, thumb_scale=None, random=False, show_dates=False, exclude_context=True, no_icons=False, no_thumbs=False):


        # lista di data, che viene passata all'instanza dell'assignment
        self.header = header
        self.target_collection = target_collection
        self.limit = limit
        self.show_more = show_more
        self.show_more_text = show_more_text
        self.show_more_path = show_more_path
        self.show_description = show_description
        self.show_tipologia_bando = show_tipologia_bando
        self.show_effective = show_effective
        self.show_scadenza_bando = show_scadenza_bando

        self.uid = uid
        self.thumb_scale = thumb_scale
        self.random = random
        self.show_dates = show_dates
        self.exclude_context = exclude_context
        self.no_icons = no_icons
        self.no_thumbs = no_thumbs

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):

    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    _template = ViewPageTemplateFile('collection.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        self.voc_tipologia = getUtility(
            IVocabularyFactory, name='rer.bandi.tipologia.vocabulary')(self.context)

    # Cached version - needs a proper cache key
    # @ram.cache(render_cachekey)
    # def render(self):
    #     if self.available:
    #         return xhtml_compress(self._template())
    #     else:
    #         return ''

    render = _template

    @property
    def available(self):
        #se la lista di risultati è maggiore di zero allora si puo mostrare la portlet
        return len(self.results())

    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return None
        else:
            #torna una lista di url
            return collection.absolute_url()

    def more_target_url(self):
        """
        link target to use (either the default collection or the alternate one)
        """
        if self.data.show_more_path:
            return self.portal().absolute_url() + self.data.show_more_path

        return self.collection_url()

    # controllare bene questa funzione
    def results(self):
        results = []
        resultList = []
        # la collection su cui vogliamo costrire la portlet ?
        collection = self.collection()
        if collection is not None:
            # tornano tutti gli oggetti della mia collezione
            results = collection.queryCatalog()

            resultList = list(results)
            for el in list(results):

                # controllo che gli elementi all interno della lista siano dei bandi
                if not el.ContentTypeClass() == "contenttype-bando":
                    resultList.pop()

            # se è settato un limite e se il limite è maggiore di zero
            if self.data.limit and self.data.limit > 0:
                resultList = resultList[:self.data.limit]

        #ottengo tutti i bandi che devo mostrare nella collection
        return resultList

    def isValidDeadline(self, date):
        """
        """
        if not date:
            return False
        if date.Date() == '2100/12/31':
           #a default date for bandi that don't have a defined deadline
            return False
        return True

    def isTipologiaValid(self, tipologia_bando):
        """
        """
        return tipologia_bando in [x.value for x in self.voc_tipologia._terms]

    @memoize
    def collection(self):
        """ get the collection the portlet is pointing to"""

        # collection_path = self.data.target_collection
        # if not collection_path:
        #     return None

        # if collection_path.startswith('/'):
        #     collection_path = collection_path[1:]

        # if not collection_path:
        #     return None

        # portal = self.portal()
        # return portal.restrictedTraverse(collection_path, default=None)
        # collectionUID = self.data.target_collection
        collectionUID = self.data.uid
        if not collectionUID:
            return ""

        return api.content.get(UID=collectionUID)

    def getScadenzaDate(self, brain):
        date = brain.getScadenza_bando
        long_format = True
        if brain.getScadenza_bando.Time() == '00:00:00':
            # indexer add 1 day to this date, to make a bando ends at midnight
            # of the day-after, if time is not provided
            date = date - 1
            long_format = False
        return api.portal.get_localized_time(
            datetime=date,
            long_format=long_format
        )

    def portal(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        return portal_state.portal()

    def getBandoState(self, bando):
        """
        return corretc bando state
        """
        scadenza_bando = bando.getScadenza_bando
        chiusura_procedimento_bando = bando.getChiusura_procedimento_bando
        state = ('open', translate(_(u'Open'), context=self.request))
        if scadenza_bando and scadenza_bando.isPast():
            if chiusura_procedimento_bando and chiusura_procedimento_bando.isPast():
                state = (
                    'closed', translate(_(u'Closed'), context=self.request))
            else:
                state = (
                    'inProgress', translate(_(u'In progress'), context=self.request))
        else:
            if chiusura_procedimento_bando and chiusura_procedimento_bando.isPast():
                state = (
                    'closed', translate(_(u'Closed'), context=self.request))

        return state

    def has_effective_date(self, bando):
        if bando.EffectiveDate() == 'None':
            return False
        else:
            effective_date = bando.effective.Date()
            return effective_date != 'None' and effective_date != "1969/12/31"


class AddForm(formhelper.AddForm):

    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    schema = IBandoCollectionPortlet

    label = _(u"Add Bandi Portlet")
    description = _(
         u"This portlet display a listing of bandi from a Collection.")

    def create(self, data):
        return Assignment(**data)


class EditForm(formhelper.EditForm):

    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    schema = IBandoCollectionPortlet

    label = _(u"Edit Bandi Portlet")
    description = _(
         u"This portlet display a listing of bandi from a Collection.")
