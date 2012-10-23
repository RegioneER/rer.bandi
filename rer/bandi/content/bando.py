
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from rer.bandi import bandiMessageFactory as _

from rer.bandi.interfaces import IBando
from rer.bandi.config import PROJECTNAME

BandoSchema = folder.ATFolderSchema.copy() + document.ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'tipologia_bando',
        storage=atapi.AnnotationStorage(),
        vocabulary_factory='rer.bandi.tipologia.vocabulary',
        widget=atapi.SelectionWidget(
            label=_('tipologia_bando_label', default=u"Announcement type"),
            description=_('tipologia_bando_help', default=''),
        ),
        required=True,
    ),


    atapi.LinesField(
        'destinatari',
        storage=atapi.AnnotationStorage(),
        vocabulary_factory='rer.bandi.destinatari.vocabulary',
        widget=atapi.MultiSelectionWidget(
            label=_('destinatari_label', default=u"Recipients"),
            description=_('destinatari_help', default=''),
            format='checkbox',
        ),
    ),

    atapi.LinesField(name='ente_bando',
                     default_method="getDefaultEnte",
                     widget=atapi.KeywordWidget(
                     label=_(u'ente_label',
                                default=u'Authority'),
                        description=_(u'ente_help',
                                      default=u'Select some authorities.'),
                       ),
            ),

    atapi.DateTimeField(
        'scadenza_bando',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_('scadenza_bando_label', default=u"Expiration date and time"),
            description=_('scadenza_bando_help', default=u"Deadline to participate in the announcement"),
        ),
        validators=('isValidDate'),
    ),


    atapi.DateTimeField(
        'chiusura_procedimento_bando',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_('chiusura_procedimento_bando_label', default=u"Closing date procedure"),
            description=_('chiusura_procedimento_bando_help', default=u''),
            show_hm=False,
        ),
        validators=('isValidDate'),
    ),


    atapi.TextField(
        'riferimenti_bando',
        storage=atapi.AnnotationStorage(),
        searchable=True,
        widget=atapi.RichWidget(
            label=_('riferimenti_bando_label', default=u"References"),
            description=_('riferimenti_bando_help', default=u""),
        ),
    ),


))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BandoSchema['title'].storage = atapi.AnnotationStorage()
BandoSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    BandoSchema,
    folderish=True,
    moveDiscussion=False
)

BandoSchema['relatedItems'].widget.visible = {'view': 'visible', 'edit': 'visible'}


class Bando(folder.ATFolder):
    implements(IBando)

    meta_type = "Bando"
    schema = BandoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    tipologia_bando = atapi.ATFieldProperty('tipologia_bando')

    destinatari = atapi.ATFieldProperty('destinatari')

    scadenza_bando = atapi.ATFieldProperty('scadenza_bando')

    chiusura_procedimento_bando = atapi.ATFieldProperty('chiusura_procedimento_bando')

    riferimenti_bando = atapi.ATFieldProperty('riferimenti_bando')

    def getDefaultEnte(self):
        """
        return a default value for Ente
        """
        portal_properties = getToolByName(self, 'portal_properties')
        rer_bandi_settings = getattr(portal_properties, 'rer_bandi_settings', None)
        if rer_bandi_settings:
            return rer_bandi_settings.getProperty('default_ente', '')
        return ''

atapi.registerType(Bando, PROJECTNAME)
