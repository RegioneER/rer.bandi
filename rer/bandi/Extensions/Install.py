# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from cStringIO import StringIO


def runProfile(portal, profileName):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profileName)


def uninstall(portal, reinstall=False):
    out = StringIO()
    if not reinstall:
        runProfile(portal, 'profile-rer.bandi:uninstall')
