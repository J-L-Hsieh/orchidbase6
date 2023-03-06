from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse,FileResponse   
import os
import pymysql
import pandas as pd
import json,random,string
#import subprocess
#import multiprocessing
from itertools import combinations
from operator import itemgetter 
import numpy as np

# Create your views here.
def promoter_table(request):
	return(render(request,"promoter_table.html",locals()))

def promoter_table_data(request):
	Type = request.POST.get('type')
	species = request.POST.get('species')#ath
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')	
	sql_string = "SELECT * FROM {}_promoter_{}".format(Type,species)
	data = pd.read_sql(sql_string,conn)
	conn.commit()
	head = list(data)
	body = data.values.tolist()
	#data = [1,2,3,4,5]

	return JsonResponse({0:head,1:body},safe = False)

def promoter(request):
    return (render(request,"promoter.html",locals()))

@csrf_exempt
def sequence_result(request):
	Type =request.POST.get("type")#Phalaenopsis
	ID = request.POST.get("ID")#Peq000001
	species = request.POST.get("species")
	##2000 gene data
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	sql_string = "SELECT * FROM {}_2000_gene WHERE `ID_strand` LIKE '{}%'".format(Type,ID)
	#print(sql_string)
	data = pd.read_sql(sql_string,conn)
	#print(data)
	data = data.values.tolist()[0]
	#print(data)
	ID_data = data[0]
	temp_seq_data = data[1]
	temp_complement_data = data[2]

	seq_data = ""
	num_data = ""
	for i in range(len(temp_seq_data)//100):
		seq_data += temp_seq_data[100*i:100*(i+1)] + "<br>" + temp_complement_data[100*i:100*(i+1)] + "<br>" + "────────────────────────────────────────────────────────────────────────────────────────────────────" +"<br>"
		num_data += str(100*(i+1)) + "<br><br><br>"
	##pattern search results data
	type_dic={"Phalaenopsis":"Peq","Dendrobium":"Dca","Apostasia":"Ash","Vpompona":"Vpo","Vshenzhenica":"Vsh","Pguangdongensis":"Pgu","Pzijinensis":"Pzi","ath":"AT","osa":"OS","Ldiscolor":"Ldi"}
	species_dic={"ath":"Arabidopsis_thaliana","osa":"Oryza_sativa"}
	#file = "/home/t50504/Django/t50504_project/data/promoter/promoter_final_rev_family/"+ species_dic[species] +"/"+ type_dic[Type] +"/"+ ID +"_"+ type_dic[species] +"_rev_family.csv"
	file = "/home/st1/promoter/Regulation_TF_Family/"+ species_dic[species] +"/"+ type_dic[Type] +"/"+ ID +"_"+ type_dic[species] +".csv"
	data2 = pd.read_csv(file)
	#print(data2)
	
	data3 = data2.drop_duplicates("Query ID","first").reset_index(drop=True)
	data3 = data3.fillna("No family")
	#print(data3)
	family_dic={}
	for i in range(len(data3)):
		if data3["Family"][i] in family_dic:
			family_dic[data3["Family"][i]].append(data3["Query ID"][i])
		else:
			family_dic[data3["Family"][i]]=[]
			family_dic[data3["Family"][i]].append(data3["Query ID"][i])
	#print(family_dic)# {'TALE': ['Peq001329', 'Peq006685', 'Peq007917'...],'No family':['Peq001812', 'Peq002361'...]
	#family_list = list(set(data2["Family"].tolist()))
	
	#id_list = list(set(data2["Query ID"].tolist()))
	#print(len(id_list))#563
	first=1
	first2=1
	count = 1
	family_list ="<div class='ui segment'>"
	family_header= "<div class='ui header block' id='Family'>Family:"
	family_segment="<div><table border='2'><tbody><tr>"
	data_list = "<div class='ui segment'><div class='ui header block'>Transcription factor</div><div class='ui segment'>"
	for family_id in family_dic:
		#for item in id_list:
		#print(string_family)#WOX、TALE...
		value = family_id.replace(" ","_").replace("/","_").replace(";", "_")
		if count%10!=0:
			family_segment += "<td><a href='#' name='family' value='"+ value +"'>" + family_id + "("+ str(len(family_dic[family_id])) +")</a></td>"

		else:
			family_segment += "<td><a href='#' name='family' value='"+ value +"'>" + family_id + "("+ str(len(family_dic[family_id])) + ")</a></td></tr>"
		count+=1
	family_segment+="</tbody></table></div>"

	for family_id in family_dic:
		#for item in id_list:
		#print(string_family)#WOX、TALE...
		value = family_id.replace(" ","_").replace("/","_").replace(";", "_")

		if first2==1:
			data_list += "<div name='family_id' style='display: block;' id='"+ value +"'>"
			family_header += family_id +"</div>"
			first2=2
		else:
			data_list += "<div name='family_id' style='display: none;' id='"+ value +"'>"
		for item in family_dic[family_id]:
			#print(item)
			if first==1:
				#print("ok")
				first_checkbox=item.replace(".", "")
				first=2
			temp_data = data2[data2["Query ID"]==item].reset_index(drop=True)
			#print(temp_data)
			Query_ID = temp_data["Query ID"][0].replace(".", "")
			string_checkbox = "<table><tbody><tr><td><input type='checkbox' id='"+Query_ID+"' name='checkbox' value='"+temp_data["Query ID"][0]+":"
			string_table = " <td><table width='800' border='2' align='center' id='tab_"+Query_ID+"' style='display:none;'><tbody><tr><td align='center'><strong>TF ID</strong></td><td align='center'><strong>Matrix ID</strong></td><td align='center'><strong>Position</strong></td><td align='center'><strong>Strand</strong></td><td align='center'><strong>Hit Sequence</strong></td></tr>"
			string_Start = ""
			string_Strand = ""
			string_sequence = ""
			string_TFmatrix = ""
			for i in range(len(temp_data)):
				string_Start += str(temp_data["Position"][i])+","
				string_Strand += temp_data["Strand"][i]+","
				string_sequence += temp_data["Hit Sequence"][i]+","
				string_TFmatrix += temp_data["Matrix ID"][i]+","
				string_table += "<tr><td align='center'>"+temp_data["TF ID"][i]+"</td><td align='center'><a href='http://plantpan.itps.ncku.edu.tw/TFBSinfo.php?matrix="+temp_data["Matrix ID"][i]+"' target='_blank'>"+temp_data["Matrix ID"][i]+"</a></td><td align='center'>"+str(temp_data["Position"][i])+"</td><td align='center'>"+temp_data["Strand"][i]+"</td><td align='center'>"+temp_data["Hit Sequence"][i]+"</td></tr>"
			string_Start = string_Start.strip(",")+":"
			string_Strand = string_Strand.strip(",")+":"
			string_sequence = string_sequence.strip(",")+":"
			string_TFmatrix = string_TFmatrix.strip(",")+"'"
			string_checkbox += string_Start+string_Strand+string_sequence+string_TFmatrix+">"+temp_data["Query ID"][0]+"</td>"	
			string_table += "</td></tbody></table></td></tr></tbody></table>"
			string_checkbox += string_table
			data_list+= string_checkbox
		data_list+="</div>"
	data_list+="</div></div>"
	family_list+=family_header+family_segment+"</div>"
	#print(len(data_list))#563

	return JsonResponse({'ID_data':ID_data,'seq_data':seq_data,'num_data':num_data,'family_list':family_list,'data_list':data_list,'first_checkbox':first_checkbox})

def click_result(request):
	val = json.loads(request.POST.get("val"))
	#print(type(val))#<class 'list'>
	#print(val)#[["Peq022244:1637,1637,1826,1136,1136,1835,1753,1753,1826:+,-,+,+,-,+,+,-,-:aAATATattc,aaatATATTc,aAATATaatc,taATTAAttg,taaTTAATtg,ctATTAAata,tATTATaatt,atattATAATt,aaatATAATc"],["Peq006449:1334,122,602,1293,1982:+,+,-,-,+:atttcAAATTtat,TGTCTc,gAGACA,gAGACAc,TGTCTc:TFmatrixID_0004,TFmatrixID_0004...:#436fe6"]]
	Type =request.POST.get("type")
	ID = request.POST.get("ID")
	species = request.POST.get("species")
	conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
	#print(ID)

	#<================================================整理visualization和sequence view會用到的資訊===================================================>
	data_dic ={}
	id_list=[]
	for i in range(len(val)):
		temp_id = val[i].split(":")[0]#Peq022244
		start_list = val[i].split(":")[1].split(",")#[1637,1637,1826,1136,1136,1835,1753,1753,1826]
		strand_list = val[i].split(":")[2].split(",")#[+,-,+,+,-,+,+,-,-]
		hit_seq_list = val[i].split(":")[3].split(",")#[aAATATattc,aaatATATTc,aAATATaatc,taATTAAttg,taaTTAATtg,ctATTAAata,tATTATaatt,atattATAATt,aaatATAATc]
		Matrix = val[i].split(":")[4].split(",")#[TFmatrixID_0004,TFmatrixID_0004,TFmatrixID_0004,TFmatrixID_0005,TFmatrixID_0005,TFmatrixID_0005,TFmatrixID_0006,TFmatrixID_0006,TFmatrixID_0006]
		color = val[i].split(":")[5]# #668561
		id_list.append(temp_id)#["Peq022244","Peq006449"]
		data_dic[temp_id] ={"start_list":start_list,"strand_list":strand_list,"hit_seq_list":hit_seq_list,"color":color,"Matrix":Matrix}
	#print(data_dic) #{'Peq022244': {'strand_list': ['-', '+'], 'start_list': ['1797', '1818'], 'hit_seq_list': ['atttcAAATTtat', 'ttaAATTTaaata'], 'color': '#656473'}, 
					 #'Peq006449': {'strand_list': ['+', '-'], 'start_list': ['1637', '1637'], 'hit_seq_list': ['aAATATattc', 'aaatATATTc'], 'color': '#65e29e'}}



	#<================================================滑鼠移動到色塊上顯示的資訊===================================================>
	#print(data_dic) #{'Peq022244': {'color': '#f6bfa7', 'start_list': ['1637', '1637', '1826', '1136', '1136', '1835', '1753', '1753', '1826'], 'strand_list': ['+', '-', '+', '+', '-', '+', '+', '-', '-'], 'hit_seq_list': ['aAATATattc', 'aaatATATTc', 'aAATATaatc', 'taATTAAttg', 'taaTTAATtg', 'ctATTAAata', 'tATTATaatt', 'atattATAATt', 'aaatATAATc']}, 
					#'Peq006449': {'color': '#7927bd', 'start_list': ['1334', '122', '602', '1293', '1982'], 'strand_list': ['+', '+', '-', '-', '+'], 'hit_seq_list': ['atttcAAATTtat', 'TGTCTc', 'gAGACA', 'gAGACAc', 'TGTCTc']}}
	for i in id_list:
		tooltip_list = []
		for j in range(len(data_dic[i]["start_list"])):
			#sql_string2 = "SELECT * FROM {}_promoter_Peq000001 WHERE `Position`='{}' AND `Strand`='{}'".format(Type,data_dic[i]["start_list"][j],data_dic[i]["strand_list"][j])

			type_dic={"Phalaenopsis":"Peq","Dendrobium":"Dca","Apostasia":"Ash","Vpompona":"Vpo","Vshenzhenica":"Vsh","Pguangdongensis":"Pgu","Pzijinensis":"Pzi","ath":"AT","osa":"OS","Ldiscolor":"Ldi"}
			species_dic={"ath":"Arabidopsis_thaliana","osa":"Oryza_sativa"}
			#file = "/home/t50504/Django/t50504_project/data/promoter/promoter_final/{}/{}/{}_{}.csv".format(species_dic[species],type_dic[Type],ID,type_dic[species])
			file = "/home/st1/promoter/Regulation_TF_Family/{}/{}/{}_{}.csv".format(species_dic[species],type_dic[Type],ID,type_dic[species])
			data2 = pd.read_csv(file)
			#data2 = data2.loc[(data2["Position"]==1637) & (data2["Strand"]=="+")]
			data2 = data2.loc[(data2["Position"]==int(data_dic[i]["start_list"][j])) & (data2["Strand"]==data_dic[i]["strand_list"][j])]
			#print(data2)
			#data2 = data2[["Position","Strand","Hit Sequence","TF ID","Query ID"]]
			data_body = data2.values.tolist()
			data_head = list(data2)
			#print(data_head)#['Position', 'Strand', 'Hit Sequence', 'TF ID', 'Query ID']
			#print(data_body)#[[1637, '+', 'aAATATattc', 'AT4G14465', 'Peq022244']]
			string_tooltip =''''''
			string_tooltip += '''<table border='2'><tr>'''
			for k in range(len(data_head)):
				string_tooltip += '''<th>''' + data_head[k] +'''</th>'''
			string_tooltip += '''</tr><tbody><tr>'''

			for k in range(len(data_body)):
				for l in range(len(data_body[k])):
					string_tooltip += '''<td>''' + str(data_body[k][l]) +'''</td>'''
				string_tooltip += '''</tr>'''

			string_tooltip += '''</tbody></table>'''
			tooltip_list.append(string_tooltip)

			#print(tooltip_list) 
			#["<table border='1'><tr><th>Position</th><th>Strand</th><th>Hit Sequence</th><th>TF ID</th><th>Query ID</th></tr><tbody><tr><td>1637</td><td>+</td><td>aAATATattc</td><td>AT4G14465</td><td>Peq022244</td></tr></tbody></table>", 
			#"<table border='1'><tr><th>Position... 
			
		data_dic[i]["tooltip_list"] = tooltip_list
	#print(data_dic)


	#<================================================整理visualization用到的資訊===================================================>
	vis_pos_start=[]
	vis_pos_end=[]
	vis_pos_color=[]
	vis_pos_tooltip=[]
	vis_neg_start=[]
	vis_neg_end=[]
	vis_neg_color=[]
	vis_neg_tooltip=[]
	for ID1 in id_list:
		for i in range(len(data_dic[ID1]["strand_list"])):
			if data_dic[ID1]["strand_list"][i] == "+": 
				vis_pos_start.append(data_dic[ID1]["start_list"][i])
				vis_pos_end.append(str(int(data_dic[ID1]["start_list"][i])+len(data_dic[ID1]["hit_seq_list"][i])-1))
				vis_pos_color.append(data_dic[ID1]["color"])
				vis_pos_tooltip.append(data_dic[ID1]["tooltip_list"][i])
			else:
				vis_neg_start.append(data_dic[ID1]["start_list"][i])
				vis_neg_end.append(str(int(data_dic[ID1]["start_list"][i])+len(data_dic[ID1]["hit_seq_list"][i])-1))
				vis_neg_color.append(data_dic[ID1]["color"])
				vis_neg_tooltip.append(data_dic[ID1]["tooltip_list"][i])
	#sort
	#print(vis_pos_start)#['171', '771', '781', '1209', '1347', '1670', '171', '771', '781', '1209', '1347', '1670']
	#print(vis_pos_end)#['179', '779', '789', '1217', '1355', '1678', '179', '779', '789', '1217', '1355', '1678']
	#print(vis_pos_color)#['#434a58', '#434a58', '#434a58', '#434a58', '#434a58', '#434a58', '#da6335', '#da6335', '#da6335', '#da6335', '#da6335', '#da6335']
	#print(vis_pos_tooltip)



	#分層判斷:正的
	record_level_pos={}
	if len(vis_pos_start)!=0:
		vis_pos_start_int = [int(i) for i in vis_pos_start]
		vis_pos_end_int = [int(i) for i in vis_pos_end]
		vis_pos_start_int,vis_pos_end_int,vis_pos_start,vis_pos_end,vis_pos_color,vis_pos_tooltip = zip(*sorted(zip(vis_pos_start_int,vis_pos_end_int,vis_pos_start,vis_pos_end,vis_pos_color,vis_pos_tooltip)))
		#print(vis_pos_start)
		#print(vis_pos_end)
		record_level_pos = {1:[[vis_pos_start_int[0],vis_pos_end_int[0],vis_pos_color[0],vis_pos_tooltip[0]]]}#先放第一個start position,end position,color,tooltip進去，並在前面記錄1
		for i in range(1,len(vis_pos_start)):
			count=1
			while True:
				try:#正常的情況
					if vis_pos_start_int[i]>record_level_pos[count][-1][1]:#若下一個start > 上一個的end
						record_level_pos[count].append([vis_pos_start_int[i],vis_pos_end_int[i],vis_pos_color[i],vis_pos_tooltip[i]])#將end加到同一層
						break
					else:#若下一個start <= 上一個的end
						count += 1

				except:	#如果沒有下一層的資訊，則新增
					record_level_pos[count]=[]	
					record_level_pos[count].append([vis_pos_start_int[i],vis_pos_end_int[i],vis_pos_color[i],vis_pos_tooltip[i]])#則將end加到同一層
					break
		
		#print(record_level_pos)

	#分層判斷:負的
	record_level_neg={}
	if len(vis_neg_start)!=0:
		vis_neg_start_int = [int(i) for i in vis_neg_start]
		vis_neg_end_int = [int(i) for i in vis_neg_end]
		vis_neg_start_int,vis_neg_end_int,vis_neg_start,vis_neg_end,vis_neg_color,vis_neg_tooltip = zip(*sorted(zip(vis_neg_start_int,vis_neg_end_int,vis_neg_start,vis_neg_end,vis_neg_color,vis_neg_tooltip)))
		#print(vis_neg_start)
		#print(vis_neg_end)
		record_level_neg = {1:[[vis_neg_start_int[0],vis_neg_end_int[0],vis_neg_color[0],vis_neg_tooltip[0]]]}#先放第一個start position,end position,color,tooltip進去，並在前面記錄1
		for i in range(1,len(vis_neg_start)):
			count=1
			while True:
				try:#正常的情況
					if vis_neg_start_int[i]>record_level_neg[count][-1][1]:#若下一個start > 上一個的end
						record_level_neg[count].append([vis_neg_start_int[i],vis_neg_end_int[i],vis_neg_color[i],vis_neg_tooltip[i]])#將end加到同一層
						break
					else:#若下一個start <= 上一個的end
						count += 1

				except:	#如果沒有下一層的資訊，則新增
					record_level_neg[count]=[]	
					record_level_neg[count].append([vis_neg_start_int[i],vis_neg_end_int[i],vis_neg_color[i],vis_neg_tooltip[i]])#則將end加到同一層
					break
		
		#print(record_level_neg)


	#<================================================整理sequence view會用到的資訊===================================================>
	##2000序列資料和他的complement資料
	#print(ID)
	#print(Type)
	sql_string = "SELECT * FROM {}_2000_gene WHERE `ID_strand` LIKE '{}%'".format(Type,ID)
	data = pd.read_sql(sql_string,conn)
	data = data.values.tolist()[0]
	temp_seq_data = data[1]
	temp_complement_data = data[2]

	seq_data_pos = [temp_seq_data[i:i+100] for i in range(0, len(temp_seq_data), 100)]
	seq_data_neg = [temp_complement_data[i:i+100] for i in range(0, len(temp_complement_data), 100)]
	divider = ["────────────────────────────────────────────────────────────────────────────────────────────────────" for i in range(0, len(temp_seq_data), 100)]

	##record_level_pos和record_level_neg的過百紀錄+修正，用於畫sequence view //record_level_pos={1: [[346, 355, "#b463d8", "<table border='2'><tr><th>Matrix ID</th><th>Positi…624;Peq0],[]...], 2: Array(3), 3: Array(3), 4: Array(2)}
	seq_level_pos = {}
	temp_seq_pos = record_level_pos
	seq_level_neg = {}
	temp_seq_neg = record_level_neg

	##先將end有過100，200，300的做修正，拆成兩個
	for hundred in range(1,2000,100):
		for i in range(1,len(record_level_pos)+1):#level: 1,2,3...
			for j in range(len(record_level_pos[i])):#第一層有...,第二層有...
				if  ((record_level_pos[i][j][0] >= hundred) and (record_level_pos[i][j][0] < hundred+100)) and (record_level_pos[i][j][1] >= hundred+100):#ex: 95 105
					#temp_seq_pos[i][j][1] = hundred + 100 #過百修正

					temp_end = temp_seq_pos[i][j][1]
					temp_seq_pos[i][j] = [temp_seq_pos[i][j][0],hundred+99,temp_seq_pos[i][j][2],temp_seq_pos[i][j][3]]
					temp_seq_pos[i].append([hundred+100,temp_end,temp_seq_pos[i][j][2],temp_seq_pos[i][j][3]])#過百修正，新增一個
					
					#print(len(temp_seq_pos[i]))
				
				else:
					continue
		for i in range(1,len(record_level_neg)+1):#level: 1,2,3...
			for j in range(len(record_level_neg[i])):#第一層有...,第二層有...
				if  ((record_level_neg[i][j][0] >= hundred) and (record_level_neg[i][j][0] < hundred+100)) and (record_level_neg[i][j][1] >= hundred+100):#ex: 95 105
					#temp_seq_pos[i][j][1] = hundred + 100 #過百修正

					temp_end = temp_seq_neg[i][j][1]
					temp_seq_neg[i][j] = [temp_seq_neg[i][j][0],hundred+99,temp_seq_neg[i][j][2],temp_seq_neg[i][j][3]]
					temp_seq_neg[i].append([hundred+100,temp_end,temp_seq_neg[i][j][2],temp_seq_neg[i][j][3]])#過百修正，新增一個
					
				else:
					continue
	"""
	for i in range(len(temp_seq_pos[1])):
		print(temp_seq_pos[1][i][1])
	for i in range(len(temp_seq_pos[2])):
		print(temp_seq_pos[2][i][1])
	"""
	##將start、end取餘數方便畫圖
	for hundred in range(1,2000,100):
		temp_list_pos = {}
		for i in range(1,len(temp_seq_pos)+1):#level: 1,2,3...
			#count=0
			temp_list_pos[i]=[]		
			for j in range(len(temp_seq_pos[i])):#第一層有...,第二層有...
				if  ((temp_seq_pos[i][j][0] >= hundred) and (temp_seq_pos[i][j][0] < hundred+100)) and ((temp_seq_pos[i][j][1] >= hundred) and (temp_seq_pos[i][j][1] < hundred+100)):#ex: 95 100
					#print("ok1")
					
					if temp_seq_pos[i][j][1]%100==0:#end剛好等於100時取餘數會變成0
						end = 100
					else:
						end = temp_seq_pos[i][j][1]%100
					#print([(temp_seq_pos[i][j][0])%100-1,end])
					#count+=1
					temp_list_pos[i].append([(temp_seq_pos[i][j][0])%100-1,end,temp_seq_pos[i][j][2],temp_seq_pos[i][j][3]])	#過百紀錄，取餘數
					
				
				#elif  ((temp_seq_pos[i][j][0] >= hundred) and (temp_seq_pos[i][j][0] < hundred+100)) and (temp_seq_pos[i][j][1] >= hundred+100):#ex: 95 105
					#print("ok2")
					#temp_seq_pos[i][j][1] = hundred + 100 #過百修正
					#temp_list_pos[i]=[]
					#temp_list_pos[i].append([(temp_seq_pos[i][j][0])%100-1,100,temp_seq_pos[i][j][2],temp_seq_pos[i][j][3]])
					#temp_seq_pos[i].append([hundred+100,temp_seq_pos[i][j][1],temp_seq_pos[i][j][2],temp_seq_pos[i][j][3]])#過百修正，新增一個
					
				else:#ex: 205 210
					#print("ok3")
					continue
			##空list修正，若有空list，則會使序列多增加空格
			if temp_list_pos[i]==[]:
				temp_list_pos.pop(i, None)

			#print(str(hundred)+":"+str(count))
		seq_level_pos[hundred] = temp_list_pos
	#print(seq_level_pos)

	for hundred in range(1,2000,100):
		temp_list_neg = {}
		for i in range(1,len(temp_seq_neg)+1):#level: 1,2,3...
			temp_list_neg[i]=[]
			for j in range(len(temp_seq_neg[i])):#第一層有...,第二層有...
				if  ((temp_seq_neg[i][j][0] >= hundred) and (temp_seq_neg[i][j][0] < hundred+100)) and ((temp_seq_neg[i][j][1] >= hundred) and (temp_seq_neg[i][j][1] < hundred+100)):#ex: 95 100
					#print("ok1")
					
					if temp_seq_neg[i][j][1]%100==0:#end剛好等於100時取餘數會變成0
						end = 100
					else:
						end = temp_seq_neg[i][j][1]%100
					temp_list_neg[i].append([(temp_seq_neg[i][j][0])%100-1,end,temp_seq_neg[i][j][2],temp_seq_neg[i][j][3]])	#過百紀錄，取餘數
					
				
				#elif  ((temp_seq_neg[i][j][0] >= hundred) and (temp_seq_neg[i][j][0] < hundred+100)) and (temp_seq_neg[i][j][1] >= hundred+100):#ex: 95 105
					#print("ok2")
					#temp_seq_neg[i][j][1] = hundred + 100 #過百修正
					#temp_list_neg[i]=[]
					#temp_list_neg[i].append([(temp_seq_neg[i][j][0])%100-1,100,temp_seq_neg[i][j][2],temp_seq_neg[i][j][3]])
					#temp_seq_neg[i].append([hundred+100,temp_seq_neg[i][j][1],temp_seq_neg[i][j][2],temp_seq_neg[i][j][3]])#過百修正，新增一個
				
				else:#ex: 205 210
					#print("ok3")
					continue
			##空list修正，若有空list，則會使序列多增加空格
			if temp_list_neg[i]==[]:
				temp_list_neg.pop(i, None)

		seq_level_neg[hundred] = temp_list_neg
	#print(seq_level_neg)

	return JsonResponse({'record_level_pos':record_level_pos,'record_level_neg':record_level_neg,'seq_data_pos':seq_data_pos,'seq_data_neg':seq_data_neg,'divider':divider,'seq_level_pos':seq_level_pos,'seq_level_neg':seq_level_neg})
