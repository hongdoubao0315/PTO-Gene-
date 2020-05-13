'''
对从PTO挖掘的结果进行整理，不关注挖掘的PTO所在的句子
将每篇文献挖掘的PTO去重，统计出现的频次。
输入文件：nltk_pro.py后生成的result_fen.tt文件
输出文件：sort_match_PTO.txt

分别按照总频次和文献数排序
sort_match_PTO_1.txt
sort_match_PTO_2.txt
'''

from collections import defaultdict
from collections import Counter

f = open('/Users/apple/Downloads/PTO and Gene/match/result_fen.txt',encoding="utf-8")
wf = open('/Users/apple/Downloads/PTO and Gene/match/sort_match_PTO.txt', 'w')

wf.write('pmid\tPTO\tterm\ttime\n')

f_list = f.readlines()
f.close()
PMID_dict = defaultdict(list)  #使用字典，在每个pmid中存放多个PTO
PTO_dict = {}

a=0
for line in f_list:  #遍历reference中挖掘的PTO
    l = line.strip()
    line = l.split('\t')
    a+=1
    try:
        if line[2] != 'pmid':
            PMID = line[2]
            PTO = line[0]
            Term = line[3]
            PTO_dict[PTO] = Term   #将PTO号和Term对应存放
            PMID_dict[PMID].append(PTO) #在相同的PMID中存放对应的PTO号
    except:
        print(line)
        print(a)
    
        

for i in PMID_dict.keys():  #遍历每个PMID
    time_dict = Counter(PMID_dict['{0}'.format(i)])  #time_dict是该PMID下，每个PTO对应的次数
    for j in time_dict.keys():  #遍历每个PTO
        time = time_dict['{0}'.format(j)]
        wf.write('{0}\t{1}\t{2}\t{3}\n'.format(i,j,PTO_dict['{0}'.format(j)],time))
    


def statistic(out_file, out_file2, out_file3):
    a = open(out_file2, 'w')
    a.write('TO term\ttime\tabs\n')
    b = open(out_file3, 'w')
    b.write('TO term\ttime\tabs\n')
    ff = open(out_file,encoding="utf-8")
    f_list = ff.readlines()
    ff.close()
    
    time_sta_dic = {}
    time_abs_dic = {}
    for line in f_list:
        line = line.strip()
        line = line.split('\t')
        if line[0] != 'pmid':  #跳过标题行
            PTO = line[1]
            time_sta_dic[PTO] = 0
            time_abs_dic[PTO] = 0
            
    for line in f_list:
        line = line.strip()
        line = line.split('\t')
        if line[0] != 'pmid':  #跳过标题行
            PTO = line[1]
            time = line[3]
            time_sta_dic[PTO] += int(time)
            time_abs_dic[PTO] += 1
    
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
    a.close()
    b.close()
    
def t_t_dict(aaa,outfile_4):
    f = open(aaa,encoding="utf-8")
    out_list = f.readlines()
    pmid_PTO_dic = defaultdict(list)
    PTO_PTO_dic = {}
    for line in out_list:
        line = line.strip()
        line = line.split('\t')
        if line[0] != 'pmid':  #跳过标题行
            pmid = line[0]
            PTO = line[1]
            pmid_PTO_dic[pmid].append(PTO)  #pmid_gene_dic:key为pmid，value为多个geneid的字典
            
    for i in list(pmid_PTO_dic.keys()):  
        if len(list(pmid_PTO_dic[i])) > 1:
            aaa = pmid_PTO_dic[i]
            for j in itertools.combinations(aaa,2):
                PTO_PTO_dic[j] = 0
            
    for i in list(pmid_PTO_dic.keys()):
        if len(list(pmid_PTO_dic[i])) > 1:
            aaa = pmid_PTO_dic[i]
            for j in itertools.combinations(aaa,2):
                PTO_PTO_dic[j] += 1
    
    wff = open(outfile_4,'w')
    wff.write('time\tPTO\tterm\tPTO\tterm\n')
    for i in PTO_PTO_dic:
        wff.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(PTO_PTO_dic[i],i[0],PTO_dict[i[0]],i[1],PTO_dict[i[1]]))
    wff.close()


'''改文件'''
aaa = '/Users/apple/Downloads/PTO and Gene/match/sort_match_PTO.txt' 
outfile2 = '/Users/apple/Downloads/PTO and Gene/match/sort_match_PTO_1.txt'  #按照gene在所有文献中出现次数排序
outfile3 = '/Users/apple/Downloads/PTO and Gene/match/sort_match_PTO_2.txt'  #按照文献含有gene的篇数排序
outfile4 = '/Users/apple/Downloads/PTO and Gene/match/t_t_dict.txt'
statistic(aaa, outfile2,outfile3)
t_t_dict(aaa, outfile4)