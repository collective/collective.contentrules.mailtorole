from setuptools import setup, find_packages

setup(name='collective.contentrules.mailtorole',
      version='2.0.dev0',
      description="Plone rule: send email to users having a role on the object",
      long_description=(open("README.txt").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 6.0",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='plone contentrules action mail',
      author='Zest Software (Fred van Dijk)',
      author_email='info@zestsoftware.nl',
      url='https://github.com/collective/collective.contentrules.mailtorole',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.contentrules'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.app.contentrules',
          'plone.api'
      ],
      extras_require={
          'test': [
            'plone.api',
            'plone.app.testing',
            'plone.app.contenttypes',
            'Products.SecureMailHost',
            'Products.PloneTestCase == 0.9.18'
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
