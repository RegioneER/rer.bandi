Introduction
============

rer.bandi is a product for announcements.

It is a folderish content (like `rer.structured_content`__) and it allows to set some infos about the announcement like the deadline to participate or the closing date.

__ http://pypi.python.org/pypi/rer.structured_content

Composition
===========

Different layouts
-----------------
There are two allowed views for an announcement:

* default view, with basic infos on the right (like events) and extra infos (folder deepenings) in the middle.
* alternative view that moves extra infos slot below basic infos.

Folder deepening
----------------
Like in **rer.structured_content**, it has a special folder type called "*Folder Deepening*" that allows to manage some extra infos or attachment that should be shown in the announcement's view.

Topic criterias
---------------
There are some new topic criterias that allows to set topic queries for announcements.

Announcements search
--------------------
There is a search form (http://yoursite/search_bandi_form) for quick searches.

Announcement state information
------------------------------
In the search results and in the two new topic views, there are also some infos about the announcement, like his state (open, closed or in progress).

Announcements portlet
---------------------
There is also a portlet that show announcement infos from a topic (this portlet extends base collection portlet)


Configurations
==============
An announcement has two fields for set the announcement type and recipients.

Recipients vocabulary
---------------------

This information is taken from a property in portal_properties:

    portal_properties.rer_bandi_settings.destinatari_bandi

If the property is empty, the item use a default list of values:

* Cittadini
* Imprese
* Enti locali
* Associazioni
* Altro


Types vocabulary
----------------

To handle this vocabulary, we need an enviroment variable called ``PLONE_RER_BANDI_VOCAB``.
We need to set it into buildout::

  [instance]
  ...
  environment-vars =
      PLONE_RER_BANDI_VOCAB ${buildout:directory}/var/rer_bandi_vocab.xml

This variable set the path for an xml file that contains a list of announcement types; if the file doesn't exist, it will be automatically generated with some default values::

  <?xml version='1.0' encoding='utf-8'?>
  <vocab-list>
    <vocabulary name="rer.bandi.tipologia.vocabulary">
      <term token="beni_servizi">Acquisizione beni e servizi</term>
      <term token="agevolazioni">Agevolazioni, finanziamenti, contributi</term>
      <term token="altro">Altro</term>
    </vocabulary>
  </vocab-list>

Authority Default value
-----------------------

A default authority value can be set for announcements. This information is taken from a property in portal_properties:

**portal_properties -> rer_bandi_settings -> default_ente**

If the property is empty, the default value isn't set.


Dependencies
============

This product has been tested on Plone 5 and Plone 5.1

Credits
=======

Developed with the support of `Regione Emilia Romagna`__;

Regione Emilia Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/
