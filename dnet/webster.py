

import os
import re
import enchant

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import OrderedDict
import networkx as nx


class Webster(object):


    def __init__(self):

        """
        Open the dictionary file.
        """

        # Porter stemmer.
        self.stem = PorterStemmer().stem

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

        self.words = OrderedDict()
        estopwords = stopwords.words('english')
        dictionary = enchant.Dict()

        w_pattern = re.compile(r'''
            (\n(?P<word>[A-Z-]+))           # word
            (.*?)(?=Defn:|\d\.|\([a-z]\))   # variants/origin
            (?P<defn>.*?)                   # definition
            (?=\n[A-Z-]+[;\n]|$)            # next word
            ''', re.S+re.X)

        # Extract words.
        for m in re.finditer(w_pattern, self.raw):

            word = m.group('word').lower()
            defn = m.group('defn').lower()

            # Break if word isn't recognized.
            if not dictionary.check(word): continue

            tokens = []

            # Filter out stopwords / noise.
            for t in re.findall('[a-z]+', defn):
                if dictionary.check(t) and t not in estopwords:
                    tokens.append(self.stem(t))

            self.words[self.stem(word)] = tokens


    def network(self):

        """
        Generate a network from the term -> siblings dictionary.
        """

        graph = nx.Graph()

        for term, siblings in self.words.iteritems():
            for sibling in siblings:

                # Add edge if it doesn't exist.
                if not graph.has_edge(term, sibling):
                    graph.add_edge(term, sibling, weight=1)

                # Otherwise, increment the weight.
                else: graph[term][sibling]['weight'] += 1

        return graph
