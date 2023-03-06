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

def GeneAnnotation(request):
	return render(request, 'GeneAnnotation.html', locals())

def GeneAnnotation_data(request):
	t1 = time.time()
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	Type = request.POST.get('type')
	#print(content)
	sql_string = "SELECT * FROM " + Type +"_table"
	sql_string2 = "SELECT * FROM " + Type + "_location"
	data = pd.read_sql(sql_string,conn)
	print(data)
	data2 = pd.read_sql(sql_string2,conn)
	conn.commit()
	header = list(data)
	body = data.values.tolist()
	loc_header = list(data2) 
	loc_body = data2.values.tolist()
	#data = [1,2,3,4,5]
	t2 = time.time()
	print('time elapsed: ' + str(round(t2-t1, 2)) + ' seconds')
	return JsonResponse({0:header,1:body,2:loc_header,3:loc_body},safe = False)	


	#以下為舊版的多重查詢功能
	"""
	Type = request.POST.get('type')
	query = request.POST.get('query')
	annotation = request.POST.get('annotation')
	species = request.POST.get('species')
	#print(Type)
	#print(query)
	#print(annotation)
	#print(species)
	if (query == None or query == "") and (annotation == None or annotation == "") and (species == None or species == ""):
		print("all none")
		conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
		Type = request.POST.get('type')
		#print(content)
		sql_string = "select * from " + Type +"_table"
		sql_string2 = "select * from " + Type + "_location"
		data = pd.read_sql(sql_string,conn) 
		data2 = pd.read_sql(sql_string2,conn)
		conn.commit()
		header = list(data)
		body = data.values.tolist()
		loc_header = list(data2) 
		loc_body = data2.values.tolist()
		#data = [1,2,3,4,5]
		return JsonResponse({'d':{0:header,1:body,2:loc_header,3:loc_body,4:"1"}},safe = False)
	else:
		conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
		sql_string = "SHOW COLUMNS FROM "+ Type + "_table"
		cursor = conn.cursor()
		cursor.execute(sql_string)
		temp  = []
		head = cursor.fetchall()
		for i in range(len(head)):
			temp = np.append(temp,head[i][0])
		header = list(temp)
		conn.close()


		conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
		sql_string = "SELECT * FROM  {}_table WHERE `Gene ID`='{}' and `Annotation`='{}' and `Species`='{}'".format(Type,query,annotation,species)
		print(sql_string)
		cursor = conn.cursor()	
		cursor.execute(sql_string)
		body = list(cursor.fetchall()[0]) 
		#data = pd.DataFrame(list(result))
		sql_string2 = "SELECT * FROM " + Type + "_location WHERE `id` = %s"
		cursor2 = conn.cursor()
		cursor2.execute(sql_string2,query)
		loc_body = list(cursor2.fetchall()[0])


		conn.close()

		return JsonResponse({'d':{0:header,1:body,2:loc_body,4:"2"}},safe = False)
 	"""

def GeneAnnotation_select_data(request):

	ID = request.POST.get('id')
	Type = request.POST.get('type')
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SHOW COLUMNS FROM "+ Type + "_table2"
	cursor = conn.cursor()
	cursor.execute(sql_string)
	temp  = []
	head = cursor.fetchall()
	for i in range(len(head)):
		temp = np.append(temp,head[i][0])
	header = list(temp)
	conn.close()


	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SELECT * FROM " + Type + "_table2 WHERE `Gene ID` = %s"
	cursor = conn.cursor()	
	cursor.execute(sql_string,ID)
	body = list(cursor.fetchall()[0]) 
	#data = pd.DataFrame(list(result))
	sql_string2 = "SELECT * FROM " + Type + "_location WHERE `id` = %s"
	cursor2 = conn.cursor()
	cursor2.execute(sql_string2,ID)
	loc_body = list(cursor2.fetchall()[0])


	conn.close()

	return JsonResponse({'d':{0:header,1:body,2:loc_body}},safe = False)

def GeneID_detail(request):
	ID = request.GET.get("id")
	Type = request.GET.get("type")
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SELECT * FROM {}_cds WHERE sqName = %s".format(Type)
	cursor = conn.cursor()
	cursor.execute(sql_string,ID)
	cds = cursor.fetchall()[0] 
	CDS =">" + cds[0] + " locusName:" + cds[2] + " from:" + str(cds[3]) + " to:" + str(cds[4]) + cds[5]  + "\n" + cds[6] 
	#data = pd.DataFrame(list(result))
	conn.close()

	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string2 = "SELECT * FROM {}_pep WHERE sqName = %s".format(Type)
	cursor = conn.cursor()	
	cursor.execute(sql_string2,ID)
	pep = cursor.fetchall()[0] 
	PEP =">" + pep[0] + " locusName:" + pep[2] + " from:" + str(pep[3]) + " to:" + str(pep[4]) + pep[5]  + "\n" + pep[6]
	conn.close()
	return render(request, "GeneID_detail.html",locals())

def ViewPathway(request):
	return render(request,"ViewPathway.html",locals())

def ViewPathway_data(request):
	ID = request.POST.get('id')
	Type = request.POST.get('type')
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SHOW COLUMNS FROM {}_ViewPathway".format(Type)
	cursor = conn.cursor()
	cursor.execute(sql_string)
	temp  = []
	head = cursor.fetchall()
	for i in range(len(head)):
		temp = np.append(temp,head[i][0])
	header = list(temp)
	conn.close()
	

	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SELECT * FROM {}_ViewPathway WHERE `contig Name` = %s".format(Type)
	cursor = conn.cursor()	
	cursor.execute(sql_string,ID)
	body = list(cursor.fetchall()) 
	#data = pd.DataFrame(list(result))
	conn.close()
	
	return JsonResponse({'d':{0:header,1:body,2:ID}},safe = False)

def ViewGoTerm(request):
	return render(request,"ViewGoTerm.html",locals())

def ViewGoTerm_data(request):
	ID = request.POST.get('id')
	Type = request.POST.get('type')
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SHOW COLUMNS FROM {}_GO".format(Type)
	cursor = conn.cursor()
	cursor.execute(sql_string)
	temp  = []
	head = cursor.fetchall()
	for i in range(len(head)):
		temp = np.append(temp,head[i][0])
	header = list(temp)
	conn.close()
	

	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SELECT * FROM {}_GO WHERE `Locus Name` = %s".format(Type)
	cursor = conn.cursor()	
	cursor.execute(sql_string,ID)
	body = list(cursor.fetchall()) 
	#data = pd.DataFrame(list(result))
	conn.close()
	
	return JsonResponse({'d':{0:header,1:body,2:ID}},safe = False)

def ViewInterPro(request):
	return render(request,"ViewInterPro.html",locals())


def ViewInterPro_data(request):
	ID = request.POST.get('id')
	Type = request.POST.get('type')
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SHOW COLUMNS FROM {}_IPR".format(Type)
	cursor = conn.cursor()
	cursor.execute(sql_string)
	temp  = []
	head = cursor.fetchall()
	for i in range(len(head)):
		temp = np.append(temp,head[i][0])
	header = list(temp)
	conn.close()
	

	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SELECT * FROM {}_IPR WHERE `Locus Name` = %s".format(Type)
	cursor = conn.cursor()	
	cursor.execute(sql_string,ID)
	body = list(cursor.fetchall()) 
	#data = pd.DataFrame(list(result))
	conn.close()
	
	return JsonResponse({'d':{0:header,1:body,2:ID}},safe = False)