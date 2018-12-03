# -*- coding: utf-8 -*-
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.supermodel import model
from rer.bandi import bandiMessageFactory as _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from plone.autoform import directives as form


def getDefaultEnte():
    default_ente = api.portal.get_registry_record(
        'rer.bandi.interfaces.settings.IBandoSettings.default_ente'
    )
    if default_ente:
        return default_ente
    else:
        return None


class IBandoSchema(model.Schema):
    """ A Dexterity schema for Annoucements """

    form.order_after(riferimenti_bando='IRichText.text')
    riferimenti_bando = RichText(
        title=_('riferimenti_bando_label', default=u"References"),
        description=_('riferimenti_bando_help', default=u""),
        required=False
    )

    form.order_after(chiusura_procedimento_bando='IRichText.text')
    chiusura_procedimento_bando = schema.Date(
        title=_(
            'chiusura_procedimento_bando_label',
            default=u"Closing date procedure"
        ),
        description=_('chiusura_procedimento_bando_help', default=u''),
        required=False
    )

    form.order_after(scadenza_bando='IRichText.text')
    scadenza_bando = schema.Datetime(
        title=_('scadenza_bando_label', default=u"Expiration date and time"),
        description=_(
            'scadenza_bando_help',
            default=u"Deadline to participate in the announcement"
        ),
        required=False
    )

    form.order_after(ente_bando='IRichText.text')
    directives.widget('ente_bando', AjaxSelectFieldWidget,
                      vocabulary='rer.bandi.enti.vocabulary')
    ente_bando = schema.Tuple(
        title=_(u'ente_label', default=u'Authority'),
        description=_(u'ente_help', default=u'Select some authorities.'),
        required=False,
        defaultFactory=getDefaultEnte,
        value_type=schema.TextLine(),
        missing_value=None
    )

    form.order_after(destinatari='IRichText.text')
    directives.widget(destinatari=CheckBoxFieldWidget)
    destinatari = schema.List(
        title=_('destinatari_label', default=u"Recipients"),
        description=_('destinatari_help', default=''),
        required=True,
        value_type=schema.Choice(vocabulary='rer.bandi.destinatari.vocabulary')
    )

    form.order_after(tipologia_bando='IRichText.text')
    directives.widget(tipologia_bando=RadioFieldWidget)
    tipologia_bando = schema.Choice(
        title=_('tipologia_bando_label', default=u"Announcement type"),
        description=_('tipologia_bando_help', default=''),
        vocabulary='rer.bandi.tipologia.vocabulary',
        required=True
    )
