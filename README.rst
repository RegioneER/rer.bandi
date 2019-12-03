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


Tile
====

In order to use layout bandi for tile is necessary have installed collective.tiles.collection product.


Development
===========

New `@@search_bandi_form` view is a React view that searches through the catalog with a plone.restapi endpoint.

To develop the new view, you need to install its dependencies with yarn::

    > yarn

or npm::

    > npm install

And then run development server::

    > yarn start


To see your changes, you need to enable resources registry in `development mode`.

Before releasing a new package, you need to build the production app::

    > yarn build

and then commit.

Release
=======

Simpy call::

    > make deploy

And a production build will be created and committed before a fullrelease.


Compatibility
=============

This product has been tested on Plone 5.1 and 5.2

For Plone 4 (and Archetypes), use 2.x branch/versions

From 4.0.0 version, there is a breaking change in bando fields. If you need to use old implementation, use 3.x branch.


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
