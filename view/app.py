#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import codecs


labels = ["CRP", "血圧", "血糖"]


env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
#ATE部分
tmpATE = env.get_template('view/template/temp_ATE.html')
htmlATE = tmpATE.render(name1="testtttttt", name2="太郎")

f = codecs.open('view/o_ATE.html', 'w', 'utf-8')
f.write(htmlATE)
f.close()

#Find similar patient部分
tmpSIM = env.get_template('view/template/temp_SIM.html')
htmlSIM = tmpSIM.render(name1="testtttttt", name2="太郎")

f = codecs.open('view/o_SIM.html', 'w', 'utf-8')
f.write(htmlSIM)
f.close()

#cumulative chart部分
f = open("view/json/cumu.json", 'r')
texts = f.read()
f.close()
tmpCUM1 = env.get_template('view/template/temp_cumulativeLineChart.html')
htmlCUM1 = tmpCUM1.render(label="CRP", json=texts)

f = codecs.open('view/o_CUM1.html', 'w', 'utf-8')
f.write(htmlCUM1)
f.close()

#cumulative chart部分
f = open("view/json/cumu.json", 'r')
texts = f.read()
f.close()
tmpCUM2 = env.get_template('view/template/temp_cumulativeLineChart.html')
htmlCUM2 = tmpCUM2.render(label="CRP", json=texts)

f = codecs.open('view/o_CUM2.html', 'w', 'utf-8')
f.write(htmlCUM2)
f.close()

#sunburst部分
f = open("view/json/d_sunburst.json", 'r')
texts = f.read()
f.close()
tmpSUN = env.get_template('view/template/temp_sunburst.html')
htmlSUN = tmpSUN.render(label="CRP", json=texts.decode('utf-8'))

f = codecs.open('view/o_SUN.html', 'w', 'utf-8')
f.write(htmlSUN)
f.close()

#parallelCordinates
f = open("view/json/d_parallelCordinates.json", 'r')
texts = f.read()
f.close() 
tmpPAR = env.get_template('view/template/temp_parallelCoordinates.html')
htmlPAR = tmpPAR.render(label= ["Stage", "BP", "CRP", "HR", "Tempeture", "Weight", "Age"], json=texts)

f = codecs.open('view/o_PAR.html', 'w', 'utf-8')
f.write(htmlPAR)
f.close()
