import json
import milestone1
import queryprocess
from collections import defaultdict
def inputquery():
    #return divided query list
    q=input("Input query:")
    query= queryprocess.query(q)
    query.processquery()
    return query.getdividedquery()
def search(dividedquery):
    firstdict = json.loads('partialIndex1.json')
    seconddict = json.loads('partialIndex2.json')
    thirddict = json.loads('partialIndex3.json')
    querydict = dict()
    mergeddict = defaultdict(list)
    for i in dividedquery:
        querydict[i]=firstdict.get(i,None)
        querydict[i]=seconddict.get(i,None)
        querydict[i]=thirddict.get(i,None)

    for wordkey,wordval in querydict:
        for key,val in wordval.items():
            mergeddict[key].append(val)
    for k,v in mergeddict:
        if len(v)!=len(querydict):
            mergeddict.pop(k)
    print(mergeddict)
if __name__ == '__main__':
    search(inputquery())

