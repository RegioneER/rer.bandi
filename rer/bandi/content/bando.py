# -*- coding: utf-8 -*-
from zope.interface import implements
from rer.bandi.interfaces.bando import IBando
from plone.dexterity.content import Container


class Bando(Container):
    implements(IBando)

    # BBB
    isReferenceable = True
    portal_type = 'Bando'
    meta_type = 'Dexterity Item' # senza l'oggetto non è incollabile
