# -*- coding: utf-8 -*-

from functools import reduce
import math
from prettytable import PrettyTable
from nltk.corpus import stopwords
import sys
from downloadPages import downloadPages
import trie

useless_char = " .,!@#$%^&*();:\n\t\\\"?!{}[]<>"  # Strip these characters in the document
useless_words = set(stopwords.words('english'))


# take an input query and search for all web pages that contain this query ( lsit them by relativity)
def search():
    t = PrettyTable(['Match Score', 'Web page'])

    query = input("Input query or input exit:  ")
    if query == "exit":
        sys.exit()

    query = query.lower().split()
    if not query:
        print("Warning: Your input cannot be empty, please input again!\n")
        return

    query = [q.strip(useless_char) for q in query]
    query = [i for i in query if i not in useless_words]
    unique_query = set([i for i in query if len(i) != 0])
    if not unique_query: # no useful information in query
        print("Warning: Your input dese not conatin any useful information, please input again!\n")
        return

    else:
        # store numerous dictionaries, each dictionary store a word's appear times in every page.
        frequency = {}
        for word in unique_query:
            frequency[word] = (trie.findPages(word))

        sets = [set(f.keys()) for f in frequency.values()]
        unique_page_id = reduce(set.union, [s for s in sets])
        if not unique_page_id:
            print ("Sorry! No matching documents\n")
        else:
            print (str(len(unique_page_id))+" documents matched")
            scores = sorted([(id,similarity(unique_query,id, frequency))for id in unique_page_id], key=lambda x: x[1],reverse=True)
            for (id,score) in scores:
                t.add_row([round(score, 4), pages[id].strip('.txt').split('/pages/')[1]])
            print(t)
            print()


def similarity(query,id,frequency):
    similarity = 0.0
    for word in query:
        if word in dictionary and id in trie.findPages(word):
                inverseFrequency = math.log(len(pages) / len(frequency[word]), 2)
                importance = frequency[word][id]*inverseFrequency
                similarity += importance**2
    if pageLength[id] != 0:
        similarity = similarity / pageLength[id]
    return similarity

        
if __name__ == "__main__":
    pages = downloadPages('input.txt')
    trie = trie.Trie(pages)
    dictionary = trie.dictionary
    pageLength = trie.pageLength
    while True:
        search()

