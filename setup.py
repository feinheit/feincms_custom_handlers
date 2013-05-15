#!/usr/bin/env python

from distutils.core import setup

setup(
    name='feincms_custom_handlers',
    version='0.3',
    packages=['feincms_handlers', 'feincms_handlers.views',
              'feincms_handlers.views.cbv'],
    url='https://github.com/feinheit/feincms_custom_handlers',
    license='BSD License',
    author='Simon Baechler',
    author_email='sb@feinheit.ch',
    description='This module allows to include custom feincms handlers. Major use cases are ajax-responses that only return a small part of the page or mobile versions of the site.'
)
