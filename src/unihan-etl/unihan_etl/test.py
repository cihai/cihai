"""Test helpers functions for downloading and processing Unihan data."""


def assert_dict_contains_subset(subset, dictionary, msg=None):
    """
    Ported assertion for dict subsets in py.test.

    Parameters
    ----------
    subset : dict
        needle
    dictionary : dict
        haystack
    msg : str, optional
        message display if assertion fails
    """
    for key, value in subset.items():
        assert key in dictionary, msg
        assert dictionary[key] == value, msg
