"""Definition of the Bando Folder Deepening content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFPlone.interfaces.breadcrumbs import IHideFromBreadcrumbs

# -*- Message Factory Imported Here -*-

from rer.bandi.interfaces import IBandoFolderDeepening
from rer.bandi.config import PROJECTNAME

BandoFolderDeepeningSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BandoFolderDeepeningSchema['title'].storage = atapi.AnnotationStorage()
BandoFolderDeepeningSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    BandoFolderDeepeningSchema,
    folderish=True,
    moveDiscussion=False
)

BandoFolderDeepeningSchema.changeSchemataForField('excludeFromNav', 'default')
BandoFolderDeepeningSchema['relatedItems'].widget.visible = {'view': 'visible', 'edit': 'visible'}



class BandoFolderDeepening(folder.ATFolder):
    """A folder that is handled in a special way by Bando."""
    implements(IBandoFolderDeepening, IHideFromBreadcrumbs)

    meta_type = "BandoFolderDeepening"
    schema = BandoFolderDeepeningSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(BandoFolderDeepening, PROJECTNAME)
