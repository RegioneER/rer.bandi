# -*- coding: utf-8 -*-
"""
This module contains the tool of rer.bandi
"""
import os
from setuptools import setup, find_packages

version = '1.0.6'

tests_require = ['zope.testing']

setup(name='rer.bandi',
      version=version,
      description="A product for bandi",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='https://rersvn.ente.regione.emr.it/svn/plone/prodotti/rer.bandi/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rer', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
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
