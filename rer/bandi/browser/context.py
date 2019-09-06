# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.layout.globals.context import ContextState as BaseClass
from plone.app.layout.globals.interfaces import IContextState
from zope.interface import implementer


@implementer(IContextState)
class ContextState(BaseClass):
    """modifica il metodo Folder, per poter aggiungere elementi al documento anche quando è 
       impostato come vista predefinita
    """

    def folder(self):
        if self.is_structural_folder():
            return aq_inner(self.context)
        else:
            return self.parent()

