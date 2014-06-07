"""This module holds logic responsible for turning JSON representations into usable UI descriptions, i.e.
Python objects representing modes and options.
"""

import json

from . import option
from . import mode
from . import shared
from . import errors


def readfile(path):
    """Reads file and returns string with contents of it.
    """
    ifstream = open(path)
    content = ifstream.read()
    ifstream.close()
    return content

def readjson(path):
    """Reads JSON file and returns decoded object.
    """
    return json.loads(readfile(path))


class Builder:
    """Object used to convert JSON representation of UI to
    appropriate CLAP objects.
    """
    def __init__(self):
        self._model = None
        self._mode = None

    def load(self, path):
        """Loads file from path.
        """
        self._model = readjson(path)
        return self

    def set(self, model):
        """Set model of the UI.
        """
        self._model = model
        return self

    def build(self):
        """Builds UI from loaded JSON.
        """
        return self

    def get(self):
        """Returns built mode.
        """
        return self._mode