# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.autoform import directives as form
from plone.supermodel import model
from rer.bandi import bandiMessageFactory as _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import NOVALUE
from zope import schema
from z3c.form.browser.radio import RadioFieldWidget
from zope.interface import Invalid
from zope.schema._messageid import _ as zsm


def checkRequiredField(value):
    if value == NOVALUE or value == []:
        raise Invalid(zsm("""Required input is missing."""))
    return True


class IBandoSchema(model.Schema):
    """ A Dexterity schema for Annoucements """

    directives.widget(tipologia_bando=RadioFieldWidget)
    tipologia_bando = schema.Choice(
        title=_('tipologia_bando_label', default=u"Announcement type"),
        description=_('tipologia_bando_help', default=''),
        vocabulary='rer.bandi.tipologie.vocabulary',
        required=True,
    )

    directives.widget(destinatari=CheckBoxFieldWidget)
    destinatari = schema.List(
        title=_('destinatari_label', default=u'Who can apply'),
        description=_(
            'bandi_multiselect_help', default='Select one or more values.'
        ),
        constraint=checkRequiredField,
        required=True,
        value_type=schema.Choice(
            vocabulary='rer.bandi.destinatari.vocabulary'
        ),
    )

    directives.widget(finanziatori=CheckBoxFieldWidget)
    finanziatori = schema.List(
        title=_('finanziatori_label', default=u'Financed by EU programmes'),
        description=_(
            'bandi_multiselect_help', default='Select one or more values.'
        ),
        required=False,
        value_type=schema.Choice(
            vocabulary='rer.bandi.finanziatori.vocabulary'
        ),
    )

    directives.widget(materie=CheckBoxFieldWidget)
    materie = schema.List(
        title=_('materie_label', default=u'Topic'),
        description=_(
            'bandi_multiselect_help', default='Select one or more values.'
        ),
        required=False,
        value_type=schema.Choice(vocabulary='rer.bandi.materie.vocabulary'),
    )

    scadenza_bando = schema.Datetime(
        title=_('scadenza_bando_label', default=u"Expiration date and time"),
        description=_(
            'scadenza_bando_help',
            default=u"Deadline to participate in the announcement",
        ),
        required=False,
    )
    chiusura_procedimento_bando = schema.Date(
        title=_(
            'chiusura_procedimento_bando_label',
            default=u"Closing date procedure",
        ),
        description=_('chiusura_procedimento_bando_help', default=u''),
        required=False,
    )

    riferimenti_bando = RichText(
        title=_('riferimenti_bando_label', default=u"References"),
        description=_('riferimenti_bando_help', default=u""),
        required=False,
    )

    form.order_after(tipologia_bando='IRichText.text')
    form.order_after(destinatari='tipologia_bando')
    form.order_after(finanziatori='destinatari')
    form.order_after(materie='finanziatori')
    form.order_after(scadenza_bando='materie')
    form.order_after(chiusura_procedimento_bando='scadenza_bando')
    form.order_after(riferimenti_bando='chiusura_procedimento_bando')
