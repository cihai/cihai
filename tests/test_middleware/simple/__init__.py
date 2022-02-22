class DatasetExample(object):

    """Sample dataset to demonstrate a simple extension with Cihai.

    This object is passed into :meth:`cihai.Cihai.use` in the
    :class:`cihai.Cihai` object.

    """

    def get(self, request, response):
        """Return chinese character data from sample dataset.

        The source of information in this example is a :obj:`dict`. In real
        modules, the dataset may be a CSV, sqlite database, or an API. As long
        as the data appends to the :param:`response` and returns it.

        :param request: The character or string being looked up, e.g. '好'.
        :type request: str
        :returns: Cihai response dictionary
        :rtype: dict

        """
        dataset = {"好": {"definition": "hao"}}

        if request in dataset:
            response.update(dataset[request])

        return response

    def reverse(self, request, response):
        """Return chinese character data from a reverse lookup sample dataset.

        :param request: The character or string being looked up, e.g. '好'.
        :type request: str
        :returns: Cihai reverse look up. The results should be formatted as::

            {
                '好': {
                    'definition': 'good.'
                }
            }

        When the character already exists in :param:`response`, the character
        ``好`` must be mixed-in with, not overwritten.

        :rtype: dict

        """
        dataset = {"好": {"definition": "hao"}}

        for char, key in dataset.items():
            for key, val in dataset[char].items():
                if request in val:
                    response.update({char: dataset[char]})

        return response
