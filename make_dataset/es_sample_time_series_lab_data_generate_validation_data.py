# coding: utf-8
import sys
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
import string
import random
import shelve
import numpy as np
import scipy.sparse as sparse
import cPickle as pickle
from collections import defaultdict, namedtuple
import codecs, json
import make_Object 

def randomString(length=16):
	return "".join([random.choice(string.letters) for _ in xrange(length)])

def token((disp, repr)):
	return {'disp':disp, 'repr':repr}

def randomText(length, words):
	return " ".join([random.choice(words) for _ in xrange(length)])

def remove_prefix(w):
	if '_' in w:
		return w.split('_', 1)[1]
	else:
		return w

def word_shuffle(words_list):
	random.shuffle(words_list)
	#words_list = words_list[:500]
	words_list = words_list[:500]
	#vocab_list = set(words_list)
        return words_list

def read_file(filename):
	f = codecs.open(filename,"r","utf-8")
	text = f.read()
	f.close()
	return text

def devide_dictionary(words, div_n):
	words = word_shuffle(words)
    	l = len(words)
    	size = l / div_n + (l % div_n > 0)
    	return [words[i:i+size] for i in range(0, l, size)]


random.seed(2014)

AP_words = read_file('sample_karte/qb_karte.txt')
A_words = read_file('sample_karte/problem_list.txt')
P_words = read_file('sample_karte/Action_list.txt')

History_words = read_file('sample_karte/History.txt')
O_words = read_file('sample_karte/O.txt')
S_words = read_file('sample_karte/S.txt')


AP_words = AP_words.split("\n")
A_words = A_words.split("\n")
P_words = P_words.split("\n")

del P_words[-1]
del A_words[-1]


History_words = History_words.split("\n")
#History_words[-1] = History_words[-1].strip("\n")

O_words = O_words.split("\n")
S_words = S_words.split("\n")



def randomPatient(p_id, f, i_name):
	Time_points = 3
	global vocab
	p_dict = {}
	#pat['index'] = randomString()
        tmp = ''
	pat_id = randomString()
	age_tmp = str(np.random.choice(range(20,80)))
	sex_tmp = np.random.choice(['M', 'F'])[0]
	change_id = random.randint(0, Time_points-1)
        #時系列ごとに疾患が増えて行 -> MD commentの所に加えて行く

	#Time seris 患者の情報
	label_1 = { "index": { "_index": "test2", "_type": "Patient", "_id": "%s"%p_id } }
	
	f.write("{ \"index\": { \"_index\": \"%s\", \"_type\": \"Patient\", \"_id\": \"%s\" } }"%(i_name, p_id))
	f.write("\n")
        f.write("{ \"id\":\"%s\", \"Age\":\"%s\", \"Sex\":\"%s\", \"Department\":\"Not Yet\" }"%(p_id, age_tmp, sex_tmp))	
	f.write("\n")

	Subject = ""
	Object = ""
	Assesment = ""
	Plan = ""

	BP = random.randint(80,150)
	WBC = random.randint(3500,9000)
	CRP = random.randint(1,10)
	HR = random.randint(50,90)
	BS = random.randint(70,130)

        for t in xrange(Time_points):
		random_int = random.randint(3,5)
        	Subject += randomText(3, S_words)
        	Object += randomText(random_int , O_words)
        	noise = randomText(random_int + 2 , AP_words)
		Assesment += "#%s " % randomText(1 , A_words)
		Plan += randomText(2 , P_words)

		BP += random.randint(-20,20)
        	WBC += random.randint(-1000,1000)
        	CRP += random.randint(-1, -1)
        	HR += random.randint(-10,10)
        	BS += random.randint(-10,10)

		if int(t) == int(change_id):
			tmp_Triage = randomText(random_int + 10, History_words)
		else:
			tmp_Triage = randomText(random_int, History_words)
                tmp += tmp_Triage
                t_dict = {}
		#順序をここで変えて順番の大切さを見るため
                word_list = noise + Plan
                word_list = word_list.split(" ")
		#Shuffle words to predict order
		random.shuffle(word_list)
                word_list = " ".join(word_list)
		t_dict = {
				"patient_id": pat_id,
				"Subject" : Subject,
				"Object" : Object,
				"History" : tmp_Triage,
				"A/P" : Assesment + word_list,
				"Age" : age_tmp,
				"Sex" : sex_tmp,
				"Time" : t,
				"change_point" : change_id,
				"BP" : BP,
				"WBC" : WBC,
				"CRP" : CRP,
				"HR" : HR,
				"BS" : BS
			}
		p_dict[t] = t_dict

		f.write("{ \"index\": { \"_index\": \"%s\", \"_type\":  \"karte\", \"_parent\": \"%s\" } }"%(i_name, p_id))
		f.write("\n")
		f.write("{ \"id\": \"%s\", \"time\": \"%s\", \"Subject\": \"%s\", \"Object\": \"%s\", \"History\": \"%s\", \"A/P\": \"%s\", \"BP\": \"%s\",\"WBC\": \"%s\",\"CRP\": \"%s\",\"HR\": \"%s\", \"BS\": \"%s\" }"%(p_id, t, Subject, Object, tmp_Triage,  Assesment + word_list, BP, WBC, CRP, HR, BS))
		#f.write("{ \"id\": \"%s\", \"Subject\": \"%s\", \"Object\": \"%s\", \"History\": \"%s\", \"A/P\": \"%s\" }"%(p_id, Subject, Object, tmp_Triage,  word_list))
		f.write("\n")

	label = {
			"patient_id": pat_id,
                        "change_point" : change_id
		}
        return p_dict, label, label_1

def generate_patients(n):
    for _ in xrange(n):
        pat = randomPatient()

    jsonstring = json.dumps(pat, ensure_ascii=False)
    return jsonstring

if __name__ == "__main__":

    try:
        n = int(sys.argv[1])
    except:
        print "usage: python generate_patients.py numPatients"
        sys.exit()

    pat_dics = {}
    p_labels = {}
    f = codecs.open("elastic_search/multi_lab_es_sample_karte.txt","w","utf-8")

    index_name = sys.argv[2]
    for t in xrange(n):
       pat_dics[t], p_labels[t], lab = randomPatient(t,f, index_name)

    f.close()

    f.close()
    jsonstring = json.dumps(pat_dics, ensure_ascii=False)
    label_jsonstring = json.dumps(p_labels, ensure_ascii=False)

    fa = codecs.open("output/json_multi_lab_time_series_patient.json","w","utf-8")
    f_label = codecs.open("output/p_labels.json","w","utf-8")
    json.dump(pat_dics, fa, ensure_ascii=False)
    json.dump(p_labels, f_label, ensure_ascii=False)


