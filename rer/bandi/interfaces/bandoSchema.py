# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.autoform import directives as form
from plone.supermodel import model
from rer.bandi import bandiMessageFactory as _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import NOVALUE
from zope import schema


def checkRequiredField(value):
    return value != NOVALUE


class IBandoSchema(model.Schema):
    """ A Dexterity schema for Annoucements """

    form.order_after(riferimenti_bando='IRichText.text')
    riferimenti_bando = RichText(
        title=_('riferimenti_bando_label', default=u"References"),
        description=_('riferimenti_bando_help', default=u""),
        required=False,
    )

    form.order_after(chiusura_procedimento_bando='IRichText.text')
    chiusura_procedimento_bando = schema.Date(
        title=_(
            'chiusura_procedimento_bando_label',
            default=u"Closing date procedure",
        ),
        description=_('chiusura_procedimento_bando_help', default=u''),
        required=False,
    )

    form.order_after(scadenza_bando='IRichText.text')
    scadenza_bando = schema.Datetime(
        title=_('scadenza_bando_label', default=u"Expiration date and time"),
        description=_(
            'scadenza_bando_help',
            default=u"Deadline to participate in the announcement",
        ),
        required=False,
    )

    form.order_after(destinatari='IRichText.text')
    directives.widget(destinatari=CheckBoxFieldWidget)
    destinatari = schema.List(
        title=_('destinatari_label', default=u'Who can apply'),
        description=_('destinatari_help', default=''),
        required=True,
        value_type=schema.Choice(
            vocabulary='rer.bandi.destinatari.vocabulary'
        ),
    )

    form.order_after(tipologia_bando='IRichText.text')
    # directives.widget(tipologia_bando=RadioFieldWidget)
    tipologia_bando = schema.Choice(
        title=_('tipologia_bando_label', default=u"Announcement type"),
        description=_('tipologia_bando_help', default=''),
        vocabulary='rer.bandi.tipologie.vocabulary',
        required=True,
        constraint=checkRequiredField,
    )

    form.order_after(finanziatori='IRichText.text')
    directives.widget(finanziatori=CheckBoxFieldWidget)
    finanziatori = schema.List(
        title=_('finanziatori_label', default=u'Founded with European funds'),
        description=_('finanziatori_help', default=''),
        required=True,
        value_type=schema.Choice(
            vocabulary='rer.bandi.finanziatori.vocabulary'
        ),
    )

    form.order_after(materie='IRichText.text')
    directives.widget(materie=CheckBoxFieldWidget)
    materie = schema.List(
        title=_('materie_label', default=u'Topic'),
        description=_('materie_help', default=''),
        required=True,
        value_type=schema.Choice(vocabulary='rer.bandi.materie.vocabulary'),
    )
