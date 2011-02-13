from setuptools import setup, find_packages


setup(
    name = 'jarn.jenkins',
    version = '1.0b1',
    author = "Hanno Schlichting",
    author_email = "hanno@jarn.com",
    description = "Buildout recipe for installing a Jenkins instance",
    long_description=(open('README.txt').read() + '\n' +
                      open('CHANGES.txt').read()),
    license = "BSD",
    keywords = "jenkins buildout",
    url='http://pypi.python.org/pypi/jarn.jenkins',
    classifiers=[
      "License :: OSI Approved :: BSD License",
      "Framework :: Buildout",
      "Framework :: Buildout :: Recipe",
      ],
    tests_require=['zope.testing'],
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'': 'src'},
    namespace_packages = ['jarn'],
    install_requires = [
        'iw.recipe.template',
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
    ],
    zip_safe=False,
    entry_points = {'zc.buildout': ['default = jarn.jenkins:Recipe']},
    )
