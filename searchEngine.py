# -*- coding: utf-8 -*-

from functools import reduce
import math
from prettytable import PrettyTable
from nltk.corpus import stopwords
import sys
from downloadPages import downloadPages
import trie

useless_char = " .,!@#$%^&*();:\n\t\\\"?!{}[]<>"  # Strip these characters in the document

stop_words = set(stopwords.words('english'))


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

# search:
# desc: takes user input and performs search
def search():
    t = PrettyTable(['Match Score', 'Account'])
    query = input("Input query or input exit:  ")
    if query == "exit":
        sys.exit()

    query = query.lower().split()
    useful_query = [q.strip(useless_char) for q in query]
    useful_query = [i for i in useful_query if not i in (stop_words and '')]

    unique_query = set(useful_query)

    if not query :
        print("Warning: Your input cannot be empty, please input again!")

    elif not unique_query:
        print("Warning: Your input dese not conatin any useful information, please input again!")

    else:
        # store numerous dictionaries, each dictionary store a word's appear times in every page.
        frequency = {}
        for word in unique_query:
            frequency[word] = (trie.findPages(word))

        sets = [set(f.keys()) for f in frequency.values()]
        unique_page_id = reduce(set.union, [s for s in sets])
        if not unique_page_id:
            print ("No documents matched the given query")
        else:
            print (str(len(unique_page_id))+" documents matched the given query")
            scores = sorted([(id,similarity(unique_query,id, frequency))for id in unique_page_id], key=lambda x: x[1],reverse=True)
            for (id,score) in scores:
                t.add_row([round(score, 4), pages[id].strip('.txt').split('/pages/')[1]])
            print(t)
        
if __name__ == "__main__":
    pages = downloadPages('input.txt')
    trie = trie.Trie(pages)
    dictionary = trie.dictionary
    pageLength = trie.pageLength
    while True:
        search()

