#!/usr/bin/python3

class Node:
    def __init__(self, sm=None, ibif=None, ethif=None, available=None):
        """ Represents a node"""
        self.sm=sm
        self.ibif=ibif
        self.ethif=ethif
        self._available=available

    def isUp(self):
        pass

    def isDown(self):
        pass

    def isAvailable(self):
        return self._available

    def setAvailable(self, bool):
        if bool is True:
            self._available=True

        elif bool is False:
            self._available=False

        else:
            raise TypeError


