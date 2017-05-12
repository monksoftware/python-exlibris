try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PACKAGE_NAME = 'exlibris'

setup(
    name='python-exlibris',
    version='0.1.0',
    description='Python client for the bookrepublic exlibris API',
    url='https://github.com/monksoftware/python-exlibris',
    author='Leonardo Donelli',
    author_email='learts92@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='exlibris client api ebook',
    packages=[PACKAGE_NAME],
    install_requires=['requests'],
)
