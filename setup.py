from setuptools import setup, find_packages
import os

version = '2.0.2'

setup(name='collective.portlet.collectionmultiview',
      version=version,
      description="A collection portlet product which supports multiple views",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone portlet inigo collection multi view',
      author='Izhar Firdaus',
      author_email='izhar@inigo-tech.com',
      url='http://www.inigo-tech.com/',
      license='GPLv2+',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'':'src'},
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.portlet.collection>=2.0',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
