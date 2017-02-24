# -*- coding: utf-8 -*-

from Products.ATContentTypes.interface import IATTopic, IATContentType
from plone.app.collection.interfaces import ICollection
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.memoize.instance import memoize
from rer.bandi import bandiMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from rer.bandi.interfaces import IBando
from zope import schema
from zope.component import getMultiAdapter, getUtility
from zope.formlib import form
from zope.i18n import translate
from zope.interface import implements
try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory


COLLECTION_TYPES_LIST = [IATTopic.__identifier__, ICollection.__identifier__]


class IBandoCollectionPortlet(IPortletDataProvider):

    """A portlet which renders the results of a collection object.
    """

    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)

    target_collection = schema.Choice(title=_(u"Target collection"),
                                      description=_(
                                          u"Find the collection which provides the items to list"),
                                      required=True,
                                      source=SearchableTextSourceBinder(
        {
            'object_provides': COLLECTION_TYPES_LIST
        },
        default_query='path:'
    ))

    limit = schema.Int(title=_(u"Limit"),
                       description=_(u"Specify the maximum number of items to show in the portlet. "
                                     "Leave this blank to show all items."),
                       required=False)

    show_more = schema.Bool(title=_(u"Show more... link"),
                            description=_(u"If enabled, a more... link will appear in the footer of the portlet, "
                                          "linking to the underlying Collection."),
                            required=True,
                            default=True)

    show_more_text = schema.TextLine(title=_(u"Other text"),
                                     description=_(
                                         u"Alternative text to show in 'other' link."),
                                     required=True,
                                     default=u'Altro\u2026')

    show_more_path = schema.Choice(title=_(u"Alternative link to other"),
                                   description=_(
                                       u"Select a different link to 'other'."),
                                   required=False,
                                   source=SearchableTextSourceBinder({'sort_on': 'getObjPositionInParent'},
                                                                     default_query='path:'))

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

    def __init__(self, header=u"", target_collection=None, limit=None, show_more=True, show_more_text=None, show_more_path=None,
                 show_description=False, show_tipologia_bando=False, show_effective=False, show_scadenza_bando=False):
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
        return len(self.results())

    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return None
        else:
            return collection.absolute_url()

    def more_target_url(self):
        """
        link target to use (either the default collection or the alternate one)
        """
        if self.data.show_more_path:
            return self.portal().absolute_url() + self.data.show_more_path

        return self.collection_url()

    def results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            results = collection.queryCatalog(
                object_provides=IBando.__identifier__)
            if self.data.limit and self.data.limit > 0:
                results = results[:self.data.limit]
        return results

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
        return tipologia_bando in [x.title for x in self.voc_tipologia._terms]

    @memoize
    def collection(self):
        """ get the collection the portlet is pointing to"""

        collection_path = self.data.target_collection
        if not collection_path:
            return None

        if collection_path.startswith('/'):
            collection_path = collection_path[1:]

        if not collection_path:
            return None

        portal = self.portal()
        return portal.restrictedTraverse(collection_path, default=None)

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
        effective_date = bando.effective.Date()
        return effective_date != 'None' and effective_date != "1000/01/01"


class AddForm(base.AddForm):

    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IBandoCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields['show_more_path'].custom_widget = UberSelectionWidget

    label = _(u"Add Bandi Portlet")
    description = _(
        u"This portlet display a listing of bandi from a Collection.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(IBandoCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields['show_more_path'].custom_widget = UberSelectionWidget

    label = _(u"Edit Bandi Portlet")
    description = _(
        u"This portlet display a listing of bandi from a Collection.")
