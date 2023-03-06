from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse,FileResponse   
import os
import pymysql
import pandas as pd
import json,random,string
import subprocess
import numpy as np
import multiprocessing
import json,random,string
import seaborn as sns; sns.set(color_codes=True)
from sklearn.decomposition import PCA
# Create your views here.
def hmmer(request):
    return (render(request,"pfam.html",locals()))

@csrf_exempt
def Ajax_func(request):

    #使用者輸入查詢的pfam表
    inp_text = request.POST.get('inp')
    #print(inp_text)

    with open('/home/t50504/Django/t50504_project/data/pfam.txt', 'w') as wfile:
        wfile.write(inp_text)    

    path = "/home/t50504/hmmer/hmmer-3.3.2/src/hmmscan --cut_ga --domtblout /home/t50504/Django/t50504_project/data/pfam_result.txt /home/t50504/hmmer/Pfam-A.hmm /home/t50504/Django/t50504_project/data/pfam.txt"

    os.system(path)
    
    with open('/home/t50504/Django/t50504_project/data/pfam_result.txt', 'r') as rfile:
        a = rfile.readlines()
    
    body1,accession = pfam(a)
    #print(accession)# ['PF16363.5', 'PF01370.21', 'PF01073.19', 'PF02719.15', 'PF04321.17', 'PF13460.6', 'PF07993.12']
    if body1==[]:
        body1=[['-', '-', '-', '-', '-', '-', '-', '-', '-']]

    head1 = ["Pfam ID", 'Envelope Start', 'Envelope End', 'Aligment Start',
             'Aligment End', 'Hmm From', 'Hmm End',  "independent Evalue", "conditional Evalue"]

    df = pd.DataFrame(body1,columns=head1)
    df["Pfam ID"] = df["Pfam ID"].map(lambda x : x.split(".")[0])

    #加description
    conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8') 
    sql_string = "SELECT * FROM `pfam_database`"
    data = pd.read_sql(sql_string,conn)
    conn.commit()
    #head = list(data)
    head2 = ["Pfam ID","Description"]
    #body = data.values.tolist()
    body2 = data[head2].values.tolist()
    df2 = pd.DataFrame(body2,columns=head2)

    merge_data = pd.merge(df,df2,left_on="Pfam ID",right_on="Pfam ID",how="inner")
    #print(merge_data)
    #header = list(merge_data)
    header = ["Pfam ID", 'Envelope Start', 'Envelope End', 'Aligment Start',
              'Aligment End', 'Hmm From', 'Hmm End',  "independent Evalue", "conditional Evalue", "Description"]
    body = merge_data[header].values.tolist()

    return JsonResponse({'header':header,'body':body,"accession":accession})

def task(path):
    os.system(path)
def Interproscan(request):
    inp_text = request.POST.get('inp')

    with open('/home/t50504/Django/t50504_project/data/interproscan.fasta', 'w') as wfile:
        wfile.write(inp_text)

    path1 = "/home/t50504/Django/t50504_project/data/interproscan_output.tsv"
    if os.path.exists(path1):
        os.remove(path1)   
    
    path = "/home/t50504/InterProScan/interproscan-5.50-84.0/interproscan.sh -goterms -i /home/t50504/Django/t50504_project/data/interproscan.fasta -b /home/t50504/Django/t50504_project/data/interproscan_output -f tsv"

    # os.system(path)
    #f = os.popen(path)
    #print(f.read())#此行為less /var/log/apache2/error.log中顯示跑interproscan.sh的結果，如果沒加這行，不知道為啥會先跑下面那行，而導致找不到interproscan_output.tsv檔。
    
    #平行處理
    pool = multiprocessing.Pool(20)
    result = pool.apply_async(task,args=(path,))            
    pool.close()
    pool.join()

    with open('/home/t50504/Django/t50504_project/data/interproscan_output.tsv', 'r') as rfile:
        a = rfile.readlines()


    result=[]
    accession=[]
    for i in range(len(a)):
        tmp = a[i].split('\t')
        #print(tmp)#['2abl_A', '2c76d432678476bd87a1a37ccd27be3b', '163', 'SUPERFAMILY', 'SSF55550', 'SH2 domain', '44', '162', '4.43E-37', 'T', '25-03-2021', 'IPR036860', 'SH2 domain superfamily\n']
        tmp[12] = tmp[12].strip('\n')
        accession.append(tmp[11])
        try:
            result.append([tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8],tmp[11],tmp[12], tmp[13]])
        except:
            result.append([tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8],tmp[11],tmp[12], '-'])
    header = ["analysis","Signature accession","Signature description","Start location","Stop location","Score","InterPro accession","InterPro description", "GO Terms"]
    
    return JsonResponse({"header":header,"body":result,"accession":accession})


def similar_gene(request):
    library = request.POST.get('library')
    values = float(request.POST.get("numbers")) 
    Similarity = request.POST.get("Similarity")
    accession_arr = json.loads(request.POST.get("accession_arr"))
    Jaccard_arr = json.loads(request.POST.get("Jaccard_arr"))
    accession_arr = [i.split(".")[0] for i in accession_arr]#去除版本號
    Jaccard_arr = [i.split(".")[0] for i in Jaccard_arr]#去除版本號
    #對照資料庫基因的pfam相似度表
    #print(Jaccard_arr)#['PF00017.24', 'PF00018.28', 'PF14604.6', 'PF07653.17']

    #print(Similarity)
    #print(accession_arr)
    #print(Jaccard_arr)

    conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
    data_list = []
    for i in range(1):
        if library == "all_species":
            library_list=["Phalaenopsis","Dendrobium","Apostasia","Vpompona","Vshenzhenica","Pguangdongensis","Pzijinensis","Paphiopedilum"]
            for j in library_list:
                locals()['data_'+str(j)] = pd.read_sql("SELECT * FROM {}_pfam_query".format(j),conn)
                data_list.append(locals()['data_'+str(j)])
            data = pd.concat(data_list,join='outer',sort=False)
            data = data.reset_index(drop=True)
        else:
            sql_string = "SELECT * FROM {}_pfam_query".format(library)
            data = pd.read_sql(sql_string,conn)


    print(data)

    #Jaccard Score
    if Similarity == "Jaccard":
        data["Jaccard"] = data["Pfam ID"].map(lambda x : (len(set([i.split(".")[0] for i in x.split(",")]).intersection(Jaccard_arr)))/(len(set([i.split(".")[0] for i in x.split(",")]).union(Jaccard_arr))))
        data = data[["gene name","Jaccard","Pfam ID"]]
        #data = data.nlargest(numbers,"Jaccard")#用來篩前幾比資料
        #print(data)
        data = data.loc[data['Jaccard'] >= values]
        data = data.sort_values(by=["Jaccard"],ascending=False)
        data = data.reset_index(drop=True)

        data_header = list(data)
        data_body = data.values.tolist()
    #
    elif Similarity == "Intersection":
        #print(accession_arr)#['PF00017.24,PF00018.28,PF14604.6,PF07653.17']
        data["intersection"] = data["Pfam ID"].map(lambda x : (len(set([i.split(".")[0] for i in x.split(",")]).intersection(accession_arr))))#1,2,3,4
        #data["accession_length"] =  data["accession"].map(lambda x : (len(set(x.split(",")))))
        #print(data)
        data = data.loc[(data['intersection'] == len(accession_arr))]#交集數一樣
        #print(data)
        data = data[["gene name","Pfam ID"]]
        data_header = list(data)
        data_body = data.values.tolist()
        """
        tempstring = ",".join(accession_arr)
        templist = []
        templist.append(tempstring)
        #print(templist)#['PF00017.24,PF00018.28,PF14604.6,PF07653.17']
        tempdataframe = pd.DataFrame(templist,columns=["accession"])
        print(tempdataframe)
        data2 = pd.merge(data,tempdataframe,left_on="accession",right_on="accession",how="inner")
        print(data2)
        data_header = list(data2)
        data_body = data2.values.tolist()
        """

    else: #Similarity == "union"
        #print(data)
        string = ""
        for i in accession_arr:
            string += i + "|" 
        string = string.strip('|')
        #print(string)
        data = data[data["Pfam ID"].str.contains(string)]
        #print(data)
        #data = data.sort_values(by=["Jaccard"],ascending=False)
        #data = data.reset_index(drop=True)

        data_header = list(data)
        data_body = data.values.tolist()

    return JsonResponse({'Jaccard_header':data_header,'Jaccard_body':data_body})

def similar_gene_interproscan(request):
    library = request.POST.get('library')
    values = float(request.POST.get("numbers")) 
    Similarity = request.POST.get("Similarity")
    accession_arr = json.loads(request.POST.get("accession_arr"))
    Jaccard_arr = json.loads(request.POST.get("Jaccard_arr"))
    accession_arr = [i.split(".")[0] for i in accession_arr]#去除版本號
    Jaccard_arr = [i.split(".")[0] for i in Jaccard_arr]#去除版本號
    #對照資料庫基因的interproscan相似度表
    #print(Jaccard_arr)#["IPR000980","IPR035837","IPR000980","IPR001452","IPR001452","IPR001452","IPR000980","IPR000980","IPR000980"]
    #print(Similarity)
    #print(accession_arr)
    Jaccard_arr = list(set(Jaccard_arr))
    Jaccard_arr = [i for i in Jaccard_arr if i != "-"] 
    print(Jaccard_arr)#['IPR036291', '-', 'IPR005886', 'IPR016040']

    conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8')
    data_list = []
    for i in range(1):
        if library == "all_species":
            library_list=["Phalaenopsis","Dendrobium","Apostasia","Vpompona","Vshenzhenica","Pguangdongensis","Pzijinensis"]
            for j in library_list:
                locals()['data_'+str(j)] = pd.read_sql("SELECT * FROM {}_interproscan_query".format(j),conn)
                data_list.append(locals()['data_'+str(j)])
            data = pd.concat(data_list,join='outer',sort=False)
            data = data.reset_index(drop=True)
        else:
            sql_string = "SELECT * FROM {}_interproscan_query".format(library)
            data = pd.read_sql(sql_string,conn)


    #Jaccard Score
    if Similarity == "Jaccard":
        data["Jaccard"] = data["InterPro accession"].map(lambda x : (len(set([i.split(".")[0] for i in x.split(",")]).intersection(Jaccard_arr)))/(len(set([i.split(".")[0] for i in x.split(",")]).union(Jaccard_arr))))
        data = data[["Gene name","Jaccard","InterPro accession"]]
        #data = data.nlargest(numbers,"Jaccard")#用來篩前幾比資料
        data = data.loc[data['Jaccard'] >= values]
        data = data.sort_values(by=["Jaccard"],ascending=False)
        data = data.reset_index(drop=True)

        data_header = list(data)
        data_body = data.values.tolist()
    #
    elif Similarity == "Intersection":
        data["intersection"] = data["InterPro accession"].map(lambda x : (len(set([i.split(".")[0] for i in x.split(",")]).intersection(accession_arr))))#1,2,3,4
        #data["accession_length"] =  data["accession"].map(lambda x : (len(set(x.split(",")))))
        #print(data)
        data = data.loc[(data['intersection'] == len(accession_arr))]#交集數一樣
        print(data)
        data = data[["Gene name","InterPro accession"]]
        data_header = list(data)
        data_body = data.values.tolist()
        """
        tempstring = ",".join(accession_arr)
        templist = []
        templist.append(tempstring)
        #print(templist)
        tempdataframe = pd.DataFrame(templist,columns=["InterPro accession"])
        #print(tempdataframe)
        data2 = pd.merge(data,tempdataframe,left_on="InterPro accession",right_on="InterPro accession",how="inner")
        #print(data3)
        data_header = list(data2)
        data_body = data2.values.tolist()
        """
    else: #Similarity == "union"
        #print(data)
        string = ""
        for i in accession_arr:
            string += i + "|" 
        string = string.strip('|')
        #print(string)
        data = data[data["InterPro accession"].str.contains(string)]
        #print(data)
        #data = data.sort_values(by=["Jaccard"],ascending=False)
        #data = data.reset_index(drop=True)

        data_header = list(data)
        data_body = data.values.tolist()

    return JsonResponse({'Jaccard_header':data_header,'Jaccard_body':data_body})   

def query_ID_Pfam(request):
    #library = request.POST.get('library')
    #values = float(request.POST.get("numbers")) 
    #Similarity = request.POST.get("Similarity")
    temp_data = request.POST.get("query_ID").replace(" ", "")
    #print(temp_data)
    accession_arr = temp_data.split(",")
    accession_arr = [i.split(".")[0] for i in accession_arr]#去除版本號
    #對照資料庫基因的pfam相似度表
    #print(Jaccard_arr)#['PF00017.24', 'PF00018.28', 'PF14604.6', 'PF07653.17']
    #print(accession_arr)
    df = pd.DataFrame(accession_arr,columns=["Pfam ID"])
    
    conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8') 
    sql_string = "SELECT * FROM `pfam_database`"
    data = pd.read_sql(sql_string,conn)
    conn.commit()
    #head = list(data)
    data = data[["Pfam ID","Description"]]

    merge_data = pd.merge(df,data,on="Pfam ID",how="left")

    head = ["Pfam ID","Description"]
    #body = data.values.tolist()
    body = merge_data.values.tolist();

    return JsonResponse({'header':head,'body':body,'accession':accession_arr},safe = False)


def query_ID_interproscan(request):
    #library = request.POST.get('library')
    #values = float(request.POST.get("numbers")) 
    #Similarity = request.POST.get("Similarity")
    temp_data = request.POST.get("query_ID").replace(" ", "")
    #print(temp_data)
    accession_arr = temp_data.split(",")

    #對照資料庫基因的interproscan相似度表
    #print(Jaccard_arr)#["IPR000980","IPR035837","IPR000980","IPR001452","IPR001452","IPR001452","IPR000980","IPR000980","IPR000980"]
    df = pd.DataFrame(accession_arr,columns=["Interpro ID"])
    
    conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8') 
    sql_string = "SELECT * FROM `interproscan_database`"
    data = pd.read_sql(sql_string,conn)
    conn.commit()
    #head = list(data)

    merge_data = pd.merge(df,data,on="Interpro ID",how="left")

    #head = ["Pfam ID","Description"]
    head = list(merge_data)
    #body = data.values.tolist()
    body = merge_data.values.tolist();

    return JsonResponse({'header':head,'body':body,'accession':accession_arr},safe = False)

def query_keyword_Pfam(request):
    query_keyword = request.POST.get('query_keyword')#k-box
    conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8') 
    sql_string = "SELECT * FROM `pfam_database` WHERE `Description` LIKE '{}%' OR `Description` LIKE '%{}' OR `Description` LIKE '%{}%'".format(query_keyword,query_keyword,query_keyword)
    data = pd.read_sql(sql_string,conn)
    conn.commit()
    #head = list(data)
    head = ["Pfam ID","Description"]
    #body = data.values.tolist()
    body = data[head].values.tolist();
    accession = list(data['Pfam ID'])

    return JsonResponse({'header':head,'body':body,'accession':accession},safe = False)

def query_keyword_interproscan(request):
    query_keyword = request.POST.get('query_keyword')#k-box
    conn = pymysql.connect(host = "localhost",port= 3306 ,user = "t50504",passwd = "624001479",db = "t50504_testdb",charset='utf8') 
    sql_string = "SELECT * FROM `interproscan_database` WHERE `Entry name` LIKE '{}%' OR `Entry name` LIKE '%{}' OR `Entry name` LIKE '%{}%'".format(query_keyword,query_keyword,query_keyword)
    data = pd.read_sql(sql_string,conn)
    conn.commit()
    head = list(data)
    body = data.values.tolist()
    accession = list(data["Interpro ID"])

    return JsonResponse({'header':head,'body':body,'accession':accession},safe = False)

def GeneExpressionProfile(request):
    temp_data = request.POST.get("data")
    #Type = request.POST.get("type")
    shorthand = {"Peq":"Phalaenopsis","Dca":"Dendrobium","Ash":"Apostasia","Vpo":"Vpompona","Vsh":"Vshenzhenica","Pgu":"Pguangdongensis","Pzi":"Pzijinensis", "evm": "Ldiscolor"}
    data_type = request.POST.get('select_data_type')    
    print(data_type)#contig
    arry = json.loads(temp_data)
    print(arry)#['Ash007886', 'Ash001498', 'Ash000913', 'Ash010827', 'Ash018814', 'Ash017037', 'Ash001920']
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

    # print(data_list)
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
        pic_name = plot_cluster(body3,header2,geneid)
        #data_array = [[0.0,0.0,0.0,0.0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        #columns_label_list=[1,2,3,4]
        #index_label_list=['I','am','a','handsome']
        #pic_name = plot_cluster(data_array,columns_label_list,index_label_list)

        pca_list = plot_pca(body3).tolist()
        #temp_list = [[0,0,0,0],[0,1,1,0],[0,1,1,1],[0,0,0,0]]
        #X_new = plot_pca(temp_list).tolist()#numpy.ndarray to list
        #print(X_new)   #[[-0.74737806 -0.0626581 ]
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

def file_download(request):  
    file = open('/home/t50504/Django/t50504_project/data/pfam_result.txt','rb')  
    response =FileResponse(file)  
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename="Pfam_result.txt"'  
    return response

def pfam(inp):
    for i in range(len(inp)):
        if inp[i].startswith('#'):
            inp[i]=''

    b=['']*(len(inp)-3)
    for j in range(3,len(inp)):
        b[j-3] = inp[j]

    query = []
    accession = []
    indE = []
    conE = []
    result = []
    hmm_start = []
    hmm_end = []
    env_start = []
    env_end = []
    ali_start = []
    ali_end = []
    for k in range(len(b)-10):
        tmp = b[k].split(' ')
        tmp = list(filter(None, tmp))
        query.append(tmp[3])
        accession.append(tmp[1])
        indE.append(tmp[12])
        conE.append(tmp[11])
        hmm_start.append(tmp[15])
        hmm_end.append(tmp[16])
        ali_start.append(tmp[17])
        ali_end.append(tmp[18])
        env_start.append(tmp[19])
        env_end.append(tmp[20])
        result.append([accession[k], env_start[k], env_end[k], ali_start[k],
                      ali_end[k], hmm_start[k], hmm_end[k], indE[k], conE[k]])

    return result,accession

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