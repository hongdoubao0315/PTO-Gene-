'''
从pubtator返回的结果中，筛选出每篇文献挖掘出的Gene，并对频次进行统计，存储文件名为gene.txt
输入文件：result_xia_Pubtator.txt 从Pubtator上返回的结果

分别按照总频次和文献数排序
gene2.txt
gene3.txt

改进：gene2.txt中，没有gene name？？？
     g_g_dict，基因和基因对照字典
'''
from collections import Counter
from collections import defaultdict
import itertools

def read_gene(gene_file,out_file):
    wf = open(out_file, 'w')
    wf.write('PMID\tgene_id\ttime\tgene_name\t\n') #标题行：pmid、gene_id、匹配次数、基因名称
    f = open(gene_file,encoding="utf-8")
    f_list = f.readlines()  #读取文件所有内容到f_list中
    f.close()

    count_pmid = 0   #统计挖掘的文献数量
    count_gene = 0   #统计挖掘出的gene数量
    
    entrez_dict = defaultdict(list)  #使用字典，在每个gene id中存放多个基因名称
    entrez_list1 = []
    entrez_list = []  #记录一篇文献中挖到的所有gene id（可能有重复）
    
    for line in f_list:
        l = line.strip()
        if '|t|' in l:
        #如果是标题行,pmid数+1
            time_dict = Counter(entrez_list) #统计一篇文献挖掘出的不同gene id次数
            if time_dict != Counter():  #如果不是第一次读到标题行（即entrez_list不为空）
                for i in time_dict:  #i是每一个entrez_id，[]中将id中的名字去重，以便写入文件中
                    [entrez_list1.append(j) for j in entrez_dict[i] if not j in entrez_list1]
                    wf.write('{0}\t{1}\t{2}\t{3}\n'.\
                             format(PMID,i,time_dict[i],entrez_list1))
                    count_pmid += 1
                    entrez_list1 = []
            PMID = l[:l.find('|')]  #记录PMID号、清空entrez_list
            entrez_list = []

        line1 = l.split('\t')
        if len(line1) == 6:
            if line1[4] == 'Gene':
            #如果挖掘的Gene，gene数+1，并记录基因名字、entrezid
                count_gene += 1
                name = line1[3]
                entrez_id = line1[5]
                entrez_list.append(entrez_id)
                entrez_dict[entrez_id].append(name) #相同的id放对应的名字
    '''ttt = ['842733','831441','835710', '842859','4337575','843244','829969','817267','830878','4340746']
    for i in ttt:
        print(entrez_dict[i])
    '''
    print('一共有{0}篇文献挖掘出{1}种gene的结果,共{2}次。'.format(count_pmid,len(entrez_dict),count_gene))
    return entrez_dict
    
def statistic(out_file, out_file2, out_file3):
    a = open(out_file2, 'w')
    a.write('gene_id\ttime\tabs\n')
    b = open(out_file3, 'w')
    b.write('gene_id\ttime\tabs\n')
    f = open(out_file,encoding="utf-8")
    f_list = f.readlines()
    f.close()
    
    time_sta_dic = {}
    time_abs_dic = {}
    for line in f_list:
        line = line.strip()
        line = line.split('\t')
        if line[0] != 'PMID':  #跳过标题行
            gene_id = line[1]
            time_sta_dic[gene_id] = 0
            time_abs_dic[gene_id] = 0
            
    for line in f_list:
        line = line.strip()
        line = line.split('\t')
        if line[0] != 'PMID':  #跳过标题行
            gene_id = line[1]
            time = line[2]
            time_sta_dic[gene_id] += int(time)
            time_abs_dic[gene_id] += 1
    
    a_list = []
    b_list = []
    for i in sorted(time_sta_dic.items(),key=lambda k:k[1],reverse=True):
        a_list.append(i[0])
    for j in sorted(time_abs_dic.items(),key=lambda k:k[1],reverse=True):
        b_list.append(j[0])  #按照基因出现在不同文献的篇数，从大到小排序

    for i in a_list:
        a.write('{0}\t{1}\t{2}\n'.format(i,time_sta_dic[i],time_abs_dic[i]))
    for j in b_list:
        b.write('{0}\t{1}\t{2}\n'.format(j,time_sta_dic[j],time_abs_dic[j]))
    
def g_g_dict(out_file,outfile_4):
    f = open(out_file,encoding="utf-8")
    out_list = f.readlines()
    pmid_gene_dic = defaultdict(list)
    gene_gene_dic = {}
    for line in out_list:
        line = line.strip()
        line = line.split('\t')
        if line[0] != 'PMID':  #跳过标题行
            pmid = line[0]
            geneid = line[1]
            pmid_gene_dic[pmid].append(geneid)  #pmid_gene_dic:key为pmid，value为多个geneid的字典
            
    for i in list(pmid_gene_dic.keys()):  
        if len(list(pmid_gene_dic[i])) > 1:
            aaa = pmid_gene_dic[i]
            for j in itertools.combinations(aaa,2):
                gene_gene_dic[j] = 0
            
    for i in list(pmid_gene_dic.keys()):
        if len(list(pmid_gene_dic[i])) > 1:
            aaa = pmid_gene_dic[i]
            for j in itertools.combinations(aaa,2):
                gene_gene_dic[j] += 1
    
    wf = open(outfile_4,'w')
    wf.write('gene\tgene\ttime\n')
    for i in gene_gene_dic:
        wf.write('{0}\t{1}\t{2}\n'.format(i[0],i[1],gene_gene_dic[i]))
    wf.close()






outfile = '/Users/apple/Downloads/PTO and Gene/PMID脚本结果/gene.txt'
outfile2 = '/Users/apple/Downloads/PTO and Gene/PMID脚本结果/gene2.txt'  #按照gene在所有文献中出现次数排序
outfile3 = '/Users/apple/Downloads/PTO and Gene/PMID脚本结果/gene3.txt'  #按照文献含有gene的篇数排序
outfile4 = '/Users/apple/Downloads/PTO and Gene/PMID脚本结果/g_g_dict.txt'
genefile = '/Users/apple/Downloads/PTO and Gene/PMID脚本结果/result_xia_Pubtator.txt'
read_gene(genefile,outfile)
statistic(outfile,outfile2,outfile3)
g_g_dict(outfile,outfile4)
