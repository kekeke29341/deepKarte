###Generating_karte
This repository is for the purpose of research in medical records processing.
ALL Data is not real data. They are generated by random from random dictionary.  

###Elastic Search Use  
Generate medical records for evaluating patient similarity  
	python make_dataset/es_sample_generate_validation_data.py NumberPatient INDEX_Name  

###Flask $ Learning Usage  
1. python flask/generate_textbox_html.py Speech/karte/karte_ep7.json
2. python flask/add_escape.py 
3. python flask/app.py 

###Text summarization  
####Data Conversion (This part is important when you use Japanese data) 
1. python src/strip_n.py text_summarization/Raw_data/Formatted_Training_Data.tsv  
  (Sentences into each word)  
2. python text_summarization/generate_data.py --input_dir=text_summarization/train --data_path=text_summarization/binary_train/NE109  
3. python text_summarization/check_data.py --data_path=text_summarization/binary_train/NE109 --crc=4  
(Raw data -> train -> Binary_train)
(If you want to convert google drive word file, first you convert it to Excel and A&B to TSV and then start from 1.)  
####Generate Vocab dictionary  
python src/mecab_word_count.py text_summarization/data/national_exam109.txt  

###Learning Start  
1. python text_summarization/convert_data.py Speech/data/ep6/scripts.txt flask/learn/32.txt  
2. python text_summarization/generate_data.py --input_dir=text_summarization/train --data_path=text_summarization/binary_train/output  
(Second argument is directory)  


###Recording and Learning(+ Searching Realtime using Google Chrome)  
sh shellscript/record.sh  
python shellscript/main.py  
python flask/app.py  

###Recording and export Ruby on Rails(extraction method is completely diffrenet so src is in RB dir):  
sh shellscript/record_voice_model2.sh  
cd rails directory  
rails s  
rails runner app/batch/load_text.rb  

##PS  
Generate medical records for evaluating patient similarity
(under construction)  

##For View  
ex)  
1. python view/bulk_data_for_parallelcordinates.py output/d_lab.json view/space_parallelCoordinates.html view/done_parallelCoordinates.html   
2. python view/bulk_data_for_chart.py view/tchart.json view/space_cumulativeLineChart.html view/done_cumulativeLineChart.html  


#Simple Patient History View  
1st step:  
	These codes generate different dataset.
	Generate Patinets -> python src/json_time_series_generate_patients.py n  
	n - number of patinets  

2nd step:  
	Generate Graphs -> python src/dump_to_graph.py  


