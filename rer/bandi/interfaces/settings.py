from zope.interface import Interface
from zope import schema


class IBandoSettings(Interface):
    """
    DEPRECATED: It's still here only for 3000 upgrade-step
    """

    default_ente = schema.Tuple(
        title=u"default_ente",
        required=False,
        value_type=schema.TextLine(),
        missing_value=None,
    )

    default_destinatari = schema.Tuple(
        title=u"default_destinatari_bandi",
        required=False,
        value_type=schema.TextLine(),
        missing_value=None,
    )
