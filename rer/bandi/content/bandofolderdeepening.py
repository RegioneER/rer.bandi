# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from rer.bandi.interfaces.bandofolderdeepening import IBandoFolderDeepening
from zope.interface import implementer


@implementer(IBandoFolderDeepening)
class BandoFolderDeepening(Container):
    """ """
