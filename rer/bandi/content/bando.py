# -*- coding: utf-8 -*-
from zope.interface import implementer
from rer.bandi.interfaces.bando import IBando
from plone.dexterity.content import Container


@implementer(IBando)
class Bando(Container):
    """ """
