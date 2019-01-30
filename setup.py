from setuptools import setup, find_packages
from janus import __version__


setup(
    name="janus-allauth-provider",
    version='.'.join(str(x) for x in __version__),
    license="BSD",
    description="Janus provider is a allauth provider for authentication with the django janus SSO.",
    author="Daniel Leinfelder",
    author_email="daniel@smart-lgt.com",
    url="http://github.com/smartlgt/janus-allauth-provider",
    zip_safe=False,
    packages=find_packages(),
    package_data={
        "janus": ["janus/templates/*.html", ]},
    install_requires=[
        'django>=1.11',
        'django-allauth',
        'requests'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Framework :: Django",
    ]
)