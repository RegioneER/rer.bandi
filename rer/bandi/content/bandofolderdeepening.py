from zope.interface import implements
from rer.bandi.interfaces.bandofolderdeepening import IBandoFolderDeepening
from plone.dexterity.content import Container
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs


class BandoFolderDeepening(Container):
    implements(IBandoFolderDeepening)
    portal_type = 'Bando Folder Deepening'
    meta_type = 'Bando Folder Deepening'
