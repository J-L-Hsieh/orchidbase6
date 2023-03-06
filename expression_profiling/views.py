from django.shortcuts import render
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
import os,datetime
import pandas as pd
import numpy as np
import time
import sys
from django.http import HttpResponse,JsonResponse
import collections
import pymysql
import json,random,string
#import matplotlib.pyplot as plt
import seaborn as sns; sns.set(color_codes=True)
from sklearn.decomposition import PCA

def BLAST_SCA(request):
	return render(request, 'enhance_sequence_SCA.html', locals())

@csrf_exempt
def Run_BLAST_SCA(request):
	seq = request.POST.get('data')
	Type = request.POST.get('Type')
	#print(Type)
	temp_parameters = request.POST.get('Parameters')
	parameters = json.loads(temp_parameters)
	#print(parameters)#{'outfmt': '0', 'database': 'Phalaenopsis_cds', 'gapextend': '2', 'blast_type': 'blastn', 'evalue': '10.0', 'num_alignments': '250', 'reward': '2', 'penalty': '-3', 'gapopen': '5', 'dust': 'yes'}
	with open ("/home/t50504/Django/t50504_project/data/temp_fasta.fasta","w") as fastafile:
		fastafile.write(seq)
	#BLASTn  "num_alignments". Incompatible with argument:  `max_target_seqs'
	string = "-task blastn -evalue " + parameters["evalue"] +" -outfmt " + parameters["outfmt"] + " -num_alignments " + parameters["num_alignments"] + " -penalty " + parameters["penalty"] + " -reward " + parameters["reward"] + " -gapopen " + parameters["gapopen"] + " -gapextend " + parameters["gapextend"] + " -dust " + parameters["dust"]
	path = "/home/t50504/blast/ncbi-blast-2.11.0+/bin/"+ parameters["blast_type"] +" -db /home/t50504/blastdb/"+ Type +"/"+ parameters["database"] +" -query /home/t50504/Django/t50504_project/data/temp_fasta.fasta -out /home/t50504/Django/t50504_project/data/result.out "+ string	
	print(path)
	os.system(path)
	print('finish')

	temp_list=[]
	detail_list = []
	table_list = {}
	id_list = []
	Score_list = []
	Evalue_list = []
	Identities_list = []
	Gaps_list = []

	file = "/home/t50504/Django/t50504_project/data/result.out"
	with open (file,'r') as result:
		lines = result.readlines()
	result.close()
	print(len(lines))
	for i in range(len(lines)):
		# if lines[i][0:3] == "Peq" or lines[i][0:3] == "Dca" or lines[i][0:3] == "Ash" or lines[i][0:3] == "Vpo" or lines[i][0:3] == "Vsh" or lines[i][0:3] == "Pgu" or lines[i][0:3] == "Pzi" or lines[i][0:3] == "evm":
		# 	id_list = id_list + [lines[i][0:9]]
			#lines[i] =  "<a href=\"" + "http://140.116.214.130/t50504_project/GeneAnnotation/?id="+ lines[i][0:9] +"&type="+ Type + "\"  target=\"_blank\">" + lines[i][0:9] + "</a>" + lines[i][9:]		
		if lines[i][0] == ">":
			id_list = id_list + [lines[i].split(' ')[0].split('>')[1]]
			temp_detail_list =[]
			j = 5
			while True:
				if lines[i+j][0] == ">" or lines[i+j][0:6] == "Lambda":
					#print(lines[i+j])
					break
				temp_detail_list = temp_detail_list + [lines[i+j]]
				j+=1
			temp_detail_list = "".join(temp_detail_list)#將list 元素合併
			detail_list = detail_list + [temp_detail_list]
			#lines[i] = lines[i][0] + "<a href=\"" + "http://140.116.214.130/t50504_project/GeneAnnotation/?id="+ lines[i][1:10] +"&type="+ Type + "\"  target=\"_blank\">" + lines[i][1:10] + "</a>" + lines[i][10:]
		if lines[i][1:6] == "Score":
			temp_list2 = lines[i].split(",")
			Score = temp_list2[0].split("=")[1]
			Score_list = Score_list + [Score]
			Evalue = temp_list2[1].split("=")[1]
			Evalue_list = Evalue_list +[Evalue]
		if lines[i][1:11] == "Identities":
			temp_list3 = lines[i].split(",")
			Identities = temp_list3[0].split("=")[1]
			Identities_list = Identities_list + [Identities]
			Gaps = temp_list3[1].split("=")[1]
			Gaps_list = Gaps_list + [Gaps]
		# temp_list = temp_list + [lines[i]]
	# print(temp_list)
	return JsonResponse({1:id_list,2:Score_list,3:Evalue_list,4:Identities_list,5:Gaps_list,6:detail_list},safe = False)

def BLAST_PEP(request):
	return render(request, 'enhance_sequence_PEP.html', locals())

def Run_BLAST_PEP(request):
	seq = request.POST.get('data')
	Type = request.POST.get('Type')
	#print(Type)
	temp_parameters = request.POST.get('Parameters')
	parameters = json.loads(temp_parameters)
	with open ("/home/t50504/Django/t50504_project/data/temp_fasta.fasta","w") as fastafile:
		fastafile.write(seq)
	#BLASTp沒有 "-dust ,penalty ,reward" ,"num_alignments". Incompatible with argument:  `max_target_seqs'
	string = "-evalue " + parameters["evalue"] + " -outfmt " + parameters["outfmt"] + " -num_alignments " + parameters["num_alignments"] + " -gapopen " + parameters["gapopen"] + " -gapextend " + parameters["gapextend"]
	path = "/home/t50504/blast/ncbi-blast-2.11.0+/bin/" + parameters["blast_type"] + " -db /home/t50504/blastdb/"+ Type +"/"+ parameters["database"] +" -query /home/t50504/Django/t50504_project/data/temp_fasta.fasta -out /home/t50504/Django/t50504_project/data/result.out "+ string	
	#print(path)
	os.system(path)

	temp_list=[]
	detail_list = []
	table_list = {}
	id_list = []
	Score_list = []
	Evalue_list = []
	Identities_list = []
	Positives_list = []
	Gaps_list = []

	file = "/home/t50504/Django/t50504_project/data/result.out"
	with open (file,'r') as result:
		lines = result.readlines()
	result.close()

	for i in range(len(lines)):
		# if lines[i][0:3] == "Peq" or lines[i][0:3] == "Dca" or lines[i][0:3] == "Ash" or lines[i][0:3] == "Vpo" or lines[i][0:3] == "Vsh" or lines[i][0:3] == "Pgu" or lines[i][0:3] == "Pzi" or lines[i][0:3] == "evm":
		# 	id_list = id_list + [lines[i].split(' ')[0]]
			#lines[i] =  "<a href=\"" + "http://140.116.214.130/t50504_project/GeneAnnotation/?id="+ lines[i][0:9] +"&type="+ Type + "\"  target=\"_blank\">" + lines[i][0:9] + "</a>" + lines[i][9:]		
		if lines[i][0] == ">":
			id_list = id_list + [lines[i].split(' ')[0].split('>')[1]]
			temp_detail_list =[]
			j = 5
			while True:
				if lines[i+j][0] == ">" or lines[i+j][0:6] == "Lambda":
					#print(lines[i+j])
					break
				temp_detail_list = temp_detail_list + [lines[i+j]]
				j+=1
			temp_detail_list = "".join(temp_detail_list)#將list 元素合併
			detail_list = detail_list + [temp_detail_list]
			#lines[i] = lines[i][0] + "<a href=\"" + "http://140.116.214.130/t50504_project/GeneAnnotation/?id="+ lines[i][1:10] +"&type="+ Type + "\"  target=\"_blank\">" + lines[i][1:10] + "</a>" + lines[i][10:]
		if lines[i][1:6] == "Score":
			temp_list2 = lines[i].split(",")
			Score = temp_list2[0].split("=")[1]
			Score_list = Score_list + [Score]
			Evalue = temp_list2[1].split("=")[1]
			Evalue_list = Evalue_list +[Evalue]
		if lines[i][1:11] == "Identities":
			temp_list3 = lines[i].split(",")
			Identities = temp_list3[0].split("=")[1]
			Identities_list = Identities_list + [Identities]
			Positives = temp_list3[1].split("=")[1]
			Positives_list = Positives_list + [Positives]
			Gaps = temp_list3[2].split("=")[1]
			Gaps_list = Gaps_list + [Gaps]
		# temp_list = temp_list + [lines[i]]
	#print(temp_list)
	#print(id_list)
	#print(Score_list)
	#print(Evalue_list)
	#print(Identities_list)
	#print(Positives_list)
	#print(Gaps_list)
	#print(detail_list)
	return JsonResponse({1:id_list,2:Score_list,3:Evalue_list,4:Identities_list,5:Positives_list,6:Gaps_list,7:detail_list},safe = False)

def expression(request):
	temp_data = request.POST.get("data")
	#Type = request.POST.get("type")
	shorthand = {"Peq":"Phalaenopsis","Dca":"Dendrobium","Apo":"Apostasia","Vpo":"Vpompona","Vsh":"Vshenzhenica","Pgu":"Pguangdongensis","Pzi":"Pzijinensis","evm":"Ldiscolor"}
	data_type = request.POST.get('select_data_type')	
	#print(data_type)
	arry = json.loads(temp_data)
	#print(arry)
	#print(Type)
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')

	
	data_list = []
	
	for i in range(len(arry)):
		try:
			locals()['ID'+str(i)] = arry[i]
			locals()['Type'+str(i)] = shorthand[arry[i][0:3]]
			locals()['sql_string'+str(i)] = "SELECT * FROM {}_FPKM WHERE id = '{}'".format(locals()['Type'+str(i)],locals()['ID'+str(i)])
			locals()['data'+str(i)] = pd.read_sql(locals()['sql_string'+str(i)],conn)
			data_list.append(locals()['data'+str(i)])
		except:
			continue

	#print(data_list)
	compare_data = pd.concat(data_list,join='outer',sort=False)
	compare_data = pd.concat(data_list,join='outer',sort=False)
	compare_data.reset_index(drop=True, inplace=True)


	compare_data_null = compare_data.fillna("null")
	compare_data_bar = compare_data.fillna("-1")

	head = list(compare_data.columns.values)

	if data_type == "contig":
		head = [i for i in head if "TPM" not in i and "FPKM" not in i]	
	elif data_type == "TPM":
		head =  [i for i in head if "TPM" in i or "id" in i]
	else:
		head =  [i for i in head if "FPKM" in i or "id" in i]

	compare_data_null = compare_data_null[head]		
	header = list(compare_data_null)
	#header = list(compare_data.columns.values)
	header[0] = "<input type='checkbox' id=checkall> CheckAll ID"
	body = compare_data_null.values.tolist()


	#整理heatmap、cluster、pca、bar會用到的資料
	header2 = [i for i in header if "id" not in i]
	geneid = list(compare_data_null["id"])
	body2 = compare_data_null[header2].values.tolist()

	try:
		body3 = list(np.float_(body2))#text轉float
		#print(body3)
		pic_name = plot_cluster(body3,header2,geneid)
		#data_array = [[0.0,0.0,0.0,0.0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		#columns_label_list=[1,2,3,4]
		#index_label_list=['I','am','a','handsome']
		#pic_name = plot_cluster(data_array,columns_label_list,index_label_list)

		pca_list = plot_pca(body3).tolist()
		#temp_list = [[0,0,0,0],[0,1,1,0],[0,1,1,1],[0,0,0,0]]
		#X_new = plot_pca(temp_list).tolist()#numpy.ndarray to list
		#print(X_new)	#[[-0.74737806 -0.0626581 ]
						#[ 0.54191096  0.51849061]
						#[ 0.95284515 -0.3931744 ]
						#[-0.74737806 -0.0626581 ]]
		#print(type(X_new))
	except:
		pic_name = "no picture"
		pca_list = "no pca"

	return JsonResponse({0:header,1:body,2:header2,3:geneid,4:body2,5:pic_name,6:pca_list},safe = False)

def select_plot_cluster(request):
	body2 = json.loads(request.POST.get("cluster_body"))
	head = json.loads(request.POST.get("cluster_head"))
	geneid = json.loads(request.POST.get("cluster_geneid"))

	temp_figsize = request.POST.get("figsize")#"(0.02, 0.8, 0.05, 0.18)"
	figsize_list=[]
	for item in temp_figsize.split(","):#[(0.02, 0.8, 0.05,0.18)]
		num = float(item.replace("(", "").replace(")", ""))
		figsize_list.append(num)
	figsize = tuple(figsize_list)

	row_cluster = request.POST.get("row_cluster")
	if row_cluster == "True":
		row_cluster = True
	else:
		row_cluster = False

	temp_cbar_pos = request.POST.get("cbar_pos")
	cbar_pos_list=[]
	for item in temp_cbar_pos.split(","):#[(0.02, 0.8, 0.05,0.18)]
		num = float(item.replace("(", "").replace(")", ""))
		cbar_pos_list.append(num)
	cbar_pos = tuple(cbar_pos_list)

	cmap = request.POST.get("cmap")
	#print(figsize)
	vmin = request.POST.get("vmin")
	vmax = request.POST.get("vmax")
	if vmin=="default" and vmax=="default":
		try:
			body = list(np.float_(body2))
			pic_name = plot_cluster(body,head,geneid,figsize=figsize,row_cluster=row_cluster,cbar_pos=cbar_pos,cmap=cmap)

		except:
			pic_name = "no picture"

	else:
		vmin = int(vmin)
		vmax = int(vmax)
		try:
			body = list(np.float_(body2))
			pic_name = plot_cluster(body,head,geneid,figsize=figsize,row_cluster=row_cluster,cbar_pos=cbar_pos,cmap=cmap,vmin=vmin, vmax=vmax)

		except:
			pic_name = "no picture"

	return JsonResponse({"pic_name":pic_name},safe = False)

def plot_cluster(data_array,columns_label_list,index_label_list,figsize=(10,10),row_cluster=True,cbar_pos=(0.02, 0.8, 0.05, 0.18),cmap="mako",**parameters):	
	df = pd.DataFrame(data_array, columns=columns_label_list, index=index_label_list)
	#print(type(df))
	#print(parameters)#{'vmax': 10, 'vmin': 0}
	if len(parameters)==0:
		g = sns.clustermap(df,figsize=figsize,row_cluster=row_cluster,cbar_pos=cbar_pos,cmap=cmap)
	else:
		g = sns.clustermap(df,figsize=figsize,row_cluster=row_cluster,cbar_pos=cbar_pos,cmap=cmap,vmax=parameters["vmax"],vmin=parameters["vmin"])
	#plt.show()
	tempname = ''.join(random.choice(string.ascii_letters) for x in range(5))
	path1 ="/home/t50504/Django/t50504_project/static/img/heatmap/"+tempname+".png"
	if os.path.exists(path1):
		os.remove(path1)
	g.savefig("/home/t50504/Django/t50504_project/static/img/heatmap/"+tempname+".png")
	return tempname

def plot_pca(X):
	#print(type(X))
	pca = PCA(n_components=2)
	pca.fit(X)
	X_new = pca.transform(X)

	return X_new

def select_expression(request):
	select_header = json.loads(request.POST.get("select_header"))
	select_geneid = json.loads(request.POST.get("select_geneid"))
	select_body = json.loads(request.POST.get("select_body"))
	#print(select_header)
	#print(select_geneid) 
	#print(select_body)
	try:
		body = list(np.float_(select_body))#text轉float
		pic_name = plot_cluster(body,select_header,select_geneid)

		pca_list = plot_pca(body).tolist()
	except:
		pic_name = "no picture"
		pca_list = "no pca"
	return JsonResponse({0:pic_name,1:pca_list},safe = False)