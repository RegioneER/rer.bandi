# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger('rer.bandi')


def import_various(context):
    if context.readDataFile('rer.bandi_various.txt') is None:
        return
