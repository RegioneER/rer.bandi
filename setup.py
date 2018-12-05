# -*- coding: utf-8 -*-
"""
This module contains the tool of rer.bandi
"""
import os
from setuptools import setup, find_packages

version = '3.0.12'

tests_require = ['zope.testing', 'Products.PloneTestCase']

setup(name='rer.bandi',
      version=version,
      description="A product for announcements management",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        ],
      keywords='rer bandi announcements',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/products/rer.bandi',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rer', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'lxml',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='rer.bandi.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
