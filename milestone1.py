import os
import json
import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

def tokenizer(content):
    return re.findall(r"[A-Za-z0-9]+", content.lower())

def indexing(docid,content,inverted_index):

    soup = BeautifulSoup(content,"html.parser")
    texts = soup.findAll(text=True)
    ps = PorterStemmer()
    position = 0

    for text in texts:
        for i in tokenizer(text):
            token = ps.stem(i)
            if token not in inverted_index.keys():
                inverted_index[token] = {'freq': 1, docid: {'positions': [position]}}
            # if token was in invertedIndex, update it
            else:
                inverted_index[token]['freq'] += 1
                if docid not in inverted_index[token].keys():
                    inverted_index[token][docid] = {'positions': [position]}
                else:
                    inverted_index[token][docid]['positions'].append(position)
            position += 1



def geturl_dic(folder):
    docid_url = {}  #  key: url,value: unique id num of doc
    inverted_index = {}  # inverted_index = {key: token; value: {'freq': INT, docid: {rank: INT, positions:[INT]}})
    for (root, dirs, files) in os.walk(folder):
        for page_name in files:
            file_loc = os.path.join(root, page_name)
            print(file_loc)
            try:
                f = open(file_loc, 'r', encoding='utf-8')
                file_dic = json.loads(f.read())
                url = file_dic["url"]
                content = file_dic['content']
                f.close()
                if url not in docid_url.values():
                    docid = len(docid_url)
                    docid_url[url] = docid
                else:
                    docid = docid_url[url]
                indexing(docid,content,inverted_index)
            except ValueError as e:
                print(e)
    print(inverted_index)



if __name__ == '__main__':
    geturl_dic("/Users/mac/Desktop/Test")
