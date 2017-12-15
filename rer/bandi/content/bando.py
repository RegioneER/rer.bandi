# -*- coding: utf-8 -*-
from zope.interface import implements
from rer.bandi.interfaces.bando import IBando
from plone.dexterity.content import Container


class Bando(Container):
    implements(IBando)
