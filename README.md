# Generating_karte
This repository is for the purpose of research in medical records processing.
ALL Data is not real data. They are generated by random from random dictionary.  

##Elastic Search Use  
Generate medical records for evaluating patient similarity  
	python make_dataset/es_sample_generate_validation_data.py NumberPatient INDEX_Name  

##Task1  
Generate medical records for evaluating patient similarity

#Patient History View  
1st step:  
	Generate Patinets -> python src/json_time_series_generate_patients.py n  
	n - number of patinets  

2nd step:  
	Generate Graphs -> python src/dump_to_graph.py  

#Generate Dataset for validating patient similarity  
##1st step:  
	**Generating validation dataset(ここでの辞書の割合が類似患者の精度に大きく変わる)**  
	python make_dataset/generate_validation_data.py n  
	n - number of patients  

##2nd step:  
	**Vectorize the dataset**  
	python patient_similarity/make_dictionary.py  
	-> output is dic_out  
 
##3rd step:  
	**Validating dataset**  
	python patient_similarity/main.py  
	-> validating dictionary ids and changing points  

##4st step:   
	**Visualizing Similarity Patients**  
	python patient_similarity/find_high_frequency.py  
	-> tree.html is showing the high frequency words between similar patients  



