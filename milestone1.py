import os
import json
import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from bs4.element import Comment



def tokenizer(content):
    return re.findall(r"[A-Za-z0-9]+", content.lower())

def indexing(docid,content,inverted_index):

    soup = BeautifulSoup(content,"html.parser")
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    text1 = " ".join(visible_texts)
    ps = PorterStemmer()
    position = 0


    for i in tokenizer(text1):
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

    #count th total number of files
    count1 = 0
    for (root, dirs, files) in os.walk(folder):
        count1 += len(files)

    stop_pos = count1 // 3
    print(count1,stop_pos)

    count2 = 0
    num_pindex = 1
    for (root, dirs, files) in os.walk(folder):
        for page_name in files:
            count2 += 1
            file_loc = os.path.join(root, page_name)
            try:

                f = open(file_loc, 'rb')
                file_dic = json.loads(f.read())
                url = file_dic["url"]
                content = file_dic['content']
                f.close()
                if url not in docid_url.values():
                    docid = len(docid_url)
                    docid_url[url] = docid
                else:
                    docid = docid_url[url]

                #store index into three
                if count2 > stop_pos and num_pindex != 3:
                    jsonfile(inverted_index,num_pindex)
                    num_pindex += 1
                    count2 = 0
                    inverted_index = {}
                indexing(docid,content,inverted_index)
            except ValueError as e:
                print(e)
    print(docid_url)
    jsonfile(inverted_index,num_pindex)

def jsonfile(invert_index, num_pindex):
    with open("partialIndex"+str(num_pindex)+".json", "w")as f:
        line = json.dumps(invert_index)
        f.write(line)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

if __name__ == '__main__':
    geturl_dic("/Users/mac/Desktop/Test")
