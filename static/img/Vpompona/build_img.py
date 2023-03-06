from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import re
import subprocess
row=[]
row_list=[]
structure_list=[]
with open("Vpo_miRLocator_predResults.txt") as f:
    result=f.readlines()
    for item in result:
        A=item.split("\t")
        if A[0]:
            row=[A[0]]
            premiRNA=A[1]
            structure_list.append(A[2].split("\n")[0])
            
        else:
            row.append(A[1])
            row.append(A[2].split("\n")[0])
            row.append(premiRNA)
            row_list.append(row)
for row in row_list:
    mature_1=row[1].split("(")
    mature_2=row[2].split("(")
    m1=re.search(mature_1[0],row[3])
    m2=re.search(mature_2[0],row[3])
    seq=SeqRecord(Seq(row[3]),id=row[0],description=row[0])
    SeqIO.write([seq],"temp.seq", "fasta")
    subprocess.call("RNAfold < temp.seq > temp.fold",shell=True)
    subprocess.call('RNAplot --pre "'+str(m1.start()+1)+' '+str(m1.end())+' 8 RED omark '+str(m2.start()+1)+' '+str(m2.end())+' 8 RED omark" < temp.fold',shell=True)
    subprocess.call("sam2p "+row[0]+"_ss.ps "+row[0]+".jpg",shell=True)