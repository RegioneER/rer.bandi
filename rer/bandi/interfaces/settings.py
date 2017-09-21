from zope.interface import Interface
from zope import schema


#bisogna fare delle traduzioni che non sono state ancora fatte
class IBandoSettings(Interface):
    """
    Settings used for announcements default value
    """

    default_ente = schema.Tuple(
        title=u"default_ente",
        required=False,
        value_type=schema.TextLine(),
        missing_value=None
    )

    default_destinatari = schema.Tuple(
        title=u"default_destinatari_bandi",
        required=False,
        missing_value=None
    )