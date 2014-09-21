

import os
import re


class Webster(object):


    def __init__(self):

        """
        Open the dictionary file.
        """

        # Get the dictionary file path.
        dirname = os.path.dirname(os.path.realpath(__file__))
        webster = os.path.join(dirname, 'webster.txt')

        # Read in the raw text content.
        self.raw = open(webster, 'r').read()
        self.index()


    def index(self):

        """
        Build out a word -> definition(s) dictionary.
        """

        words = re.compile(r'''
            (\n(?P<word>[A-Z-]+))   # Word.
            (; [A-Z]+)*?\n          # Alternate spellings.
            (?P<defn>.*?)           # Definition.
            (?=\n[A-Z-]+[;\n]|$)    # Next word.
            ''', re.S+re.X)

        for match in re.finditer(words, self.raw):
            print match.group('word')
            print match.group('defn')
