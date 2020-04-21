# -*- coding: utf-8 -*-
"""
This module contains the tool of rer.bandi
"""
import os
from setuptools import setup, find_packages

version = '4.0.7'

setup(
    name='rer.bandi',
    version=version,
    description="A product for announcements management",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Addon",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python",
    ],
    keywords='rer bandi announcements',
    author='RedTurtle Technology',
    author_email='sviluppoplone@redturtle.it',
    url='https://github.com/PloneGov-IT/rer.bandi',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/rer.bandi',
        'Source': 'https://github.com/PloneGov-IT/rer.bandi',
        'Tracker': 'https://github.com/PloneGov-IT/rer.bandi/issues',
        # 'Documentation': 'https://rer.bandi.readthedocs.io/en/latest/',
    },
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['rer'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools', 'lxml', 'plone.restapi'],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
            'requests',
        ]
    },
    test_suite='rer.bandi.tests.test_docs.test_suite',
    entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
