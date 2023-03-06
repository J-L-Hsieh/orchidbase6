from django.shortcuts import render
from django.views.decorators import csrf
import os,datetime
import pandas as pd
import numpy as np
import time
import sys
from django.http import HttpResponse,JsonResponse
import collections
import pymysql
import json,random,string
import seaborn as sns; sns.set(color_codes=True)
from sklearn.decomposition import PCA

def GeneExpression(request):
	return render(request, 'transcriptome.html', locals())

def GeneExpression_data(request):
	t1 = time.time()
	Type = request.POST.get('type')
	data_type = request.POST.get('select_data_type')


	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')	
	sql_string = "SELECT * FROM {}_transcriptome".format(Type)
	data = pd.read_sql(sql_string,conn)
	head = list(data.columns.values)
	#print(head)	
	if data_type == "contig":
		head = [i for i in head if "TPM" not in i and "FPKM" not in i]
			#print(head)	
	elif data_type == "TPM":
		head = [i for i in head if "TPM" in i or "id" in i or "Annotation" in i]
	else:
		head = [i for i in head if "FPKM" in i or "id" in i or "Annotation" in i]
	data = data[head]		
	conn.commit()
	header = list(data)
	body = data.values.tolist()
	#data = [1,2,3,4,5]
	t2 = time.time()
	print('time elapsed: ' + str(round(t2-t1, 2)) + ' seconds')
	return JsonResponse({'d':{0:header,1:body,2:"1"}},safe = False)


def GeneExpression_select_data(request):
	
	ID = request.POST.get('id')
	Type = request.POST.get('type')
	data_type = request.POST.get('select_data_type')
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SELECT * FROM {}_compare_other_species WHERE `{}` = '{}'".format(Type,Type,ID)
	data = pd.read_sql(sql_string,conn)
	#print(data)

	#print(len(list(data.columns.values)))
	data_list = []
	Species_list = []
	shorthand = {"Phalaenopsis":"Phalaenopsis equestris","Dca":"Dendrobium catenatum","Apostasia":"Apostasia shenzhenica","Vpompona":"Vanilla pompona","Vshenzhenica":"Vanilla shenzhenica","Pguangdongensis":"Platanthera guangdongensis","Pzijinensis":"Platanthera zijinensis"}
	for i in range(len(list(data.columns.values))):
		try:
			locals()['ID'+str(i)] = data.iloc[:,i][0]
			#print(locals()['ID'+str(i)])
			locals()['Type'+str(i)] = list(data.columns.values)[i]
			locals()['sql_string'+str(i)] = "SELECT * FROM {}_transcriptome WHERE id = '{}'".format(locals()['Type'+str(i)],locals()['ID'+str(i)])
			locals()['data'+str(i)] = pd.read_sql(locals()['sql_string'+str(i)],conn)
			if locals()['ID'+str(i)] != "not available":
				Species_list.append(shorthand[locals()['Type'+str(i)]])
			data_list.append(locals()['data'+str(i)])
		except:
			continue
	#print(data_list)

	compare_data = pd.concat(data_list,join='outer',sort=False)
	compare_data.reset_index(drop=True, inplace=True)
	compare_data = compare_data.fillna("null")
	#compare_data = compare_data.round(2)
	#print(type(compare_data["Pollinium_TPM"][2]))#<class 'float'>轉成float 後還是無法用round來取小數點後兩位
	#print(compare_data)
	#print(Species_list)
	#補丁
	compare_data.insert(loc=0,column="Species",value=Species_list)
	#print(compare_data)
	#篩選contig、TPM、FPKM資料
	head = list(compare_data.columns.values)

	if data_type == "contig":
		head = [i for i in head if "TPM" not in i and "FPKM" not in i]	
	elif data_type == "TPM":
		head =  [i for i in head if "TPM" in i or "id" in i or "Species" in i or "Annotation" in i]
	else:
		head =  [i for i in head if "FPKM" in i or "id" in i or "Species" in i or "Annotation" in i]

	compare_data = compare_data[head]	
	header = list(compare_data)
	#header = list(compare_data.columns.values)
	body = compare_data.values.tolist()
	
	#head.remove("Species")
	head = [i for i in head if i != "Species" and i != "Annotation"]

	compare_data = compare_data[head]
	#head.remove("id")
	head = [i for i in head if i != "id"]

	geneid = list(compare_data["id"])
	body2 = compare_data[head].values.tolist()
	#print(body2)
	return JsonResponse({0:header,1:body,2:head,3:geneid,4:body2},safe = False)

def GeneExpression_search_data(request):
	temp_data = request.POST.get("query").replace(" ", "")
	Type = request.POST.get("type")
	shorthand = {"Peq":"Phalaenopsis","Dca":"Dendrobium","Apo":"Apostasia","Vpo":"Vpompona","Vsh":"Vshenzhenica","Pgu":"Pguangdongensis","Pzi":"Pzijinensis", "evm": "Ldiscolor"}
	data_type = request.POST.get('select_data_type')	
	
	#arry = json.loads(temp_data)
	arry = temp_data.split(",")

	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')

	
	data_list = []
	for i in range(len(arry)):
		try:
			locals()['ID'+str(i)] = arry[i]
			locals()['Type'+str(i)] = shorthand[arry[i][0:3]]
			locals()['sql_string'+str(i)] = "SELECT * FROM {}_transcriptome WHERE id = '{}'".format(locals()['Type'+str(i)],locals()['ID'+str(i)])
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
		head =  [i for i in head if "TPM" in i or "id" in i or "Annotation" in i]
	else:
		head =  [i for i in head if "FPKM" in i or "id" in i or "Annotation" in i]
	#print(head)

	compare_data_null = compare_data_null[head]		
	header = list(compare_data_null)
	#print(header)
	#header = list(compare_data.columns.values)
	#header[0] = "<input type='checkbox' id=checkall> CheckAll ID"
	body = compare_data_null.values.tolist()
	#print(body)
	#整理heatmap、cluster、pca、bar會用到的資料
	header2 = [i for i in header if "id" not in i and "Annotation" not in i]
	geneid = list(compare_data_null["id"])
	body2 = compare_data_null[header2].values.tolist()
	#print(geneid)
	#print(body2)

	try:
		body3 = list(np.float_(body2))#text轉float
		pic_name = plot_cluster(body3,header2,geneid)
		pca_list = plot_pca(body3).tolist()

	except:
		pic_name = "no picture"
		pca_list = "no pca"

	return JsonResponse({0:header,1:body,2:header2,3:geneid,4:body2,5:pic_name,6:pca_list},safe = False)

def GeneExpression_key_word_data(request):
	temp_data = request.POST.get("query")
	Type = request.POST.get("type")
	shorthand = {"Peq":"Phalaenopsis","Dca":"Dendrobium","Apo":"Apostasia","Vpo":"Vpompona","Vsh":"Vshenzhenica","Pgu":"Pguangdongensis","Pzi":"Pzijinensis"}
	data_type = request.POST.get('select_data_type')	
	
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	string = "SELECT * FROM {}_transcriptome WHERE Annotation like '%{}' or Annotation like '{}%' or Annotation like '%{}%'".format(Type,temp_data,temp_data,temp_data)
	data = pd.read_sql(string,conn)
	#print(data)
	head = list(data.columns.values)

	if data_type == "contig":
		head = [i for i in head if "TPM" not in i and "FPKM" not in i]	
	elif data_type == "TPM":
		head =  [i for i in head if "TPM" in i or "id" in i or "Annotation" in i]
	else:
		head =  [i for i in head if "FPKM" in i or "id" in i or "Annotation" in i]
	
	#print(head)
	body = data[head].values.tolist()


	#整理heatmap、cluster、pca、bar會用到的資料
	head2 = [i for i in head if "id" not in i and "Annotation" not in i]
	geneid = list(data["id"])
	body2 = data[head2].values.tolist()

	try:
		body3 = list(np.float_(body2))#text轉float
		pic_name = plot_cluster(body3,head2,geneid)
		pca_list = plot_pca(body3).tolist()

	except:
		pic_name = "no picture"
		pca_list = "no pca"

	return JsonResponse({0:head,1:body,2:head2,3:geneid,4:body2,5:pic_name,6:pca_list},safe = False)

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
