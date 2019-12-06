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
        self.postings = defaultdict(dict)
        self.pageLength = defaultdict(float) # value is Euclidean length of each page.
        self.dictionary = set()
        self.root = TrieNode('*')

        self.createDictionary(pages)

        for word in self.dictionary: # create a normal trie by adding words one by one
            self.add(self.root, word)

        self.compress(self.root) # remove redundant node to became a compress trie

        self.findDocLength(pages)


    # traversal all the documents and add every unique word to a set
    def createDictionary(self, pages):
        useless_char = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"  # Strip these characters in the document
        useless_words = set(stopwords.words('english'))

        for id in pages:
            f = codecs.open(pages[id], encoding='utf-8')
            text = f.read()
            f.close()

            words = text.lower().split()
            words = [word.strip(useless_char) for word in words]
            words = [i for i in words if not i in useless_words]
            unique_words = set(words)

            self.dictionary = self.dictionary.union(unique_words)

            for word in unique_words:
                self.postings[word][id] = words.count(word)  # the value is the frequency of the term in the document


    # removing redundant nodes recursively
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


    # add a word to the trie
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


    # find all web pages that contain a word
    def findPages(self, word):
        node = self.root

        if not self.root.children:
            return {}

        word = list(word)
        while(len(word)!=0):
            char_not_found = True
            for child in node.children:
                childChars = list(child.char)
                if self.isPrefix(childChars, word):
                    char_not_found = False
                    node = child
                    word = word[len(child.char):]
                    break
            if char_not_found:
                return{}
        return node.pageIDs
        #for char in chars:
        #    char_not_found = True
        #    for child in node.children:
        #        if child.char == char:
        #            char_not_found = False
        #            node = child
        #            break
        #    if char_not_found:
        #        return {}
        #return node.pageIDs


    # validate prifix of a word
    def isPrefix(self, prefix, word):
        is_prefix = True
        for c1, c2 in zip(prefix, word):
            if c1 != c2:
                is_prefix = False
        return is_prefix


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


