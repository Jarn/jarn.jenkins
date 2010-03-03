from setuptools import setup, find_packages

name = "collective.recipe.hudson"
version = '1.0a1'

setup(
    name = name,
    version = version,
    author = "Hanno Schlichting",
    author_email = "hannosch@plone.org",
    description = "Buildout recipe for installing a Hudson instance",
    long_description=(open('README.txt').read() + '\n' +
                      open('CHANGES.txt').read()),
    license = "ZPL 2.1",
    keywords = "hudson buildout",
    url='http://pypi.python.org/pypi/collective.recipe.hudson',
    classifiers=[
      "License :: OSI Approved :: Zope Public License",
      "Framework :: Buildout",
      ],
    tests_require=['zope.testing'],
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['collective', 'collective.recipe'],
    install_requires = [
        'iw.recipe.template',
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
    ],
    zip_safe=False,
    entry_points = {'zc.buildout': ['default = %s:Recipe' % name]},
    )
