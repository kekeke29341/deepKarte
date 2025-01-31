# -*- coding: utf-8 -*-
import json, MeCab, sys, os, random
import re


def split_conversation(conversatioin):
    seped = re.split('すか|です|たか|した', conversation)
    return seped


def find_in_dic(dic, word):
    for d in dic:
	#部分一致
        if d.find(word.encode("utf-8")) != -1:
	#完全一致
        #if d == word :
	    return 0

    return 1   

def con(word):
    #No
    if word == u"ん":
        return 0
    

def note(conversation):
    m = MeCab.Tagger ("-Owakati")
    #encode_text = conversation.encode('utf-8')
    res = m.parseToNode(conversation)

    f = open("RB/data/symptom.txt")
    dic = f.readlines()
    f.close()

    box = []
    im_box = []
    while res:
    	tmp = res.feature.decode('utf-8').split(",")
        print tmp[0], tmp[6]
        box.append(tmp[6])
        if tmp[0] == u'名詞':
	    if find_in_dic(dic, tmp[6]) == 0:
	        #box.append(tmp[6])
	        im_box.append(tmp[6])
        if tmp[0] == u'動詞' or tmp[0] == u'形容詞':
            im_box.append(tmp[6])
        if tmp[6].find(u"ない") != -1 or tmp[6].find(u"ん") != -1:
	    im_box.append(tmp[6])
        res = res.next


    print conversation
    print "------"
    for i in xrange(len(im_box)):
        print im_box[i]

    print "------"
    dic_yes = []
    dic_no = []
    #文章単位で流すかどうかが問題
    for i in xrange(len(box)):
        print box[i]
	#名刺以外はスキップ
	if not box[i] in im_box:
	    continue
	for j in xrange(len(box)-i):
	    #どこまで先を見に行くか
            if j > 3:
                break
            if con(box[j+i]) == 0:
                dic_no.append(box[i])
	    else:
		dic_yes.append(box[i])
	   

    dic_no = list(set(dic_no))
    dic_yes = list(set(dic_yes))

    print 'Negative Symptom'

    for d in dic_no:
	print d
	dic_yes.remove(d)

    print 'Positive Symptom'
    for d in dic_yes:
	print d


if __name__ == '__main__':
    f = open("Speech/data/ep_text/scripts.txt")
    conversation = f.read()
    f.close()

    se_conv =  split_conversation(conversation)
    note(conversation)
