from setuptools import setup, find_packages
from gcm import VERSION

setup(
    name='django-gcm',
    version=VERSION,
    description='Google Cloud Messaging Server',
    long_description=open('README.rst').read(),
    author='Adam Bogdal',
    author_email='adam@bogdal.pl',
    url='https://github.com/bogdal/django-gcm',
    download_url='https://github.com/bogdal/django-gcm/zipball/master',
    packages=find_packages(),
    package_data={
        'gcm': ['locale/*/LC_MESSAGES/*']
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'],
    zip_safe=False,
    install_requires=[
        'django>=1.5',
        'django-tastypie>=0.9.13',
        'python-mimeparse>=0.1.4',
        'pytz==2013.8',
        'requests>=1.2.0',
    ],
)
