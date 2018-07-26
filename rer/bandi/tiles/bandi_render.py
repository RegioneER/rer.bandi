# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from collective.tiles.collection.interfaces import ICollectionTileRenderer
from zope.interface import implementer
from rer.bandi import bandiMessageFactory as _


@implementer(ICollectionTileRenderer)
class View(BrowserView):

    display_name = _('bandi_layout', default='Layout Bandi')
