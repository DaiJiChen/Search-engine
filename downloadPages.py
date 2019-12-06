import time
import requests
from bs4 import BeautifulSoup
import os


def downloadPages(input):
    pages = {}

    f = open(input, "r")

    for url in f:
        print("Getting contents from " +url.strip().strip('https://'))
        getDocument(url.strip())

    pagesList = [f for f in os.listdir('./pages') if f.endswith('.txt')]
    for i in range(len(pagesList)):
        pages[i]= './pages/' +pagesList[i]
    print()
    return pages



def getDocument(url):
    for i in range(3): # try to get content for 3 times
        try:
            page =requests.get(url)
            htmlCode = page.content
            break

        except Exception as e:
            print('failed attempt', i)
            time.sleep(2) # wait 2 secs

    if not htmlCode :return # couldnt get the page, ignore

    text = BeautifulSoup(htmlCode.decode('ascii', 'ignore') ,'lxml')
    sections = text.find_all('section') # get all the question divs

    paragraphs = []
    for section in sections:
        for p in section.find_all('p', class_="zn-body__paragraph speakable"):
            paragraphs.append(p.text)
        for p in section.find_all('div', class_="zn-body__paragraph"):
            paragraphs.append(p.text)

    f = open("./pages/"+url.split("politics/")[1].split("/index.html")[0]+'.txt', 'w', encoding='utf-8')
    for paragraph in paragraphs:
        f.write(paragraph.replace('\n', ' ')+"\n")
    f.close()