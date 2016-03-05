# coding=utf-8

from distutils.version import LooseVersion


class VersionHelper(object):

    @staticmethod
    def version_compare(v1, v2, op=None):
        """

        :param v1: Version to compare
        :param v2: Recommended version
        :param op: Compare operation
        :return:
        """
        _map = {
            '<': [-1],
            'lt': [-1],
            '<=': [-1, 0],
            'le': [-1, 0],
            '>': [1],
            'gt': [1],
            '>=': [1, 0],
            'ge': [1, 0],
            '==': [0],
            'eq': [0],
            '!=': [-1, 1],
            'ne': [-1, 1],
            '<>': [-1, 1]
        }
        v1 = LooseVersion(v1)
        v2 = LooseVersion(v2)
        result = cmp(v1, v2)
        if op:
            assert op in _map.keys()
            return result in _map[op]
        return result