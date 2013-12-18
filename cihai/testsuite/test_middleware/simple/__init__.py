# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_unihan
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""


class DatasetExample(object):

    def get(self, request, response):
        dataset = {
            '好': {
                'definition': 'ni hao'
            }
        }

        if request in dataset:
            response.update(dataset[request])

        return response

    def reverse(self, request, response):
        dataset = {
            '好': {
                'definition': 'ni hao'
            }
        }

        for char, key in dataset.items():
            for key, val in dataset[char].items():
                if request in val:
                    response.update(dataset[char])

        return response
