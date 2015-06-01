# ~*~ coding: utf-8 ~*~
from setuptools import setup, find_packages
from gcm import VERSION

setup(
    name='django-gcm',
    version=VERSION,
    description='Google Cloud Messaging Server',
    long_description=open('README.rst').read(),
    author='Adam Bogdał',
    author_email='adam@bogdal.pl',
    url='https://github.com/bogdal/django-gcm',
    packages=find_packages(),
    package_data={
        'gcm': ['locale/*/LC_MESSAGES/*']
    },
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    zip_safe=False,
    install_requires=[
        'django>=1.6',
        'django-tastypie>=0.12.2-dev',
        'pytz>=2013.8',
        'requests>=1.2.0',
    ],
    dependency_links=[
        'https://github.com/django-tastypie/django-tastypie/tarball/master#egg=django-tastypie-0.12.2-dev',
    ],
    extras_require={
        'dev': [
            'mock>=1.0.1',
            'coverage'
        ]
    }
)
