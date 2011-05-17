Introduzione
============

Prodotto per i Bandi regionali


Configurazione vocabolario destinatari
--------------------------------------

Il prodotto cerca l'elenco dei possibili destinatari in una property:

    portal_properties.rer_bandi_settings.destinatari_bandi

Questa viene interpretata come campo multilinea.

In assenza di questo oggetto o property, viene usato l'elenco di default:

    Cittadini
    Imprese
    Enti locali
    Associazioni
    Altro



Configurazione vocabolario tipologie
------------------------------------

Il prodotto si aspetta un variabile d'ambiente di nome ``PLONE_RER_BANDI_VOCAB``.
E' possibile specificarla nel buildout::

    [instance]
    ...
    environment-vars =
        PLONE_RER_BANDI_VOCAB ${buildout:directory}/var/rer_bandi_vocab.xml

Questa va fornita come percorso ad un file XML contenente i bandi; se il file non esiste la procedura
genera un file predefinito::

    <?xml version='1.0' encoding='utf-8'?>
    <vocab-list>
      <vocabulary name="rer.bandi.tipologia.vocabulary">
        <term token="beni_servizi">Acquisizione beni e servizi</term>
        <term token="agevolazioni">Agevolazioni, finanziamenti, contributi</term>
        <term token="altro">Altro</term>
      </vocabulary>
    </vocab-list>

Ricerca bandi
-------------
Per cercare i bandi, basta richiamare la vista "search_bandi_form" da qualunque zona del sito.
