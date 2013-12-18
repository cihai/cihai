# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_middleware.simple
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals


class DatasetExample(object):

    def get(self, request, response):
        dataset = {
            '好': {
                'definition': 'hao'
            }
        }

        if request in dataset:
            response.update(dataset[request])

        return response

    def reverse(self, request, response):
        dataset = {
            '好': {
                'definition': 'hao'
            }
        }

        for char, key in dataset.items():
            for key, val in dataset[char].items():
                if request in val:
                    response.update({
                        char: dataset[char]
                    })

        return response
