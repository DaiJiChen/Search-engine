from nltk.corpus import stopwords
import codecs
from collections import defaultdict
import math



class TrieNode(object):
    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.word_finished = False
        self.counter = 1
        self.pageIDs = {}

class Trie:

    def __init__(self, pages):
        self.pages = pages
        self.useless_char = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"  # Strip these characters in the document
        self.stop_words = set(stopwords.words('english'))

        self.postings = defaultdict(dict)
        self.pageLength = defaultdict(float) # value is Euclidean length of each page.

        self.dictionary = set()
        self.root = TrieNode('*')

        for id in pages:
            words = self.getWords(id)
            unique_words = set(words)
            self.dictionary = self.dictionary.union(unique_words)

            for word in unique_words:
                self.postings[word][id] = words.count(word)  # the value is the frequency of the term in the document

        # create a trie by inserting words one by one
        for word in self.dictionary:
            self.add(self.root, word)

        for child in self.root.children:
            if (child.char == 't'):
                for tchild in child.children:
                    if tchild.char == 'r':
                        for rchild in tchild.children:
                            print(rchild.char)

        # traverse the whole trie and remove redundant nodes.
        self.compress(self.root)

        for child in self.root.children:
            if (child.char == 't'):
                for tchild in child.children:
                    if tchild.char == 'r':
                        for rchild in tchild.children:
                            print(rchild.char)

        self.findDocLength(pages)

    # an recursive method that removing redundant nodes.
    def compress(self, node):
        node = node
        # This is a external node
        if len(node.children) == 0 and node.word_finished == True:
            return
        # this is a redundant node
        elif len(node.children) == 1:
            child = node.children[0]

            node.char = node.char + child.char
            node.children = child.children
            node.word_finished = child.word_finished
            node.pageIDs = child.pageIDs

            self.compress(node)

        # this node has more than one child
        elif len(node.children) > 1:
            for child in node.children:
                self.compress(child)

        # An error occur
        else:
            print("Error: found a external node that has no child")

    def add(self,root, word):
        node = root
        for char in word:
            found_in_child = False

            for child in node.children:
                if child.char == char:
                    child.counter += 1
                    node = child
                    found_in_child = True
                    break

            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                node = new_node

        # Everything finished. Mark it as the end of a word.
        node.word_finished = True
        node.pageIDs = self.postings[word]

    def findPages(self, word):
        node = self.root

        if not self.root.children:
            return {}

        for char in word:
            char_not_found = True
            for child in node.children:
                if child.char == char:
                    char_not_found = False
                    node = child
                    break
            if char_not_found:
                return {}

        return node.pageIDs



    # calculete Euclidean length of each document.
    def findDocLength(self, pages):
        for id in pages:
            l = 0
            for word in self.dictionary:
                if self.findPages(word) != {} and id in self.findPages(word):
                    inverseFrequency =  math.log(len(pages) / len(self.findPages(word)), 2)
                    importance = self.findPages(word)[id] * inverseFrequency
                    l += importance ** 2
            self.pageLength[id] = math.sqrt(l)


    def getWords(self, id):
        f = codecs.open(self.pages[id], encoding='utf-8')
        text = f.read()
        f.close()

        words = text.lower().split()
        words = [word.strip(self.useless_char) for word in words]
        words = [i for i in words if not i in self.stop_words]

        return words
